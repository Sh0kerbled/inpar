<script setup>
import { computed, watch, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import Navbar from "../components/Navbar.vue";
import AppFooter from "../components/AppFooter.vue";
import { updateSEO } from "../utils/seo";
import {
  Building2,
  ShieldAlert,
  Cctv,
  Home,
  Speaker,
  Network,
  Combine,
  CheckCircle2,
  ArrowRight,
  MessageCircle,
  Phone,
  ChevronDown,
  Layers,
  Wrench,
  Sparkles
} from "lucide-vue-next";

const route = useRoute();
const router = useRouter();
const { t, locale } = useI18n();

const WHATSAPP_PHONE = "77019954217";

const servicesMap = {
  "bms-dispatching": {
    slug: "bms-dispatching",
    icon: Building2,
    color: "#B8A276",
    badge: "BMS & Dispatching",
    titleRu: "Диспетчеризация BMS и автоматизация зданий",
    titleKz: "BMS диспетчерлеу және ғимараттарды автоматтандыру",
    titleEn: "BMS Dispatching & Building Automation",
    descRu: "Комплексное управление инженерными системами зданий в Алматы и по всему Казахстану. Интеграция вентиляции (ОВиК), отопления, кондиционирования, освещения и энергоучета в единую платформу с удобным веб-интерфейсом для снижения энергопотребления до 30%.",
    descKz: "Қазақстан бойынша ғимараттардың инженерлік жүйелерін кешенді басқару. Энергия тұтынуды 30%-ға дейін азайту үшін желдету, жылыту, кондиционерлеу және жарықты бірыңғай веб-интерфейсі бар платформаға біріктіру.",
    descEn: "Comprehensive building management systems in Kazakhstan. Integrating HVAC, lighting, energy metering into a unified web dashboard to reduce operating costs and energy consumption by up to 30%.",
    featuresRu: [
      "Единая цифровая панель мониторинга всех инженерных узлов объекта в режиме 24/7",
      "Снижение затрат на электроэнергию и отопление на 15–30% благодаря умным расписаниям",
      "Мгновенное оповещение службы эксплуатации об авариях и утечках в Telegram / SMS",
      "Поддержка открытых протоколов автоматизации: BACnet, Modbus, KNX, LonWorks",
      "Архивация параметров и построение наглядных графиков энергоэффективности"
    ],
    stagesRu: [
      { step: "01", title: "Технический аудит объекта", desc: "Анализируем проектные чертежи, схемы вентиляции, теплопунктов и электроснабжения." },
      { step: "02", title: "Проектирование и подбор оборудования", desc: "Разрабатываем функциональные схемы автоматизации, спецификацию контроллеров и датчиков." },
      { step: "03", title: "Сборка шкафов автоматики (ЩА)", desc: "Собираем сертифицированные щиты управления на собственной сборочной базе с маркировкой." },
      { step: "04", title: "Монтаж и пусконаладочные работы", desc: "Прокладываем линии связи, устанавливаем датчики, приводы и программируем контроллеры." },
      { step: "05", title: "Ввод в эксплуатацию и обучение", desc: "Обучаем персонал службы эксплуатации заказчика и берем объект на гарантийное ТО." }
    ],
    faqsRu: [
      { q: "Для каких объектов целесообразно внедрение BMS?", a: "Для бизнес-центров, торговых комплексов (ТРЦ), отелей, медицинских клиник, логистических центров и элитных жилых комплексов площадью от 1 000 м²." },
      { q: "Какой срок окупаемости системы диспетчеризации?", a: "В среднем окупаемость составляет от 1.5 до 3 лет за счет прямой экономии энергоресурсов и продления срока службы оборудования." },
      { q: "С какими брендами контроллеров вы работаете?", a: "Мы используем надежное сертифицированное оборудование Siemens, Schneider Electric, Honeywell, Carel, Johnson Controls и Beckhoff." }
    ]
  },

  "fire-safety": {
    slug: "fire-safety",
    icon: ShieldAlert,
    color: "#D00000",
    badge: "Fire Protection",
    titleRu: "Пожарная безопасность и системы оповещения (АПС и СОУЭ)",
    titleKz: "Өрт қауіпсіздігі және хабарландыру жүйелері",
    titleEn: "Fire Safety & Emergency Notification (PA/VA)",
    descRu: "Проектирование, поставка и сертифицированный монтаж адресной пожарной сигнализации (АПС), систем оповещения и управления эвакуацией (СОУЭ) 1-5 типов под ключ по нормам Республики Казахстан.",
    descKz: "Қазақстан Республикасының нормаларына сәйкес адрестік өрт дабылын (АПС), 1-5 үлгідегі хабарландыру және эвакуацияны басқару жүйелерін (СОУЭ) жобалау, жеткізу және кілтке дейін орнату.",
    descEn: "Turnkey design, supply, and installation of addressable fire alarm and public address/evacuation systems in full compliance with the regulatory standards of Kazakhstan.",
    featuresRu: [
      "Адресные пожарные панели с точным указанием помещения и типа датчика",
      "Системы речевого и звукового оповещения (СОУЭ 1-5 типов) с трансляцией зонных сообщений",
      "Автоматическая интеграция с СКУД (разблокировка дверей), лифтами и клапанами ОЗК",
      "Проектирование и сдача объекта пожарной инспекции РК без замечаний",
      "Огнестойкие кабельные линии и сертифицированные резервированные блоки питания"
    ],
    stagesRu: [
      { step: "01", title: "Обследование и ТЗ", desc: "Определяем категорию пожарной опасности помещений и требуемый тип СОУЭ." },
      { step: "02", title: "Разработка проекта", desc: "Создаем разделы АПС, СОУЭ, планы расстановки извещателей и расчет акустики оповещения." },
      { step: "03", title: "Поставка и прокладка линий", desc: "Используем сертифицированные огнестойкие кабели типа FRLS / FRHF." },
      { step: "04", title: "Пусконаладка приборов", desc: "Программируем адресные извещатели, сценарии при тревоге и пульты управления." },
      { step: "05", title: "Комплексные испытания и сдача", desc: "Проводим реальное тестирование звукового давления и сдаем систему заказчику." }
    ],
    faqsRu: [
      { q: "Имеет ли ваша компания лицензию на монтаж пожарной безопасности?", a: "Да, монтажные работы выполняются квалифицированными специалистами в строгом соответствии с действующим законодательством и лицензиями РК." },
      { q: "Предоставляете ли вы периодическое техническое обслуживание?", a: "Да, мы заключаем официальные договоры на ежемесячное регламентное ТО противопожарных систем." }
    ]
  },

  "cctv-access-control": {
    slug: "cctv-access-control",
    icon: Cctv,
    color: "#A8ADB5",
    badge: "Surveillance & Access",
    titleRu: "Видеонаблюдение и контроль доступа (СКУД, NVR, Биометрия)",
    titleKz: "Бейнебақылау және қолжетімділікті басқару (СКУД)",
    titleEn: "CCTV Video Surveillance & Access Control",
    descRu: "Современные системы безопасности: IP-видеонаблюдение высокой четкости с искусственным интеллектом, биометрический контроль доступа (Face ID, отпечатки), турникеты, шлагбаумы и учет рабочего времени.",
    descKz: "Заманауи қауіпсіздік жүйелері: жасанды интеллектісі бар IP-бейнебақылау, биометриялық рұқсат бақылауы (Face ID), турникеттер және жұмыс уақытын есепке алу.",
    descEn: "Enterprise IP video surveillance with AI analytics, Face ID biometrics, turnstiles, barriers, and automated time-attendance tracking.",
    featuresRu: [
      "IP-камеры с видеоаналитикой: распознавание лиц, автомобильных номеров, контроль периметра",
      "Биометрические терминалы доступа Face ID и считыватели мобильного доступа (NFC/BLE)",
      "Интеграция с системой 1С:Предприятие для автоматического табеля учета рабочего времени",
      "Удаленный защищенный просмотр онлайн-потоков и архива со смартфона и ПК",
      "Надежные серверы видеозаписи с защитой данных RAID и резервным питанием"
    ],
    stagesRu: [
      { step: "01", title: "Аудит объекта и слепых зон", desc: "Рассчитываем фокусные расстояния объективов и углы обзора камер." },
      { step: "02", title: "Подбор оборудования", desc: "Выбираем оптимальные решения Hikvision, Dahua, Uniview, Suprema под бюджет." },
      { step: "03", title: "Монтаж камер и турникетов", desc: "Прокладываем экранированные трассы, устанавливаем замки, доводчики и видеокамеры." },
      { step: "04", title: "Настройка серверов и прав", desc: "Конфигурируем пользователей, уровни доступа для сотрудников и сетевую безопасность." },
      { step: "05", title: "Обучение службы охраны", desc: "Демонстрируем работу с архивом, экспорт видеофрагментов и правила эксплуатации." }
    ],
    faqsRu: [
      { q: "Сколько времени хранится видеозапись?", a: "Мы рассчитываем объем дисковых накопителей под требуемую глубину архива: от 14 до 90+ дней постоянной записи." },
      { q: "Работает ли распознавание лиц в темноте?", a: "Да, современные камеры и биометрические терминалы оснащены инфракрасной и тепловизионной подсветкой." }
    ]
  },

  "smart-home-knx": {
    slug: "smart-home-knx",
    icon: Home,
    color: "#3B82F6",
    badge: "Smart Home KNX",
    titleRu: "Умный дом стандарта KNX/EIB под ключ",
    titleKz: "KNX/EIB стандартындағы Смарт үй кілтке дейін",
    titleEn: "Smart Home KNX/EIB Certified Automation",
    descRu: "Проектирование и внедрение премиальных систем домашней автоматизации по всемирному стандарту KNX. Полный контроль освещения, диммирования, штор, микроклимата (HVAC), мультирум и безопасности с элегантных выключателей и смартфона.",
    descKz: "Халықаралық KNX стандарты бойынша үй автоматикасын жобалау және енгізу. Жарықтандыруды, перделерді, климатты және қауіпсіздікті смартфоннан және дизайнерлік панельдерден толық басқару.",
    descEn: "Premium residential automation engineered on the global KNX standard. Effortless control of lighting scenarios, motorized shades, HVAC climate, and multi-room audio.",
    featuresRu: [
      "Децентрализованный европейский стандарт KNX — гарантия надежности на десятилетия вперед",
      "Управление климатом: согласованная работа кондиционеров, отопления и теплого пола без конфликтов",
      "Сценарии освещения («Кинотеатр», «Вечер», «Ушел из дома») и плавное диммирование DALI",
      "Интеграция с Apple HomeKit, Яндекс Алиса, Google Home и планшетами",
      "Эксклюзивные выключатели и сенсорные термостаты из натурального стекла, латуни и алюминия"
    ],
    stagesRu: [
      { step: "01", title: "Разработка сценариев жизни", desc: "Учитываем привычки и пожелания владельцев для каждого помещения." },
      { step: "02", title: "Инженерный проект KNX", desc: "Создаем кабельный журнал, схемы коммутации щита и перечень исполнительных модулей." },
      { step: "03", title: "Черновой монтаж кабеля", desc: "Прокладываем специализированный экранированный зеленый кабель KNX bus." },
      { step: "04", title: "Сборка щита и чистовой монтаж", desc: "Устанавливаем реле, диммеры, актуаторы климата и дизайнерские клавиши." },
      { step: "05", title: "Программирование ETS и отладка", desc: "Программируем логику, настраиваем графику на планшетах и передаем ключи заказчику." }
    ],
    faqsRu: [
      { q: "Почему именно KNX, а не беспроводные системы?", a: "KNX — это проводной промышленный стандарт, поддерживаемый более 500 мировыми производителями. Он не зависит от серверов, Wi-Fi и работает безотказно 20+ лет." },
      { q: "Когда нужно начинать проектирование умного дома?", a: "На этапе разработки дизайн-проекта, до начала штукатурных и электромонтажных работ." }
    ]
  },

  "sound-and-light": {
    slug: "sound-and-light",
    icon: Speaker,
    color: "#B8A276",
    badge: "Pro Audio & Lighting",
    titleRu: "Профессиональный звук и сценический свет",
    titleKz: "Кәсіби дыбыс және сахналық жарық",
    titleEn: "Professional Sound & Stage Lighting",
    descRu: "Акустическое проектирование и оснащение конференц-залов, концертных площадок, ресторанов, культовых сооружений и ТРЦ. Линейные массивы, фоновое озвучивание, микрофонные системы и динамический сценический свет.",
    descKz: "Конференц-залдар, концерт алаңдары, мейрамханалар мен сауда орталықтарын кәсіби дыбыстық және жарық жабдықтарымен жабдықтау. Акустикалық есептеу, сызықтық массивтер және сахналық жарық.",
    descEn: "Acoustic design and installation for conference halls, concert venues, hospitality, and retail spaces. Line arrays, DSP processing, microphone arrays, and intelligent lighting.",
    featuresRu: [
      "Компьютерное электроакустическое моделирование для исключения эха и идеальной разборчивости речи",
      "High-End акустические системы, линейные массивы и сабвуферы мирового класса",
      "Конференц-связь, радиосистемы и синхронный перевод для залов заседаний",
      "Управление сценическим светом по DMX-протоколу: подвижные головы, споты, заливной свет",
      "Светодиодные LED-экраны высокого разрешения с бесшовной передачей изображения"
    ],
    stagesRu: [
      { step: "01", title: "Акустический замер помещения", desc: "Анализируем время реверберации и форму зала для выбора конфигурации акустики." },
      { step: "02", title: "Расчет и подбор оборудования", desc: "Подбираем мощности усилителей, диаграммы направленности и сценические фермы." },
      { step: "03", title: "Монтаж подвесов и коммутации", desc: "Прокладываем бескислородные акустические кабели и монтируем подвесные системы." },
      { step: "04", title: "Калибровка звукового процессора (DSP)", desc: "Настраиваем эквализацию, задержки и фазировку при помощи измерительных микрофонов." },
      { step: "05", title: "Финальная сдача и обучение операторов", desc: "Настраиваем готовые пресеты («Конференция», «Концерт», «Диско») для удобного запуска одной кнопкой." }
    ],
    faqsRu: [
      { q: "Поставляете ли вы оборудование для фонового звука в рестораны и магазины?", a: "Да, мы устанавливаем распределенные трансляционные 100V системы фонового звука с зонным управлением громкостью." },
      { q: "Входят ли в проект микрофоны и конференц-системы?", a: "Да, мы комплектуем объекты проводными и беспроводными микрофонными пультами с функцией автонаведения поворотных камер." }
    ]
  },

  "networks-smatv": {
    slug: "networks-smatv",
    icon: Network,
    color: "#A8ADB5",
    badge: "Networks & SMATV",
    titleRu: "Информационные сети, СКС и SMATV (IPTV, Спутниковое ТВ)",
    titleKz: "Ақпараттық желілер, СКС және SMATV",
    titleEn: "Data Networks, Structured Cabling & SMATV",
    descRu: "Проектирование и построение структурированных кабельных систем (СКС), оптоволоконных линий связи (ВОЛС), бесшовного корпоративного Wi-Fi и гостиничных систем интерактивного спутникового телевидения.",
    descKz: "Құрылымдалған кәбілдік желілерді (СКС), талшықты-оптикалық байланыс желілерін, корпоративтік үздіксіз Wi-Fi және қонақүй спутниктік интерактивті теледидар жүйелерін жобалау және құру.",
    descEn: "Structured cabling (SCS), fiber optic infrastructure, enterprise-grade seamless Wi-Fi, and interactive SMATV/IPTV systems for hospitality and commercial buildings.",
    featuresRu: [
      "Сертифицированные кабельные системы категорий 5e, 6, 6A, 7 с системной гарантией",
      "Оптоволоконные магистрали (ВОЛС) и профессиональная сварка оптических волокон",
      "Корпоративный Wi-Fi с бесшовным роумингом и гостевой авторизацией по СМС",
      "IP-телефония (IP-АТС) с интеграцией корпоративной почты и CRM-систем",
      "Гостиничное телевидение SMATV / IPTV с брендированным приветственным экраном"
    ],
    stagesRu: [
      { step: "01", title: "Аудит сетевых потребностей", desc: "Определяем число рабочих мест, требуемую пропускную способность и плотность клиентов." },
      { step: "02", title: "Проект СКС и серверных", desc: "Разрабатываем компоновку 19-дюймовых шкафов, кабельных лотков и схемы кроссировки." },
      { step: "03", title: "Монтаж кабельной инфраструктуры", desc: "Укладываем витую пару и оптику с соблюдением радиусов изгиба и стандартов TIA/EIA." },
      { step: "04", title: "Сертификационное тестирование Fluke", desc: "Каждый порт тестируется кабельным анализатором с предоставлением отчета." },
      { step: "05", title: "Настройка активного оборудования", desc: "Настраиваем коммутаторы, маршрутизаторы, VLAN, межсетевые экраны и Wi-Fi контроллеры." }
    ],
    faqsRu: [
      { q: "Предоставляете ли вы протоколы тестирования линий?", a: "Да, на каждую смонтированную линию СКС предоставляется официальный паспорт теста Fluke Networks." }
    ]
  },

  "system-integration": {
    slug: "system-integration",
    icon: Combine,
    color: "#3B82F6",
    badge: "Full Integration",
    titleRu: "Системная интеграция слаботочных систем под ключ",
    titleKz: "Төменгі ток жүйелерінің кешенді интеграциясы",
    titleEn: "End-to-End Systems Integration",
    descRu: "Генеральный подряд по слаботочным и инженерным системам объектов любого масштаба в Казахстане. Объединение BMS, пожарной сигнализации, СКУД, видеонаблюдения, звука и мультимедиа в единую слаженно функционирующую цифровую экосистему.",
    descKz: "Қазақстандағы кез келген ауқымдағы нысандардың төменгі ток және инженерлік жүйелері бойынша бас мердігерлік. BMS, өрт қауіпсіздігі, СКУД, бейнебақылау және мультимедианы бірыңғай цифрлық жүйеге біріктіру.",
    descEn: "Master technology contractor for low-voltage systems. Harmonizing BMS, fire safety, access control, CCTV, and audio-visual into a cohesive, reliable infrastructure.",
    featuresRu: [
      "Единый подрядчик и единая ответственность за все инженерные слаботочные сети здания",
      "Бесшовная аппаратная и программная стыковка оборудования разных мировых производителей",
      "Слаженная работа при чрезвычайных ситуациях (пожар, авария, обесточивание объекта)",
      "Оптимизация сметы до 20% благодаря исключению дублирующих трасс и коммуникаций",
      "Штат сертифицированных инженеров с опытом реализации объектов в Казахстане и СНГ"
    ],
    stagesRu: [
      { step: "01", title: "Комплексный аудит проекта", desc: "Изучаем архитектурные и смежные разделы для устранения пространственных и схемных коллизий." },
      { step: "02", title: "Единая архитектура интеграции", desc: "Создаем сводный проект системной интеграции и протоколов межсистемного взаимодействия." },
      { step: "03", title: "Прямые поставки оборудования", desc: "Осуществляем официальные прямые поставки от заводов-изготовителей без посредников." },
      { step: "04", title: "Монтаж и пусконаладка", desc: "Выполняем параллельный монтаж всех разделов силами собственных профильных бригад." },
      { step: "05", title: "Сдача надзорным органам и сервис", desc: "Готовим исполнительную документацию, сдаем объект госкомиссии и обеспечиваем сервис." }
    ],
    faqsRu: [
      { q: "В каких городах Казахстана вы работаете?", a: "Мы работаем по всему Казахстану: Алматы, Астана, Шымкент, Актобе, Караганда, Туркестан, а также в странах СНГ." }
    ]
  }
};

const currentSlug = computed(() => route.params.slug);
const currentService = computed(() => servicesMap[currentSlug.value] || null);

// Аккордеон FAQ
const openFaqIndex = ref(null);
const toggleFaq = (idx) => {
  openFaqIndex.value = openFaqIndex.value === idx ? null : idx;
};

// Другие услуги для внутренней перелинковки
const otherServices = computed(() => {
  return Object.values(servicesMap).filter((s) => s.slug !== currentSlug.value);
});

const applySeo = () => {
  const service = currentService.value;
  if (!service) {
    updateSEO({
      title: "Услуги компании — Проектирование и интеграция | INPAR.KZ",
      description: "Комплексные инженерные решения: BMS, Умный дом KNX, пожарная безопасность, звук и видеонаблюдение в Алматы.",
    });
    return;
  }

  const title = `${service.titleRu} в Алматы под ключ | INPAR.KZ`;
  const description = `${service.descRu.slice(0, 160)}... Сертифицированные инженеры, поставка оборудования и гарантия от компании INPAR.`;
  const keywords = `${service.badge}, ${service.titleRu}, слаботочные системы Алматы, монтаж Казахстан, INPAR`;
  const canonical = `https://inpar.kz/services/${service.slug}`;

  const jsonLd = [
    {
      "@context": "https://schema.org",
      "@type": "Service",
      "name": service.titleRu,
      "description": service.descRu,
      "provider": {
        "@type": "LocalBusiness",
        "name": "INPAR.KZ",
        "telephone": "+77019954217",
        "url": "https://inpar.kz",
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
    },
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Главная", "item": "https://inpar.kz/" },
        { "@type": "ListItem", "position": 2, "name": "Услуги", "item": "https://inpar.kz/#services" },
        { "@type": "ListItem", "position": 3, "name": service.titleRu, "item": canonical }
      ]
    },
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": (service.faqsRu || []).map((faq) => ({
        "@type": "Question",
        "name": faq.q,
        "acceptedAnswer": {
          "@type": "Answer",
          "text": faq.a
        }
      }))
    }
  ];

  updateSEO({
    title,
    description,
    keywords,
    url: canonical,
    jsonLd
  });
};

