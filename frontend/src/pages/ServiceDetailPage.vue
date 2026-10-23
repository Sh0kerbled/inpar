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
  Cpu,
  Box,
  Factory
} from "lucide-vue-next";

const route = useRoute();
const router = useRouter();
const { t, locale } = useI18n();

const WHATSAPP_PHONE = "77019954217";

// 12 направлений инжиниринга
const servicesMap = {
  "mcc-cabinets": {
    slug: "mcc-cabinets",
    icon: Layers,
    color: "#3B82F6",
    badgeRu: "MCC & Приводы",
    badgeKz: "MCC және жетектер",
    badgeEn: "MCC & Motor Control",
    titleRu: "Шкафы управления двигателями MCC (Motor Control Center) и ЧРП",
    titleKz: "MCC (Motor Control Center) қозғалтқыштарды басқару шкафтары мен жиілік түрлендіргіштер",
    titleEn: "Motor Control Center (MCC) Panels & VFD Automation Cabinets",
    descRu: "Проектирование и сборка шкафов MCC (Motor Control Center), щитов управления электродвигателями, насосными станциями, вентиляторами и конвейерами с частотными преобразователями (ЧРП) и устройствами плавного пуска (УПП) в Алматы и по всему Казахстану.",
    descKz: "Қазақстанда жиілік түрлендіргіштері (ЖТ) мен жұмсақ іске қосқыштары бар MCC (Motor Control Center) шкафтарын, электр қозғалтқыштарын, сорғы станцияларын, желдеткіштерді басқару қалқандарын жобалау және құрастыру.",
    descEn: "Engineering, custom manufacturing, and commissioning of Motor Control Center (MCC) panels, Variable Frequency Drives (VFD), and soft starter cabinets for pumps, ventilation, and industrial machinery across Kazakhstan.",
    featuresRu: [
      "Сборка силовых шкафов MCC по международным стандартам IEC 61439 и ГОСТ",
      "Интеграция частотных преобразователей (Danfoss, Schneider Electric, ABB, INVT) и УПП",
      "Комплексная защита двигателей от перегрузок, перекоса фаз, сухого хода насосов",
      "Промышленные интерфейсы связи Modbus, Profinet, Ethernet для интеграции в SCADA и BMS",
      "Корпуса со степенью защиты IP31, IP54, IP65 для тяжелых промышленных условий"
    ],
    featuresKz: [
      "IEC 61439 халықаралық стандарттары бойынша MCC күштік шкафтарын жеке жобалау",
      "Danfoss, Schneider Electric, ABB жиілік түрлендіргіштерін біріктіру",
      "Электр қозғалтқыштарын шамадан тыс жүктемеден және фазалардың қисаюынан толық қорғау",
      "SCADA және BMS жүйелеріне қосылу үшін Modbus, Profinet, Ethernet интерфейстері",
      "IP31, IP54, IP65 қорғаныс дәрежесі бар сенімді металл корпустар"
    ],
    featuresEn: [
      "Custom-engineered MCC switchboards compliant with IEC 61439 standards",
      "Integration of leading VFD brands (Danfoss, Schneider Electric, ABB, Siemens)",
      "Advanced motor thermal protection, phase loss prevention, and automatic transfer switches (ATS)",
      "Industrial protocols: Modbus RTU/TCP, Profinet, BACnet for SCADA and BMS integration",
      "Enclosures up to IP65 for harsh industrial, outdoor, and utility environments"
    ],
    stagesRu: [
      { step: "01", title: "Расчет нагрузок", desc: "Рассчитываем пусковые и номинальные токи, подбираем сечения шин и защитные аппараты." },
      { step: "02", title: "Проектирование схемы", desc: "Разрабатываем однолинейные и принципиальные схемы, подбираем ЧРП и контакторы." },
      { step: "03", title: "Сборка в цехе", desc: "Собираем щиты на собственной сборочной базе с лазерной маркировкой цепей." },
      { step: "04", title: "Заводские тесты", desc: "Проверяем изоляцию мегаомметром, тестируем логику защит и блокировок." },
      { step: "05", title: "Пусконаладка на объекте", desc: "Параметрируем частотные приводы под реальные нагрузки двигателей на объекте." }
    ],
    faqsRu: [
      { q: "Для чего применяются шкафы MCC?", a: "Для централизованного силового электроснабжения и автоматического управления группами электродвигателей на насосных станциях, водоканалах, заводах и в системах вентиляции." },
      { q: "Сколько длится сборка шкафа управления?", a: "Сборка занимает от 7 до 20 рабочих дней в зависимости от мощности и комплектации." }
    ]
  },

  "ddc-automation": {
    slug: "ddc-automation",
    icon: Cpu,
    color: "#B8A276",
    badgeRu: "DDC & ОВиК",
    badgeKz: "DDC және Желдету",
    badgeEn: "DDC Automation",
    titleRu: "Шкафы и контроллеры прямого цифрового управления DDC (Direct Digital Control)",
    titleKz: "DDC (Direct Digital Control) тікелей цифрлық басқару шкафтары мен контроллерлері",
    titleEn: "Direct Digital Control (DDC) Panels & HVAC Automation",
    descRu: "Проектирование, сборка шкафов DDC и программирование свободно программируемых контроллеров прямого цифрового управления для приточно-вытяжных установок (ПВУ), тепловых пунктов (ИТП), чиллеров, фанкойлов и кондиционирования в Алматы.",
    descKz: "Алматыда желдету қондырғылары, жылу пункттері (ЖТП), чиллерлер мен ауа баптау жүйелері үшін DDC тікелей цифрлық басқару шкафтарын жобалау, құрастыру және контроллерлерді бағдарламалау.",
    descEn: "Design, panel assembly, and programming of Direct Digital Control (DDC) field controllers for air handling units (AHU), heating substations, chillers, and precision climate systems across Kazakhstan.",
    featuresRu: [
      "Свободно программируемые DDC-контроллеры с поддержкой BACnet IP/MSTP и Modbus",
      "Прецизионное поддержание температуры, влажности, CO2 и перепада давления",
      "Плавное ПИД-управление водяными клапанами, приводами воздушных заслонок и рекуперацией",
      "Автоматическая защита от замерзания калориферов и сигнализация засорения фильтров",
      "Встроенный веб-сервер контроллеров для настройки с браузера без платного ПО"
    ],
    featuresKz: [
      "BACnet және Modbus хаттамаларын қолдайтын бағдарламаланатын DDC контроллерлері",
      "Температура, ылғалдылық және CO2 деңгейін жоғары дәлдікпен реттеу",
      "Жылытқыштарды қатып қалудан автоматты түрде кешенді қорғау",
      "Смартфоннан немесе ДК-ден тікелей басқаруға арналған кірістірілген веб-интерфейс"
    ],
    featuresEn: [
      "Freely programmable DDC controllers natively supporting BACnet IP/MS-TP and Modbus",
      "Precision PID control of temperature, relative humidity, air quality (CO2), and static pressure",
      "Frost protection routines for heating coils and smart filter differential pressure alerts",
      "Integrated web-server interfaces for direct commissioning without proprietary software"
    ],
    stagesRu: [
      { step: "01", title: "Изучение ТЗ и схем ОВиК", desc: "Анализируем типы теплообменников, вентиляторов и требования к микроклимату." },
      { step: "02", title: "Проект шкафа DDC", desc: "Разрабатываем схемы внешних подключений датчиков температуры, давления и приводов." },
      { step: "03", title: "Сборка щита DDC", desc: "Устанавливаем контроллеры, реле, блоки питания и защитные автоматы." },
      { step: "04", title: "Программирование логики", desc: "Создаем прикладную программу регулирования с защитными алгоритмами." },
      { step: "05", title: "Калибровка на объекте", desc: "Настраиваем коэффициенты ПИД-регуляторов под тепловую инерцию здания." }
    ],
    faqsRu: [
      { q: "Что дает внедрение DDC в вентиляции?", a: "Точное соблюдение температурного графика, отсутствие сквозняков, защиту калориферов от разморозки зимой и экономию до 30% тепла." }
    ]
  },

  "electrical-cabinets": {
    slug: "electrical-cabinets",
    icon: Box,
    color: "#EAB308",
    badgeRu: "Электрощитовое производство",
    badgeKz: "Электр қалқандары",
    badgeEn: "Electrical Switchgear",
    titleRu: "Сборка электрических шкафов, щитов автоматики (ЩА, ЩУ, ВРУ, ГРЩ)",
    titleKz: "Электр шкафтары мен автоматтандыру қалқандарын (ЩА, ЩУ, ВРУ, ГРЩ) құрастыру",
    titleEn: "Custom Electrical Enclosures, Control Panels & Switchgear Assembly",
    descRu: "Собственное сертифицированное электрощитовое производство в Алматы: сборка шкафов автоматики (ЩА), щитов управления (ЩУ), главных распределительных щитов (ГРЩ), вводно-распределительных устройств (ВРУ) и щитов освещения (ЩО) любой сложности по индивидуальным схемам.",
    descKz: "Алматыдағы жеке сертификатталған электрощит өндірісі: автоматтандыру шкафтары (ЩА), басқару қалқандары (ЩУ), бас тарату қалқандары (ГРЩ), кіріс-тарату құрылғылары (ВРУ) кез келген күрделіліктегі сызбалар бойынша.",
    descEn: "Professional electrical panel manufacturing in Almaty: assembly of custom automation panels (PLC cabinets), main distribution boards (MDB), low-voltage switchgear (LVSG), and motor control enclosures according to IEC and GOST standards.",
    featuresRu: [
      "Собственный сборочный цех в Алматы с контролем качества ОТК",
      "Сборка на комплектующих Schneider Electric, ABB, Chint, IEK под ваш бюджет",
      "Полный пакет исполнительной документации: паспорта, схемы, сертификаты соответствия",
      "Лазерная термоусадочная маркировка проводов и клеммных групп",
      "Эргономичная компоновка и удобство подключения кабелей монтажниками"
    ],
    featuresKz: [
      "Алматы қаласындағы жеке өндірістік цех және сапа бақылауы",
      "Тапсырыс берушінің бюджетіне сай Schneider Electric, ABB, Chint жабдықтарымен жинау",
      "Толық құжаттама топтамасы: төлқұжаттар, электр сызбалары, сәйкестік сертификаттары",
      "Сымдар мен клеммаларды лазерлік таңбалау"
    ],
    featuresEn: [
      "In-house certified panel building workshop in Almaty with multi-stage QC",
      "Components from Schneider Electric, ABB, Siemens, Chint tailored to client budget",
      "Complete documentation package: single-line diagrams, factory test certificates",
      "Clear laser-printed heat-shrink wire labeling and ferruled connections"
    ],
    stagesRu: [
      { step: "01", title: "Согласование схем", desc: "Проверяем электрические схемы заказчика и оптимизируем спецификацию." },
      { step: "02", title: "3D-моделирование", desc: "Планируем размещение оборудования с учетом тепловыделения и воздушных зазоров." },
      { step: "03", title: "Слесарные и шинные работы", desc: "Выполняем ошиновку медью, монтаж DIN-реек и защитных аппаратов." },
      { step: "04", title: "Монтажная обвязка", desc: "Прокладываем жгуты проводов в кабельных коробах с маркировкой." },
      { step: "05", title: "Контроль ОТК", desc: "Проводим проверку изоляции, прозвонку всех цепей и оформляем паспорт." }
    ],
    faqsRu: [
      { q: "Собираете ли вы шкафы по индивидуальным схемам?", a: "Да, более 80% проектов выполняются по индивидуальным схемам и требованиям заказчика." }
    ]
  },

  "industrial-automation": {
    slug: "industrial-automation",
    icon: Factory,
    color: "#EF4444",
    badgeRu: "АСУ ТП & Индустрия",
    badgeKz: "Өндіріс автоматтандыру",
    badgeEn: "Industrial Automation",
    titleRu: "Индустриальная автоматизация и АСУ ТП в Казахстане",
    titleKz: "Өндірістік автоматтандыру және ТП ББЖ (АСУ ТП) Қазақстанда",
    titleEn: "Industrial Automation, PLC Programming & SCADA Systems",
    descRu: "Комплексная автоматизация технологических процессов (АСУ ТП), производственных линий, конвейеров, насосных и компрессорных станций. Программирование промышленных контроллеров (ПЛК / PLC), разработка диспетчерских SCADA-систем и HMI-панелей оператора.",
    descKz: "Технологиялық процестерді, өндірістік желілерді, конвейерлер мен сорғы станцияларын кешенді автоматтандыру (АСУ ТП). Өндірістік контроллерлерді (ПЛК) бағдарламалау, диспетчерлік SCADA жүйелері мен оператор панельдерін әзірлеу.",
    descEn: "End-to-end industrial automation and process control (I&C / SCADA): programmable logic controller (PLC) programming, human-machine interface (HMI) design, conveyor and pumping automation for manufacturing plants in Kazakhstan.",
    featuresRu: [
      "Программирование ПЛК: Siemens S7-1200/1500, Schneider Electric, Omron, Delta",
      "Разработка интуитивно понятных SCADA-систем и сенсорных панелей оператора HMI",
      "Снижение человеческого фактора, процента брака и простоев оборудования",
      "Интеграция датчиков КИПиА (давление, расход, уровень, температура)",
      "Построение надежных промышленных сетей Profinet, Industrial Ethernet"
    ],
    featuresKz: [
      "Siemens, Schneider Electric, Omron өндірістік контроллерлерін бағдарламалау",
      "Ыңғайлы SCADA жүйелері мен сенсорлық операторлық панельдерді (HMI) әзірлеу",
      "Өндірістік ақауларды және жабдықтың бос тұруын азайту",
      "КИПиА датчиктерін (қысым, температура, шығын) кешенді біріктіру"
    ],
    featuresEn: [
      "PLC programming for Siemens Simatic S7, Schneider Modicon, Omron, Allen-Bradley",
      "Development of modern SCADA supervisory systems and operator touch panels (HMI)",
      "Full integration of industrial instrumentation (flowmeters, pressure transmitters)",
      "Fail-safe industrial networking over Profinet, Modbus TCP, EtherNet/IP"
    ],
    stagesRu: [
      { step: "01", title: "Технологический аудит", desc: "Изучаем технологический регламент производства и выявляем узкие места." },
      { step: "02", title: "Проект АСУ ТП", desc: "Разрабатываем архитектуру системы, спецификацию датчиков и алгоритмы." },
      { step: "03", title: "Сборка шкафов управления", desc: "Собираем щиты управления ПЛК с гальванической развязкой сигналов." },
      { step: "04", title: "Программирование ПЛК и SCADA", desc: "Создаем логику управления процессами и экраны мнемосхем для операторов." },
      { step: "05", title: "Пусконаладка под нагрузкой", desc: "Тестируем линии в реальном технологическом цикле и обучаем персонал." }
    ],
    faqsRu: [
      { q: "Для каких отраслей промышленности вы работаете?", a: "Пищевая промышленность, стройматериалы, насосные станции водоканалов, склады и логистика, металлообработка." }
    ]
  },

  "low-voltage-systems": {
    slug: "low-voltage-systems",
    icon: Network,
    color: "#06B6D4",
    badgeRu: "Слаботочка под ключ",
    badgeKz: "Төменгі ток желілері",
    badgeEn: "Low-Voltage ELV",
    titleRu: "Проектирование и монтаж слаботочных систем под ключ",
    titleKz: "Төменгі ток жүйелерін жобалау және монтаждау кілтке дейін",
    titleEn: "Turnkey Extra Low Voltage (ELV) Systems Engineering & Installation",
    descRu: "Полный комплекс работ по слаботочным системам для коммерческих, общественных и жилых зданий: проектирование стадий П и Р, поставка сертифицированного оборудования, монтаж кабельных трасс, пусконаладка и сдача надзорным органам.",
    descKz: "Коммерциялық, қоғамдық және тұрғын үй ғимараттарына арналған төменгі ток (әлсіз ток) жүйелерінің толық кешені: жобалау, жабдық жеткізу, монтаж, баптау және мемлекеттік комиссияға тапсыру.",
    descEn: "Full lifecycle engineering and contracting of Extra Low Voltage (ELV) systems for commercial towers, hotels, malls, and residential complexes: structured cabling, CCTV, access control, fire alarm, and public address.",
    featuresRu: [
      "Все слаботочные разделы из одних рук: СКС, СКУД, видеонаблюдение, АПС, СОУЭ, звук",
      "Исключение межведомственных конфликтов монтажников и дублирующих трасс",
      "Строгое соответствие строительным нормам Республики Казахстан (СНиП РК)",
      "Использование огнестойкого кабеля пониженной токсичности (HF / LS)",
      "Исполнительная документация со схемами и протоколами измерений"
    ],
    featuresKz: [
      "Бір қолдан барлық бөлімдер: СКС, СКУД, бейнебақылау, өрт дабылы, дыбыс, ТВ",
      "Қазақстанның құрылыс нормалары мен ережелеріне (ҚР ҚНжЕ) толық сәйкестік",
      "Өртке қауіпсіз жоғары сапалы сертификатталған кабельдерді қолдану",
      "Кешенді кепілдік және техникалық қызмет көрсету"
    ],
    featuresEn: [
      "All ELV packages from a single source: SCS, CCTV, ACS, Fire Alarm, PA/VA, IPTV",
      "Zero inter-subcontractor finger-pointing and optimized shared cable pathways",
      "Full compliance with Kazakhstan building codes and international IEEE/TIA standards",
      "Comprehensive as-built drawings, testing reports, and warranty support"
    ],
    stagesRu: [
      { step: "01", title: "Изучение проекта", desc: "Анализируем архитектурные чертежи здания и технические условия." },
      { step: "02", title: "Рабочий проект", desc: "Разрабатываем планы трасс, схемы стояков и кабельные журналы." },
      { step: "03", title: "Монтаж трасс", desc: "Прокладываем перфорированные лотки, гофротрубы и кабели." },
      { step: "04", title: "Оконечные устройства", desc: "Монтируем розетки, датчики, камеры, пожарные извещатели." },
      { step: "05", title: "Комплексные тесты", desc: "Проверяем взаимодействие всех подсистем и сдаем госкомиссии." }
    ],
    faqsRu: [
      { q: "В чем выгода единого подрядчика по слаботочке?", a: "Один подрядчик отвечает за весь комплекс, исключает перекрестные ошибки и экономит до 20% бюджета." }
    ]
  },

  "smart-home-knx": {
    slug: "smart-home-knx",
    icon: Home,
    color: "#3B82F6",
    badgeRu: "Smart Home KNX",
    badgeKz: "KNX Ақылды үй",
    badgeEn: "KNX Smart Home",
    titleRu: "Умный дом стандарта KNX/EIB под ключ в Казахстане",
    titleKz: "KNX/EIB стандартындағы Ақылды үй (Smart Home) кілтке дейін",
    titleEn: "KNX/EIB Certified Smart Home Automation in Kazakhstan",
    descRu: "Проектирование и внедрение премиальных систем домашней автоматизации по всемирному стандарту KNX. Полный контроль освещения, диммирования, штор, микроклимата (HVAC), мультирум и безопасности с элегантных выключателей и смартфона.",
    descKz: "Халықаралық KNX стандарты бойынша пәтерлер мен коттедждерге арналған премиум «Ақылды үй» жүйелерін жобалау және енгізу. Жарықтандыруды, перделерді, климатты және қауіпсіздікті смартфоннан және дизайнерлік панельдерден басқару.",
    descEn: "Bespoke smart residence automation built on the world-renowned KNX/EIB standard in Almaty and Astana. Seamless control of lighting, DALI dimming, motorized shading, HVAC climate, and multiroom audio via bespoke keypads and mobile apps.",
    featuresRu: [
      "Децентрализованный европейский стандарт KNX — надежность на десятилетия вперед",
      "Управление климатом: согласованная работа кондиционеров, отопления и теплого пола",
      "Сценарии освещения («Кинотеатр», «Вечер», «Ушел из дома») и диммирование DALI",
      "Интеграция с Apple HomeKit, Яндекс Алиса, Google Home и планшетами",
      "Эксклюзивные выключатели из стекла, латуни, алюминия и кожи"
    ],
    featuresKz: [
      "Халықаралық KNX стандарты — серверлерге тәуелсіз жоғары сенімділік",
      "Жылыту, еден жылыту және кондиционерлеу жүйелерінің келісілген жұмысы",
      "Apple HomeKit, Алиса және смартфондар арқылы оңай басқару",
      "Эксклюзивті дизайнерлік пернетақталар мен сенсорлық экрандар"
    ],
    featuresEn: [
      "Decentralized global KNX standard backed by 500+ premium European manufacturers",
      "Coordinated HVAC control: underfloor heating, AC, and fresh air ventilation",
      "Native voice and mobile integration: Apple HomeKit, Google Home, touchscreens",
      "Luxury architectural switches crafted in solid brass, glass, aluminum, and leather"
    ],
    stagesRu: [
      { step: "01", title: "Сценарии жизни", desc: "Учитываем привычки семьи для каждого помещения." },
      { step: "02", title: "Проект KNX", desc: "Создаем кабельный журнал и схему щита автоматики." },
      { step: "03", title: "Черновой монтаж", desc: "Прокладываем кабель KNX bus на этапе черновой отделки." },
      { step: "04", title: "Сборка щита", desc: "Устанавливаем актуаторы, диммеры и чистовые выключатели." },
      { step: "05", title: "ETS программирование", desc: "Программируем сценарии и настраиваем интерфейс на смартфонах." }
    ],
    faqsRu: [
      { q: "Почему именно KNX, а не беспроводные системы?", a: "KNX — промышленный проводной протокол, который работает стабильно 25+ лет без батареек, сбоев Wi-Fi и облачных серверов." }
    ]
  },

  "bms-dispatching": {
    slug: "bms-dispatching",
    icon: Building2,
    color: "#B8A276",
    badgeRu: "BMS Диспетчеризация",
    badgeKz: "BMS Диспетчерлеу",
    badgeEn: "BMS Automation",
    titleRu: "Диспетчеризация BMS и автоматизация зданий в Алматы",
    titleKz: "BMS диспетчерлеу және ғимараттарды автоматтандыру",
    titleEn: "Building Management Systems (BMS) & Dispatching",
    descRu: "Комплексное управление инженерными системами зданий в Казахстане. Интеграция вентиляции, отопления, кондиционирования, освещения и энергоучета в единую платформу с веб-интерфейсом для снижения энергопотребления до 30%.",
    descKz: "Қазақстан бойынша ғимараттардың инженерлік жүйелерін кешенді басқару. Энергия тұтынуды 30%-ға дейін азайту үшін желдету, жылыту, кондиционерлеу және жарықты бірыңғай веб-интерфейсі бар платформаға біріктіру.",
    descEn: "Integrated building automation and energy management systems (BMS) in Kazakhstan. Centralized supervision of HVAC, electrical distribution, lighting, and metering to trim operating costs by up to 30%.",
    featuresRu: [
      "Единая цифровая панель мониторинга всех узлов объекта 24/7",
      "Снижение затрат на электроэнергию и отопление на 15–30%",
      "Оперативное оповещение об авариях в Telegram / SMS / Email",
      "Интеграция протоколов BACnet, Modbus, KNX, LonWorks"
    ],
    featuresKz: [
      "24/7 режимінде барлық инженерлік түйіндерді бақылаудың бірыңғай цифрлық панелі",
      "Ақылды кестелер арқылы электр және жылу шығындарын 15–30%-ға үнемдеу",
      "Апаттық жағдайлар туралы Telegram / SMS арқылы жедел хабарлау"
    ],
    featuresEn: [
      "24/7 centralized monitoring dashboard for all mechanical and electrical infrastructure",
      "15–30% measurable energy savings using occupancy schedules and enthalpy economizers",
      "Instant emergency alarming to mobile devices and facility maintenance teams"
    ],
    stagesRu: [
      { step: "01", title: "Аудит объекта", desc: "Анализируем инженерные сети объекта." },
      { step: "02", title: "Проект BMS", desc: "Разрабатываем схемы автоматики и диспетчеризации." },
      { step: "03", title: "Сборка щитов", desc: "Собираем щиты управления и поставляем контроллеры." },
      { step: "04", title: "Пусконаладка", desc: "Программируем SCADA/BMS интерфейс." },
      { step: "05", title: "Обучение службы", desc: "Обучаем персонал заказчика эксплуатации системы." }
    ],
    faqsRu: [
      { q: "Каков срок окупаемости BMS?", a: "В среднем окупаемость составляет 1.5–3 года за счет экономии энергоресурсов." }
    ]
  },

  "fire-safety": {
    slug: "fire-safety",
    icon: ShieldAlert,
    color: "#D00000",
    badgeRu: "Пожарная безопасность",
    badgeKz: "Өрт қауіпсіздігі",
    badgeEn: "Fire Protection",
    titleRu: "Пожарная безопасность и системы оповещения (АПС и СОУЭ)",
    titleKz: "Өрт қауіпсіздігі және хабарландыру жүйелері",
    titleEn: "Fire Safety & Emergency Notification (PA/VA)",
    descRu: "Проектирование, поставка и сертифицированный монтаж адресной пожарной сигнализации (АПС), систем оповещения и управления эвакуацией (СОУЭ) 1-5 типов под ключ по нормам Республики Казахстан.",
    descKz: "Қазақстан Республикасының нормаларына сәйкес адрестік өрт дабылын (АПС), 1-5 үлгідегі хабарландыру және эвакуацияны басқару жүйелерін (СОУЭ) жобалау, жеткізу және кілтке дейін орнату.",
    descEn: "Turnkey design, supply, and installation of addressable fire alarm and public address/evacuation systems in full compliance with the regulatory standards of Kazakhstan.",
    featuresRu: [
      "Адресные пожарные панели с точным определением места задымления",
      "Цифровые системы оповещения и трансляции звука (СОУЭ 1-5 типов)",
      "Интеграция с СКУД, лифтами, вентиляцией и клапанами ОЗК"
    ],
    featuresKz: [
      "Түтін шыққан орынды дәл анықтайтын адрестік өрт панельдері",
      "Эвакуацияны дауыспен басқару және хабарландыру жүйелері"
    ],
    featuresEn: [
      "Intelligent addressable fire alarm control panels with pinpoint detector location",
      "Multi-zone digital voice alarm and public address (PA/VA) systems"
    ],
    stagesRu: [
      { step: "01", title: "Проект АПС/СОУЭ", desc: "Разрабатываем проектно-сметную документацию." },
      { step: "02", title: "Монтаж линий", desc: "Прокладываем огнестойкие кабельные линии." },
      { step: "03", title: "Пусконаладка", desc: "Настраиваем адресные извещатели и приборы." },
      { step: "04", title: "Сдача инспекции", desc: "Проводим испытания и сдаем объект пожарной инспекции." }
    ],
    faqsRu: [
      { q: "Предоставляете ли вы гарантию?", a: "Да, предоставляем официальную гарантию и регламентное ТО." }
    ]
  },

  "cctv-access-control": {
    slug: "cctv-access-control",
    icon: Cctv,
    color: "#A8ADB5",
    badgeRu: "СКУД & CCTV",
    badgeKz: "Бейне & СКУД",
    badgeEn: "CCTV & Access",
    titleRu: "Видеонаблюдение и контроль доступа (СКУД, NVR, Биометрия)",
    titleKz: "Бейнебақылау және қолжетімділікті басқару (СКУД)",
    titleEn: "CCTV Video Surveillance & Access Control",
    descRu: "Современные системы безопасности: IP-видеонаблюдение высокой четкости с искусственным интеллектом, биометрический контроль доступа (Face ID, отпечатки), турникеты, шлагбаумы и учет рабочего времени.",
    descKz: "Заманауи қауіпсіздік жүйелері: жасанды интеллектісі бар IP-бейнебақылау, биометриялық рұқсат бақылауы (Face ID), турникеттер және жұмыс уақытын есепке алу.",
    descEn: "Enterprise IP video surveillance with AI analytics, Face ID biometrics, turnstiles, barriers, and automated time-attendance tracking.",
    featuresRu: [
      "IP-камеры с видеоаналитикой (распознавание лиц, номеров, периметр)",
      "Биометрические терминалы Face ID и доступ со смартфона",
      "Интеграция с 1С для учета рабочего времени"
    ],
    featuresKz: [
      "Жасанды интеллектісі бар смарт IP-камералар",
      "Face ID және биометриялық рұқсат терминалдары"
    ],
    featuresEn: [
      "High-definition IP cameras with edge AI recognition",
      "Contactless Face ID terminals and mobile Bluetooth/NFC credentials"
    ],
    stagesRu: [
      { step: "01", title: "Аудит объекта", desc: "Рассчитываем зоны обзора и точки доступа." },
      { step: "02", title: "Монтаж камер", desc: "Прокладываем трассы и устанавливаем камеры и турникеты." },
      { step: "03", title: "Настройка прав", desc: "Настраиваем сервер записи NVR и права персонала." }
    ],
    faqsRu: [
      { q: "Сколько хранится архив?", a: "От 14 до 90+ суток в зависимости от объема дисков." }
    ]
  },

  "sound-and-light": {
    slug: "sound-and-light",
    icon: Speaker,
    color: "#B8A276",
    badgeRu: "Звук и свет",
    badgeKz: "Дыбыс және жарық",
    badgeEn: "Audio & Light",
    titleRu: "Профессиональный звук и сценический свет в Алматы",
    titleKz: "Кәсіби дыбыс және сахналық жарық",
    titleEn: "Professional Sound & Stage Lighting",
    descRu: "Акустическое проектирование и оснащение конференц-залов, концертных площадок, ресторанов, культовых сооружений и ТРЦ. Линейные массивы, фоновое озвучивание, микрофонные системы и динамический сценический свет.",
    descKz: "Конференц-залдар, концерт алаңдары, мейрамханалар мен сауда орталықтарын кәсіби дыбыстық және жарық жабдықтарымен жабдықтау. Акустикалық есептеу, сызықтық массивтер және сахналық жарық.",
    descEn: "Acoustic design and installation for conference halls, concert venues, hospitality, and retail spaces. Line arrays, DSP processing, microphone arrays, and intelligent lighting.",
    featuresRu: [
      "Электроакустический расчет для идеальной разборчивости речи",
      "Линейные массивы, сабвуферы и потолочная трансляционная акустика",
      "Сценический динамический свет DMX и LED-экраны"
    ],
    featuresKz: [
      "Сөз анықтығын қамтамасыз ететін акустикалық есептеу",
      "DMX сахналық динамикалық жарықтандыру"
    ],
    featuresEn: [
      "Computer-modeled acoustic simulation for speech intelligibility",
      "Line arrays, distributed audio, and High-End amplification"
    ],
    stagesRu: [
      { step: "01", title: "Замеры зала", desc: "Проводим акустические измерения зала." },
      { step: "02", title: "Монтаж подвесов", desc: "Монтируем подвесы акустики и аудио-трассы." },
      { step: "03", title: "Калибровка DSP", desc: "Настраиваем процессоры измерительными микрофонами." }
    ],
    faqsRu: [
      { q: "Делаете ли вы фоновый звук?", a: "Да, монтируем многозонные 100V трансляционные системы." }
    ]
  },

  "networks-smatv": {
    slug: "networks-smatv",
    icon: Network,
    color: "#A8ADB5",
    badgeRu: "СКС & SMATV",
    badgeKz: "СКС & Желілер",
    badgeEn: "Networks & SMATV",
    titleRu: "Информационные сети, СКС и SMATV (IPTV, Спутниковое ТВ)",
    titleKz: "Ақпараттық желілер, СКС және SMATV",
    titleEn: "Data Networks, Structured Cabling & SMATV",
    descRu: "Проектирование и построение структурированных кабельных систем (СКС), оптоволокна (ВОЛС), бесшовного корпоративного Wi-Fi и гостиничного телевидения SMATV/IPTV.",
    descKz: "Құрылымдалған кабельдік желілерді (СКС), талшықты-оптикалық байланыс желілерін (ВОЛС), үздіксіз Wi-Fi және қонақүйлерге арналған интерактивті теледидар жүйелерін құру.",
    descEn: "Structured cabling (SCS), fiber optic infrastructure, enterprise-grade seamless Wi-Fi, and interactive SMATV/IPTV systems for hospitality and commercial buildings.",
    featuresRu: [
      "Сертифицированные кабельные системы категорий 5e, 6, 6A, 7 с гарантией",
      "Сварка оптоволокна и тестирование линий сканером Fluke Networks",
      "Корпоративный Wi-Fi с бесшовным роумингом"
    ],
    featuresKz: [
      "5e, 6, 6A санатты сертификатталған СКС желілері",
      "Оптикалық талшықтарды кәсіби дәнекерлеу және Fluke сынағы"
    ],
    featuresEn: [
      "Certified Cat 6 / 6A / 7 structured cabling with warranties",
      "High-density seamless enterprise Wi-Fi networks"
    ],
    stagesRu: [
      { step: "01", title: "Аудит потребностей", desc: "Определяем число портов и плотность Wi-Fi." },
      { step: "02", title: "Монтаж кабелей", desc: "Прокладываем витую пару и оптоволокно." },
      { step: "03", title: "Тест Fluke", desc: "Тестируем порты и настраиваем коммутаторы." }
    ],
    faqsRu: [
      { q: "Предоставляете ли протоколы Fluke?", a: "Да, на каждую смонтированную линию предоставляется официальный паспорт теста." }
    ]
  },

  "system-integration": {
    slug: "system-integration",
    icon: Combine,
    color: "#3B82F6",
    badgeRu: "Генеральный подряд",
    badgeKz: "Бас мердігерлік",
    badgeEn: "Systems Integration",
    titleRu: "Системная интеграция слаботочных систем под ключ",
    titleKz: "Төменгі ток жүйелерінің кешенді интеграциясы",
    titleEn: "End-to-End Systems Integration",
    descRu: "Генеральный подряд по слаботочным системам. Объединение разрозненного оборудования (BMS, пожарная сигнализация, СКУД, CCTV, звук, мультимедиа) в единую слаженно работающую экосистему с централизованным управлением.",
    descKz: "Ғимараттардың барлық инженерлік және әлсіз ток желілері бойынша бас мердігерлік. BMS, өрт дабылы, СКУД, бейнебақылау және мультимедианы бірыңғай цифрлық жүйеге біріктіру.",
    descEn: "Master technology contractor for low-voltage systems. Harmonizing BMS, fire safety, access control, CCTV, and audio-visual into a cohesive, reliable infrastructure.",
    featuresRu: [
      "Единая точка ответственности за все слаботочные разделы объекта",
      "Бесшовная аппаратная и программная стыковка оборудования разных брендов",
      "Оптимизация бюджета стройки за счет исключения дублирующих трасс"
    ],
    featuresKz: [
      "Нысанның барлық төменгі ток бөлімдері үшін бірыңғай жауапкершілік",
      "Құрылыс сметасын 20%-ға дейін оңтайландыру"
    ],
    featuresEn: [
      "Single point of responsibility for all building technology packages",
      "Seamless multi-vendor interoperability via open standards"
    ],
    stagesRu: [
      { step: "01", title: "Аудит проекта", desc: "Координируем смежные разделы инженерии." },
      { step: "02", title: "Прямые поставки", desc: "Осуществляем поставки оборудования с заводов." },
      { step: "03", title: "Монтаж и пусконаладка", desc: "Параллельно монтируем и тестируем системы." },
      { step: "04", title: "Сдача надзору", desc: "Сдаем объект госкомиссии под ключ." }
    ],
    faqsRu: [
      { q: "В каких городах вы работаете?", a: "Алматы, Астана, Шымкент, Актобе, Караганда и по всему Казахстану." }
    ]
  }
};

