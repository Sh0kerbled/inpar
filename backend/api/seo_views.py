import re
import html
import json
from decimal import Decimal
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Category
from .utils import get_usd_to_kzt_rate

BASE_URL = "https://inpar.kz"

SERVICES_DATA = {
    "bms-dispatching": {
        "title": "Диспетчеризация BMS и автоматизация зданий в Алматы",
        "badge": "BMS & Automation",
        "description": "Комплексное управление инженерными системами зданий в Казахстане. Интеграция вентиляции, отопления, кондиционирования, освещения и энергоучета в единую платформу с веб-интерфейсом для снижения энергопотребления до 30%.",
        "keywords": "диспетчеризация BMS Алматы, автоматизация зданий Казахстан, BMS системы, энергоэффективность зданий, автоматизация ОВиК, SCADA диспетчеризация",
        "icon": "Building2",
        "features": [
            "Единая панель мониторинга всех инженерных узлов объекта",
            "Снижение затрат на электроэнергию и отопление на 15–30%",
            "Оперативное оповещение об авариях в Telegram / SMS / Email",
            "Интеграция протоколов BACnet, Modbus, KNX, LonWorks",
            "Сбор архивов данных и аналитика работы оборудования"
        ],
        "stages": [
            "Аудит инженерных систем объекта и ТЗ",
            "Проектирование шкафов автоматики и схем диспетчеризации",
            "Сборка щитов автоматики и поставка контроллеров",
            "Пусконаладочные работы и программирование SCADA/BMS",
            "Обучение службы эксплуатации и гарантийная поддержка"
        ],
        "faqs": [
            {
                "q": "Какие объекты подходят для внедрения BMS?",
                "a": "Бизнес-центры, торговые комплексы (ТРЦ), отели, медицинские центры, склады и жилые комплексы любого масштаба."
            },
            {
                "q": "За какой срок окупается система автоматизации BMS?",
                "a": "В среднем окупаемость составляет от 1.5 до 3 лет за счет снижения потребления энергии и сокращения расходов на ремонт."
            }
        ]
    },
    "fire-safety": {
        "title": "Пожарная безопасность и системы оповещения (АПС и СОУЭ) в Алматы",
        "badge": "Fire Safety",
        "description": "Проектирование, поставка и монтаж адресной пожарной сигнализации (АПС), систем оповещения и управления эвакуацией (СОУЭ) 1-5 типов, газового и водяного пожаротушения под ключ по нормам Республики Казахстан.",
        "keywords": "пожарная сигнализация Алматы, монтаж АПС СОУЭ, адресная пожарная сигнализация, системы оповещения при пожаре, пожаротушение Казахстан",
        "icon": "ShieldAlert",
        "features": [
            "Адресные пожарные панели с точным определением места задымления",
            "Цифровые системы оповещения и трансляции звука (СОУЭ 1-5 типов)",
            "Интеграция с СКУД, лифтами, вентиляцией и огнезадерживающими клапанами",
            "Полное соответствие СНиП и противопожарным нормам РК",
            "Сертифицированное оборудование ведущих мировых производителей"
        ],
        "stages": [
            "Разработка проектно-сметной документации (стадии П и Р)",
            "Согласование проекта в надзорных органах",
            "Прокладка огнестойких кабельных линий и монтаж извещателей",
            "Установка приборов управления и настройка сценариев эвакуации",
            "Комплексные испытания и сдача объекта пожарной инспекции"
        ],
        "faqs": [
            {
                "q": "Предоставляете ли вы гарантию и сервисное обслуживание?",
                "a": "Да, компания INPAR предоставляет официальную гарантию на оборудование и монтажные работы, а также регламентное ТО."
            },
            {
                "q": "Возможна ли модернизация существующей пожарной сигнализации?",
                "a": "Да, мы проводим аудит текущих систем и поэтапную замену устаревших компонентов на современные адресные панели."
            }
        ]
    },
    "cctv-access-control": {
        "title": "Видеонаблюдение и контроль доступа (СКУД, NVR, Биометрия) в Алматы",
        "badge": "Security & Access",
        "description": "Интеллектуальные системы IP-видеонаблюдения высокой четкости, видеоаналитика, распознавание лиц и номеров авто, биометрический контроль доступа (СКУД) и турникеты для коммерческих и промышленных объектов.",
        "keywords": "видеонаблюдение Алматы, установка СКУД Казахстан, распознавание лиц, IP камеры, турникеты, учет рабочего времени, NVR системы",
        "icon": "Cctv",
        "features": [
            "IP-камеры с искусственным интеллектом (распознавание лиц, номеров, детекция скоплений)",
            "Биометрические терминалы Face ID, отпечатки пальцев, RFID и мобильный доступ",
            "Турникеты, шлагбаумы и автоматические ворота с контролем проезда",
            "Учет рабочего времени персонала и интеграция с 1С:Предприятие",
            "Удаленный защищенный доступ к видеоархиву со смартфона и ПК"
        ],
        "stages": [
            "Обследование объекта и расчет зон обзора камер",
            "Подбор камер, серверов хранения данных и контроллеров доступа",
            "Монтаж кабельной трассы, установка камер и запорных устройств",
            "Настройка видеоаналитики, серверов записи и прав доступа",
            "Передача системы заказчику с инструкциями по эксплуатации"
        ],
        "faqs": [
            {
                "q": "Сколько времени хранится видеоархив?",
                "a": "Глубина архива рассчитывается под ваши требования — обычно от 30 до 90 суток непрерывной записи в высоком разрешении."
            },
            {
                "q": "Работает ли система при отключении электроэнергии?",
                "a": "Мы комплектуем узлы бесперебойным питанием (ИБП), обеспечивающим автономную работу критических участков."
            }
        ]
    },
    "smart-home-knx": {
        "title": "Умный дом стандарта KNX/EIB под ключ в Алматы и Казахстане",
        "badge": "KNX Smart Home",
        "description": "Проектирование и реализация премиальных систем «Умный дом» мирового стандарта KNX. Комплексное управление освещением, моторизованными шторами, климатом (HVAC), мультирум и безопасностью с единого приложения и дизайнерских панелей.",
        "keywords": "умный дом Алматы, KNX Казахстан, автоматизация коттеджей, управление климатом умный дом, дизайнерские выключатели KNX, умный дом под ключ",
        "icon": "Home",
        "features": [
            "Международный стандарт KNX — надежность и независимость от одного производителя",
            "Управление сценариями освещения, шторами и диммированием DALI",
            "Климат-контроль: согласованная работа кондиционеров, теплого пола и фанкойлов",
            "Интеграция с Apple HomeKit, Яндекс Алиса, Google Home и панелями Crestron/Control4",
            "Дизайнерские выключатели из стекла, латуни, алюминия и кожи"
        ],
        "stages": [
            "Разработка концепции умного дома и выбор сценариев жизни",
            "Проектирование кабельных трасс, щитов и спецификации KNX",
            "Монтаж слаботочных трасс на стадии чернового ремонта",
            "Сборка щита автоматики, установка приводов, датчиков и выключателей",
            "Индивидуальное программирование сценариев и финальная отладка"
        ],
        "faqs": [
            {
                "q": "На каком этапе ремонта нужно начинать проектирование умного дома?",
                "a": "Оптимально — на этапе дизайн-проекта до начала черновых электромонтажных работ, чтобы заложить необходимые кабели."
            },
            {
                "q": "Что произойдет с умным домом при сбое интернета?",
                "a": "Шина KNX полностью децентрализована и работает автономно внутри дома без интернета. Все клавиши, датчики и климат продолжают функционировать."
            }
        ]
    },
    "sound-and-light": {
        "title": "Профессиональный звук и сценический свет в Алматы",
        "badge": "Pro Audio & Light",
        "description": "Проектирование и оснащение конференц-залов, концертных площадок, ресторанов, мечетей и торговых центров профессиональным звуковым и световым оборудованием. Акустический расчет, линейные массивы, микрофонные парки и LED-экраны.",
        "keywords": "профессиональный звук Алматы, сценический свет, звуковое оборудование для ресторанов, акустический расчет, линейный массив Казахстан, конференц-системы",
        "icon": "Speaker",
        "features": [
            "Компьютерный акустический расчет помещений (EASE) для идеальной разборчивости речи",
            "Линейные массивы, сабвуферы, потолочная и настенная акустика High-End класса",
            "Конференц-системы, синхронный перевод и радиомикрофоны",
            "Интеллектуальный динамический сценический свет (Spot, Beam, Wash) и DMX-управление",
            "Светодиодные LED-экраны высокого разрешения для сцен и холлов"
        ],
        "stages": [
            "Акустические замеры помещения и 3D-моделирование звукового поля",
            "Составление спецификации оборудования под бюджет и задачи",
            "Поставка, монтаж ферм, подвеса акустики и прокладка аудио-линий",
            "Пусконаладка DSP-аудиопроцессоров и настройка световых пресетов",
            "Тестовые прогоны и обучение звукорежиссеров заказчика"
        ],
        "faqs": [
            {
                "q": "Делаете ли вы акустический расчет перед подбором оборудования?",
                "a": "Да, акустический расчет обязателен для предотвращения эха, реверберации и обеспечения равномерного звукового давления."
            }
        ]
    },
    "networks-smatv": {
        "title": "Информационные сети, СКС и SMATV (IPTV, Спутниковое ТВ) в Алматы",
        "badge": "Networks & SMATV",
        "description": "Проектирование и построение структурированных кабельных сетей (СКС), оптоволоконных трасс, бесшовного корпоративного Wi-Fi, IP-телефонии (АТС) и гостиничных систем интерактивного телевидения SMATV/IPTV.",
        "keywords": "монтаж СКС Алматы, корпоративный Wi-Fi, гостиничное телевидение SMATV, IPTV для отелей, оптические сети Казахстан, офисные сети",
        "icon": "Network",
        "features": [
            "СКС категорий 5e, 6, 6A, 7 с сертификацией и гарантией до 25 лет",
            "Оптоволоконные магистрали (ВОЛС) и сварка оптики",
            "Бесшовный роуминг Wi-Fi для офисов, складов и отелей с высокой плотностью клиентов",
            "IP-телефония и виртуальные АТС с интеграцией в CRM",
            "Комплексные системы SMATV/IPTV с брендированным меню для отелей"
        ],
        "stages": [
            "Радиообследование и аудит сетевых потребностей объекта",
            "Проектирование серверных помещений, кроссовых и кабельных трасс",
            "Монтаж лотков, протяжка витой пары/оптики, монтаж розеток и патч-панелей",
            "Тестирование линий кабельными анализаторами Fluke Networks",
            "Настройка сетевого оборудования, маршрутизации, VLAN и политик безопасности"
        ],
        "faqs": [
            {
                "q": "Предоставляете ли вы паспорта и сертификацию на СКС?",
                "a": "Да, мы проводим сертифицированное тестирование линий сканером Fluke с предоставлением протокола на каждый порт."
            }
        ]
    },
    "system-integration": {
        "title": "Системная интеграция слаботочных систем под ключ в Казахстане",
        "badge": "Systems Integration",
        "description": "Генеральный подряд по слаботочным системам. Объединение разрозненного оборудования (BMS, пожарная сигнализация, СКУД, CCTV, звук, мультимедиа) в единую слаженно работающую экосистему с централизованным управлением.",
        "keywords": "системная интеграция Алматы, генеральный подрядчик слаботочные сети Казахстан, комплексные инженерные системы, интеграция оборудования",
        "icon": "Combine",
        "features": [
            "Единая точка ответственности за все слаботочные системы объекта",
            "Бесшовная стыковка оборудования разных брендов по открытым протоколам",
            "Согласованная работа систем безопасности (при пожаре: разблокировка дверей СКУД, отключение вентиляции)",
            "Снижение бюджета стройки за счет исключения дублирующих кабельных трасс",
            "Собственный штат квалифицированных инженеров и программистов"
        ],
        "stages": [
            "Анализ генерального проекта здания и координация смежных разделов",
            "Разработка комплексного проекта автоматизации и интеграции",
            "Централизованная поставка оборудования напрямую от заводов",
            "Шеф-монтаж, пусконаладка и интеграционные тесты систем",
            "Сдача объекта госкомиссии и службам технического надзора"
        ],
        "faqs": [
            {
                "q": "Работаете ли вы по всему Казахстану?",
                "a": "Да, мы реализуем масштабные проекты в Алматы, Астане, Шымкенте, Актобе, Туркестане и других городах РК."
            }
        ]
    }
}


