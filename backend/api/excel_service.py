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
import urllib3
from django.core.files.base import ContentFile
from .models import Category, Product
from .utils import get_usd_to_kzt_rate

# Disable InsecureRequestWarning when downloading images with verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
    """Normalize string cell value"""
    if val is None:
        return ''
    if isinstance(val, float) and val.is_integer():
        return str(int(val)).strip()
    return str(val).strip()


def parse_decimal(val, default=None):
    """
    Robust decimal parser for prices in KZT, USD, etc.
    Handles non-breaking spaces (\\xa0, \\u202f), currency symbols (₸, $, тг, тенге, руб),
    commas, dots, and formulas.
    """
    if val is None:
        return default
    if isinstance(val, (int, float, Decimal)):
        try:
            return Decimal(str(val))
        except Exception:
            return default

    val_str = str(val).strip()
    if not val_str or val_str.lower() in ['-', '—', 'n/a', 'none', 'null', 'договорная', 'бесплатно']:
        return default

    # Remove all unicode whitespace (non-breaking spaces, thin spaces, etc)
    val_str = re.sub(r'[\s\xa0\u202f\u2007\t\r\n]+', '', val_str)

    # Remove currency words and symbols
    val_str = re.sub(r'(?i)(тг\.?|тнг\.?|тенге|kzt|usd|руб\.?|rub|\$|₸|€|₽|шт\.?|за\s*шт\.?)', '', val_str)
    val_str = val_str.strip().strip(':=-')

    # Handle commas and dots
    if ',' in val_str and '.' in val_str:
        if val_str.rfind(',') > val_str.rfind('.'):
            # European format: 15.000,00 -> 15000.00
            val_str = val_str.replace('.', '').replace(',', '.')
        else:
            # US format: 15,000.00 -> 15000.00
            val_str = val_str.replace(',', '')
    elif ',' in val_str:
        parts = val_str.split(',')
        if len(parts) == 2 and len(parts[1]) in [1, 2]:
            # Decimal fraction: "15000,50" -> "15000.50"
            val_str = val_str.replace(',', '.')
        else:
            # Thousand separator: "15,000" -> "15000"
            val_str = val_str.replace(',', '')

    # Extract digits with optional decimal point
    match = re.search(r'[-+]?\d+(?:\.\d+)?', val_str)
    if not match:
        return default

    try:
        return Decimal(match.group(0))
    except (InvalidOperation, ValueError):
        return default


def parse_int(val, default=0):
    """Parse integer quantities (stock, MOQ) handling strings with 'шт', 'pcs'"""
    if val is None:
        return default
    if isinstance(val, int):
        return val
    if isinstance(val, float):
        return int(val)
    val_str = str(val).strip()
    val_str = re.sub(r'[\s\xa0\u202f\u2007\t\r\n]+', '', val_str)
    val_str = re.sub(r'(?i)(шт\.?|pcs\.?|ед\.?|штук)', '', val_str)
    match = re.search(r'\d+', val_str)
    if match:
        try:
            return int(match.group(0))
        except (ValueError, TypeError):
            pass
    return default


def normalize_image_url(url):
    """Convert Google Drive, Dropbox, etc. sharing URLs to direct image download URLs"""
    if not url:
        return ""
    url = url.strip()

    # Google Drive share link
    if 'drive.google.com' in url:
        match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', url)
        if match:
            return f"https://lh3.googleusercontent.com/d/{match.group(1)}"
        match = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', url)
        if match:
            return f"https://lh3.googleusercontent.com/d/{match.group(1)}"

    # Dropbox link
    if 'dropbox.com' in url:
        url = url.replace('dl=0', 'raw=1')
        if 'raw=1' not in url:
            url += ('&raw=1' if '?' in url else '?raw=1')
        return url

    return url