onMounted(() => {
  applySeo();
  window.scrollTo(0, 0);
});

watch(
  () => route.params.slug,
  () => {
    applySeo();
    openFaqIndex.value = null;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
);

const whatsappLink = computed(() => {
  const s = currentService.value;
  const name = s ? s.titleRu : "Инженерные услуги";
  const text = `Здравствуйте! Меня интересует услуга «${name}». Хочу получить расчет стоимости и консультацию инженера.`;
  return `https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(text)}`;
});
</script>

<template>
  <div class="min-h-screen bg-[#13151A] text-[#E8E9ED]">
    <Navbar />

    <main v-if="currentService" class="pt-32 pb-24">
      <!-- Хлебные крошки -->
      <nav class="max-w-7xl mx-auto px-6 lg:px-12 mb-8 text-xs text-[#9BA1AB] flex items-center gap-2">
        <router-link to="/" class="hover:text-[#3B82F6] transition-colors">Главная</router-link>
        <span>/</span>
        <router-link to="/#services" class="hover:text-[#3B82F6] transition-colors">Услуги</router-link>
        <span>/</span>
        <span class="text-[#E8E9ED]">{{ currentService.titleRu }}</span>
      </nav>

      <!-- Заглавный блок Hero услуги -->
      <section class="max-w-7xl mx-auto px-6 lg:px-12 mb-20">
        <div class="relative p-8 md:p-14 border border-[#333842] bg-gradient-to-br from-[#1A1D23] via-[#20242D] to-[#16181F] rounded-2xl overflow-hidden shadow-2xl">
          <div class="absolute -right-20 -top-20 w-80 h-80 rounded-full opacity-10 blur-3xl pointer-events-none" :style="{ backgroundColor: currentService.color }"></div>

          <div class="flex items-center gap-3 mb-6">
            <div class="h-px w-8 bg-[#B8A276]" />
            <span class="text-[#B8A276] text-xs uppercase tracking-[0.2em] font-medium">
              {{ currentService.badge }}
            </span>
          </div>

          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-8 mb-8">
            <div class="max-w-3xl">
              <h1 class="text-3xl md:text-5xl font-light tracking-tight text-[#FFFFFF] mb-6 leading-tight">
                {{ currentService.titleRu }}
              </h1>
              <p class="text-[#9BA1AB] text-base md:text-lg leading-relaxed font-light">
                {{ currentService.descRu }}
              </p>
            </div>

            <div class="flex flex-col gap-3 min-w-[240px]">
              <a
                :href="whatsappLink"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center justify-center gap-3 px-6 py-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-sm transition-all duration-300 shadow-lg shadow-emerald-950/40 hover:scale-[1.02]"
              >
                <MessageCircle class="w-5 h-5" />
                Рассчитать смету в WhatsApp
              </a>

              <a
                href="tel:+77019954217"
                class="inline-flex items-center justify-center gap-3 px-6 py-3.5 rounded-xl border border-[#333842] hover:border-[#3B82F6]/50 bg-[#1A1D23]/60 text-[#E8E9ED] text-sm font-light transition-all duration-300"
              >
                <Phone class="w-4 h-4 text-[#B8A276]" />
                +7 (701) 995-42-17
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- Ключевые преимущества / Возможности -->
      <section class="max-w-7xl mx-auto px-6 lg:px-12 mb-20">
        <div class="flex items-center gap-4 mb-4">
          <div class="h-px w-8 bg-[#3B82F6]" />
          <span class="text-[#3B82F6] text-xs uppercase tracking-[0.2em]">Возможности</span>
        </div>
        <h2 class="text-2xl md:text-3xl font-light tracking-tight text-white mb-8">
          Что входит в реализацию системы
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="(feature, idx) in currentService.featuresRu"
            :key="idx"
            class="p-6 border border-[#333842] bg-[#1A1D23]/60 rounded-xl hover:border-[#3B82F6]/40 transition-all duration-300 flex items-start gap-4"
          >
            <div class="p-2 rounded-lg bg-[#252932] border border-[#333842] text-[#B8A276] shrink-0 mt-0.5">
              <CheckCircle2 class="w-5 h-5" />
            </div>
            <p class="text-sm font-light text-[#D1D5DB] leading-relaxed">
              {{ feature }}
            </p>
          </div>
        </div>
      </section>

      <!-- Этапы выполнения работ -->
      <section class="max-w-7xl mx-auto px-6 lg:px-12 mb-20">
        <div class="flex items-center gap-4 mb-4">
          <div class="h-px w-8 bg-[#B8A276]" />
          <span class="text-[#B8A276] text-xs uppercase tracking-[0.2em]">Процесс</span>
        </div>
        <h2 class="text-2xl md:text-3xl font-light tracking-tight text-white mb-8">
          Этапы проектирования и внедрения
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
          <div
            v-for="(stage, idx) in currentService.stagesRu"
            :key="idx"
            class="p-6 border border-[#333842] bg-gradient-to-b from-[#1E222A]/80 to-[#16181F]/80 rounded-xl relative"
          >
            <span class="text-3xl font-bold text-[#B8A276]/30 mb-3 block font-mono">
              {{ stage.step }}
            </span>
            <h3 class="text-base font-normal text-white mb-2 leading-snug">
              {{ stage.title }}
            </h3>
            <p class="text-xs text-[#9BA1AB] font-light leading-relaxed">
              {{ stage.desc }}
            </p>
          </div>
        </div>
      </section>

      <!-- Часто задаваемые вопросы (FAQ) -->
      <section v-if="currentService.faqsRu && currentService.faqsRu.length" class="max-w-4xl mx-auto px-6 lg:px-12 mb-20">
        <div class="text-center mb-10">
          <span class="text-[#B8A276] text-xs uppercase tracking-[0.2em] block mb-2">FAQ</span>
          <h2 class="text-2xl md:text-3xl font-light tracking-tight text-white">
            Часто задаваемые вопросы
          </h2>
        </div>

        <div class="space-y-3">
          <div
            v-for="(faq, fIdx) in currentService.faqsRu"
            :key="fIdx"
            class="border border-[#333842] rounded-xl overflow-hidden bg-[#1A1D23]/50 transition-colors"
          >
            <button
              @click="toggleFaq(fIdx)"
              class="w-full p-5 text-left flex items-center justify-between gap-4 text-[#E8E9ED] hover:text-white font-medium text-sm md:text-base cursor-pointer"
            >
              <span>{{ faq.q }}</span>
              <ChevronDown
                class="w-5 h-5 text-[#9BA1AB] transition-transform duration-300 shrink-0"
                :class="{ 'rotate-180': openFaqIndex === fIdx }"
              />
            </button>
            <div
              v-show="openFaqIndex === fIdx"
              class="px-5 pb-5 pt-1 text-sm font-light text-[#9BA1AB] leading-relaxed border-t border-[#333842]/40"
            >
              {{ faq.a }}
            </div>
          </div>
        </div>
      </section>

      <!-- CTA Блок -->
      <section class="max-w-7xl mx-auto px-6 lg:px-12 mb-20">
        <div class="p-10 md:p-14 border border-[#333842] bg-gradient-to-r from-[#1A1D23] via-[#252932] to-[#1A1D23] rounded-2xl text-center">
          <h2 class="text-2xl md:text-4xl font-light text-white mb-4">
            Готовы обсудить ваш проект в Алматы или регионах РК?
          </h2>
          <p class="text-[#9BA1AB] max-w-2xl mx-auto mb-8 font-light text-sm md:text-base">
            Получите бесплатную консультацию ведущего инженера, предварительный аудит документации и расчет сметы.
          </p>
          <div class="flex flex-wrap items-center justify-center gap-4">
            <a
              :href="whatsappLink"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center gap-3 px-8 py-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-medium transition-all duration-300 shadow-lg shadow-emerald-950/40"
            >
              <MessageCircle class="w-5 h-5" />
              Написать в WhatsApp
            </a>
            <router-link
              to="/projects"
              class="inline-flex items-center gap-3 px-8 py-4 rounded-xl border border-[#333842] hover:border-[#3B82F6] bg-[#1A1D23] text-white font-light text-sm transition-all duration-300"
            >
              Смотреть реализованные проекты
              <ArrowRight class="w-4 h-4" />
            </router-link>
          </div>
        </div>
      </section>

      <!-- Другие услуги компании (Перелинковка) -->
      <section class="max-w-7xl mx-auto px-6 lg:px-12">
        <h2 class="text-xl font-light tracking-tight text-[#9BA1AB] mb-6 uppercase tracking-wider text-xs">
          Другие инженерные направления INPAR
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <router-link
            v-for="other in otherServices"
            :key="other.slug"
            :to="`/services/${other.slug}`"
            class="p-5 border border-[#333842] bg-[#1A1D23]/40 hover:bg-[#20242D] hover:border-[#3B82F6]/50 rounded-xl transition-all duration-300 flex items-center justify-between group"
          >
            <div>
              <span class="text-[11px] text-[#B8A276] uppercase tracking-wider block mb-1">
                {{ other.badge }}
              </span>
              <h3 class="text-sm font-normal text-[#E8E9ED] group-hover:text-white transition-colors">
                {{ other.titleRu }}
              </h3>
            </div>
            <ArrowRight class="w-4 h-4 text-[#9BA1AB] group-hover:text-[#3B82F6] group-hover:translate-x-1 transition-all" />
          </router-link>
        </div>
      </section>
    </main>

    <!-- Если услуга не найдена -->
    <div v-else class="max-w-4xl mx-auto px-6 py-40 text-center">
      <h1 class="text-3xl text-white mb-4">Услуга не найдена</h1>
      <p class="text-[#9BA1AB] mb-8">Возможно, страница была перемещена или адрес введен с ошибкой.</p>
      <router-link to="/#services" class="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[#3B82F6] text-white">
        Вернуться ко всем услугам
      </router-link>
    </div>

    <AppFooter />
  </div>
</template>
