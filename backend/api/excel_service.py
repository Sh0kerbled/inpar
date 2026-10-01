import io
import os
import re
import logging
from decimal import Decimal, InvalidOperation
from urllib.parse import urlparse

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

import requests
from django.core.files.base import ContentFile
from .models import Category, Product
from .utils import get_usd_to_kzt_rate

logger = logging.getLogger(__name__)

# Patterns that indicate row numbering or IDs that MUST NOT be used as product name
ROW_NUMBER_KEYWORDS = ['№', '№ п/п', '№ п.п.', 'п/п', 'п.п.', 'номер', 'номер п/п', 'row', 'index', '#', 'id']

# Words that disqualify a column from being a Product Name
NAME_DISQUALIFIERS = [
    'код', 'артикул', 'sku', 'группа', 'категория', 'цена', 'стоимость',
    'прайс', 'опт', 'розниц', 'кол-во', 'кол во', 'количество', 'остаток',
    'фото', 'картинк', 'ссылк', 'источник', 'номер', '№', 'date', 'дата', 'статус'
]


def clean_cell_str(val):
    if val is None:
        return ''
    if isinstance(val, float) and val.is_integer():
        return str(int(val)).strip()
    return str(val).strip()


def parse_decimal(val, default=None):
    if val is None:
        return default
    val_str = str(val).strip().replace('$', '').replace('₸', '').replace(' ', '').replace(',', '.')
    if not val_str:
        return default
    try:
        return Decimal(val_str)
    except (InvalidOperation, ValueError):
        return default


def parse_int(val, default=0):
    if val is None:
        return default
    val_str = str(val).strip().replace(' ', '')
    if not val_str:
        return default
    try:
        return int(float(val_str))
    except (ValueError, TypeError):
        return default


def download_image_from_url(url):
    """Safely download an image from a public URL and return (filename, ContentFile) or (None, None)"""
    if not url or not (url.startswith('http://') or url.startswith('https://')):
        return None, None
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        resp = requests.get(url, timeout=8, headers=headers)
        if resp.status_code == 200 and resp.content:
            path = urlparse(url).path
            ext = os.path.splitext(path)[1].lower()
            if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                ext = '.jpg'
            filename = f"import_{os.urandom(6).hex()}{ext}"
            return filename, ContentFile(resp.content)
    except Exception as e:
        logger.warning(f"Failed to download image from {url}: {e}")
    return None, None