def download_image_from_url(url):
    """
    Safely download an image from a public URL and return (filename, ContentFile) or (None, None)
    Bypasses SSL issues common with CIS image hosts, follows redirects, checks content-type.
    """
    if not url or not (url.startswith('http://') or url.startswith('https://')):
        return None, None

    url = normalize_image_url(url)
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
        }
        resp = requests.get(url, timeout=12, headers=headers, verify=False, allow_redirects=True)
        if resp.status_code == 200 and resp.content:
            content_type = resp.headers.get('content-type', '').lower()
            content = resp.content

            # Guard against HTML error pages
            if 'text/html' in content_type and not (content.startswith(b'\x89PNG') or content.startswith(b'\xff\xd8\xff')):
                logger.warning(f"URL returned HTML preview instead of image bytes: {url}")
                return None, None

            ext = '.jpg'
            if 'png' in content_type or content.startswith(b'\x89PNG'):
                ext = '.png'
            elif 'webp' in content_type or (content.startswith(b'RIFF') and b'WEBP' in content[:16]):
                ext = '.webp'
            elif 'gif' in content_type or content.startswith(b'GIF8'):
                ext = '.gif'
            elif 'jpeg' in content_type or content.startswith(b'\xff\xd8\xff'):
                ext = '.jpg'
            else:
                path = urlparse(url).path
                guessed_ext = os.path.splitext(path)[1].lower()
                if guessed_ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
                    ext = guessed_ext

            filename = f"import_{os.urandom(6).hex()}{ext}"
            return filename, ContentFile(content)
    except Exception as e:
        logger.warning(f"Failed to download image from {url}: {e}")
    return None, None


def extract_embedded_images(sheet):
    """
    Extract embedded images inserted directly into the Excel worksheet.
    Returns dict mapping row_index (0-indexed) to (filename, ContentFile)
    """
    embedded_images = {}
    if not hasattr(sheet, '_images') or not sheet._images:
        return embedded_images

    for idx, img in enumerate(sheet._images):
        try:
            row_num = None
            if hasattr(img, 'anchor'):
                anchor = img.anchor
                if hasattr(anchor, '_from') and hasattr(anchor._from, 'row'):
                    row_num = anchor._from.row
                elif hasattr(anchor, 'row'):
                    row_num = anchor.row

            if row_num is None:
                continue

            image_bytes = None
            format_ext = '.jpg'

            # 1. Try _data() callable
            if hasattr(img, '_data') and callable(img._data):
                image_bytes = img._data()
            # 2. Try ref stream
            elif hasattr(img, 'ref') and hasattr(img.ref, 'read'):
                image_bytes = img.ref.read()
            # 3. Try PIL Image directly
            elif hasattr(img, 'image'):
                buf = io.BytesIO()
                pil_fmt = img.image.format or 'JPEG'
                if pil_fmt.upper() in ['PNG', 'WEBP']:
                    format_ext = f".{pil_fmt.lower()}"
                else:
                    pil_fmt = 'JPEG'
                    format_ext = '.jpg'
                img.image.save(buf, format=pil_fmt)
                image_bytes = buf.getvalue()

            if image_bytes:
                # Detect format from magic bytes
                if image_bytes.startswith(b'\x89PNG'):
                    format_ext = '.png'
                elif image_bytes.startswith(b'\xff\xd8\xff'):
                    format_ext = '.jpg'
                elif image_bytes.startswith(b'RIFF') and b'WEBP' in image_bytes[:16]:
                    format_ext = '.webp'
                elif image_bytes.startswith(b'GIF8'):
                    format_ext = '.gif'

                fname = f"excel_{os.urandom(6).hex()}{format_ext}"
                # Keep first image encountered for this row
                if row_num not in embedded_images:
                    embedded_images[row_num] = (fname, ContentFile(image_bytes))
        except Exception as e:
            logger.warning(f"Failed to extract embedded image #{idx}: {e}")

    return embedded_images