const currentSlug = computed(() => route.params.slug);
const currentService = computed(() => servicesMap[currentSlug.value] || null);

// Языковая адаптация полей
const activeLang = computed(() => locale.value || "ru");

const serviceTitle = computed(() => {
  const s = currentService.value;
  if (!s) return "";
  if (activeLang.value === "kz") return s.titleKz || s.titleRu;
  if (activeLang.value === "en") return s.titleEn || s.titleRu;
  return s.titleRu;
});

const serviceBadge = computed(() => {
  const s = currentService.value;
  if (!s) return "";
  if (activeLang.value === "kz") return s.badgeKz || s.badgeRu;
  if (activeLang.value === "en") return s.badgeEn || s.badgeRu;
  return s.badgeRu;
});

const serviceDesc = computed(() => {
  const s = currentService.value;
  if (!s) return "";
  if (activeLang.value === "kz") return s.descKz || s.descRu;
  if (activeLang.value === "en") return s.descEn || s.descRu;
  return s.descRu;
});

const serviceFeatures = computed(() => {
  const s = currentService.value;
  if (!s) return [];
  if (activeLang.value === "kz" && s.featuresKz) return s.featuresKz;
  if (activeLang.value === "en" && s.featuresEn) return s.featuresEn;
  return s.featuresRu || [];
});

