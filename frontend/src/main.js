import { createApp } from "vue";
import { MotionPlugin } from "@vueuse/motion";
import { createI18n } from "vue-i18n";
import { createPinia } from "pinia";
import router from "./router.js";
import App from "./App.vue";
import "./assets/main.css";

const getRuntimeLocale = () => localStorage.getItem("user-locale") || "ru";

const messages = {
  en: {
    nav: {
      engineering: "Engineering",
      services: "Services",
      partners: "Partners",
      about: "About",
      contact: "Contact",
      catalog: "Catalog",
    },
    hero: {
      badge: "Engineering Excellence",
      title: "INPAR",
      description:
        "Precision-engineered infrastructure solutions for complex technical environments.",
      button: "Explore Projects",
    },
    services: {
      badge: "Core Services",
      title: "Capabilities",
      items: {
        infrastructure: {
          title: "Infrastructure",
          desc: "Advanced structural engineering and technical planning",
        },
        integration: {
          title: "Systems Integration",
          desc: "Complex multi-system coordination and optimization",
        },
        design: {
          title: "Precision Design",
          desc: "High-tolerance technical documentation and specification",
        },
        performance: {
          title: "Performance",
          desc: "Real-time monitoring and efficiency optimization",
        },
      },
      serviceItems: [
        {
          title: "BMS Dispatching",
          description:
            "Comprehensive building management. Integration of systems into a single platform with a unified web interface to reduce energy consumption.",
        },
        {
          title: "Fire Safety",
          description:
            "Intelligent addressable fire panels and emergency notification systems (PA) for facilities of any scale.",
        },
        {
          title: "Video Surveillance and Access Control",
          description:
            "NVR systems, IP biometrics and access control. Management of authorized access with integration into fire networks.",
        },
        {
          title: "Smart Home (KNX/EIB)",
          description:
            "Design and integration of home automation. Full control of lighting, climate and multimedia.",
        },
        {
          title: "Professional Sound and Light",
          description:
            "High-End acoustics, line arrays, moving lights and LED screens for concerts, conference halls and commercial spaces.",
        },
        {
          title: "Information Networks and SMATV",
          description:
            "Network infrastructure design, IP telephony and satellite television systems with channel access control.",
        },
        {
          title: "Systems Integration",
          description:
            "Seamless integration of equipment from various manufacturers. Configuration, program simulation and technical support.",
        },
      ],
    },
    about: {
      badge: "Intelligent Partner",
      title: "Intelligent Automation",
      description1:
        "Founded in 2014 in Almaty, INPAR.KZ specializes in the implementation of low-current systems, building automation (BMS) and Smart Home technologies to the KNX/EIB standard.",
      description2:
        "We handle the full cycle: from acoustic and system design to programming and post-warranty maintenance. Our goal is to create energy-efficient, safe and easily managed spaces with a single interface.",
      stats: {
        projects: "Projects implemented",
        countries: "Countries",
        staff: "Technical staff",
        uptime: "Uptime Guarantee",
      },
    },
    partners: {
      badge: "Trusted By",
      title: "Intelligent Partners",
    },
    contact: {
      badge: "Get In Touch",
      title: "Contact",
      office: "Head Office",
      details: "Contact Details",
      phone: "Phone",
      email: "Email",
      hours: "Business Hours",
      weekdays: "Mon - Fri",
      address:
        "Saryarka Residential Complex, 1st Microdistrict, 68/4, Almaty, Kazakhstan",
    },
    footer: {
      description: "Precision infrastructure solutions.",
    },
    catalog: {
      badge: "Catalog",
      title: "Products",
      description: "Premium smart home and systems integration solutions",
      search: "Search",
      searchPlaceholder: "Enter product name or keywords...",
      category: "Category",
      allCategories: "All categories",
      sorting: "Sorting",
      sortDefault: "Default",
      sortPriceAsc: "Price (↑)",
      sortPriceDesc: "Price (↓)",
      sortName: "By name",
      sortNew: "New first",
      loading: "Loading products...",
      notFound: "Products not found",
      inStock: "✓ In stock:",
      outOfStock: "Out of stock",
      premiumQuality: "Premium quality",
      resetFilters: "Reset filters",
      contactWhatsapp: "Contact via WhatsApp",
      whatsappMessage:
        'Hello! I\'m interested in this product:\n"{name}"\nPrice: ₸{price}\n{url}',
      backToCatalog: "Back to catalog",
      characteristics: "Specifications",
    },
    projects: {
      badge: "Our Portfolio",
      title: "Completed Projects",
      countLabel: "completed projects",
      empty: "No projects found",
      filters: {
        all: "All Projects",
        hotel: "Hotels",
        mall: "Shopping Malls",
        office: "Offices & Business",
        residential: "Residential",
        public: "Public Buildings",
      },
      systems: {
        fire: "Fire Alarm",
        access: "Access Control",
        cctv: "CCTV",
        lighting: "Lighting Automation",
        audio: "Audio System",
        network: "Network System",
        smart: "Smart Home KNX",
        parking: "Auto Parking",
        wifi: "Wi-Fi Network",
        tv: "IP Television",
        hvac: "HVAC Automation",
        conference: "Conference System",
        phone: "PBX Phone",
        security: "Security System",
      },
      cities: {
        almaty: "Almaty",
        astana: "Astana",
        ekaterinburg: "Ekaterinburg",
        tripoli: "Tripoli, Libya",
        shymkent: "Shymkent",
        turkestan: "Turkestan",
        aktobe: "Aktobe",
        qyzylorda: "Qyzylorda",
        boroboe: "Boroboe",
      },
    },
  },

  ru: {
    nav: {
      engineering: "Engineering",
      services: "Услуги",
      partners: "Партнеры",
      about: "О компании",
      contact: "Контакты",
      catalog: "Каталог",
    },
    hero: {
      badge: "Инженерное совершенство",
      title: "INPAR",
      description:
        "Прецизионные инженерные инфраструктурные решения для сложных технических сред.",
      button: "Изучить проекты",
    },
    services: {
      badge: "Основные услуги",
      title: "Возможности",
      items: {
        infrastructure: {
          title: "Инфраструктура",
          desc: "Передовое структурное проектирование и техническое планирование",
        },
        integration: {
          title: "Системная интеграция",
          desc: "Сложная координация и оптимизация мультисистем",
        },
        design: {
          title: "Прецизионный дизайн",
          desc: "Высокоточная техническая документация и спецификации",
        },
        performance: {
          title: "Производительность",
          desc: "Мониторинг в реальном времени и оптимизация эффективности",
        },
      },
      serviceItems: [
        {
          title: "Диспетчеризация BMS",
          description:
            "Комплексное управление зданием. Интеграция систем в единую платформу с унифицированным веб-интерфейсом для снижения потребления энергии.",
        },
        {
          title: "Пожарная безопасность",
          description:
            "Интеллектуальные адресные пожарные панели и системы экстренного оповещения (PA) для объектов любого масштаба.",
        },
        {
          title: "Видеонаблюдение и контроль доступа",
          description:
            "Системы NVR, IP-биометрия и контроль доступа. Управление авторизованным доступом с интеграцией в пожарные сети.",
        },
        {
          title: "Умный дом (KNX/EIB)",
          description:
            "Проектирование и интеграция домашней автоматизации. Полное управление освещением, климатом и мультимедиа.",
        },
        {
          title: "Профессиональный звук и свет",
          description:
            "High-End акустика, линейные массивы, движущийся свет и LED-экраны для концертов, конференц-залов и коммерческих пространств.",
        },
        {
          title: "Информационные сети и SMATV",
          description:
            "Проектирование сетевой инфраструктуры, IP-телефония и системы спутникового телевидения с управлением доступом к каналам.",
        },
        {
          title: "Системная интеграция",
          description:
            "Бесшовная интеграция оборудования различных производителей. Настройка, программное моделирование и техническая поддержка.",
        },
      ],
    },
    about: {
      badge: "Intelligent Partner",
      title: "Интеллектуальная автоматизация",
      description1:
        "Основанная в 2014 году в Алматы, компания INPAR.KZ специализируется на внедрении слаботочных систем, автоматизации зданий (BMS) и технологий «Умный дом» стандарта KNX/EIB.",
      description2:
        "Мы берем на себя полный цикл: от акустического и системного проектирования до программирования и постгарантийного обслуживания. Наша цель — создание энергоэффективных, безопасных и легко управляемых пространств с единым интерфейсом.",
      stats: {
        projects: "Реализовано проектов",
        countries: "Стран",
        staff: "Технический персонал",
        uptime: "Гарантия аптайма",
      },
    },
    partners: {
      badge: "Нам доверяют",
      title: "Интеллектуальные партнеры",
    },
    contact: {
      badge: "Связаться с нами",
      title: "Контакты",
      office: "Главный офис",
      details: "Контактные данные",
      phone: "Телефон",
      email: "Email",
      hours: "Рабочие часы",
      weekdays: "Пн - Пт",
      address: "ЖК «Сарыарка», 1-й микрорайон, 68/4, Алматы, Казахстан",
    },
    footer: {
      description: "Прецизионные инфраструктурные решения.",
    },
    catalog: {
      badge: "Каталог",
      title: "Продукты",
      description: "Премиум решения для умного дома и системной интеграции",
      search: "Поиск",
      searchPlaceholder: "Введите название или ключевые слова...",
      category: "Категория",
      allCategories: "Все категории",
      sorting: "Сортировка",
      sortDefault: "По умолчанию",
      sortPriceAsc: "Цена (↑)",
      sortPriceDesc: "Цена (↓)",
      sortName: "По названию",
      sortNew: "Новые первыми",
      loading: "Загрузка товаров...",
      notFound: "Товары не найдены",
      inStock: "✓ В наличии:",
      outOfStock: "Нет в наличии",
      premiumQuality: "Премиум качество",
      resetFilters: "Сбросить фильтры",
      contactWhatsapp: "Связаться в WhatsApp",
      whatsappMessage:
        "Здравствуйте! Меня интересует товар:\n«{name}»\nЦена: ₸{price}\n{url}",
      backToCatalog: "Вернуться в каталог",
      characteristics: "Характеристики",
    },
    projects: {
      badge: "Наши объекты",
      title: "Реализованные проекты",
      countLabel: "завершённых объектов",
      empty: "Проекты не найдены",
      filters: {
        all: "Все проекты",
        hotel: "Отели",
        mall: "Торговые центры",
        office: "Офисы и бизнес",
        residential: "Жилые объекты",
        public: "Общественные здания",
      },
      systems: {
        fire: "Пожарная сигнализация",
        access: "Контроль доступа",
        cctv: "Видеонаблюдение",
        lighting: "Автоматизация освещения",
        audio: "Аудиосистема",
        network: "Сетевая система",
        smart: "Умный дом KNX",
        parking: "Автопарковка",
        wifi: "Wi-Fi сеть",
        tv: "IP-телевидение",
        hvac: "Автоматизация HVAC",
        conference: "Конференц-система",
        phone: "Телефонная АТС",
        security: "Система безопасности",
      },
      cities: {
        almaty: "Алматы",
        astana: "Астана",
        ekaterinburg: "Екатеринбург",
        tripoli: "Триполи, Ливия",
        shymkent: "Шымкент",
        turkestan: "Туркестан",
        aktobe: "Актобе",
        qyzylorda: "Қызылорда",
        boroboe: "Бурабай",
      },
    },
  },

  kz: {
    nav: {
      engineering: "Engineering",
      services: "Қызметтер",
      partners: "Серіктестер",
      about: "Біз туралы",
      contact: "Байланыс",
      catalog: "Каталог",
    },
    hero: {
      badge: "Инженерлік кемелдік",
      title: "INPAR",
      description:
        "Күрделі техникалық орталарға арналған жоғары дәлдіктегі инженерлік инфрақұрылымдық шешімдер.",
      button: "Жобаларды қарау",
    },
    services: {
      badge: "Негізгі қызметтер",
      title: "Мүмкіндіктер",
      items: {
        infrastructure: {
          title: "Инфрақұрылым",
          desc: "Жоғары деңгейдегі құрылымдық инженерия және техникалық жоспарлау",
        },
        integration: {
          title: "Жүйелік интеграция",
          desc: "Күрделі мультижүйелік үйлестіру және оңтайландыру",
        },
        design: {
          title: "Прецизионды дизайн",
          desc: "Жоғары дәлдіктегі техникалық құжаттама мен спецификациялар",
        },
        performance: {
          title: "Өнімділік",
          desc: "Нақты уақыттағы мониторинг және тиімділікті оңтайландыру",
        },
      },
      serviceItems: [
        {
          title: "BMS Диспетчерлеу",
          description:
            "Ғимаратты кешенді басқару. Жүйелерді энергия тұтынуды азайту үшін бірыңғай веб-интерфейсі бар бір платформаға интеграциялау.",
        },
        {
          title: "Өрт қауіпсіздігі",
          description:
            "Кез келген ауқымдағы объектілерге арналған интеллектуалды адрестік өрт панельдері және төтенше хабарлама жүйелері (PA).",
        },
        {
          title: "Бейнебақылау және қолжетімділікті бақылау",
          description:
            "NVR жүйелері, IP биометриясы және қолжетімділікті бақылау. Өрт желілеріне интеграциямен рұқсат етілген қолжетімділікті басқару.",
        },
        {
          title: "Смарт үй (KNX/EIB)",
          description:
            "Үй автоматикасын жобалау және интеграциялау. Жарықтандыруды, климатты және мультимедианы толық басқару.",
        },
        {
          title: "Кәсіби дыбыс және жарық",
          description:
            "High-End акустика, сызықтық массивтер, жылжымалы жарық және LED экрандары концерттерге, конференц-залдар мен коммерциялық кеңістіктерге.",
        },
        {
          title: "Ақпараттық желілер және SMATV",
          description:
            "Желілік инфрақұрылымды жобалау, IP телефония және арналарға қолжетімділікті басқаруы бар жерсерін теледидар жүйелері.",
        },
        {
          title: "Жүйелік интеграция",
          description:
            "Әртүрлі өндірушілердің жабдықтарын үздіксіз интеграциялау. Баптау, бағдарламалық модельдеу және техникалық қолдау.",
        },
      ],
    },
    about: {
      badge: "Intelligent Partner",
      title: "Интеллектуалды автоматтандыру",
      description1:
        "2014 жылы Алматыда құрылған INPAR.KZ компаниясы төменгі ток жүйелерін енгізу, ғимараттарды автоматтандыру (BMS) және KNX/EIB стандартындағы «Смарт үй» технологияларына маманданған.",
      description2:
        "Біз толық циклды өз мойнымызға аламыз: акустикалық және жүйелік жобалаудан бастап бағдарламалау мен кепілдіктен кейінгі қызмет көрсетуге дейін. Біздің мақсатымыз — бірыңғай интерфейспен энергия үнемдейтін, қауіпсіз және оңай басқарылатын кеңістіктер жасау.",
      stats: {
        projects: "Жүзеге асырылған жобалар",
        countries: "Елдер",
        staff: "Техникалық персонал",
        uptime: "Uptime кепілдігі",
      },
    },
    partners: {
      badge: "Бізге сенеді",
      title: "Интеллектуалды серіктестер",
    },
    contact: {
      badge: "Бізбен байланысыңыз",
      title: "Контактілер",
      office: "Бас кеңсе",
      details: "Байланыс мәліметтері",
      phone: "Телефон",
      email: "Email",
      hours: "Жұмыс уақыты",
      weekdays: "Дс - Жм",
      address: "«Сарыарқа» ТҮК, 1-ші ықшамаудан, 68/4, Алматы, Қазақстан",
    },
    footer: {
      description: "Жоғары дәлдіктегі инфрақұрылымдық шешімдер.",
    },
    catalog: {
      badge: "Каталог",
      title: "Өнімдер",
      description: "Ақылды үй және жүйелер интеграциясының премиум шешімдері",
      search: "Іздеу",
      searchPlaceholder: "Өнім атын немесе кілт сөздерді енгізіңіз...",
      category: "Санат",
      allCategories: "Барлық санаттар",
      sorting: "Сұрыптау",
      sortDefault: "Әдепкі",
      sortPriceAsc: "Баға (↑)",
      sortPriceDesc: "Баға (↓)",
      sortName: "Аты бойынша",
      sortNew: "Жаңалары алдымен",
      loading: "Өнімдер жүктелуде...",
      notFound: "Өнімдер табылмады",
      inStock: "✓ Қоймада бар:",
      outOfStock: "Қоймада жоқ",
      premiumQuality: "Премиум сапа",
      resetFilters: "Сүзгілерді тазарту",
      contactWhatsapp: "WhatsApp арқылы хабарласу",
      whatsappMessage:
        "Сәлеметсіз бе! Мені мына тауар қызықтырды:\n«{name}»\nБағасы: ₸{price}\n{url}",
      backToCatalog: "Каталогқа оралу",
      characteristics: "Сипаттамалары",
    },
    projects: {
      badge: "Біздің объектілер",
      title: "Жүзеге асырылған жобалар",
      countLabel: "аяқталған объект",
      empty: "Жобалар табылмады",
      filters: {
        all: "Барлық жобалар",
        hotel: "Қонақүйлер",
        mall: "Сауда орталықтары",
        office: "Кеңселер және бизнес",
        residential: "Тұрғын үй объектілері",
        public: "Қоғамдық ғимараттар",
      },
      systems: {
        fire: "Өрт сигнализациясы",
        access: "Қолжетімділік бақылауы",
        cctv: "Бейнебақылау",
        lighting: "Жарықтандыруды автоматтандыру",
        audio: "Аудиожүйе",
        network: "Желілік жүйе",
        smart: "Смарт үй KNX",
        parking: "Автотұрақ",
        wifi: "Wi-Fi желісі",
        tv: "IP-теледидар",
        hvac: "HVAC автоматтандыру",
        conference: "Конференц-жүйе",
        phone: "Телефон АТС",
        security: "Қауіпсіздік жүйесі",
      },
      cities: {
        almaty: "Алматы",
        astana: "Астана",
        ekaterinburg: "Екатеринбург",
        tripoli: "Триполі, Ливия",
        shymkent: "Шымкент",
        turkestan: "Түркістан",
        aktobe: "Ақтөбе",
        qyzylorda: "Қызылорда",
        boroboe: "Бурабай",
      },
    },
  },
};

const i18n = createI18n({
  legacy: false,
  locale: getRuntimeLocale(),
  fallbackLocale: "en",
  messages,
});

const pinia = createPinia();
const app = createApp(App);

import { useAuthStore } from "./stores/index.js";
app.use(pinia);
const authStore = useAuthStore();
authStore.init();

app.use(MotionPlugin);
app.use(i18n);
app.use(router);
app.mount("#app");

window.i18n = i18n;