def find_header_row_and_mapping(rows):
    """
    Scans the first 15 rows of the Excel sheet to find the real header row
    and maps columns to canonical fields reliably.
    """
    best_row_idx = 0
    best_score = -1
    best_mapping = {}

    for row_idx in range(min(15, len(rows))):
        row = rows[row_idx]
        if not any(row):
            continue

        mapping = {}
        score = 0

        for col_idx, cell in enumerate(row):
            if not cell:
                continue
            text = str(cell).strip().lower()

            # Ignore pure row numbers
            if text in ROW_NUMBER_KEYWORDS or re.match(r'^(№|#|п/п|no\.?)$', text):
                continue

            # 1. Product Name (Highest priority)
            if 'name' not in mapping:
                is_name_match = (
                    any(k in text for k in ['наименование', 'название', 'номенклатура', 'товар', 'позиция', 'продукт', 'product_name', 'item_name']) or
                    text in ['name', 'title', 'товар', 'товары']
                )
                # Ensure it doesn't contain disqualifiers like "код товара" or "группа товара"
                has_disqualifier = any(dq in text for dq in NAME_DISQUALIFIERS)
                # Allow if explicitly "наименование товара" or "название товара"
                if is_name_match and (not has_disqualifier or 'наименование' in text or 'название' in text or text == 'товар'):
                    mapping['name'] = col_idx
                    score += 10
                    continue

            # 2. SKU / Code
            if 'sku' not in mapping:
                if (any(k in text for k in ['артикул', 'sku', 'product_code']) or
                    (any(k in text for k in ['код', 'code']) and 'штрих' not in text and 'валют' not in text)):
                    mapping['sku'] = col_idx
                    score += 5
                    continue

            # 3. Category / Group
            if 'category' not in mapping:
                if any(k in text for k in ['группа товара', 'группа', 'подгруппа', 'категория', 'раздел', 'category', 'group']):
                    mapping['category'] = col_idx
                    score += 4
                    continue

            # 4. Wholesale Price
            if 'wholesale_price_usd' not in mapping:
                if any(k in text for k in ['цена оптом', 'цена опт', 'оптовая цена', 'цена оптовая', 'опт ($)', 'wholesale_price', 'wholesale']):
                    mapping['wholesale_price_usd'] = col_idx
                    score += 5
                    continue

            # 5. Retail Price
            if 'price_usd' not in mapping:
                if any(k in text for k in ['цена розница', 'цена в розницу', 'розница', 'розничная цена', 'цена ($)', 'цена usd', 'стоимость', 'прайс', 'price', 'retail']):
                    mapping['price_usd'] = col_idx
                    score += 5
                    continue
                # If column is simply named "Цена" or "Цена товара" or "Цена за шт"
                if text in ['цена', 'цена товара', 'цена за шт', 'цена за единицу', 'цена, тенге', 'цена (тг)', 'цена тенге', 'цена usd', 'цена ($)']:
                    mapping['price_usd'] = col_idx
                    score += 4
                    continue

            # 6. Combined "Опт / розница" column
            if 'wholesale_price_usd' not in mapping and any(k in text for k in ['опт/розница', 'опт / розница', 'опт/розн']):
                # If we don't have wholesale yet, assign this column to wholesale or check
                mapping['wholesale_price_usd'] = col_idx
                score += 3
                continue

            # 7. Min Wholesale Quantity
            if 'min_wholesale_quantity' not in mapping:
                if any(k in text for k in ['мин. количество оптом', 'мин количество оптом', 'мин. опт', 'мин опт', 'мин заказ', 'минимально оптом', 'min_qty']):
                    mapping['min_wholesale_quantity'] = col_idx
                    score += 3
                    continue

            # 8. Stock quantity
            if 'stock_quantity' not in mapping:
                if any(k in text for k in ['количество в наличии', 'количество в общем', 'количество', 'остаток', 'в наличии', 'кол-во', 'кол во', 'склад', 'всего', 'stock', 'qty', 'quantity']):
                    mapping['stock_quantity'] = col_idx
                    score += 4
                    continue

            # 9. Image URL
            if 'image_url' not in mapping:
                if any(k in text for k in ['фото товара', 'фото', 'ссылка на фото', 'картинка', 'изображение', 'image', 'photo']):
                    mapping['image_url'] = col_idx
                    score += 3
                    continue

            # 10. Source URL
            if 'source_url' not in mapping:
                if any(k in text for k in ['ссылка на источник', 'источник', 'ссылка', 'url', 'source']):
                    mapping['source_url'] = col_idx
                    score += 2
                    continue

            # 11. Description
            if 'description' not in mapping:
                if any(k in text for k in ['описание', 'характеристики', 'инфо', 'детали', 'description']):
                    mapping['description'] = col_idx
                    score += 3
                    continue

        if score > best_score and 'name' in mapping:
            best_score = score
            best_row_idx = row_idx
            best_mapping = mapping

    # Fallback: If no row had an explicit 'name' match, pick the text row with highest candidate score
    if not best_mapping or 'name' not in best_mapping:
        for row_idx in range(min(5, len(rows))):
            row = rows[row_idx]
            # Find first column that has text and is not a number
            for col_idx, cell in enumerate(row):
                if cell and not str(cell).strip().isdigit() and str(cell).strip().lower() not in ROW_NUMBER_KEYWORDS:
                    best_mapping['name'] = col_idx
                    best_row_idx = row_idx
                    break
            if 'name' in best_mapping:
                break

    return best_row_idx, best_mapping