// UI текстовые метки на 3 языках
const uiLabels = computed(() => {
  const l = activeLang.value;
  return {
    home: l === "kz" ? "Басты бет" : (l === "en" ? "Home" : "Главная"),
    services: l === "kz" ? "Қызметтер" : (l === "en" ? "Services" : "Услуги"),
    capabilities: l === "kz" ? "Мүмкіндіктер" : (l === "en" ? "Capabilities" : "Возможности"),
    capabilitiesTitle: l === "kz" ? "Жүйені енгізуге не кіреді" : (l === "en" ? "System Scope & Deliverables" : "Что входит в реализацию системы"),
    process: l === "kz" ? "Кезеңдер" : (l === "en" ? "Process" : "Процесс"),
    processTitle: l === "kz" ? "Жобалау және енгізу кезеңдері" : (l === "en" ? "Engineering & Deployment Stages" : "Этапы проектирования и внедрения"),
    faqTitle: l === "kz" ? "Жиі қойылатын сұрақтар" : (l === "en" ? "Frequently Asked Questions" : "Часто задаваемые вопросы"),
    ctaTitle: l === "kz" ? "Жобаңызды талқылауға дайынсыз ба?" : (l === "en" ? "Ready to discuss your project in Kazakhstan?" : "Готовы обсудить ваш проект в Алматы или регионах РК?"),
    ctaDesc: l === "kz" ? "Жетекші инженерден тегін кеңес алыңыз және сметаны есептетіңіз." : (l === "en" ? "Get a free engineering consultation and turnkey budget estimate." : "Получите бесплатную консультацию ведущего инженера и предварительный расчет сметы."),
    whatsappBtn: l === "kz" ? "WhatsApp арқылы сметаны есептеу" : (l === "en" ? "Request Estimate on WhatsApp" : "Рассчитать смету в WhatsApp"),
    callBtn: "+7 (701) 995-42-17",
    otherTitle: l === "kz" ? "Басқа инженерлік бағыттар" : (l === "en" ? "Other Engineering Capabilities" : "Другие инженерные направления INPAR"),
    notFound: l === "kz" ? "Қызмет табылмады" : (l === "en" ? "Service not found" : "Услуга не найдена"),
    backBtn: l === "kz" ? "Барлық қызметтерге оралу" : (l === "en" ? "Back to services" : "Вернуться ко всем услугам")
  };
});

