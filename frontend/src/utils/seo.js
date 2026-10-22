/**
 * SEO helper for dynamic meta tags and JSON-LD schema injection in Vue 3 SPA
 */

const DEFAULT_META = {
  title: "INPAR.KZ — Системная интеграция, Умный дом KNX и BMS в Алматы",
  description: "Компания INPAR.KZ с 2014 года выполняет проектирование, монтаж и интеграцию слаботочных систем, автоматизации зданий (BMS), пожарной безопасности и умных домов KNX в Казахстане.",
  keywords: "умный дом Алматы, KNX Казахстан, BMS диспетчеризация, пожарная сигнализация, видеонаблюдение, СКУД, профессиональный звук, слаботочные системы",
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

export function updateSEO({
  title = DEFAULT_META.title,
  description = DEFAULT_META.description,
  keywords = DEFAULT_META.keywords,
  image = DEFAULT_META.image,
  url = window.location.href,
  type = "website",
  jsonLd = null
} = {}) {
  // 1. Update Title
  document.title = title;

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
  let canonical = document.querySelector('link[rel="canonical"]');
  if (!canonical) {
    canonical = document.createElement("link");
    canonical.setAttribute("rel", "canonical");
    document.head.appendChild(canonical);
  }
  canonical.setAttribute("href", url);

  // 6. JSON-LD Structured Data
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
      }
    });
  }
}