def import_products_from_excel(file_obj, default_category_id=None, currency='USD'):
    """
    Import products from uploaded Excel file (.xlsx) with robust header auto-detection.
    """
    try:
        wb = openpyxl.load_workbook(file_obj, data_only=True)
    except Exception as e:
        return {
            'success': False,
            'created': 0,
            'updated': 0,
            'total_rows': 0,
            'errors': [f"Не удалось прочитать Excel файл: {str(e)}"]
        }

    sheet = wb.active
    rows = list(sheet.iter_rows(values_only=True))
    if not rows:
        return {
            'success': False,
            'created': 0,
            'updated': 0,
            'total_rows': 0,
            'errors': ["Файл Excel пуст"]
        }

    header_row_idx, col_mapping = find_header_row_and_mapping(rows)

    if 'name' not in col_mapping:
        header_sample = [str(c) for c in (rows[header_row_idx] if rows else []) if c]
        return {
            'success': False,
            'created': 0,
            'updated': 0,
            'total_rows': 0,
            'errors': [
                f"Не удалось определить колонку с названием товара. Найденные заголовки: {', '.join(header_sample[:8])}"
            ]
        }

    exchange_rate = get_usd_to_kzt_rate() or Decimal('460')

    # Resolve default category if specified
    default_category = None
    if default_category_id:
        try:
            default_category = Category.objects.filter(id=default_category_id).first()
        except Exception:
            pass

    uncategorized_category = None

    def get_uncategorized():
        nonlocal uncategorized_category
        if uncategorized_category is None:
            uncategorized_category, _ = Category.objects.get_or_create(
                name="Без категории",
                defaults={"description": "Товары, требующие ручного распределения по категориям"}
            )
        return uncategorized_category

    categories_cache = {c.name.strip().lower(): c for c in Category.objects.all()}

    created_count = 0
    updated_count = 0
    errors = []
    total_data_rows = 0

    # Start data rows AFTER header_row_idx
    for row_idx, row in enumerate(rows[header_row_idx + 1:], start=header_row_idx + 2):
        if not any(row):
            continue

        def get_val(field):
            idx = col_mapping.get(field)
            if idx is not None and idx < len(row):
                return row[idx]
            return None

        raw_name = clean_cell_str(get_val('name'))
        if not raw_name:
            continue

        # If name is just a row number (e.g. "1", "25", "30") and another column might have the real title
        if raw_name.isdigit() and len(raw_name) <= 3:
            # Check if there is another column with text
            candidate_name = None
            for c_idx, c_val in enumerate(row):
                if c_idx != col_mapping.get('name') and c_val:
                    c_str = clean_cell_str(c_val)
                    if len(c_str) > 3 and not c_str.isdigit():
                        candidate_name = c_str
                        break
            if candidate_name:
                raw_name = candidate_name
            else:
                # Skip pure numbering row if no title exists
                continue

        name = raw_name
        total_data_rows += 1

        sku = clean_cell_str(get_val('sku')) or None
        description = clean_cell_str(get_val('description'))
        category_name = clean_cell_str(get_val('category'))
        source_url = clean_cell_str(get_val('source_url')) or None
        image_url = clean_cell_str(get_val('image_url'))

        raw_price = parse_decimal(get_val('price_usd'), default=Decimal('0.00'))
        raw_wholesale = parse_decimal(get_val('wholesale_price_usd'), default=None)

        # Currency handling:
        # If user explicitly chose KZT, or if prices are large (> 500) which strongly indicates KZT in KZ market
        is_kzt = (currency.upper() == 'KZT') or (raw_price is not None and raw_price > Decimal('800'))

        if is_kzt and exchange_rate > 0:
            price_usd = round(raw_price / exchange_rate, 2) if raw_price else Decimal('0.00')
            wholesale_price_usd = round(raw_wholesale / exchange_rate, 2) if raw_wholesale else None
        else:
            price_usd = raw_price
            wholesale_price_usd = raw_wholesale

        min_wholesale_quantity = parse_int(get_val('min_wholesale_quantity'), default=1)
        stock_quantity = parse_int(get_val('stock_quantity'), default=0)

        # Category determination
        product_category = None
        if category_name:
            cat_key = category_name.lower()
            if cat_key in categories_cache:
                product_category = categories_cache[cat_key]
            else:
                try:
                    product_category = Category.objects.create(name=category_name)
                    categories_cache[cat_key] = product_category
                except Exception as cat_err:
                    errors.append(f"Строка {row_idx}: Ошибка категории '{category_name}': {cat_err}")
                    product_category = default_category or get_uncategorized()
        elif default_category:
            product_category = default_category
        else:
            product_category = get_uncategorized()

        # Find existing product
        product = None
        if sku:
            product = Product.objects.filter(sku=sku).first()
        if not product:
            product = Product.objects.filter(name__iexact=name).first()

        try:
            if product:
                product.name = name
                if description:
                    product.description = description
                if sku:
                    product.sku = sku
                product.price_usd = price_usd
                product.wholesale_price_usd = wholesale_price_usd
                product.min_wholesale_quantity = min_wholesale_quantity
                product.stock_quantity = stock_quantity
                if product_category:
                    product.category = product_category
                if source_url:
                    product.source_url = source_url

                if image_url and not product.main_image:
                    fname, fcontent = download_image_from_url(image_url)
                    if fname and fcontent:
                        product.main_image.save(fname, fcontent, save=False)

                product.save()
                updated_count += 1
            else:
                new_product = Product(
                    name=name,
                    sku=sku,
                    description=description or "",
                    price_usd=price_usd,
                    wholesale_price_usd=wholesale_price_usd,
                    min_wholesale_quantity=min_wholesale_quantity,
                    stock_quantity=stock_quantity,
                    category=product_category,
                    source_url=source_url,
                    is_active=True
                )

                if image_url:
                    fname, fcontent = download_image_from_url(image_url)
                    if fname and fcontent:
                        new_product.main_image.save(fname, fcontent, save=False)

                new_product.save()
                created_count += 1

        except Exception as e:
            errors.append(f"Строка {row_idx} ({name}): Ошибка: {str(e)}")

    return {
        'success': True,
        'created': created_count,
        'updated': updated_count,
        'total_rows': total_data_rows,
        'errors': errors,
        'detected_header_row': header_row_idx + 1,
        'detected_columns': {k: v + 1 for k, v in col_mapping.items()}
    }