// FAQ Аккордеон
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
  if (!service) return;

  const l = activeLang.value;
  const langPrefix = l === "kz" ? "/kz" : (l === "en" ? "/en" : "");
  const canonical = `https://inpar.kz${langPrefix}/services/${service.slug}`;

  const title = `${serviceTitle.value} | INPAR.KZ`;
  const description = `${serviceDesc.value.slice(0, 160)}... Сертификатталған инжиниринг, поставка и монтаж.`;
  const keywords = `${serviceBadge.value}, ${serviceTitle.value}, слаботочные системы, автоматизация Казахстан, MCC, DDC, KNX, INPAR`;

  const jsonLd = [
    {
      "@context": "https://schema.org",
      "@type": "Service",
      "name": serviceTitle.value,
      "description": serviceDesc.value,
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
      "areaServed": {"@type": "Country", "name": "Kazakhstan"}
    },
    {
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": uiLabels.value.home, "item": `https://inpar.kz${langPrefix}/` },
        { "@type": "ListItem", "position": 2, "name": uiLabels.value.services, "item": `https://inpar.kz${langPrefix}/#services` },
        { "@type": "ListItem", "position": 3, "name": serviceTitle.value, "item": canonical }
      ]
    }
  ];

  updateSEO({
    title,
    description,
    keywords,
    url: canonical,
    lang: l,
    path: route.path,
    jsonLd
  });
};

