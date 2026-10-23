# scripts/apply_seo_enrichment.py
import sys
import os
import json
import ast

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.enrich_seo_data import ENRICHMENTS

seo_views_path = 'backend/api/seo_views.py'
with open(seo_views_path, 'r', encoding='utf-8') as f:
    orig_code = f.read()

start_pos = orig_code.find('SERVICES_DATA = {')
end_pos = orig_code.find('def robots_txt(')

data_code = orig_code[start_pos:end_pos].strip()
namespace = {}
exec(data_code, namespace)
services_data = namespace['SERVICES_DATA']

print(f"Loaded {len(services_data)} services.")

for slug, extra in ENRICHMENTS.items():
    if slug in services_data:
        s = services_data[slug]
        if 'knowsAbout' in extra:
            s['knowsAbout'] = extra['knowsAbout']
        if 'related_services' in extra:
            s['related_services'] = extra['related_services']

        for lang in ('ru', 'kz', 'en'):
            if lang in extra and lang in s:
                lang_extra = extra[lang]
                lang_data = s[lang]
                if 'problems' in lang_extra:
                    lang_data['problems'] = lang_extra['problems']
                if 'keywords' in lang_extra:
                    lang_data['keywords'] += lang_extra['keywords']
                if 'faqs' in lang_extra:
                    existing_qs = [f['q'] for f in lang_data.get('faqs', [])]
                    for new_f in lang_extra['faqs']:
                        if new_f['q'] not in existing_qs:
                            lang_data.setdefault('faqs', []).append(new_f)

print("Enriched services_data.")

new_services_data_code = "SERVICES_DATA = " + json.dumps(services_data, ensure_ascii=False, indent=4) + "\n\n"

# Recombine: start of file up to start_pos + new_services_data_code + rest of file
tail_code = orig_code[end_pos:]

# Add helper for product-to-service links if not present
product_links_code = '''
PRODUCT_SERVICE_LINKS = {
    "obt": ["sound-and-light", "fire-safety", "low-voltage-systems"],
    "lunatek": ["electrical-cabinets", "mcc-cabinets", "system-integration"],
    "sunark": ["electrical-cabinets", "mcc-cabinets", "system-integration"],
    "dahua": ["cctv-access-control", "low-voltage-systems", "smart-home-knx"],
    "sprut": ["cctv-access-control", "low-voltage-systems"],
    "temco": ["ddc-automation", "bms-dispatching", "industrial-automation"],
    "cabinet": ["electrical-cabinets", "mcc-cabinets", "ddc-automation"],
    "w5500": ["industrial-automation", "bms-dispatching", "system-integration"]
}

def _get_related_services_for_product(product_name, product_sku):
    combined = f"{product_name} {product_sku or ''}".lower()
    services = set()
    if any(k in combined for k in ("obt", "колонк", "динамик", "усилител", "акустик")):
        services.update(PRODUCT_SERVICE_LINKS["obt"])
    if any(k in combined for k in ("lunatek", "инвертор", "стабилизатор")):
        services.update(PRODUCT_SERVICE_LINKS["lunatek"])
    if any(k in combined for k in ("sunark", "аккум", "батаре", "dg12")):
        services.update(PRODUCT_SERVICE_LINKS["sunark"])
    if any(k in combined for k in ("dahua", "dhi", "контроллер доступа", "face")):
        services.update(PRODUCT_SERVICE_LINKS["dahua"])
    if any(k in combined for k in ("sprut", "замок", "кнопка", "bracket")):
        services.update(PRODUCT_SERVICE_LINKS["sprut"])
    if any(k in combined for k in ("temco", "датчик", "wts", "dts", "psn")):
        services.update(PRODUCT_SERVICE_LINKS["temco"])
    if any(k in combined for k in ("шкаф", "щит")):
        services.update(PRODUCT_SERVICE_LINKS["cabinet"])
    if any(k in combined for k in ("w5500", "ethernet")):
        services.update(PRODUCT_SERVICE_LINKS["w5500"])
    if not services:
        services.update(["low-voltage-systems", "electrical-cabinets", "system-integration"])
    return list(services)[:3]

'''

new_full_code = orig_code[:start_pos] + new_services_data_code + product_links_code + tail_code

# Update schema_service to include knowsAbout
old_schema_service_target = '"areaServed": {"@type": "Country", "name": "Kazakhstan"}\n            }'
new_schema_service_replacement = '''"areaServed": {"@type": "Country", "name": "Kazakhstan"},
                "knowsAbout": [
                    {"@type": "DefinedTerm", "name": k["name"], "sameAs": k["sameAs"]}
                    for k in service_root.get("knowsAbout", [])
                ]
            }'''
if old_schema_service_target in new_full_code:
    new_full_code = new_full_code.replace(old_schema_service_target, new_schema_service_replacement, 1)
    print("Injected knowsAbout into schema_service")

# Update schema_organization on homepage to include full knowsAbout
old_schema_org_target = '"latitude": 43.233071,\n            "longitude": 76.852412\n        }\n    }'
new_schema_org_replacement = '''"latitude": 43.233071,
            "longitude": 76.852412
        },
        "knowsAbout": [
            {"@type": "DefinedTerm", "name": "Motor Control Center", "sameAs": "https://www.wikidata.org/wiki/Q175185"},
            {"@type": "DefinedTerm", "name": "Direct digital control", "sameAs": "https://www.wikidata.org/wiki/Q5271878"},
            {"@type": "DefinedTerm", "name": "Industrial control system", "sameAs": "https://www.wikidata.org/wiki/Q211050"},
            {"@type": "DefinedTerm", "name": "Building management system", "sameAs": "https://www.wikidata.org/wiki/Q629239"},
            {"@type": "DefinedTerm", "name": "KNX standard", "sameAs": "https://www.wikidata.org/wiki/Q1889"},
            {"@type": "DefinedTerm", "name": "Electric switchboard", "sameAs": "https://www.wikidata.org/wiki/Q1141753"},
            {"@type": "DefinedTerm", "name": "Extra-low voltage", "sameAs": "https://www.wikidata.org/wiki/Q1255858"},
            {"@type": "DefinedTerm", "name": "Structured cabling", "sameAs": "https://www.wikidata.org/wiki/Q1363294"}
        ]
    }'''