def robots_txt(request):
    """Serve dynamic robots.txt pointing to the XML sitemap"""
    content = f"""# INPAR.KZ robots.txt
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /api/

Sitemap: {BASE_URL}/sitemap.xml
"""
    return HttpResponse(content, content_type="text/plain; charset=utf-8")


def sitemap_xml(request):
    """
    Generate dynamic XML sitemap with all pages, services and active products.
    Includes Google image sitemap extensions.
    """
    urls = []

    # Main pages
    urls.append({
        "loc": f"{BASE_URL}/",
        "priority": "1.0",
        "changefreq": "daily"
    })
    urls.append({
        "loc": f"{BASE_URL}/products",
        "priority": "0.9",
        "changefreq": "daily"
    })
    urls.append({
        "loc": f"{BASE_URL}/projects",
        "priority": "0.8",
        "changefreq": "weekly"
    })

    # Services
    for slug in SERVICES_DATA.keys():
        urls.append({
            "loc": f"{BASE_URL}/services/{slug}",
            "priority": "0.9",
            "changefreq": "weekly"
        })

    # Products from DB
    products = Product.objects.filter(is_active=True).select_related('category').order_by('-updated_at')
    for p in products:
        lastmod = p.updated_at.strftime('%Y-%m-%d') if p.updated_at else '2026-10-22'
        prod_entry = {
            "loc": f"{BASE_URL}/products/{p.id}",
            "priority": "0.8",
            "changefreq": "weekly",
            "lastmod": lastmod,
        }
        if p.main_image:
            image_url = f"{BASE_URL}{p.main_image.url}" if not p.main_image.url.startswith('http') else p.main_image.url
            prod_entry["image"] = {
                "loc": image_url,
                "title": p.name
            }
        urls.append(prod_entry)

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]

    for item in urls:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{html.escape(item['loc'])}</loc>")
        if "lastmod" in item:
            xml_lines.append(f"    <lastmod>{item['lastmod']}</lastmod>")
        if "changefreq" in item:
            xml_lines.append(f"    <changefreq>{item['changefreq']}</changefreq>")
        if "priority" in item:
            xml_lines.append(f"    <priority>{item['priority']}</priority>")
        if "image" in item:
            xml_lines.append("    <image:image>")
            xml_lines.append(f"      <image:loc>{html.escape(item['image']['loc'])}</image:loc>")
            xml_lines.append(f"      <image:title>{html.escape(item['image']['title'])}</image:title>")
            xml_lines.append("    </image:image>")
        xml_lines.append("  </url>")

    xml_lines.append("</urlset>")
    return HttpResponse("\n".join(xml_lines), content_type="application/xml; charset=utf-8")