onMounted(() => {
  applySeo();
  window.scrollTo(0, 0);
});

watch(
  [() => route.params.slug, () => locale.value],
  () => {
    applySeo();
    openFaqIndex.value = null;
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
);

const whatsappLink = computed(() => {
  const name = serviceTitle.value || "Инженерные услуги";
  const text = `Здравствуйте! Интересует услуга «${name}». Хочу получить предварительный расчет и консультацию.`;
  return `https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(text)}`;
});

const getServiceLink = (slug) => {
  const l = activeLang.value;
  return l === "ru" ? `/services/${slug}` : `/${l}/services/${slug}`;
};
</script>

<template>
  <div class="min-h-screen bg-[#13151A] text-[#E8E9ED]">
    <Navbar />

    <main v-if="currentService" class="pt-32 pb-24">
      <!-- Хлебные крошки -->
      <nav class="max-w-7xl mx-auto px-6 lg:px-12 mb-8 text-xs text-[#9BA1AB] flex items-center gap-2">
        <router-link :to="activeLang === 'ru' ? '/' : `/${activeLang}`" class="hover:text-[#3B82F6] transition-colors">
          {{ uiLabels.home }}
        </router-link>
        <span>/</span>
        <a :href="activeLang === 'ru' ? '/#services' : `/${activeLang}/#services`" class="hover:text-[#3B82F6] transition-colors">
          {{ uiLabels.services }}
        </a>
        <span>/</span>
        <span class="text-[#E8E9ED]">{{ serviceTitle }}</span>
      </nav>

      <!-- Hero Header -->
      <section class="max-w-7xl mx-auto px-6 lg:px-12 mb-20">
        <div class="relative p-8 md:p-14 border border-[#333842] bg-gradient-to-br from-[#1A1D23] via-[#20242D] to-[#16181F] rounded-2xl overflow-hidden shadow-2xl">
          <div class="absolute -right-20 -top-20 w-80 h-80 rounded-full opacity-10 blur-3xl pointer-events-none" :style="{ backgroundColor: currentService.color }"></div>

          <div class="flex items-center gap-3 mb-6">
            <div class="h-px w-8 bg-[#B8A276]" />
            <span class="text-[#B8A276] text-xs uppercase tracking-[0.2em] font-medium">
              {{ serviceBadge }}
            </span>
          </div>

          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-8 mb-8">
            <div class="max-w-3xl">
              <h1 class="text-3xl md:text-5xl font-light tracking-tight text-[#FFFFFF] mb-6 leading-tight">
                {{ serviceTitle }}
              </h1>
              <p class="text-[#9BA1AB] text-base md:text-lg leading-relaxed font-light">
                {{ serviceDesc }}
              </p>
            </div>

            <div class="flex flex-col gap-3 min-w-[260px]">
              <a
                :href="whatsappLink"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center justify-center gap-3 px-6 py-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-sm transition-all duration-300 shadow-lg shadow-emerald-950/40 hover:scale-[1.02]"
              >
                <MessageCircle class="w-5 h-5" />
                {{ uiLabels.whatsappBtn }}
              </a>

              <a
                href="tel:+77019954217"
                class="inline-flex items-center justify-center gap-3 px-6 py-3.5 rounded-xl border border-[#333842] hover:border-[#3B82F6]/50 bg-[#1A1D23]/60 text-[#E8E9ED] text-sm font-light transition-all duration-300"
              >
                <Phone class="w-4 h-4 text-[#B8A276]" />
                {{ uiLabels.callBtn }}
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- Возможности / Характеристики -->
      <section class="max-w-7xl mx-auto px-6 lg:px-12 mb-20">
        <div class="flex items-center gap-4 mb-4">
          <div class="h-px w-8 bg-[#3B82F6]" />
          <span class="text-[#3B82F6] text-xs uppercase tracking-[0.2em]">{{ uiLabels.capabilities }}</span>
        </div>
        <h2 class="text-2xl md:text-3xl font-light tracking-tight text-white mb-8">
          {{ uiLabels.capabilitiesTitle }}
        </h2>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="(feature, idx) in serviceFeatures"
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

      <!-- Этапы работ -->
      <section v-if="currentService.stagesRu && currentService.stagesRu.length" class="max-w-7xl mx-auto px-6 lg:px-12 mb-20">
        <div class="flex items-center gap-4 mb-4">
          <div class="h-px w-8 bg-[#B8A276]" />
          <span class="text-[#B8A276] text-xs uppercase tracking-[0.2em]">{{ uiLabels.process }}</span>
        </div>
        <h2 class="text-2xl md:text-3xl font-light tracking-tight text-white mb-8">
          {{ uiLabels.processTitle }}
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

      <!-- FAQ Section -->
      <section v-if="currentService.faqsRu && currentService.faqsRu.length" class="max-w-4xl mx-auto px-6 lg:px-12 mb-20">
        <div class="text-center mb-10">
          <span class="text-[#B8A276] text-xs uppercase tracking-[0.2em] block mb-2">FAQ</span>
          <h2 class="text-2xl md:text-3xl font-light tracking-tight text-white">
            {{ uiLabels.faqTitle }}
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
            {{ uiLabels.ctaTitle }}
          </h2>
          <p class="text-[#9BA1AB] max-w-2xl mx-auto mb-8 font-light text-sm md:text-base">
            {{ uiLabels.ctaDesc }}
          </p>
          <div class="flex flex-wrap items-center justify-center gap-4">
            <a
              :href="whatsappLink"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center gap-3 px-8 py-4 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-medium transition-all duration-300 shadow-lg shadow-emerald-950/40"
            >
              <MessageCircle class="w-5 h-5" />
              {{ uiLabels.whatsappBtn }}
            </a>
            <router-link
              :to="activeLang === 'ru' ? '/projects' : `/${activeLang}/projects`"
              class="inline-flex items-center gap-3 px-8 py-4 rounded-xl border border-[#333842] hover:border-[#3B82F6] bg-[#1A1D23] text-white font-light text-sm transition-all duration-300"
            >
              Портфолио проектов / Projects
              <ArrowRight class="w-4 h-4" />
            </router-link>
          </div>
        </div>
      </section>

      <!-- Другие инженерные направления (Перелинковка) -->
      <section class="max-w-7xl mx-auto px-6 lg:px-12">
        <h2 class="text-xl font-light tracking-tight text-[#9BA1AB] mb-6 uppercase tracking-wider text-xs">
          {{ uiLabels.otherTitle }}
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <router-link
            v-for="other in otherServices"
            :key="other.slug"
            :to="getServiceLink(other.slug)"
            class="p-5 border border-[#333842] bg-[#1A1D23]/40 hover:bg-[#20242D] hover:border-[#3B82F6]/50 rounded-xl transition-all duration-300 flex items-center justify-between group"
          >
            <div>
              <span class="text-[11px] text-[#B8A276] uppercase tracking-wider block mb-1">
                {{ activeLang === 'kz' ? (other.badgeKz || other.badgeRu) : (activeLang === 'en' ? (other.badgeEn || other.badgeRu) : other.badgeRu) }}
              </span>
              <h3 class="text-sm font-normal text-[#E8E9ED] group-hover:text-white transition-colors">
                {{ activeLang === 'kz' ? (other.titleKz || other.titleRu) : (activeLang === 'en' ? (other.titleEn || other.titleRu) : other.titleRu) }}
              </h3>
            </div>
            <ArrowRight class="w-4 h-4 text-[#9BA1AB] group-hover:text-[#3B82F6] group-hover:translate-x-1 transition-all" />
          </router-link>
        </div>
      </section>
    </main>

    <!-- Если не найдено -->
    <div v-else class="max-w-4xl mx-auto px-6 py-40 text-center">
      <h1 class="text-3xl text-white mb-4">{{ uiLabels.notFound }}</h1>
      <router-link :to="activeLang === 'ru' ? '/#services' : `/${activeLang}/#services`" class="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[#3B82F6] text-white">
        {{ uiLabels.backBtn }}
      </router-link>
    </div>

    <AppFooter />
  </div>
</template>