def find_header_row_and_mapping(rows):
    """
    Scans the first 15 rows of the Excel sheet to find the real header row
    and maps columns to canonical fields reliably with support for CIS market variations.
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
            # Normalize whitespace and newlines inside header
            text = re.sub(r'[\s\r\n]+', ' ', text)

            # Ignore pure row numbers
            if text in ROW_NUMBER_KEYWORDS or re.match(r'^(№|#|п/п|no\.?)$', text):
                continue

            # 1. Product Name (Highest priority)
            if 'name' not in mapping:
                is_name_match = (
                    any(k in text for k in ['наименование', 'название', 'номенклатура', 'товар', 'позиция', 'продукт', 'product_name', 'item_name']) or
                    text in ['name', 'title', 'товар', 'товары']
                )
                has_disqualifier = any(dq in text for dq in NAME_DISQUALIFIERS)
                if is_name_match and (not has_disqualifier or 'наименование' in text or 'название' in text or text == 'товар'):
                    mapping['name'] = col_idx
                    score += 10
                    continue

            # 2. SKU / Code
            if 'sku' not in mapping:
                if (any(k in text for k in ['артикул', 'sku', 'product_code', 'партномер', 'модель']) or
                    (any(k in text for k in ['код', 'code']) and 'штрих' not in text and 'валют' not in text)):
                    mapping['sku'] = col_idx
                    score += 5
                    continue

            # 3. Wholesale Price (High priority over general price)
            if 'wholesale_price_usd' not in mapping:
                is_wholesale = (
                    any(k in text for k in [
                        'цена оптом', 'цена опт', 'оптовая цена', 'цена оптовая',
                        'оптовая стоимость', 'стоимость опт', 'стоимость оптом',
                        'опт, тг', 'опт (тг)', 'опт тг', 'опт, тенге', 'опт тенге', 'опт ($)',
                        'цена (опт)', 'цена, опт', 'цена опт, тг', 'цена оптовая, тг',
                        'дилер', 'дилерская', 'дилерская цена', 'дилер цена',
                        'партнер', 'партнерская', 'партнерская цена',
                        'b2b', 'wholesale', 'wholesale_price', 'wholesale price',
                        'опт/розница', 'опт / розница', 'опт/розн'
                    ]) or
                    text in ['опт', 'оптом', 'оптовая', 'опт.']
                )
                if is_wholesale:
                    mapping['wholesale_price_usd'] = col_idx
                    score += 6
                    continue

            # 4. Retail Price
            if 'price_usd' not in mapping:
                is_retail = (
                    any(k in text for k in [
                        'цена розница', 'цена в розницу', 'розница', 'розничная цена', 'розничная',
                        'розничная стоимость', 'цена продажи', 'цена ($)', 'цена usd', 'стоимость',
                        'прайс', 'тариф', 'retail', 'price'
                    ]) or
                    any(k in text for k in ['цена, тг', 'цена (тг)', 'цена тг', 'цена, тенге', 'цена (тенге)', 'цена тенге', 'цена в тенге', 'цена kzt', 'цена (kzt)']) or
                    any(k in text for k in ['цена за шт', 'цена за штуку', 'цена за единицу', 'цена товара']) or
                    text in ['цена', 'цена, тг.', 'цена (тг.)', 'стоимость, тг', 'прайс, тг']
                )
                if is_retail:
                    mapping['price_usd'] = col_idx
                    score += 5
                    continue

            # 5. Min Wholesale Quantity
            if 'min_wholesale_quantity' not in mapping:
                is_moq = (
                    any(k in text for k in [
                        'мин. количество оптом', 'мин количество оптом', 'минимально оптом', 'минимальный заказ оптом',
                        'мин. опт', 'мин опт', 'мин.опт',
                        'мин. заказ', 'мин заказ', 'минимальный заказ', 'мин.заказ',
                        'мин. партия', 'мин партия', 'минимальная партия',
                        'мин. количество', 'минимальное количество', 'мин количество',
                        'мин. кол-во', 'мин кол-во', 'мин.кол-во',
                        'от (шт)', 'от скольки шт', 'от (шт.)', 'от шт', 'опт от', 'кол-во опт',
                        'moq', 'min_qty', 'min_quantity', 'min_order'
                    ])
                )
                if is_moq:
                    mapping['min_wholesale_quantity'] = col_idx
                    score += 4
                    continue

            # 6. Stock Quantity
            if 'stock_quantity' not in mapping:
                is_stock = (
                    any(k in text for k in [
                        'количество в наличии', 'количество в общем', 'количество', 'остаток',
                        'в наличии', 'кол-во', 'кол во', 'склад', 'всего', 'наличие',
                        'общий остаток', 'остаток на складе', 'stock', 'qty', 'quantity'
                    ])
                )
                if is_stock:
                    mapping['stock_quantity'] = col_idx
                    score += 4
                    continue

            # 7. Category / Group
            if 'category' not in mapping:
                is_cat = any(k in text for k in ['группа товара', 'группа', 'подгруппа', 'категория', 'раздел', 'вид товара', 'тип товара', 'category', 'group'])
                if is_cat:
                    mapping['category'] = col_idx
                    score += 4
                    continue

            # 8. Image URL / Photo
            if 'image_url' not in mapping:
                is_img = any(k in text for k in ['фото товара', 'фото', 'ссылка на фото', 'картинка', 'изображение', 'фотография', 'фотографии', 'рисунок', 'image', 'photo', 'picture', 'img'])
                if is_img:
                    mapping['image_url'] = col_idx
                    score += 4
                    continue

            # 9. Source URL
            if 'source_url' not in mapping:
                is_src = any(k in text for k in ['ссылка на источник', 'источник', 'ссылка на товар', 'ссылка', 'url', 'source', 'сайт'])
                if is_src:
                    mapping['source_url'] = col_idx
                    score += 2
                    continue

            # 10. Description
            if 'description' not in mapping:
                is_desc = any(k in text for k in ['описание', 'характеристики', 'инфо', 'детали', 'о товаре', 'спецификация', 'description', 'details'])
                if is_desc:
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
            for col_idx, cell in enumerate(row):
                if cell and not str(cell).strip().isdigit() and str(cell).strip().lower() not in ROW_NUMBER_KEYWORDS:
                    best_mapping['name'] = col_idx
                    best_row_idx = row_idx
                    break
            if 'name' in best_mapping:
                break

    return best_row_idx, best_mapping


def import_products_from_excel(file_obj, default_category_id=None, currency='KZT'):
    """
    Import products from uploaded Excel file (.xlsx) with:
    - Smart column mapping & header detection
    - Accurate KZT/USD currency conversion
    - Embedded image extraction + external URL downloads
    - Full wholesale price & MOQ support
    - Detailed feedback summary
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

    # Extract any images embedded directly into sheet drawings
    embedded_images = extract_embedded_images(sheet)
    logger.info(f"Extracted {len(embedded_images)} embedded images from worksheet")

    # Read rows with cell objects so we can also access cell.hyperlink
    cell_rows = list(sheet.iter_rows())
    if not cell_rows:
        return {
            'success': False,
            'created': 0,
            'updated': 0,
            'total_rows': 0,
            'errors': ["Файл Excel пуст"]
        }

    # Extract plain values for header detection
    raw_values = [[cell.value for cell in row] for row in cell_rows]
    header_row_idx, col_mapping = find_header_row_and_mapping(raw_values)

    if 'name' not in col_mapping:
        header_sample = [str(c) for c in (raw_values[header_row_idx] if raw_values else []) if c]
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
    logger.info(f"Excel import using USD/KZT exchange rate: {exchange_rate}, requested currency: {currency}")

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
    photos_count = 0
    wholesale_count = 0
    errors = []
    total_data_rows = 0

    # Start data rows AFTER header_row_idx
    for row_idx, cells in enumerate(cell_rows[header_row_idx + 1:], start=header_row_idx + 2):
        if not any(c.value for c in cells):
            continue

        def get_cell(field):
            idx = col_mapping.get(field)
            if idx is not None and idx < len(cells):
                return cells[idx]
            return None

        def get_val(field):
            c = get_cell(field)
            return c.value if c else None

        def get_hyperlink(field):
            c = get_cell(field)
            return c.hyperlink.target if (c and c.hyperlink) else None

        raw_name = clean_cell_str(get_val('name'))
        if not raw_name:
            continue

        # If name is just a row number (e.g. "1", "25", "30") and another column might have the real title
        if raw_name.isdigit() and len(raw_name) <= 3:
            candidate_name = None
            for c_idx, cell in enumerate(cells):
                if c_idx != col_mapping.get('name') and cell.value:
                    c_str = clean_cell_str(cell.value)
                    if len(c_str) > 3 and not c_str.isdigit():
                        candidate_name = c_str
                        break
            if candidate_name:
                raw_name = candidate_name
            else:
                # Skip pure numbering row if no title exists
                continue

        # Strip accidental leading numbering in title: e.g. "1. Название" or "1) Название"
        cleaned_name = re.sub(r'^\d+[\.\)]\s*', '', raw_name).strip()
        name = cleaned_name or raw_name
        total_data_rows += 1

        sku = clean_cell_str(get_val('sku')) or None
        description = clean_cell_str(get_val('description'))
        category_name = clean_cell_str(get_val('category'))
        source_url = clean_cell_str(get_val('source_url')) or None

        # Parse prices
        raw_price = parse_decimal(get_val('price_usd'), default=None)
        raw_wholesale = parse_decimal(get_val('wholesale_price_usd'), default=None)

        # If retail is missing, but wholesale price exists:
        # Use wholesale price as base price so item doesn't show $0.00
        if (raw_price is None or raw_price == Decimal('0.00')) and raw_wholesale and raw_wholesale > Decimal('0.00'):
            raw_price = raw_wholesale

        # Determine if values are in KZT:
        # 1. User selected KZT in import modal
        # 2. Or prices are > 600 which clearly signifies KZT in KZ market
        is_kzt = (
            currency.upper() == 'KZT' or
            (raw_price is not None and raw_price > Decimal('600')) or
            (raw_wholesale is not None and raw_wholesale > Decimal('600'))
        )

        if is_kzt and exchange_rate > 0:
            price_usd = round(raw_price / exchange_rate, 2) if raw_price else Decimal('0.00')
            wholesale_price_usd = round(raw_wholesale / exchange_rate, 2) if raw_wholesale else None
        else:
            price_usd = raw_price or Decimal('0.00')
            wholesale_price_usd = raw_wholesale

        if wholesale_price_usd is not None and wholesale_price_usd > 0:
            wholesale_count += 1

        min_wholesale_quantity = parse_int(get_val('min_wholesale_quantity'), default=1)
        stock_quantity = parse_int(get_val('stock_quantity'), default=0)

        # Photo handling:
        # 1. Check embedded image for this row (0-indexed row is row_idx - 1)
        image_tuple = embedded_images.get(row_idx - 1)
        
        # 2. Check hyperlink in image column
        image_url = get_hyperlink('image_url')
        if not image_url:
            val_img = clean_cell_str(get_val('image_url'))
            if val_img and (val_img.startswith('http://') or val_img.startswith('https://')):
                image_url = val_img

        # 3. Fallback: check all cells in row for a valid image URL if still none
        if not image_tuple and not image_url:
            for cell in cells:
                hl = cell.hyperlink.target if cell.hyperlink else None
                c_val = str(cell.value or '').strip()
                target_cand = hl or c_val
                if target_cand and (target_cand.startswith('http://') or target_cand.startswith('https://')):
                    if any(target_cand.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']) or 'drive.google.com' in target_cand:
                        image_url = target_cand
                        break

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
                    errors.append(f"Строка {row_idx}: Ошибка создания категории '{category_name}': {cat_err}")
                    product_category = default_category or get_uncategorized()
        elif default_category:
            product_category = default_category
        else:
            product_category = get_uncategorized()

        # Find existing product (by SKU first, then by name)
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

                # Save photo if product currently lacks one
                if not product.main_image:
                    if image_tuple:
                        fname, fcontent = image_tuple
                        product.main_image.save(fname, fcontent, save=False)
                        photos_count += 1
                    elif image_url:
                        fname, fcontent = download_image_from_url(image_url)
                        if fname and fcontent:
                            product.main_image.save(fname, fcontent, save=False)
                            photos_count += 1

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

                if image_tuple:
                    fname, fcontent = image_tuple
                    new_product.main_image.save(fname, fcontent, save=False)
                    photos_count += 1
                elif image_url:
                    fname, fcontent = download_image_from_url(image_url)
                    if fname and fcontent:
                        new_product.main_image.save(fname, fcontent, save=False)
                        photos_count += 1

                new_product.save()
                created_count += 1

        except Exception as e:
            errors.append(f"Строка {row_idx} ({name[:30]}): {str(e)}")

    # Create human-readable detected columns mapping for user feedback
    field_labels = {
        'name': 'Название товара',
        'sku': 'Код / Артикул',
        'category': 'Категория',
        'price_usd': 'Розничная цена',
        'wholesale_price_usd': 'Оптовая цена',
        'min_wholesale_quantity': 'Мин. опт (кол-во)',
        'stock_quantity': 'Остаток на складе',
        'image_url': 'Фото / Изображение',
        'source_url': 'Ссылка на источник',
        'description': 'Описание'
    }

    detected_readable = []
    header_row_vals = raw_values[header_row_idx] if header_row_idx < len(raw_values) else []
    for field, col_idx in col_mapping.items():
        label = field_labels.get(field, field)
        col_letter = get_column_letter(col_idx + 1)
        orig_name = str(header_row_vals[col_idx] or '').strip() if col_idx < len(header_row_vals) else ''
        detected_readable.append(f"{label}: колонка {col_letter} («{orig_name}»)")

    return {
        'success': True,
        'created': created_count,
        'updated': updated_count,
        'total_rows': total_data_rows,
        'photos_count': photos_count,
        'wholesale_count': wholesale_count,
        'currency_used': f"₸ KZT (курс {exchange_rate})" if is_kzt else "$ USD",
        'detected_header_row': header_row_idx + 1,
        'detected_columns': detected_readable,
        'errors': errors[:25]
    }


def generate_excel_template():
    """
    Generate an elegant formatted Excel template for uploading products
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
        "Цена в розницу (₸ или $) *",
        "Цена оптом (₸ или $)",
        "Мин. количество оптом (шт)",
        "Количество в наличии (всего)",
        "Фото (Ссылка или вставить картинку)",
        "Ссылка на источник"
    ]

    ws.append(headers)

    sample_rows = [
        [
            "INP-KNX-01",
            "Сенсорная панель KNX 7 дюймов",
            "Умный дом (KNX)",
            "Многофункциональная настенная сенсорная панель управления освещением и климатом",
            "185 000 тг",
            "150 000 тг",
            5,
            25,
            "https://images.unsplash.com/photo-1558002038-1055907df827?w=600",
            "https://supplier.example.com/item/101"
        ],
        [
            "INP-CAM-02",
            "IP-камера 4K с ИИ-аналитикой",
            "Видеонаблюдение",
            "Купольная камера видеонаблюдения с распознаванием лиц и ночным видением",
            "55 000 тг",
            "42 000 тг",
            10,
            100,
            "https://images.unsplash.com/photo-1557597774-9d273605dfa9?w=600",
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

    ws.row_dimensions[1].height = 34

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
            if col_idx in [5, 6, 7, 8]:
                cell.alignment = Alignment(horizontal="right", vertical="center")
            else:
                cell.alignment = Alignment(vertical="center")

    column_widths = {
        1: 22, 2: 34, 3: 24, 4: 40, 5: 24, 6: 22, 7: 26, 8: 26, 9: 36, 10: 28
    }

    for col_idx, width in column_widths.items():
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    return output.getvalue()