def generate_excel_template():
    """
    Generate a formatted Excel template for uploading products
    Returns: bytes of .xlsx file
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Товары"

    headers = [
        "Код товара (Артикул)",
        "Название *",
        "Категория / Группа",
        "Описание",
        "Цена в розницу ($) *",
        "Цена оптом ($)",
        "Мин. количество оптом (шт)",
        "Количество в наличии (всего)",
        "Ссылка на фото (URL)",
        "Ссылка на источник"
    ]

    ws.append(headers)

    sample_rows = [
        [
            "INP-KNX-01",
            "Сенсорная панель KNX 7 дюймов",
            "Умный дом (KNX)",
            "Многофункциональная настенная сенсорная панель управления освещением и климатом",
            450.00,
            380.00,
            5,
            25,
            "https://images.unsplash.com/photo-1558002038-1055907df827?w=600",
            "https://supplier.example.com/item/101"
        ],
        [
            "INP-CAM-02",
            "IP-камера 4K с ИИ-аналитикой",
            "",
            "Купольная камера видеонаблюдения с распознаванием лиц и ночным видением",
            120.00,
            95.00,
            10,
            100,
            "",
            ""
        ]
    ]

    for sample in sample_rows:
        ws.append(sample)

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="1A1D23", end_color="1A1D23", fill_type="solid")
    header_align = Alignment(horizontal="center", vertical="center", wrap_text=True)

    thin_border = Border(
        left=Side(style='thin', color='D0D5DD'),
        right=Side(style='thin', color='D0D5DD'),
        top=Side(style='thin', color='D0D5DD'),
        bottom=Side(style='thin', color='D0D5DD')
    )

    ws.row_dimensions[1].height = 32

    for col_idx, col_name in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = thin_border

    for row_idx in range(2, 2 + len(sample_rows)):
        ws.row_dimensions[row_idx].height = 24
        for col_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.font = Font(name="Calibri", size=10)
            cell.border = thin_border
            if col_idx in [5, 6]:
                cell.number_format = '$#,##0.00'
                cell.alignment = Alignment(horizontal="right", vertical="center")
            elif col_idx in [7, 8]:
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal="right", vertical="center")
            else:
                cell.alignment = Alignment(vertical="center")

    column_widths = {
        1: 22, 2: 32, 3: 22, 4: 38, 5: 20, 6: 18, 7: 24, 8: 24, 9: 28, 10: 28
    }

    for col_idx, width in column_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.getvalue()