def _render_base_html(title, description, keywords, canonical, og_image, json_ld_list, body_content):
    """Helper to render server-side HTML for search bots and social crawlers"""
    og_image = og_image or f"{BASE_URL}/assets/sticker-CGlHhmMq.png"
    json_ld_scripts = "\n".join([
        f'    <script type="application/ld+json">\n{json.dumps(schema, ensure_ascii=False, indent=2)}\n    </script>'
        for schema in json_ld_list
    ])

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description)}">
    <meta name="keywords" content="{html.escape(keywords)}">
    <link rel="canonical" href="{html.escape(canonical)}">

    <!-- Open Graph / Facebook / WhatsApp / Telegram -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{html.escape(canonical)}">
    <meta property="og:title" content="{html.escape(title)}">
    <meta property="og:description" content="{html.escape(description)}">
    <meta property="og:image" content="{html.escape(og_image)}">
    <meta property="og:site_name" content="INPAR.KZ">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html.escape(title)}">
    <meta name="twitter:description" content="{html.escape(description)}">
    <meta name="twitter:image" content="{html.escape(og_image)}">

{json_ld_scripts}

    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #1A1D23;
            color: #E8E9ED;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        header {{
            border-bottom: 1px solid #333842;
            padding-bottom: 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .logo {{
            font-size: 24px;
            font-weight: 700;
            letter-spacing: 2px;
            color: #B8A276;
            text-decoration: none;
        }}
        nav a {{
            color: #9BA1AB;
            text-decoration: none;
            margin-left: 20px;
            font-size: 14px;
        }}
        nav a:hover {{
            color: #3B82F6;
        }}
        h1 {{
            font-size: 32px;
            color: #FFFFFF;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        h2 {{
            font-size: 24px;
            color: #B8A276;
            margin-top: 30px;
            border-bottom: 1px solid #333842;
            padding-bottom: 10px;
        }}
        .badge {{
            display: inline-block;
            background-color: #333842;
            color: #B8A276;
            padding: 4px 12px;
            font-size: 12px;
            border-radius: 4px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 15px;
        }}
        .price {{
            font-size: 28px;
            color: #3B82F6;
            font-weight: 700;
            margin: 15px 0;
        }}
        .btn {{
            display: inline-block;
            background-color: #25D366;
            color: #FFFFFF;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            margin-top: 15px;
        }}
        .table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .table th, .table td {{
            border: 1px solid #333842;
            padding: 12px;
            text-align: left;
        }}
        .table th {{
            background-color: #252932;
            color: #B8A276;
        }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .card {{
            background-color: #252932;
            border: 1px solid #333842;
            border-radius: 8px;
            padding: 20px;
        }}
        .card h3 {{
            margin-top: 0;
            font-size: 18px;
            color: #E8E9ED;
        }}
        .card a {{
            color: #3B82F6;
            text-decoration: none;
        }}
        footer {{
            margin-top: 60px;
            border-top: 1px solid #333842;
            padding-top: 25px;
            color: #9BA1AB;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <a href="{BASE_URL}/" class="logo">INPAR.KZ</a>
            <nav>
                <a href="{BASE_URL}/">Главная</a>
                <a href="{BASE_URL}/products">Каталог</a>
                <a href="{BASE_URL}/projects">Проекты</a>
                <a href="{BASE_URL}/#services">Услуги</a>
                <a href="{BASE_URL}/#contact">Контакты</a>
            </nav>
        </header>

        {body_content}

        <footer>
            <p><strong>ТОО «INPAR.KZ»</strong> — Системная интеграция слаботочных систем, автоматизация зданий (BMS) и Умный дом KNX.</p>
            <p>Адрес: Казахстан, г. Алматы, ЖК «Сарыарка», 1-й микрорайон, 68/4 | Тел: +7 (701) 995-42-17 | Email: info@inpar.kz</p>
            <p>© 2014–2026 INPAR.KZ. Все права защищены.</p>
        </footer>
    </div>
</body>
</html>"""


def bot_render_view(request):
    """
    Renders fully structured semantic HTML for search crawlers (Googlebot, YandexBot, etc.)
    and social share bots (WhatsApp, Telegram, Facebook, Twitter).
    """
    path = request.GET.get('path', request.path)
    # Strip trailing slash for uniform matching
    clean_path = path.rstrip('/') if path != '/' else '/'

    # 1. Product Detail Page: /products/<id>
    product_match = re.search(r'^/products/(\d+)$', clean_path)
    if product_match:
        product_id = product_match.group(1)
        try:
            product = Product.objects.select_related('category').prefetch_related('characteristics', 'images').get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return HttpResponse("Товар не найден", status=404)

        rate = Decimal(str(get_usd_to_kzt_rate()))
        price_kzt = int(round(product.price_usd * rate)) if product.price_usd else 0
        wholesale_kzt = int(round(product.wholesale_price_usd * rate)) if product.wholesale_price_usd else 0

        title = f"{product.name} — Купить в Алматы, цена, характеристики | INPAR.KZ"
        desc_text = product.description or "Профессиональное оборудование для слаботочных систем, умного дома и автоматизации от официального поставщика INPAR в Казахстане."
        description = f"Купить {product.name} в Алматы. Цена: ₸{price_kzt:,}. {desc_text[:140]}... Доставка по Казахстану, официальная гарантия."
        keywords = f"{product.name}, купить {product.name}, цена {product.name}, {product.sku or ''}, звуковое оборудование Алматы, автоматизация Казахстан"
        canonical = f"{BASE_URL}/products/{product.id}"

        image_url = f"{BASE_URL}{product.main_image.url}" if product.main_image else f"{BASE_URL}/assets/sticker-CGlHhmMq.png"

        schema_product = {
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": product.name,
            "image": [image_url],
            "description": product.description or product.name,
            "sku": product.sku or f"INPAR-{product.id}",
            "brand": {
                "@type": "Brand",
                "name": "INPAR"
            },
            "offers": {
                "@type": "Offer",
                "url": canonical,
                "priceCurrency": "KZT",
                "price": str(price_kzt),
                "priceValidUntil": "2027-12-31",
                "itemCondition": "https://schema.org/NewCondition",
                "availability": "https://schema.org/InStock" if product.stock_quantity > 0 else "https://schema.org/InStock",
                "seller": {
                    "@type": "Organization",
                    "name": "INPAR.KZ"
                }
            }
        }

        schema_breadcrumbs = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Главная", "item": f"{BASE_URL}/"},
                {"@type": "ListItem", "position": 2, "name": "Каталог", "item": f"{BASE_URL}/products"},
                {"@type": "ListItem", "position": 3, "name": product.name, "item": canonical}
            ]
        }

        char_rows = ""
        for c in product.characteristics.all():
            char_rows += f"<tr><td><strong>{html.escape(c.name)}</strong></td><td>{html.escape(c.value)}</td></tr>"

        body_content = f"""
        <span class="badge">Каталог оборудования</span>
        <h1>{html.escape(product.name)}</h1>
        {f'<p><strong>Артикул / SKU:</strong> {html.escape(product.sku)}</p>' if product.sku else ''}
        {f'<div class="price">₸{price_kzt:,} <span style="font-size: 16px; color: #9BA1AB; font-weight: normal;">($ {product.price_usd})</span></div>' if price_kzt > 0 else ''}
        {f'<p style="color: #60A5FA;">Оптовая цена от {product.min_wholesale_quantity or 1} шт.: <strong>₸{wholesale_kzt:,}</strong></p>' if wholesale_kzt > 0 else ''}

        <p><a href="https://wa.me/77019954217?text={html.escape('Здравствуйте! Интересует товар ' + product.name)}" class="btn">Заказать в WhatsApp</a></p>

        <h2>Описание товара</h2>
        <p>{html.escape(product.description or 'Высококачественное оборудование для системной интеграции, диспетчеризации и профессионального звука.')}</p>

        {f'''<h2>Технические характеристики</h2>
        <table class="table">
            <thead>
                <tr><th>Параметр</th><th>Значение</th></tr>
            </thead>
            <tbody>
                {char_rows}
            </tbody>
        </table>''' if char_rows else ''}

        <h2>Условия поставки и гарантия</h2>
        <p>Компания INPAR осуществляет поставку оборудования по всему Казахстану. Возможен самовывоз со склада в Алматы (ЖК «Сарыарка», 1-й мкр., 68/4) или курьерская доставка в любой регион (Астана, Шымкент, Караганда, Актобе). На все товары предоставляется официальная гарантия.</p>
        """

        return HttpResponse(_render_base_html(title, description, keywords, canonical, image_url, [schema_product, schema_breadcrumbs], body_content), content_type="text/html; charset=utf-8")

    # 2. Service Detail Page: /services/<slug>
    service_match = re.search(r'^/services/([a-z0-9-]+)$', clean_path)
    if service_match:
        slug = service_match.group(1)
        if slug in SERVICES_DATA:
            service = SERVICES_DATA[slug]
            canonical = f"{BASE_URL}/services/{slug}"
            title = f"{service['title']} | INPAR.KZ"
            description = service['description']
            keywords = service['keywords']

            schema_service = {
                "@context": "https://schema.org",
                "@type": "Service",
                "name": service['title'],
                "description": service['description'],
                "provider": {
                    "@type": "LocalBusiness",
                    "name": "INPAR.KZ",
                    "telephone": "+77019954217",
                    "address": {
                        "@type": "PostalAddress",
                        "streetAddress": "ЖК «Сарыарка», 1-й микрорайон, 68/4",
                        "addressLocality": "Алматы",
                        "addressCountry": "KZ"
                    }
                },
                "areaServed": {
                    "@type": "Country",
                    "name": "Kazakhstan"
                }
            }

            schema_faq = {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": faq["q"],
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": faq["a"]
                        }
                    } for faq in service.get("faqs", [])
                ]
            }

            features_html = "".join([f"<li>{html.escape(f)}</li>" for f in service['features']])
            stages_html = "".join([f"<li>{html.escape(s)}</li>" for s in service['stages']])
            faqs_html = "".join([f"<p><strong>Вопрос: {html.escape(faq['q'])}</strong><br>Ответ: {html.escape(faq['a'])}</p>" for faq in service.get("faqs", [])])

            body_content = f"""
            <span class="badge">{html.escape(service['badge'])}</span>
            <h1>{html.escape(service['title'])}</h1>
            <p style="font-size: 18px; color: #D1D5DB;">{html.escape(service['description'])}</p>
            <p><a href="https://wa.me/77019954217?text={html.escape('Здравствуйте! Интересует услуга ' + service['title'])}" class="btn">Получить расчет стоимости</a></p>

            <h2>Преимущества и возможности</h2>
            <ul>{features_html}</ul>

            <h2>Этапы выполнения проекта</h2>
            <ol>{stages_html}</ol>

            {f'''<h2>Часто задаваемые вопросы (FAQ)</h2>
            <div style="background-color: #252932; padding: 20px; border-radius: 8px; border: 1px solid #333842;">
                {faqs_html}
            </div>''' if faqs_html else ''}

            <h2>Заказать проект в компании INPAR</h2>
            <p>Свяжитесь с нашими ведущими инженерами для бесплатной консультации, выезда на объект и предварительного расчета сметы в Алматы и по всему Казахстану: <strong>+7 (701) 995-42-17</strong>.</p>
            """

            return HttpResponse(_render_base_html(title, description, keywords, canonical, None, [schema_service, schema_faq], body_content), content_type="text/html; charset=utf-8")

    # 3. Products Catalog: /products
    if clean_path == '/products':
        canonical = f"{BASE_URL}/products"
        title = "Каталог оборудования для системной интеграции и звука | INPAR.KZ"
        description = "Каталог профессионального оборудования в Алматы: акустика, датчики, контроллеры, усилители и модули автоматизации с доставкой по Казахстану."
        keywords = "каталог оборудования умный дом, акустика Алматы, датчики BMS, слаботочное оборудование Казахстан"

        products = Product.objects.filter(is_active=True)[:40]
        items_html = ""
        for p in products:
            items_html += f"""
            <div class="card">
                <h3><a href="{BASE_URL}/products/{p.id}">{html.escape(p.name)}</a></h3>
                {f'<p style="color: #9BA1AB; font-size: 13px;">Арт: {html.escape(p.sku)}</p>' if p.sku else ''}
                {f'<p style="color: #3B82F6; font-weight: bold;">$ {p.price_usd}</p>' if p.price_usd else ''}
                <p><a href="{BASE_URL}/products/{p.id}">Подробнее →</a></p>
            </div>
            """

        body_content = f"""
        <span class="badge">Каталог</span>
        <h1>Профессиональное оборудование и компоненты автоматизации</h1>
        <p>{description}</p>
        <div class="grid">
            {items_html}
        </div>
        """
        return HttpResponse(_render_base_html(title, description, keywords, canonical, None, [], body_content), content_type="text/html; charset=utf-8")

    # 4. Default: Homepage /
    canonical = f"{BASE_URL}/"
    title = "INPAR.KZ — Системная интеграция, Умный дом KNX и BMS в Алматы"
    description = "Компания INPAR с 2014 года выполняет проектирование, монтаж и интеграцию слаботочных систем, автоматизации зданий (BMS), пожарной безопасности и умных домов KNX в Казахстане."
    keywords = "умный дом Алматы, KNX Казахстан, BMS диспетчеризация, пожарная сигнализация Алматы, видеонаблюдение СКУД, профессиональный звук, слаботочные системы"

    schema_organization = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "INPAR.KZ",
        "image": f"{BASE_URL}/assets/sticker-CGlHhmMq.png",
        "telephone": "+77019954217",
        "email": "info@inpar.kz",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "ЖК «Сарыарка», 1-й микрорайон, 68/4",
            "addressLocality": "Алматы",
            "addressRegion": "Алматы",
            "postalCode": "050000",
            "addressCountry": "KZ"
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 43.233071,
            "longitude": 76.852412
        },
        "openingHoursSpecification": {
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
            "opens": "09:00",
            "closes": "18:00"
        },
        "sameAs": [
            "https://inpar.kz"
        ]
    }

    services_cards = ""
    for slug, s in SERVICES_DATA.items():
        services_cards += f"""
        <div class="card">
            <span class="badge">{html.escape(s['badge'])}</span>
            <h3><a href="{BASE_URL}/services/{slug}">{html.escape(s['title'])}</a></h3>
            <p style="font-size: 14px; color: #9BA1AB;">{html.escape(s['description'][:140])}...</p>
            <p><a href="{BASE_URL}/services/{slug}">Узнать подробнее →</a></p>
        </div>
        """

    body_content = f"""
    <span class="badge">Engineering Excellence</span>
    <h1>INPAR — Интеллектуальная автоматизация и слаботочные системы в Казахстане</h1>
    <p style="font-size: 18px; color: #D1D5DB;">Основанная в 2014 году в Алматы, компания INPAR.KZ специализируется на внедрении слаботочных систем, автоматизации зданий (BMS) и технологий «Умный дом» стандарта KNX/EIB. Мы берем на себя полный цикл: от акустического и системного проектирования до программирования и сервисного обслуживания.</p>
    <p><a href="https://wa.me/77019954217" class="btn">Связаться с инженером в WhatsApp</a></p>

    <h2>Наши ключевые направления услуг</h2>
    <div class="grid">
        {services_cards}
    </div>

    <h2>Реализованные проекты</h2>
    <p>Наш опыт включает десятки знаковых объектов: отели премиум-класса, торгово-развлекательные центры, офисные комплексы и частные резиденции в Алматы, Астане, Шымкенте, Актобе и за рубежом. <a href="{BASE_URL}/projects" style="color: #3B82F6;">Посмотреть портфолио проектов →</a></p>
    """

    return HttpResponse(_render_base_html(title, description, keywords, canonical, None, [schema_organization], body_content), content_type="text/html; charset=utf-8")
