/**
 * SEO helper for dynamic meta tags and JSON-LD schema injection in Vue 3 SPA
 */

const BASE_URL = "https://inpar.kz";

const DEFAULT_META = {
  title: "INPAR.KZ — Слаботочные системы, Индустриальная автоматизация, MCC, DDC и Умный дом в Алматы",
  description: "Компания INPAR.KZ с 2014 года выполняет проектирование, монтаж и интеграцию слаботочных систем, автоматизации зданий (BMS), индустриальной автоматизации, шкафов MCC/DDC и умных домов KNX в Казахстане.",
  keywords: "слаботочные системы Алматы, индустриальные автоматизации, шкафы MCC, контроллеры DDC, электрические шкафы Алматы, умный дом KNX Казахстан",
  image: "https://inpar.kz/assets/sticker-CGlHhmMq.png",
  url: "https://inpar.kz"
};

function ensureMetaTag(name, attr = "name") {
  let element = document.querySelector(`meta[${attr}="${name}"]`);
  if (!element) {
    element = document.createElement("meta");
    element.setAttribute(attr, name);
    document.head.appendChild(element);
  }
  return element;
}

function ensureLinkTag(rel, hreflang = null) {
  let selector = hreflang ? `link[rel="${rel}"][hreflang="${hreflang}"]` : `link[rel="${rel}"]`;
  let element = document.querySelector(selector);
  if (!element) {
    element = document.createElement("link");
    element.setAttribute("rel", rel);
    if (hreflang) element.setAttribute("hreflang", hreflang);
    document.head.appendChild(element);
  }
  return element;
}

export function updateSEO({
  title = DEFAULT_META.title,
  description = DEFAULT_META.description,
  keywords = DEFAULT_META.keywords,
  image = DEFAULT_META.image,
  url = window.location.href,
  type = "website",
  lang = "ru",
  path = "",
  jsonLd = null
} = {}) {
  // 1. Update Title and HTML lang attribute
  document.title = title;
  document.documentElement.lang = lang === "kz" ? "kk" : (lang === "en" ? "en" : "ru");

  // 2. Standard Meta Tags
  ensureMetaTag("description").setAttribute("content", description);
  ensureMetaTag("keywords").setAttribute("content", keywords);

  // 3. Open Graph Tags
  ensureMetaTag("og:title", "property").setAttribute("content", title);
  ensureMetaTag("og:description", "property").setAttribute("content", description);
  ensureMetaTag("og:image", "property").setAttribute("content", image);
  ensureMetaTag("og:url", "property").setAttribute("content", url);
  ensureMetaTag("og:type", "property").setAttribute("content", type);
  ensureMetaTag("og:site_name", "property").setAttribute("content", "INPAR.KZ");

  // 4. Twitter Tags
  ensureMetaTag("twitter:card").setAttribute("content", "summary_large_image");
  ensureMetaTag("twitter:title").setAttribute("content", title);
  ensureMetaTag("twitter:description").setAttribute("content", description);
  ensureMetaTag("twitter:image").setAttribute("content", image);

  // 5. Canonical Link
  ensureLinkTag("canonical").setAttribute("href", url);

  // 6. Hreflang Alternates (RU, KK, EN, x-default)
  let clean = path.replace(/^\/(kz|en)/, "").replace(/^\/+/, "");
  let ruUrl = clean ? `${BASE_URL}/${clean}` : `${BASE_URL}/`;
  let kzUrl = clean ? `${BASE_URL}/kz/${clean}` : `${BASE_URL}/kz`;
  let enUrl = clean ? `${BASE_URL}/en/${clean}` : `${BASE_URL}/en`;

  ensureLinkTag("alternate", "ru").setAttribute("href", ruUrl);
  ensureLinkTag("alternate", "kk").setAttribute("href", kzUrl);
  ensureLinkTag("alternate", "en").setAttribute("href", enUrl);
  ensureLinkTag("alternate", "x-default").setAttribute("href", ruUrl);

  // 7. JSON-LD Structured Data
  let script = document.getElementById("seo-schema-jsonld");
  if (!script) {
    script = document.createElement("script");
    script.id = "seo-schema-jsonld";
    script.type = "application/ld+json";
    document.head.appendChild(script);
  }

  if (jsonLd) {
    script.textContent = JSON.stringify(jsonLd);
  } else {
    // Default Organization
    script.textContent = JSON.stringify({
      "@context": "https://schema.org",
      "@type": "LocalBusiness",
      "name": "INPAR.KZ",
      "image": DEFAULT_META.image,
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
    });
  }
}