if old_schema_org_target in new_full_code:
    new_full_code = new_full_code.replace(old_schema_org_target, new_schema_org_replacement, 1)
    print("Injected knowsAbout into schema_organization")

# Add problems_html to service detail rendering
old_sec_titles_target = 'sec_titles = {\n                "ru": ("Возможности и преимущества", "Этапы реализации", "Часто задаваемые вопросы (FAQ)", "Заказать расчет в WhatsApp"),\n                "kz": ("Мүмкіндіктер мен артықшылықтар", "Іске асыру кезеңдері", "Жиі қойылатын сұрақтар (FAQ)", "WhatsApp арқылы есептеуге тапсырыс беру"),\n                "en": ("Key Capabilities & Specifications", "Implementation Stages", "Frequently Asked Questions (FAQ)", "Request an Estimate on WhatsApp")\n            }.get(lang, ("Возможности", "Этапы", "FAQ", "WhatsApp"))'

new_sec_titles_replacement = '''problems_html = ""
            for p in service_data.get("problems", []):
                problems_html += f"""
                <div style="background-color: #1C2028; border-left: 4px solid #F59E0B; border-radius: 8px; padding: 16px; margin-bottom: 16px;">
                    <h4 style="margin: 0 0 8px 0; color: #F59E0B; font-size: 16px;">⚠️ Задача / Проблема на объекте:</h4>
                    <p style="margin: 4px 0; color: #E8E9ED; font-size: 14px;">{html.escape(p['problem'])}</p>
                    <p style="margin: 6px 0 4px 0; color: #60A5FA; font-size: 14px;"><strong>🛠️ Решение INPAR:</strong> {html.escape(p['solution'])}</p>
                    <p style="margin: 4px 0; color: #10B981; font-size: 14px;"><strong>✅ Результат:</strong> {html.escape(p['benefit'])}</p>
                </div>
                """

            rel_services_html = "".join([
                f'<a href="{BASE_URL}{prefix}/services/{rel_s}" style="display: inline-block; margin: 4px 6px 4px 0; padding: 6px 12px; background: #252932; border: 1px solid #333842; border-radius: 6px; color: #60A5FA; text-decoration: none; font-size: 13px;">{html.escape(SERVICES_DATA[rel_s]["badge"].get(lang, SERVICES_DATA[rel_s]["badge"]["ru"]))}</a>'
                for rel_s in service_root.get("related_services", []) if rel_s in SERVICES_DATA
            ])

            sec_titles = {
                "ru": ("Решаемые задачи и симптомы на объекте", "Возможности и преимущества", "Этапы реализации", "Часто задаваемые вопросы (FAQ)", "Заказать расчет в WhatsApp", "Связанные инженерные направления"),
                "kz": ("Шешілетін міндеттер мен жағдайлар", "Мүмкіндіктер мен артықшылықтар", "Іске асыру кезеңдері", "Жиі қойылатын сұрақтар (FAQ)", "WhatsApp арқылы есептеуге тапсырыс беру", "Байланысты инженерлік бағыттар"),
                "en": ("Client Challenges & Engineering Solutions", "Key Capabilities & Specifications", "Implementation Stages", "Frequently Asked Questions (FAQ)", "Request an Estimate on WhatsApp", "Related Engineering Fields")
            }.get(lang, ("Задачи", "Возможности", "Этапы", "FAQ", "WhatsApp", "Связанные"))'''

if old_sec_titles_target in new_full_code:
    new_full_code = new_full_code.replace(old_sec_titles_target, new_sec_titles_replacement, 1)
    print("Injected problem rendering code")

# Add problems_html and related services to body_content of service detail
old_body_target = '<h1>{html.escape(service_data[\'title\'])}</h1>\n            <p style="font-size: 18px; color: #D1D5DB;">{html.escape(service_data[\'description\'])}</p>\n            <p><a href="https://wa.me/77019954217?text={html.escape(\'Интересует \' + service_data[\'title\'])}" class="btn">{sec_titles[3]}</a></p>\n\n            <h2>{sec_titles[0]}</h2>'

new_body_replacement = '''<h1>{html.escape(service_data['title'])}</h1>
            <p style="font-size: 18px; color: #D1D5DB;">{html.escape(service_data['description'])}</p>
            <p><a href="https://wa.me/77019954217?text={html.escape('Интересует ' + service_data['title'])}" class="btn">{sec_titles[4]}</a></p>

            {f\'\'\'<h2>{sec_titles[0]}</h2>
            {problems_html}\'\'\' if problems_html else \'\'}

            <h2>{sec_titles[1]}</h2>'''

if old_body_target in new_full_code:
    new_full_code = new_full_code.replace(old_body_target, new_body_replacement, 1)
    print("Injected problems block into service body_content")

# Verify syntax
ast.parse(new_full_code)
print("AST validation passed! Writing to backend/api/seo_views.py...")

with open(seo_views_path, 'w', encoding='utf-8') as f:
    f.write(new_full_code)

print("Saved successfully!")
