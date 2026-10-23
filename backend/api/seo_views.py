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
    "mcc-cabinets": {
        "slug": "mcc-cabinets",
        "icon": "Layers",
        "badge": {
            "ru": "MCC & Приводы",
            "kz": "MCC және жетектер",
            "en": "MCC & Motor Control"
        },
        "ru": {
            "title": "Шкафы управления двигателями MCC (Motor Control Center) и ЧРП в Алматы",
            "description": "Проектирование и сборка шкафов MCC (Motor Control Center), щитов управления электродвигателями, насосными станциями, вентиляторами и конвейерами с частотными преобразователями (ЧРП) и устройствами плавного пуска (УПП) в Казахстане.",
            "keywords": "шкафы управления MCC Алматы, Motor Control Center Казахстан, щиты управления двигателями, шкафы ЧРП Казахстан, шкафы насосных станций, щиты плавного пуска, частотно-регулируемый привод, электрощитовое производство MCC, защита насоса от гидроудара, автоматизация КНС ХВС, плавный пуск насосов, шкафы Danfoss Schneider ABB",
            "features": [
                "Индивидуальное проектирование и сборка силовых шкафов MCC по ГОСТ и МЭК (IEC 61439)",
                "Интеграция частотных преобразователей (Danfoss, Schneider Electric, ABB, INVT) и УПП",
                "Автоматический ввод резерва (АВР) и защита электродвигателей от перегрузок и перекоса фаз",
                "Интерфейсы связи RS-485 Modbus, Profinet, Ethernet для подключения к SCADA и BMS",
                "Качественные корпуса со степенью защиты IP31, IP54, IP65 для тяжелых промышленных условий"
            ],
            "stages": [
                "Расчет электрических нагрузок и составление однолинейных схем",
                "Выбор коммутационной аппаратуры, дросселей и частотных преобразователей",
                "Сборка шкафов на собственной производственной базе с лазерной маркировкой",
                "Заводское тестирование на стенде: проверка логики, блокировок и изоляции",
                "Шеф-монтаж, параметрирование приводов на объекте и ввод в промышленную эксплуатацию"
            ],
            "faqs": [
                {
                    "q": "В чем главное преимущество шкафов MCC перед обычными пускателями?",
                    "a": "Шкафы MCC объединяют управление несколькими приводами в единый модуль с комплексной защитой, плавным пуском и возможностью диспетчеризации, что продлевает ресурс двигателей в 3–5 раз и экономит до 35% электроэнергии."
                },
                {
                    "q": "Каковы сроки изготовления шкафа MCC по индивидуальному проекту?",
                    "a": "В зависимости от комплектации и мощности приводов сборка занимает от 10 до 25 рабочих дней."
                },
                {
                    "q": "Как шкаф MCC защищает от гидроударов в водопроводе?",
                    "a": "Частотный преобразователь плавно изменяет частоту тока (от 0 до 50 Гц), исключая резкий скачок давления в трубах при старте и останове насосных агрегатов."
                },
                {
                    "q": "Можно ли подключить шкаф управления MCC к общей системе SCADA или диспетчеризации здания?",
                    "a": "Да, наши шкафы комплектуются интерфейсами RS-485 Modbus RTU, Ethernet Modbus TCP или Profinet для передачи всех параметров (ток, давление, аварии, наработка моточасов) на пульт диспетчера."
                }
            ],
            "problems": [
                {
                    "problem": "Частые гидроудары в трубопроводах и разрушение рабочих колес насосов при прямом пуске от сети.",
                    "solution": "Установка шкафов MCC с частотными преобразователями (ЧРП) и устройствами плавного пуска (УПП) с S-образной кривой разгона.",
                    "benefit": "Полное устранение гидроударов, продление ресурса насосов в 3–5 раз и защита труб от прорывов."
                },
                {
                    "problem": "Сгорание электродвигателей из-за перекоса фаз, просадок напряжения или сухого хода скважины.",
                    "solution": "Интеллектуальное микропроцессорное реле защиты и датчики уровня с автоматическим вводом резервного насоса (АВР).",
                    "benefit": "100% защита мотора от перегрева и бесперебойная подача воды 24/7."
                },
                {
                    "problem": "Высокие счета за электроэнергию из-за постоянной работы двигателей на максимальных оборотах (50 Гц).",
                    "solution": "Автоматическое ПИД-регулирование частоты вращения в зависимости от фактического расхода и давления.",
                    "benefit": "Экономия электроэнергии от 25% до 40% и снижение пусковых токов в 6 раз."
                }
            ]
        },
        "kz": {
            "title": "MCC (Motor Control Center) қозғалтқыштарды басқару шкафтары мен жиілік түрлендіргіштер",
            "description": "Қазақстанда жиілік түрлендіргіштері (ЖТ) мен жұмсақ іске қосқыштары бар MCC (Motor Control Center) шкафтарын, электр қозғалтқыштарын, сорғы станцияларын, желдеткіштерді басқару қалқандарын жобалау және құрастыру.",
            "keywords": "MCC басқару шкафтары Алматы, Motor Control Center Қазақстан, қозғалтқыштарды басқару қалқандары, сорғы станцияларын басқару шкафы, жиілік түрлендіргіштер, гидросоққыдан қорғау, сорғыларды автоматтандыру, жұмсақ іске қосу шкафы, сорғы станциялары",
            "features": [
                "IEC 61439 халықаралық стандарттары бойынша MCC күштік шкафтарын жеке жобалау",
                "Danfoss, Schneider Electric, ABB жиілік түрлендіргіштерін біріктіру",
                "Электр қозғалтқыштарын шамадан тыс жүктемеден және фазалардың қисаюынан толық қорғау",
                "SCADA және BMS жүйелеріне қосылу үшін Modbus, Profinet, Ethernet интерфейстері",
                "IP31, IP54, IP65 қорғаныс дәрежесі бар сенімді металл корпустар"
            ],
            "stages": [
                "Электр жүктемелерін есептеу және бірсызықты схемаларды құру",
                "Коммутациялық жабдықтар мен жиілік реттегіштерін таңдау",
                "Шкафтарды жеке өндірістік базада таңбалаумен кәсіби құрастыру",
                "Зауыттық сынақтар: логиканы, оқшаулауды және қорғанысты тексеру",
                "Нысанда іске қосу-баптау жұмыстары және пайдалануға тапсыру"
            ],
            "faqs": [
                {
                    "q": "MCC шкафтары қандай нысандарға қажет?",
                    "a": "Өндіріс орындары, кәріз және су сорғы станциялары, ірі ғимараттардың желдету жүйелері мен конвейерлері үшін таптырмас шешім."
                },
                {
                    "q": "MCC шкафтары сорғыларды қалай қорғайды?",
                    "a": "Жиілік түрлендіргіш қозғалтқышты бірқалыпты іске қосады, құбырлардағы қысымның күрт көтерілуін жояды және фазалардың қисаюын бақылайды."
                }
            ],
            "problems": [
                {
                    "problem": "Сорғыларды тікелей қосқанда құбырлардағы гидросоққылар және жабдықтың тез істен шығуы.",
                    "solution": "Жиілік түрлендіргіштері (ЖТ) мен жұмсақ іске қосқыштары бар MCC шкафтарын орнату.",
                    "benefit": "Гидросоққыларды толық жою, сорғылардың қызмет ету мерзімін 3–5 есеге дейін ұзарту."
                },
                {
                    "problem": "Фазалардың жоғалуынан немесе сорғының кептелуінен электр қозғалтқыштарының күйіп кетуі.",
                    "solution": "Фазаларды бақылайтын микропроцессорлық релелер және құрғақ жүрістен автоматты қорғаныс.",
                    "benefit": "Қозғалтқыштарды 100% апаттан сақтау және резервтік сорғыға бірден автоматты ауысу."
                },
                {
                    "problem": "Сорғылардың үнемі толық қуатта жұмыс істеуінен электр қуатына артық шығындар.",
                    "solution": "Қысым датчиктерінің мәніне сәйкес қозғалтқыш айналымын автоматты реттеу (ПИД-реттеу).",
                    "benefit": "Электр энергиясын 35%-ға дейін үнемдеу."
                }
            ]
        },
        "en": {
            "title": "Motor Control Center (MCC) Panels & VFD Automation Cabinets in Kazakhstan",
            "description": "Engineering, custom manufacturing, and commissioning of Motor Control Center (MCC) panels, Variable Frequency Drives (VFD), and soft starter cabinets for pumps, ventilation, and industrial machinery in Almaty and across Kazakhstan.",
            "keywords": "MCC panels Almaty, Motor Control Center Kazakhstan, VFD control cabinets, pump station control panels, motor starters, industrial electrical enclosures, water hammer prevention, pump soft starters, industrial MCC panels, motor protection relays",
            "features": [
                "Custom-engineered MCC switchboards compliant with IEC 61439 standards",
                "Integration of leading VFD brands (Danfoss, Schneider Electric, ABB, Siemens)",
                "Advanced motor thermal protection, phase loss prevention, and automatic transfer switches (ATS)",
                "Industrial protocols: Modbus RTU/TCP, Profinet, BACnet for SCADA and BMS integration",
                "Enclosures up to IP65 for harsh industrial, outdoor, and utility environments"
            ],
            "stages": [
                "Electrical load calculations and single-line diagram (SLD) development",
                "Component specification: contactors, VFDs, chokes, and PLCs",
                "Panel assembly with laser wire labeling and strict QC checks",
                "Full workshop bench testing: interlocks, dielectric strength, and functional logic",
                "On-site installation supervision, parameter tuning, and final commissioning"
            ],
            "faqs": [
                {
                    "q": "What are the main advantages of an MCC panel?",
                    "a": "Centralized power and control for multiple electric motors, enhanced operator safety, seamless automation integration, and significant energy savings."
                },
                {
                    "q": "Can your MCC panels integrate with third-party BMS or SCADA platforms?",
                    "a": "Yes, we integrate Modbus RTU/TCP, BACnet, and Profinet communication cards to stream operating currents, pressures, and diagnostic fault codes to any supervisory station."
                }
            ],
            "problems": [
                {
                    "problem": "Severe hydraulic water hammer and rapid mechanical wear during direct-on-line (DOL) pump starts.",
                    "solution": "Custom MCC cabinets featuring Variable Frequency Drives (VFD) and soft starters with smooth S-ramp curves.",
                    "benefit": "Complete elimination of pipe pressure spikes, extending pump lifespan by 300-500%."
                },
                {
                    "problem": "Motor burnouts caused by voltage phase loss, unbalance, or dry-run impeller jamming.",
                    "solution": "Microprocessor motor protection relays, PTC thermistor monitoring, and automatic duty/standby pump rotation.",
                    "benefit": "Zero motor failures and 24/7 continuous water and utility service."
                },
                {
                    "problem": "Excessive electrical power bills from motors constantly running at fixed maximum speed.",
                    "solution": "Closed-loop PID pressure feedback modulation automatically matching motor output to actual process demand.",
                    "benefit": "Up to 35-40% reduction in electricity consumption and fast return on investment."
                }
            ]
        },
        "knowsAbout": [
            {
                "name": "Motor Control Center",
                "sameAs": "https://www.wikidata.org/wiki/Q175185"
            },
            {
                "name": "Variable-frequency drive",
                "sameAs": "https://www.wikidata.org/wiki/Q1055745"
            },
            {
                "name": "Motor soft starter",
                "sameAs": "https://www.wikidata.org/wiki/Q1760467"
            }
        ],
        "related_services": [
            "electrical-cabinets",
            "bms-dispatching",
            "industrial-automation"
        ]
    },
    "ddc-automation": {
        "slug": "ddc-automation",
        "icon": "Cpu",
        "badge": {
            "ru": "DDC & ОВиК",
            "kz": "DDC және Желдету",
            "en": "DDC Automation"
        },
        "ru": {
            "title": "Шкафы и контроллеры прямого цифрового управления DDC (Direct Digital Control)",
            "description": "Проектирование, сборка шкафов DDC и программирование свободно программируемых контроллеров прямого цифрового управления для приточно-вытяжных установок (ПВУ), тепловых пунктов (ИТП), чиллеров, фанкойлов и кондиционирования в Алматы.",
            "keywords": "шкафы DDC Алматы, контроллеры DDC Казахстан, прямое цифровое управление, автоматизация вентиляции DDC, щиты ОВиК DDC, шкафы ИТП, программирование DDC контроллеров, защита калорифера от замерзания, шкафы автоматики вентиляции, приводы Belimo 0-10V, контроллеры Segnetics Carel, автоматика ИТП",
            "features": [
                "Свободно программируемые DDC-контроллеры с поддержкой протоколов BACnet IP/MSTP, Modbus",
                "Прецизионное поддержание температуры, влажности, CO2 и перепада давления",
                "Плавное управление водяными клапанами, приводами воздушных заслонок и рекуператорами",
                "Автоматическая защита от замерзания калориферов и контроль загрязнения фильтров",
                "Встроенный веб-сервер контроллеров для настройки с ноутбука или смартфона без спецПО"
            ],
            "stages": [
                "Анализ аэродинамических и гидравлических схем вентиляции и ИТП",
                "Разработка шкафов автоматики DDC, подбор датчиков и сервоприводов",
                "Сборка щитов управления DDC с эргономичной компоновкой и защитой",
                "Написание прикладных алгоритмов ПИД-регулирования и энергосберегающих режимов",
                "Пусконаладочные испытания на объекте и калибровка всех измерительных каналов"
            ],
            "faqs": [
                {
                    "q": "Что такое DDC контроллер?",
                    "a": "DDC (Direct Digital Control) — микропроцессорный контроллер прямого цифрового управления, выполняющий алгоритмы управления климатом без участия оператора с высокой точностью."
                },
                {
                    "q": "Как DDC защищает калорифер от разморозки при внезапном отключении электричества?",
                    "a": "При пропадании питания привод воздушной заслонки с возвратной пружиной немедленно захлопывается, а клапан теплоносителя открывается на 100%, предотвращая доступ ледяного уличного воздуха к водяным трубкам."
                },
                {
                    "q": "Контроллеры каких производителей вы используете в сборке DDC?",
                    "a": "Мы используем надежные контроллеры Segnetics (Pixel, Matrix), Carel, Siemens Desigo, Danfoss и ОВЕН в зависимости от технического задания и бюджета заказчика."
                }
            ],
            "problems": [
                {
                    "problem": "Замерзание и разрыв медных трубок водяного калорифера приточной вентиляции в зимний период.",
                    "solution": "3-контурная аппаратная защита DDC: капиллярный термостат аварии, датчик температуры обратной воды и автопрогрев теплообменника перед открытием воздушной заслонки.",
                    "benefit": "100% гарантия сохранности калорифера от разморозки даже при морозах до -40°C."
                },
                {
                    "problem": "Нестабильный микроклимат в помещениях: духота, сквозняки или постоянные скачки температуры.",
                    "solution": "DDC контроллеры с адаптивным ПИД-регулированием и датчиками CO2, влажности и комнатной температуры.",
                    "benefit": "Идеальный комфортный микроклимат с точностью ±0.5°C и экономия тепловой энергии."
                },
                {
                    "problem": "Служба эксплуатации не знает о загрязнении фильтров или обрыве приводного ремня вентилятора.",
                    "solution": "Установка прецизионных реле перепада давления с выводом предупреждений на графическую панель шкафа DDC.",
                    "benefit": "Своевременная замена расходников без аварийной остановки системы воздухообмена."
                }
            ]
        },
        "kz": {
            "title": "DDC (Direct Digital Control) тікелей цифрлық басқару шкафтары мен контроллерлері",
            "description": "Алматыда желдету қондырғылары, жылу пункттері (ЖТП), чиллерлер мен ауа баптау жүйелері үшін DDC тікелей цифрлық басқару шкафтарын жобалау, құрастыру және контроллерлерді бағдарламалау.",
            "keywords": "DDC шкафтары Алматы, DDC контроллерлері Қазақстан, тікелей цифрлық басқару, желдетуді автоматтандыру, DDC басқару қалқандары, калориферді қатып қалудан қорғау, желдету автоматикасы шкафы, Belimo жетектері, DDC контроллерлері",
            "features": [
                "BACnet және Modbus хаттамаларын қолдайтын бағдарламаланатын DDC контроллерлері",
                "Температура, ылғалдылық және CO2 деңгейін жоғары дәлдікпен реттеу",
                "Жылытқыштарды қатып қалудан автоматты түрде кешенді қорғау",
                "Смартфоннан немесе ДК-ден тікелей басқаруға арналған кірістірілген веб-интерфейс"
            ],
            "stages": [
                "Инженерлік сызбаларды талдау және DDC шкафының жобасын жасау",
                "Щиттерді кәсіби жинау және сенсорлар мен жетектерді іріктеу",
                "ПИД-реттеу алгоритмдерін бағдарламалау",
                "Нысанда кешенді тексеру және калибрлеу жұмыстары"
            ],
            "faqs": [
                {
                    "q": "DDC жүйесі энергия үнемдеуге қалай әсер етеді?",
                    "a": "Ауа райына байланысты реттеу және түнгі/демалыс күндері режимдері арқылы жылу мен электр энергиясын 30%-ға дейін үнемдейді."
                },
                {
                    "q": "DDC жүйесі калориферді қатып қалудан қалай сақтайды?",
                    "a": "Жүйе кері қайтқан су температурасын үнемі бақылап, апаттық жағдайда сыртқы ауа қақпағын жауып, жылу клапанын толық ашады."
                }
            ],
            "problems": [
                {
                    "problem": "Қыста қатты аяздарда желдету калориферінің суы қатып, құбырларының жарылуы.",
                    "solution": "3 деңгейлі DDC қорғанысы: капиллярлық термостат, қайту суының температурасын бақылау және алдын ала жылыту циклі.",
                    "benefit": "Калорифердің қатып қалуынан 100% сенімді қорғаныс."
                },
                {
                    "problem": "Ғимараттағы ауаның бұзылуы немесе температураның үнемі ауытқуы.",
                    "solution": "CO2 және температура датчиктерімен жабдықталған ПИД-реттегіш DDC контроллерлері.",
                    "benefit": "Бөлмеде тұрақты жайлы микроклимат сақтау."
                }
            ]
        },
        "en": {
            "title": "Direct Digital Control (DDC) Panels & HVAC Automation in Kazakhstan",
            "description": "Design, panel assembly, and programming of Direct Digital Control (DDC) field controllers for air handling units (AHU), heating substations, chillers, and precision climate systems across Kazakhstan.",
            "keywords": "DDC panels Almaty, Direct Digital Control Kazakhstan, AHU automation panel, HVAC DDC controller programming, BACnet DDC controllers, HVAC frost protection, air handling unit control panel, Belimo valve actuators, DDC AHU controllers",
            "features": [
                "Freely programmable DDC controllers natively supporting BACnet IP/MS-TP and Modbus",
                "Precision PID control of temperature, relative humidity, air quality (CO2), and static pressure",
                "Frost protection routines for heating coils and smart filter differential pressure alerts",
                "Integrated web-server interfaces for direct commissioning without proprietary software"
            ],
            "stages": [
                "Review of mechanical HVAC & hydraulic engineering schematics",
                "DDC panel CAD design, I/O list mapping, and component selection",
                "Factory panel wiring, terminal ferruling, and point-to-point testing",
                "Custom control algorithm programming, setpoint optimization, and commissioning"
            ],
            "faqs": [
                {
                    "q": "What is DDC in building automation?",
                    "a": "Direct Digital Control (DDC) uses automated microprocessor controllers to regulate mechanical systems directly based on real-time sensor feedback."
                },
                {
                    "q": "How does DDC protect against coil freeze during utility power loss?",
                    "a": "Spring-return damper actuators instantly close against incoming sub-zero air while hot water modulating valves default to 100% open."
                }
            ],
            "problems": [
                {
                    "problem": "Catastrophic winter heating coil freeze bursts caused by power outages or circulation pump failures.",
                    "solution": "Triple-redundant DDC frost protection: capillary safety freeze stat, return water temperature monitoring, and pre-heat damper interlocks.",
                    "benefit": "100% prevention of coil freezing down to -40°C ambient temperatures."
                },
                {
                    "problem": "Inconsistent indoor air quality, stuffiness, and drafty temperature swings.",
                    "solution": "Adaptive PID DDC controllers utilizing indoor IAQ, humidity, and CO2 sensor feedback.",
                    "benefit": "Superior indoor comfort with ±0.5°C thermal stability and reduced thermal utility bills."
                }
            ]
        },
        "knowsAbout": [
            {
                "name": "Direct digital control",
                "sameAs": "https://www.wikidata.org/wiki/Q5271878"
            },
            {
                "name": "HVAC control system",
                "sameAs": "https://www.wikidata.org/wiki/Q5635832"
            },
            {
                "name": "Building automation",
                "sameAs": "https://www.wikidata.org/wiki/Q629239"
            }
        ],
        "related_services": [
            "bms-dispatching",
            "mcc-cabinets",
            "electrical-cabinets"
        ]
    },
    "electrical-cabinets": {
        "slug": "electrical-cabinets",
        "icon": "Box",
        "badge": {
            "ru": "Электрощиты",
            "kz": "Электр қалқандары",
            "en": "Electrical Panels"
        },
        "ru": {
            "title": "Сборка электрических шкафов, щитов автоматики (ЩА, ЩУ, ВРУ, ГРЩ) в Алматы",
            "description": "Собственное сертифицированное электрощитовое производство в Алматы: сборка шкафов автоматики (ЩА), щитов управления (ЩУ), главных распределительных щитов (ГРЩ), вводно-распределительных устройств (ВРУ) и щитов освещения (ЩО) любой сложности по индивидуальным схемам.",
            "keywords": "сборка электрических шкафов Алматы, изготовление щитов автоматики Казахстан, сборка ЩА ЩУ ВРУ ГРЩ, электрощитовое производство Алматы, шкафы автоматизации на заказ, щиты управления насосами, сборка щитов по схеме, шкаф АВР на генератор, ВРУ ГРЩ с паспортом, сертификаты технадзор электрощиты",
            "features": [
                "Собственный сборочный цех в Алматы с контролем качества на каждом этапе",
                "Сборка на комплектующих Schneider Electric, ABB, Chint, IEK, EKF под требования и бюджет",
                "Полный пакет исполнительной документации: паспорта изделий, схемы, сертификаты соответствия",
                "Лазерная гравировка маркировки проводов, аппаратов и клеммных колодок",
                "Эргономичная компоновка, аккуратная укладка жгутов и удобство подключения кабелей на объекте"
            ],
            "stages": [
                "Анализ технического задания и принципиальных электрических схем заказчика",
                "3D-компоновка шкафа и оптимизация расположения аппаратуры",
                "Слесарные работы, ошиновка медью и монтаж электроаппаратов",
                "Электромонтажная разводка силовых и сигнальных цепей",
                "Выходной контроль ОТК: проверка изоляции мегаомметром, прозвонка цепей и выдача паспорта"
            ],
            "faqs": [
                {
                    "q": "Собираете ли вы шкафы по индивидуальным нестандартным схемам?",
                    "a": "Да, более 80% наших проектов — это индивидуальные решения под конкретные требования заказчика и особенности объекта."
                },
                {
                    "q": "Предоставляется ли гарантия на собранные щиты?",
                    "a": "Мы предоставляем официальную заводскую гарантию на собранное электрощитовое оборудование от 12 до 24 месяцев."
                },
                {
                    "q": "Предоставляются ли сертификаты и паспорта на готовые шкафы?",
                    "a": "Каждый шкаф проходит заводские испытания и отгружается с паспортом изделия, схемой соединений, гарантийным талоном и сертификатом соответствия ЕАС."
                },
                {
                    "q": "Каковы сроки производства электрощитов ВРУ и ГРЩ?",
                    "a": "Сборка стандартных щитов занимает от 5 до 12 рабочих дней, сложных ГРЩ до 4000А с АВР — от 15 до 25 дней."
                }
            ],
            "problems": [
                {
                    "problem": "Претензии органов технадзора и энергонадзора к кустарной сборке щитов без маркировки, сертификатов и заводских паспортов.",
                    "solution": "Заводская сборка на собственном сертифицированном производстве по ГОСТ/МЭК с выдачей паспорта изделия и сертификатов соответствия Таможенного Союза.",
                    "benefit": "Беспрепятственная сдача объекта и подписание актов ввода в эксплуатацию с первого раза."
                },
                {
                    "problem": "Обесточивание критического оборудования (серверов, систем пожаротушения, лифтов) при аварии на главной линии.",
                    "solution": "Сборка шкафов АВР с логическим микропроцессорным контроллером и поддержкой автоматического пуска генератора.",
                    "benefit": "Бесшовное переключение на резервный ввод за 0.5–2 секунды без ущерба для бизнеса."
                },
                {
                    "problem": "Перегрев контактных групп, перекос фаз и риск пожара в щитовой из-за неправильного расчета сечений.",
                    "solution": "Точный расчет токов короткого замыкания, ошиновка электротехнической медью М1Т с тепловизионным контролем на стенде.",
                    "benefit": "Абсолютная пожаробезопасность электроустановки и безаварийная эксплуатация 15+ лет."
                }
            ]
        },
        "kz": {
            "title": "Электр шкафтары мен автоматтандыру қалқандарын (ЩА, ЩУ, ВРУ, ГРЩ) құрастыру",
            "description": "Алматыдағы жеке сертификатталған электрощит өндірісі: автоматтандыру шкафтары (ЩА), басқару қалқандары (ЩУ), бас тарату қалқандары (ГРЩ), кіріс-тарату құрылғылары (ВРУ) кез келген күрделіліктегі сызбалар бойынша.",
            "keywords": "электр шкафтарын құрастыру Алматы, автоматтандыру қалқандары Қазақстан, ВРУ ГРЩ жинау, электрощит өндірісі, тапсырыспен электр шкафтары, бірсызықты схема бойынша жинау, АВР генератор қалқаны, ВРУ ГРЩ паспорты, техқадағалау сертификаттары",
            "features": [
                "Алматы қаласындағы жеке өндірістік цех және сапа бақылауы",
                "Тапсырыс берушінің бюджетіне сай Schneider Electric, ABB, Chint жабдықтарымен жинау",
                "Толық құжаттама топтамасы: төлқұжаттар, электр сызбалары, сәйкестік сертификаттары",
                "Сымдар мен клеммаларды лазерлік таңбалау"
            ],
            "stages": [
                "Сызбалар мен техникалық тапсырманы талдау",
                "Шкафтың 3D орналасуын модельдеу және жабдықты монтаждау",
                "Сымдарды кәсіби тарту және таңбалау",
                "Оқшаулауды өлшеу және техникалық бақылаудан өткізу"
            ],
            "faqs": [
                {
                    "q": "Құрастыру мерзімі қандай?",
                    "a": "Жобаның күрделілігіне байланысты орта есеппен 5 күннен 20 күнге дейін созылады."
                },
                {
                    "q": "Қалқандарға ресми сертификат беріле ме?",
                    "a": "Иә, барлық қалқандар зауыттық сынақтан өтіп, ЕАС сәйкестік сертификатымен және паспортымен тапсырылады."
                }
            ],
            "problems": [
                {
                    "problem": "Техникалық қадағалаудың ретсіз жиналған қалқандарды қабылдамауы.",
                    "solution": "Зауыттық базада ГОСТ бойынша ресми сертификатпен жинау.",
                    "benefit": "Нысанды мемлекеттік органдарға бірінші реттен сәтті тапсыру."
                },
                {
                    "problem": "Электр қуаты сөнгенде нысанның жұмысы тоқтап қалуы.",
                    "solution": "Генераторды бірден іске қосатын сенімді АВР жүйесі.",
                    "benefit": "Нысанның үздіксіз 24/7 электрмен қамтылуы."
                }
            ]
        },
        "en": {
            "title": "Custom Electrical Enclosures, Control Panels & Switchgear Assembly in Kazakhstan",
            "description": "Professional electrical panel manufacturing in Almaty: assembly of custom automation panels (PLC cabinets), main distribution boards (MDB), low-voltage switchgear (LVSG), and motor control enclosures according to IEC and GOST standards.",
            "keywords": "electrical enclosure assembly Almaty, custom control panels Kazakhstan, switchgear manufacturing, MDB panel builder, PLC cabinet assembly, custom SLD switchboard, ATS generator panels, MDB switchgear passports, certified electrical panels Kazakhstan",
            "features": [
                "In-house certified panel building workshop in Almaty with multi-stage QC",
                "Components from Schneider Electric, ABB, Siemens, Chint tailored to client budget",
                "Complete documentation package: single-line diagrams, factory test certificates, user manuals",
                "Clear laser-printed heat-shrink wire labeling and ferruled connections"
            ],
            "stages": [
                "Customer electrical schematic review and engineering optimization",
                "Enclosure 3D internal layout and thermal dissipation verification",
                "Copper busbar fabrication and DIN-rail component assembly",
                "Wiring, harness binding, and point-to-point electrical testing",
                "Dielectric insulation resistance testing and factory acceptance protocol (FAT)"
            ],
            "faqs": [
                {
                    "q": "Do you build panels according to custom engineering schematics?",
                    "a": "Yes, we specialize in build-to-print panel assembly as well as full-cycle engineering from customer requirements."
                },
                {
                    "q": "Do your switchgear panels include test documentation and warranty?",
                    "a": "Yes, every panel is supplied with full factory test reports, SLDs, serial passports, and an official multi-year warranty."
                }
            ],
            "problems": [
                {
                    "problem": "Authority and building inspector rejection due to uncertified hand-wired switchboards.",
                    "solution": "Certified manufacturing with full compliance passports, calculation sheets, and single-line verification.",
                    "benefit": "Seamless regulatory handover and fast commissioning approval."
                },
                {
                    "problem": "Costly downtime during utility blackouts.",
                    "solution": "Intelligent ATS cabinets with sub-second dual-line transfer and automated diesel generator sequencing.",
                    "benefit": "Zero interruption to mission-critical business equipment."
                }
            ]
        },
        "knowsAbout": [
            {
                "name": "Electric switchboard",
                "sameAs": "https://www.wikidata.org/wiki/Q1141753"
            },
            {
                "name": "Distribution board",
                "sameAs": "https://www.wikidata.org/wiki/Q1411516"
            },
            {
                "name": "Automatic transfer switch",
                "sameAs": "https://www.wikidata.org/wiki/Q4826573"
            }
        ],
        "related_services": [
            "mcc-cabinets",
            "industrial-automation",
            "low-voltage-systems"
        ]
    },
    "industrial-automation": {
        "slug": "industrial-automation",
        "icon": "Factory",
        "badge": {
            "ru": "АСУ ТП & Заводы",
            "kz": "Өндіріс автоматтандыру",
            "en": "Industrial Automation"
        },
        "ru": {
            "title": "Индустриальная автоматизация и АСУ ТП в Алматы и Казахстане",
            "description": "Комплексная автоматизация технологических процессов (АСУ ТП), производственных линий, конвейеров, насосных и компрессорных станций. Программирование промышленных контроллеров (ПЛК / PLC), разработка диспетчерских SCADA-систем и HMI-панелей оператора.",
            "keywords": "индустриальная автоматизация Алматы, АСУ ТП Казахстан, промышленная автоматизация, программирование ПЛК Siemens, SCADA системы Казахстан, автоматизация производственных процессов, внедрение АСУТП, модернизация станков ПЛК, разработка SCADA систем, программирование Siemens Schneider ОВЕН, АСУ ТП цеха",
            "features": [
                "Программирование промышленных ПЛК: Siemens S7-1200/1500, Schneider Modicon, Omron, Delta",
                "Разработка интуитивно понятных SCADA-систем (WinCC, Ignition, Simple-Scada) и сенсорных HMI",
                "Снижение человеческого фактора, процента брака и простоев технологического оборудования",
                "Интеграция полевых приборов КИПиА: датчиков расхода, давления, температуры, уровня",
                "Построение защищенных промышленных сетей передачи данных Industrial Ethernet, Profinet"
            ],
            "stages": [
                "Предпроектное обследование технологического цикла предприятия",
                "Разработка технического проекта АСУ ТП, спецификации датчиков КИПиА и ПЛК",
                "Сборка шкафов управления АСУ ТП и шкафов сбора данных",
                "Написание программного обеспечения контроллеров и графического интерфейса SCADA",
                "Комплексная пусконаладка на объекте под нагрузкой и обучение операторов"
            ],
            "faqs": [
                {
                    "q": "Для каких отраслей промышленности вы внедряете АСУ ТП?",
                    "a": "Пищевая промышленность, производство стройматериалов, водоканалы и очистные сооружения, металлообработка, фармацевтика, склады и логистические хабы."
                },
                {
                    "q": "С какими промышленными контроллерами (ПЛК) вы работаете?",
                    "a": "Мы разрабатываем ПО для Siemens Simatic, Schneider Electric (Modicon), ОВЕН, Delta, Mitsubishi Electric, Wecon и других платформ."
                },
                {
                    "q": "Возможна ли поэтапная модернизация завода без полной остановки производства?",
                    "a": "Да, мы разрабатываем стратегию параллельной сборки и переключения узлов в технологические «окна» или межсменные интервалы, чтобы минимизировать простои."
                }
            ],
            "problems": [
                {
                    "problem": "Высокий процент брака и влияние человеческого фактора на качество выпускаемой продукции.",
                    "solution": "Внедрение автоматизированной системы управления (АСУ ТП) с точным соблюдением рецептур и технологических параметров.",
                    "benefit": "Снижение брака до нуля, рост производительности на 20–35% и стабильное качество каждой партии."
                },
                {
                    "problem": "Частые простои производственных линий из-за изношенной релейной автоматики и нехватки запчастей.",
                    "solution": "Реновация шкафов управления с установкой надежного ПЛК, сенсорной HMI панели и модулей удаленного ввода-вывода.",
                    "benefit": "Вторая жизнь оборудования с минимальными вложениями по сравнению с покупкой новой линии."
                },
                {
                    "problem": "Руководство не имеет объективных данных о реальной выработке, расходе сырья и причинах остановок цеха.",
                    "solution": "Разработка SCADA-системы с непрерывным сбором телеметрии, ведением журнала аварий и графиками трендов.",
                    "benefit": "Полная прозрачность технологического цикла и удаленный контроль со смартфона или ПК директора."
                }
            ]
        },
        "kz": {
            "title": "Өндірістік автоматтандыру және ТП ББЖ (АСУ ТП) Қазақстанда",
            "description": "Технологиялық процестерді, өндірістік желілерді, конвейерлер мен сорғы станцияларын кешенді автоматтандыру (АСУ ТП). Өндірістік контроллерлерді (ПЛК) бағдарламалау, диспетчерлік SCADA жүйелері мен оператор панельдерін әзірлеу.",
            "keywords": "өндірістік автоматтандыру Алматы, АСУ ТП Қазақстан, өнеркәсіптік автоматтандыру, ПЛК бағдарламалау, SCADA жүйелері, технологиялық процестерді басқару, станоктарды жаңғырту ПЛК, SCADA диспетчерлеу, өндірісті автоматтандыру, өндірістік желілер",
            "features": [
                "Siemens, Schneider Electric, Omron өндірістік контроллерлерін бағдарламалау",
                "Ыңғайлы SCADA жүйелері мен сенсорлық операторлық панельдерді (HMI) әзірлеу",
                "Өндірістік ақауларды және жабдықтың бос тұруын азайту",
                "КИПиА датчиктерін (қысым, температура, шығын) кешенді біріктіру"
            ],
            "stages": [
                "Өндірістік процесті алдын ала тексеру және ТТ құру",
                "АСУ ТП шкафтары мен контроллерлердің жобасын әзірлеу",
                "Басқару қалқандарын жинау және бағдарламалық қамтамасыз етуді жазу",
                "Жүктемемен сынау және қызметкерлерді оқыту"
            ],
            "faqs": [
                {
                    "q": "АСУ ТП өндіріске не береді?",
                    "a": "Өнім сапасын тұрақтандырады, адам қателігін жояды, өндіріс жылдамдығын арттырады және барлық көрсеткіштерді нақты уақытта жазып отырады."
                },
                {
                    "q": "Өндірісті тоқтатпай жаңғыртуға бола ма?",
                    "a": "Иә, біз жаңа шкафтарды алдын ала дайындап, ауыстыруды демалыс немесе техникалық үзілістер кезінде жүргіземіз."
                }
            ],
            "problems": [
                {
                    "problem": "Адам факторынан болатын өнім ақаулары мен өндірістің кідіруі.",
                    "solution": "Рецептураларды қатаң сақтайтын ПЛК негізіндегі ТП ББЖ жүйесін енгізу.",
                    "benefit": "Өнім шығару көлемін 20–35% арттыру және ақауларды жою."
                },
                {
                    "problem": "Ескірген жабдықтың жиі сынуы және бөлшектерінің табылмауы.",
                    "solution": "Заманауи сенсорлы HMI экраны бар жаңа басқару шкафтарына көшіру.",
                    "benefit": "Жаңа станок сатып алмай-ақ желінің сенімділігін қалпына келтіру."
                }
            ]
        },
        "en": {
            "title": "Industrial Automation, PLC Programming & SCADA Systems in Kazakhstan",
            "description": "End-to-end industrial automation and process control (I&C / SCADA): programmable logic controller (PLC) programming, human-machine interface (HMI) design, conveyor and pumping automation for manufacturing plants in Kazakhstan.",
            "keywords": "industrial automation Kazakhstan, PLC programming Almaty, SCADA systems Kazakhstan, Siemens PLC integrator, process automation, factory automation, PLC programming Siemens Schneider Owen, SCADA system development, factory machine retrofit, process automation",
            "features": [
                "PLC programming for Siemens Simatic S7, Schneider Modicon, Omron, Allen-Bradley",
                "Development of modern SCADA supervisory systems and operator touch panels (HMI)",
                "Full integration of industrial instrumentation (flowmeters, pressure transmitters, level sensors)",
                "Fail-safe industrial networking over Profinet, Modbus TCP, EtherNet/IP"
            ],
            "stages": [
                "Factory on-site process audit and user requirement specification (URS) drafting",
                "Control system architecture engineering, I/O assignment, and hardware selection",
                "Control panel manufacturing and software logic coding",
                "Commissioning, hot loop checks, and operator hands-on training"
            ],
            "faqs": [
                {
                    "q": "Which industries do you serve?",
                    "a": "Food & beverage processing, construction materials, municipal water & wastewater, packaging lines, and logistics hubs."
                },
                {
                    "q": "Can you modernize machinery without stopping ongoing plant operations?",
                    "a": "Yes, we build and test new control enclosures offsite and perform rapid cutovers during planned maintenance shifts."
                }
            ],
            "problems": [
                {
                    "problem": "High defect rates and inconsistent product quality caused by manual production processes.",
                    "solution": "Deploying turnkey PLC automation enforcing strict multi-stage recipe adherence and interlock safety.",
                    "benefit": "Defect reduction to near zero and overall throughput improvements of up to 35%."
                },
                {
                    "problem": "Recurring downtime due to unsupported legacy relay logic and obsolete spare parts.",
                    "solution": "Cabinet modernization with current-generation PLCs and color touch HMI displays.",
                    "benefit": "Restored equipment reliability without multi-million capital expenditures on new machinery."
                }
            ]
        },
        "knowsAbout": [
            {
                "name": "Industrial control system",
                "sameAs": "https://www.wikidata.org/wiki/Q211050"
            },
            {
                "name": "Programmable logic controller",
                "sameAs": "https://www.wikidata.org/wiki/Q173491"
            },
            {
                "name": "SCADA",
                "sameAs": "https://www.wikidata.org/wiki/Q211050"
            }
        ],
        "related_services": [
            "mcc-cabinets",
            "bms-dispatching",
            "system-integration"
        ]
    },
    "low-voltage-systems": {
        "slug": "low-voltage-systems",
        "icon": "Network",
        "badge": {
            "ru": "Слаботочка под ключ",
            "kz": "Төменгі ток желілері",
            "en": "Low-Voltage ELV"
        },
        "ru": {
            "title": "Проектирование и монтаж слаботочных систем в Алматы и Казахстане",
            "description": "Полный комплекс работ по слаботочным системам для коммерческих, общественных и жилых зданий: проектирование стадий П и Р, поставка сертифицированного оборудования, монтаж кабельных трасс, пусконаладка и сдача надзорным органам.",
            "keywords": "слаботочные системы Алматы, монтаж слаботочных систем Казахстан, проектирование слаботочных сетей, слаботочка под ключ, слаботочные работы генподрядчик Алматы, слаботочка под ключ Алматы, монтаж СКС СКУД видеонаблюдение, подрядчик слаботочных систем, оптоволокно ВОЛС",
            "features": [
                "Все слаботочные разделы из одних рук: СКС, СКУД, видеонаблюдение, АПС, СОУЭ, звук, ТВ",
                "Исключение межведомственных конфликтов монтажников и дублирующих кабельных трасс",
                "Строгое соответствие строительным нормам Республики Казахстан (СНиП РК)",
                "Использование сертифицированного кабеля пониженной пожароопасности (HF / LS)",
                "Исполнительная документация со схемами трасс, кабельными журналами и протоколами измерений"
            ],
            "stages": [
                "Изучение архитектурного проекта объекта и технического задания",
                "Разработка рабочей проектной документации и согласование",
                "Монтаж кабеленесущих систем (лотков, труб) и протяжка кабелей",
                "Установка оконечных устройств (камер, датчиков, панелей, динамиков)",
                "Индивидуальная пусконаладка подсистем, комплексные тесты и сдача объекта"
            ],
            "faqs": [
                {
                    "q": "Почему выгодно заказывать всю слаботочку у одного подрядчика?",
                    "a": "Единый подрядчик несет полную гарантийную ответственность, не перекладывает вину на смежников, оптимизирует кабельные трассы и экономит заказчику до 20% бюджета."
                },
                {
                    "q": "Какие слаботочные системы вы монтируете под ключ?",
                    "a": "Мы выполняем полный комплекс: СКС, ВОЛС, IP-видеонаблюдение, СКУД, адресную пожарную сигнализацию (АПС), систему оповещения и управления эвакуацией (СОУЭ), домофонию и фоновый звук."
                },
                {
                    "q": "Предоставляете ли вы исполнительную документацию для технадзора и ДЧС?",
                    "a": "Да, мы оформляем полный комплект исполнительных чертежей, кабельных журналов, актов скрытых работ и протоколов замеров изоляции."
                }
            ],
            "problems": [
                {
                    "problem": "Несколько разных субподрядчиков по интернету, камерам, пожарке и СКУД срывают сроки и перекладывают вину друг на друга.",
                    "solution": "Комплексный слаботочный подряд от INPAR: проектирование, кабельные трассы, серверные и пусконаладка в одних руках.",
                    "benefit": "Сдача объекта строго в срок, сокращение сметы за счет оптимизации трасс и единая гарантия на все системы."
                },
                {
                    "problem": "Падение скорости интернета, обрывы связи и хаос в кроссовых шкафах из-за неквалифицированной прокладки кабелей.",
                    "solution": "Монтаж сертифицированной СКС с маркировкой каждого порта и проверкой приборами Fluke Networks.",
                    "benefit": "Стабильная гигабитная сеть без скрытых затуханий и аккуратная серверная комната."
                },
                {
                    "problem": "Несанкционированный доступ посторонних лиц и отсутствие дисциплины учета рабочего времени сотрудников.",
                    "solution": "Внедрение сетевого СКУД с Face-ID терминалами, шлюзовыми турникетами и отчетами опозданий в 1С.",
                    "benefit": "Полная безопасность объекта и прозрачная трудовая дисциплина персонала."
                }
            ]
        },
        "kz": {
            "title": "Төменгі ток жүйелерін жобалау және монтаждау кілтке дейін",
            "description": "Коммерциялық, қоғамдық және тұрғын үй ғимараттарына арналған төменгі ток (әлсіз ток) жүйелерінің толық кешені: жобалау, жабдық жеткізу, монтаж, баптау және мемлекеттік комиссияға тапсыру.",
            "keywords": "төменгі ток жүйелері Алматы, әлсіз ток монтажы Қазақстан, слаботочка кілтке дейін, слаботочные сети, слаботочка кілтке дейін, әлсіз токты желілер монтаж, СКС кабель тарту, СКУД турникет Face-ID",
            "features": [
                "Бір қолдан барлық бөлімдер: СКС, СКУД, бейнебақылау, өрт дабылы, дыбыс, ТВ",
                "Қазақстанның құрылыс нормалары мен ережелеріне (ҚР ҚНжЕ) толық сәйкестік",
                "Өртке қауіпсіз жоғары сапалы сертификатталған кабельдерді қолдану",
                "Кешенді кепілдік және техникалық қызмет көрсету"
            ],
            "stages": [
                "Сәулет жобасын және техникалық талаптарды қарастыру",
                "Жұмыс құжаттамасын әзірлеу",
                "Кабель науаларын орнату және сым тарту",
                "Аспаптарды орнату және жүйені іске қосу"
            ],
            "faqs": [
                {
                    "q": "Қандай кепілдік беріледі?",
                    "a": "Монтаждау жұмыстарына және жабдықтарға 12 айдан бастап ресми кепілдік ұсынылады."
                },
                {
                    "q": "Қандай нысандармен жұмыс істейсіздер?",
                    "a": "Кеңселер, қоймалар, логистикалық орталықтар, бизнес-орталықтар, зауыттар мен көпқабатты тұрғын үй кешендері."
                }
            ],
            "problems": [
                {
                    "problem": "Әртүрлі мердігерлердің келіспеушілігі салдарынан нысанның кешігуі.",
                    "solution": "INPAR компаниясынан бірыңғай кілтке дейін кешенді монтаж.",
                    "benefit": "Нысанды уақытында тапсыру, кабелдік трассаларды оңтайландыру және бірыңғай кепілдік."
                },
                {
                    "problem": "Сервердегі ретсіздік және интернеттің баяу жұмыс істеуі.",
                    "solution": "Кәсіби СКС құру және әрбір портты таңбалау.",
                    "benefit": "Жоғары жылдамдықты сенімді байланыс."
                }
            ]
        },
        "en": {
            "title": "Turnkey Extra Low Voltage (ELV) Systems Engineering & Installation in Kazakhstan",
            "description": "Full lifecycle engineering and contracting of Extra Low Voltage (ELV) systems for commercial towers, hotels, malls, and residential complexes: structured cabling, CCTV, access control, fire alarm, and public address.",
            "keywords": "low voltage systems Almaty, ELV contractor Kazakhstan, structured cabling, access control CCTV, extra low voltage engineering, turnkey ELV contractor, structured cabling installation, access control CCTV integration, commercial low voltage",
            "features": [
                "All ELV packages from a single source: SCS, CCTV, ACS, Fire Alarm, PA/VA, IPTV",
                "Zero inter-subcontractor finger-pointing and optimized shared cable pathways",
                "Full compliance with Kazakhstan building codes and international IEEE/TIA standards",
                "Comprehensive as-built drawings, testing reports, and warranty support"
            ],
            "stages": [
                "Architectural drawing review and scope of work definition",
                "Detailed engineering design (schematics, cable schedules, riser diagrams)",
                "Cable containment and wire pulling works",
                "Field device termination, subsystem testing, and handover"
            ],
            "faqs": [
                {
                    "q": "Why choose a master ELV contractor?",
                    "a": "Having one responsible integrator ensures streamlined coordination, no duplicative labor, and lower total project cost."
                },
                {
                    "q": "Do you provide as-built documentation for building commissioning authorities?",
                    "a": "Yes, we produce complete as-built CAD drawings, cable schedules, Fluke test certificates, and compliance declarations."
                }
            ],
            "problems": [
                {
                    "problem": "Coordination disputes and delays caused by juggling separate contractors for cameras, internet, and alarms.",
                    "solution": "All-in-one integrated ELV engineering by INPAR with consolidated cable pathways and single-point responsibility.",
                    "benefit": "On-time project delivery, clean architecture, and unified long-term warranty."
                },
                {
                    "problem": "Network bottlenecks and messy telecom racks causing continuous business downtime.",
                    "solution": "Certified structured cabling with laser port tagging and Fluke Networks certification.",
                    "benefit": "Flawless gigabit speeds, zero packet drop, and orderly patch distribution."
                }
            ]
        },
        "knowsAbout": [
            {
                "name": "Extra-low voltage",
                "sameAs": "https://www.wikidata.org/wiki/Q1255858"
            },
            {
                "name": "Structured cabling",
                "sameAs": "https://www.wikidata.org/wiki/Q1363294"
            },
            {
                "name": "Access control",
                "sameAs": "https://www.wikidata.org/wiki/Q13410526"
            },
            {
                "name": "Fire alarm system",
                "sameAs": "https://www.wikidata.org/wiki/Q1365389"
            }
        ],
        "related_services": [
            "cctv-access-control",
            "networks-smatv",
            "fire-safety"
        ]
    },
    "smart-home-knx": {
        "slug": "smart-home-knx",
        "icon": "Home",
        "badge": {
            "ru": "KNX Умный дом",
            "kz": "KNX Ақылды үй",
            "en": "Smart Home KNX"
        },
        "ru": {
            "title": "Умный дом стандарта KNX/EIB под ключ в Алматы и Казахстане",
            "description": "Проектирование и реализация премиальных систем «Умный дом» мирового стандарта KNX. Комплексное управление освещением, моторизованными шторами, климатом (HVAC), мультирум и безопасностью с единого приложения и дизайнерских панелей.",
            "keywords": "умный дом Алматы, KNX Казахстан, автоматизация коттеджей, управление климатом умный дом, дизайнерские выключатели KNX, умный дом под ключ, KNX интегратор, умный дом проводной knx, выключатели knx Zennio Jung ABB, сценарии умный дом, управление светом DALI",
            "features": [
                "Децентрализованный европейский стандарт KNX — надежность на десятилетия вперед",
                "Согласованная работа отопления, теплого пола, кондиционеров и вентиляции без конфликтов",
                "Индивидуальные световые сценарии и плавное цифровое диммирование DALI-2",
                "Интеграция с Apple HomeKit, Яндекс Алиса, Google Home и смартфонами",
                "Премиальные дизайнерские выключатели из стекла, металла, латуни и натурального дерева"
            ],
            "stages": [
                "Создание сценариев жизни и технического задания под привычки семьи",
                "Разработка кабельного журнала, проекта щита автоматизации KNX и спецификации",
                "Прокладка экранированного кабеля KNX на этапе черновых работ",
                "Сборка щита автоматики, установка приводов, датчиков и чистовых панелей",
                "Программирование в среде ETS, настройка графики и сдача проекта"
            ],
            "faqs": [
                {
                    "q": "В чем отличие стандарта KNX от беспроводных умных домов?",
                    "a": "KNX — это промышленный проводной стандарт, работающий децентрализованно без единой точки отказа, без зависимости от интернета и облачных серверов с гарантированным сроком службы более 25 лет."
                },
                {
                    "q": "Почему для коттеджа или большой квартиры выбирают проводной KNX, а не беспроводные системы?",
                    "a": "KNX — это промышленный европейский стандарт с децентрализованной шиной: если откажет один прибор, остальные продолжат работать. Он не забивает Wi-Fi эфир, не зависит от облачных серверов и работает стабильно десятилетиями."
                },
                {
                    "q": "Можно ли управлять умным домом KNX с iPhone через приложение 'Дом' (Apple HomeKit)?",
                    "a": "Да, мы устанавливаем сертифицированные шлюзы, позволяющие управлять светом, шторами, сценариями и климатом через Apple HomeKit, Siri, Google Assistant и Яндекс Алису."
                }
            ],
            "problems": [
                {
                    "problem": "Беспроводные системы (Wi-Fi, Zigbee, Tuya) постоянно зависают, теряют датчики и зависят от китайских облаков.",
                    "solution": "Проводная шинная система KNX с децентрализованной логикой европейских брендов (ABB, Jung, Zennio, Schneider).",
                    "benefit": "Безупречная работа более 20 лет без сбоев, полная автономность и независимость от интернета."
                },
                {
                    "problem": "Стена из десятка разномастных выключателей, термостатов и пультов кондиционеров, портящих дизайнерский интерьер.",
                    "solution": "Замена всего ряда термостатов и пультов на единый дизайнерский сенсорный выключатель KNX с дисплеем.",
                    "benefit": "Элегантная минималистичная эстетика интерьера и интуитивное управление всеми функциями комнаты с одной панели."
                },
                {
                    "problem": "Опасения протечки воды, забытого утюга или оставленного освещения при отъезде из дома.",
                    "solution": "Сценарий 'Я ушел': отключение всех некритичных потребителей в одно касание и автоматическое перекрытие кранов при аварии.",
                    "benefit": "100% уверенность в безопасности жилья и предотвращение ущерба от затопления."
                }
            ]
        },
        "kz": {
            "title": "KNX/EIB стандартындағы Ақылды үй (Smart Home) кілтке дейін",
            "description": "Халықаралық KNX стандарты бойынша пәтерлер мен коттедждерге арналған премиум «Ақылды үй» жүйелерін жобалау және енгізу. Жарықтандыруды, перделерді, климатты және қауіпсіздікті смартфоннан және дизайнерлік панельдерден басқару.",
            "keywords": "ақылды үй Алматы, KNX Қазақстан, коттедж автоматтандыру, жарықты басқару, ақылды үй кілтке дейін, smart home, сымды KNX ақылды үй, DALI жарық басқару, ақылды үй сценарийлері, коттеджге ақылды үй бағасы",
            "features": [
                "Халықаралық KNX стандарты — сервелерге тәуелсіз жоғары сенімділік",
                "Жылыту, еден жылыту және кондиционерлеу жүйелерінің келісілген жұмысы",
                "Apple HomeKit, Алиса және смартфондар арқылы оңай басқару",
                "Эксклюзивті дизайнерлік пернетақталар мен сенсорлық экрандар"
            ],
            "stages": [
                "Тұрғындардың қалауы бойынша сценарийлер әзірлеу",
                "KNX инженерлік жобасын дайындау",
                "Қара жұмыс кезеңінде KNX кабелін тарту",
                "Щитті құрастыру және панельдерді бағдарламалау"
            ],
            "faqs": [
                {
                    "q": "Жобалауды қашан бастаған дұрыс?",
                    "a": "Дизайн-жоба дайындау кезеңінде, электр сымдарын тарту басталғанға дейін кіріскен абзал."
                },
                {
                    "q": "KNX Ақылды үйінің қарапайым жүйелерден айырмашылығы неде?",
                    "a": "Бұл еуропалық өндірістік стандарт. Ол интернетке немесе орталық серверге тәуелді емес, сондықтан ешқашан ілінбейді және өте ұзақ қызмет етеді."
                }
            ],
            "problems": [
                {
                    "problem": "Сымсыз құрылғылардың үнемі байланысты жоғалтуы және батареяларын ауыстыру әбігері.",
                    "solution": "Сенімді сымды KNX шинасы (ABB, Zennio, Jung еуропалық брендтері).",
                    "benefit": "Батареясыз, байланыс үзілмейтін ондаған жылдар бойғы тұрақты жұмыс."
                },
                {
                    "problem": "Қабырғадағы көптеген бөлек термостаттар мен қосқыштардың интерьерді бұзуы.",
                    "solution": "Барлық функцияларды бір стильді KNX шыны сенсорлы панеліне біріктіру.",
                    "benefit": "Премиум дизайн және үйді бір түймемен ыңғайлы басқару."
                }
            ]
        },
        "en": {
            "title": "KNX/EIB Certified Smart Home Automation in Kazakhstan",
            "description": "Bespoke smart residence automation built on the world-renowned KNX/EIB standard in Almaty and Astana. Seamless control of lighting, DALI dimming, motorized shading, HVAC climate, and multiroom audio via bespoke keypads and mobile apps.",
            "keywords": "smart home Almaty, KNX automation Kazakhstan, luxury residence automation, HVAC climate control KNX, architectural keypads, hardwired KNX automation, DALI-2 architectural lighting, Apple HomeKit KNX, luxury smart home Kazakhstan",
            "features": [
                "Decentralized global KNX standard backed by 500+ premium European manufacturers",
                "Coordinated HVAC control: underfloor heating, AC, and fresh air ventilation",
                "Native voice and mobile integration: Apple HomeKit, Google Home, touchscreens",
                "Luxury architectural switches crafted in solid brass, glass, aluminum, and leather"
            ],
            "stages": [
                "Lifestyle scenario design and technical specification drafting",
                "KNX engineering blueprint, cable routing, and enclosure schematics",
                "First-fix shielded green KNX bus cabling installation",
                "Panel fabrication, actuator wiring, and keypad fitting",
                "ETS software programming, custom visualization layout, and handover"
            ],
            "faqs": [
                {
                    "q": "Why choose KNX over wireless smart home devices?",
                    "a": "KNX is an industrial-grade wired protocol with zero reliance on cloud servers or Wi-Fi, offering a 25+ year lifespan and rock-solid stability."
                },
                {
                    "q": "Can I control my KNX home using Apple HomeKit and Siri?",
                    "a": "Yes, we integrate certified bidirectional bridges allowing native control via Apple HomeKit, Siri voice commands, and Apple Watch widgets."
                }
            ],
            "problems": [
                {
                    "problem": "Flimsy consumer wireless smart home gear (Wi-Fi/Zigbee) crashing, losing connectivity, and depending on foreign cloud servers.",
                    "solution": "Industrial-grade hardwired KNX bus topology utilizing decentralized hardware from premier European manufacturers (ABB, Jung, Zennio).",
                    "benefit": "Decades of bulletproof operational stability, complete privacy, and zero Wi-Fi network congestion."
                },
                {
                    "problem": "Cluttered wall surfaces packed with competing thermostats, AC controllers, and light switches.",
                    "solution": "Consolidating all functions into a single architectural glass KNX keypad featuring integrated temperature sensing.",
                    "benefit": "Uncluttered, elegant interior aesthetics and intuitive room control."
                }
            ]
        },
        "knowsAbout": [
            {
                "name": "KNX (standard)",
                "sameAs": "https://www.wikidata.org/wiki/Q1889"
            },
            {
                "name": "Home automation",
                "sameAs": "https://www.wikidata.org/wiki/Q2818960"
            },
            {
                "name": "Lighting control system",
                "sameAs": "https://www.wikidata.org/wiki/Q1842844"
            }
        ],
        "related_services": [
            "bms-dispatching",
            "electrical-cabinets",
            "sound-and-light"
        ]
    },
    "bms-dispatching": {
        "slug": "bms-dispatching",
        "icon": "Building2",
        "badge": {
            "ru": "BMS Диспетчеризация",
            "kz": "BMS Диспетчерлеу",
            "en": "BMS Dispatching"
        },
        "ru": {
            "title": "Диспетчеризация BMS и автоматизация зданий в Алматы",
            "description": "Комплексное управление инженерными системами зданий в Казахстане. Интеграция вентиляции, отопления, кондиционирования, освещения и энергоучета в единую платформу с веб-интерфейсом для снижения энергопотребления до 30%.",
            "keywords": "диспетчеризация BMS Алматы, автоматизация зданий Казахстан, BMS системы, энергоэффективность зданий, автоматизация ОВиК, SCADA диспетчеризация, диспетчеризация зданий BMS, автоматизация ИТП котельных, протоколы BACnet Modbus, энергосбережение зданий",
            "features": [
                "Единая цифровая панель мониторинга всех инженерных узлов объекта в режиме 24/7",
                "Снижение затрат на электроэнергию и отопление на 15–30% благодаря умным расписаниям",
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
                    "q": "Можно ли подключить к BMS оборудование разных производителей?",
                    "a": "Да, BMS строится на открытых международных протоколах BACnet, Modbus, KNX, что позволяет объединить приточки одного бренда, чиллеры другого и насосы третьего в единую систему."
                }
            ],
            "problems": [
                {
                    "problem": "Инженерная служба не знает о поломке насоса, разморозке калорифера или утечке воды до жалоб арендаторов.",
                    "solution": "Централизованная система диспетчеризации BMS с непрерывным опросом датчиков и мгновенными тревогами в Telegram дежурного инженера.",
                    "benefit": "Локализация и устранение инцидентов за минуты до причинения материального ущерба."
                },
                {
                    "problem": "Огромные коммунальные счета за отопление и электричество из-за круглосуточной работы инженерных систем на полную мощность.",
                    "solution": "Внедрение автоматических расписаний работы климата и освещения (будни/выходные, рабочие/нерабочие часы).",
                    "benefit": "Снижение расходов на энергоресурсы коммерческого здания на 20–30% ежегодно."
                }
            ]
        },
        "kz": {
            "title": "BMS диспетчерлеу және ғимараттарды автоматтандыру",
            "description": "Қазақстан бойынша ғимараттардың инженерлік жүйелерін кешенді басқару. Энергия тұтынуды 30%-ға дейін азайту үшін желдету, жылыту, кондиционерлеу және жарықты бірыңғай веб-интерфейсі бар платформаға біріктіру.",
            "keywords": "BMS диспетчерлеу Алматы, ғимараттарды автоматтандыру, BMS жүйелері Қазақстан, энергия үнемдеу, BMS жүйелері Алматы, ғимаратты диспетчерлеу, BACnet Modbus хаттамалары, энергия үнемдеу",
            "features": [
                "24/7 режимінде барлық инженерлік түйіндерді бақылаудың бірыңғай цифрлық панелі",
                "Ақылды кестелер арқылы электр және жылу шығындарын 15–30%-ға үнемдеу",
                "Апаттық жағдайлар туралы Telegram / SMS арқылы жедел хабарлау"
            ],
            "stages": [
                "Нысанның инженерлік желілерін тексеру",
                "Автоматика шкафтарын жобалау",
                "Қалқандарды жинау және контроллерлерді бағдарламалау",
                "Іске қосу және пайдалану қызметін оқыту"
            ],
            "faqs": [
                {
                    "q": "BMS қанша уақытта өтеледі?",
                    "a": "Орта есеппен энергия үнемдеу арқылы 1.5–3 жыл аралығында өтеледі."
                },
                {
                    "q": "BMS жүйесі қандай үнем береді?",
                    "a": "Жылыту мен электр қуатын тек қажет уақытта тұтыну арқылы коммуналдық шығындарды 20-30% төмендетеді."
                }
            ],
            "problems": [
                {
                    "problem": "Апат болған кезде инженерлердің кеш хабардар болуы.",
                    "solution": "Диспетчерлік мониторинг және Telegram арқылы лезде ескерту.",
                    "benefit": "Апаттарды алғашқы минуттарда жедел жою."
                }
            ]
        },
        "en": {
            "title": "Building Management Systems (BMS) & Dispatching in Kazakhstan",
            "description": "Integrated building automation and energy management systems (BMS) in Kazakhstan. Centralized supervision of HVAC, electrical distribution, lighting, and metering to trim operating costs by up to 30%.",
            "keywords": "BMS system Almaty, building management system Kazakhstan, HVAC automation, smart building dispatching, BMS dispatching Kazakhstan, BACnet IP Modbus supervisory, building energy optimization, central plant monitoring",
            "features": [
                "24/7 centralized monitoring dashboard for all mechanical and electrical infrastructure",
                "15–30% measurable energy savings using occupancy schedules and enthalpy economizers",
                "Instant emergency alarming to mobile devices and facility maintenance teams"
            ],
            "stages": [
                "Building MEP systems audit and design specifications",
                "Control panel schematics and BACnet network architecture",
                "Panel fabrication and field controller deployment",
                "Software commissioning, sensor calibration, and facility staff training"
            ],
            "faqs": [
                {
                    "q": "What is the ROI of a commercial BMS?",
                    "a": "Typically 1.5 to 3 years through utility savings and prolonged mechanical equipment lifespan."
                },
                {
                    "q": "Can legacy chillers and third-party panels be bridged into the BMS?",
                    "a": "Yes, we integrate open standard protocol gateways (BACnet, Modbus, SNMP) to bring multi-vendor hardware into a unified operator workstation."
                }
            ],
            "problems": [
                {
                    "problem": "Facility teams unaware of equipment failures until tenant comfort complaints escalate.",
                    "solution": "Continuous automated BMS telemetry streaming telemetry and instantaneous engineer notification.",
                    "benefit": "Proactive resolution of equipment malfunctions before tenant impact or structural damage occurs."
                }
            ]
        },
        "knowsAbout": [
            {
                "name": "Building management system",
                "sameAs": "https://www.wikidata.org/wiki/Q629239"
            },
            {
                "name": "BACnet",
                "sameAs": "https://www.wikidata.org/wiki/Q795493"
            },
            {
                "name": "Modbus",
                "sameAs": "https://www.wikidata.org/wiki/Q1130095"
            }
        ],
        "related_services": [
            "ddc-automation",
            "mcc-cabinets",
            "system-integration"
        ]
    },
    "fire-safety": {
        "slug": "fire-safety",
        "icon": "ShieldAlert",
        "badge": {
            "ru": "Пожарная безопасность",
            "kz": "Өрт қауіпсіздігі",
            "en": "Fire Safety"
        },
        "ru": {
            "title": "Пожарная безопасность и системы оповещения (АПС и СОУЭ) в Алматы",
            "description": "Проектирование, поставка и сертифицированный монтаж адресной пожарной сигнализации (АПС), систем оповещения и управления эвакуацией (СОУЭ) 1-5 типов под ключ по нормам Республики Казахстан.",
            "keywords": "пожарная сигнализация Алматы, монтаж АПС СОУЭ, адресная пожарная сигнализация, системы оповещения при пожаре, пожаротушение Казахстан, сдача АПС в ДЧС, монтаж пожарной сигнализации, речевое оповещение СОУЭ 1-5 типов, обслуживание пожарки",
            "features": [
                "Адресные пожарные панели с точным определением места задымления",
                "Цифровые системы оповещения и трансляции звука (СОУЭ 1-5 типов)",
                "Интеграция с СКУД, лифтами, вентиляцией и клапанами ОЗК",
                "Полное соответствие СНиП и противопожарным нормам РК"
            ],
            "stages": [
                "Разработка проектно-сметной документации (стадии П и Р)",
                "Прокладка огнестойких кабельных линий и монтаж извещателей",
                "Установка приборов управления и настройка сценариев эвакуации",
                "Комплексные испытания и сдача объекта пожарной инспекции"
            ],
            "faqs": [
                {
                    "q": "Предоставляете ли вы гарантию и ТО?",
                    "a": "Да, мы предоставляем официальную гарантию и заключаем договоры на ежемесячное регламентное ТО."
                },
                {
                    "q": "Имеет ли ваша компания лицензию на монтаж пожарной сигнализации?",
                    "a": "Да, у нас есть все государственные лицензии и квалифицированные специалисты для проектирования, монтажа и обслуживания систем пожарной безопасности в РК."
                }
            ],
            "problems": [
                {
                    "problem": "Риск штрафов, приостановки деятельности объекта или отказа ввода в эксплуатацию инспекцией ДЧС.",
                    "solution": "Лицензированный монтаж сертифицированного оборудования строго по СН РК с полным пакетом исполнительных актов.",
                    "benefit": "Безупречная приемка объекта инспекцией пожарного надзора с первого раза."
                }
            ]
        },
        "kz": {
            "title": "Өрт қауіпсіздігі және хабарландыру жүйелері (АПС және СОУЭ)",
            "description": "Қазақстан Республикасының нормаларына сәйкес адрестік өрт дабылын (АПС), 1-5 үлгідегі хабарландыру және эвакуацияны басқару жүйелерін (СОУЭ) жобалау және орнату.",
            "keywords": "өрт дабылы Алматы, өрт қауіпсіздігі жүйелері, СОУЭ монтаждау, дабыл жүйелері, өрт дабылын монтаждау, ТЖД тапсыру, СОУЭ құлақтандыру жүйесі, өрт қауіпсіздігі лицензия",
            "features": [
                "Түтін шыққан орынды дәл анықтайтын адрестік өрт панельдері",
                "Эвакуацияны дауыспен басқару және хабарландыру жүйелері",
                "Өрт инспекциясына нысанды еш қиындықсыз тапсыру"
            ],
            "stages": [
                "Жобалау және сметаны есептеу",
                "Өртке төзімді кабельдер мен датчиктерді орнату",
                "Іске қосу және сынақтар жүргізу"
            ],
            "faqs": [
                {
                    "q": "Қызмет көрсету шарты жасала ма?",
                    "a": "Иә, өрт жүйелеріне ай сайынғы регламенттік техникалық қызмет көрсету шартын жасаймыз."
                },
                {
                    "q": "Құжаттарды ТЖД-ға тапсыруға көмектесесіздер ме?",
                    "a": "Иә, толық атқарушылық сызбалар мен актілерді дайындап, инспекцияның қабылдауына дейін сүйемелдейміз."
                }
            ],
            "problems": [
                {
                    "problem": "ТЖД инспекциясының айыппұл салу немесе нысанды қабылдамау қаупі.",
                    "solution": "ҚР нормаларына сай ресми лицензиямен сапалы монтаждау.",
                    "benefit": "Нысанды өрт қауіпсіздігі органдарына кедергісіз тапсыру."
                }
            ]
        },
        "en": {
            "title": "Fire Alarm & Emergency Evacuation Systems (PA/VA) in Kazakhstan",
            "description": "Certified design, equipment supply, and turnkey installation of addressable fire detection, alarm, and Public Address / Voice Alarm (PA/VA) evacuation systems in Kazakhstan.",
            "keywords": "fire alarm system Almaty, voice evacuation Kazakhstan, addressable fire detection, fire safety engineering, fire alarm certification Kazakhstan, emergency voice evacuation PAVA, addressable fire detection, life safety",
            "features": [
                "Intelligent addressable fire alarm control panels with pinpoint detector location",
                "Multi-zone digital voice alarm and public address (PA/VA) systems",
                "Automated interlocks with access control, elevators, and smoke extraction dampers"
            ],
            "stages": [
                "Detailed engineering drawings according to local safety codes",
                "Fire-resistant cabling and device installation",
                "Integrated cause-and-effect matrix testing and authority sign-off"
            ],
            "faqs": [
                {
                    "q": "Do you provide regulatory compliance documentation?",
                    "a": "Yes, all our fire engineering projects are certified to pass official emergency management inspections."
                },
                {
                    "q": "Do you hold state licenses for fire safety engineering?",
                    "a": "Yes, INPAR holds all required state certifications and licensing for fire safety and emergency evacuation engineering in Kazakhstan."
                }
            ],
            "problems": [
                {
                    "problem": "Risk of regulatory shutdown and failure to pass mandatory state fire safety inspections.",
                    "solution": "Turnkey licensed installation of certified fire equipment with comprehensive testing protocols.",
                    "benefit": "Guaranteed first-time inspection acceptance by emergency authorities."
                }
            ]
        },
        "knowsAbout": [
            {
                "name": "Fire alarm system",
                "sameAs": "https://www.wikidata.org/wiki/Q1365389"
            },
            {
                "name": "Smoke detector",
                "sameAs": "https://www.wikidata.org/wiki/Q189578"
            }
        ],
        "related_services": [
            "low-voltage-systems",
            "sound-and-light",
            "bms-dispatching"
        ]
    },
    "cctv-access-control": {
        "slug": "cctv-access-control",
        "icon": "Cctv",
        "badge": {
            "ru": "СКУД & CCTV",
            "kz": "Бейне & СКУД",
            "en": "CCTV & Access Control"
        },
        "ru": {
            "title": "Видеонаблюдение и контроль доступа (СКУД, NVR, Биометрия) в Алматы",
            "description": "Интеллектуальные системы IP-видеонаблюдения, распознавание лиц и номеров авто, биометрический контроль доступа (СКУД, Face ID), турникеты и учет рабочего времени для предприятий и офисов.",
            "keywords": "видеонаблюдение Алматы, установка СКУД Казахстан, распознавание лиц, IP камеры, турникеты, учет рабочего времени, NVR системы, СКУД турникеты Face-ID, видеонаблюдение для склада, распознавание автономеров шлагбаум, учет рабочего времени 1С",
            "features": [
                "IP-камеры с ИИ-аналитикой (распознавание лиц, номеров, периметральная охрана)",
                "Биометрические терминалы Face ID, RFID и мобильный доступ по смартфону",
                "Интеграция с 1С для автоматического табеля учета рабочего времени",
                "Удаленный защищенный доступ к живому видео и архиву 24/7"
            ],
            "stages": [
                "Аудит объекта и расчет углов обзора камер",
                "Подбор камер, серверов NVR и контроллеров доступа",
                "Монтаж кабельных трасс, камер и турникетов",
                "Настройка аналитики и прав доступа персонала"
            ],
            "faqs": [
                {
                    "q": "Сколько дней хранится архив видео?",
                    "a": "Глубина архива рассчитывается под ваши задачи — от 14 до 90+ дней постоянной записи."
                },
                {
                    "q": "Какое оборудование вы используете для видеонаблюдения и СКУД?",
                    "a": "Мы работаем с официальными поставщиками Dahua, Hikvision, Sigur, Perco, Came, Uniview и предоставляем заводскую гарантию."
                }
            ],
            "problems": [
                {
                    "problem": "Хищения на складе или в торговом зале из-за 'слепых зон' и плохого качества старых аналоговых камер.",
                    "solution": "Установка профессиональных IP-камер 4K с ультрашироким углом обзора, WDR и ночной цветной подсветкой (ColorVu/FullColor).",
                    "benefit": "100% покрытие территории и детализированное видео лиц и номеров даже в полной темноте."
                }
            ]
        },
        "kz": {
            "title": "Бейнебақылау және қолжетімділікті басқару (СКУД, NVR, Биометрия)",
            "description": "IP-бейнебақылау, бет-әлпетті және көлік нөмірлерін тану, Face ID биометриялық рұқсат бақылауы, турникеттер және жұмыс уақытын есепке алу жүйелері.",
            "keywords": "бейнебақылау Алматы, СКУД орнату Қазақстан, Face ID турникеттер, камералар монтажы, СКУД Face-ID орнату, көлік нөмірін танитын шлагбаум, бейнебақылау камералары 4K, қойма күзеті",
            "features": [
                "Жасанды интеллектісі бар смарт IP-камералар",
                "Face ID және биометриялық рұқсат терминалдары",
                "Жұмыс уақытын автоматты есепке алу (1С-пен интеграция)"
            ],
            "stages": [
                "Нысанды зерттеу және камералар санын анықтау",
                "Кабель тарту және жабдықты орнату",
                "Серверлерді және бағдарламаны баптау"
            ],
            "faqs": [
                {
                    "q": "Қараңғыда түсіре ме?",
                    "a": "Иә, заманауи камералар инфрақызыл жарықпен және түнгі түсті көру технологиясымен жабдықталған."
                },
                {
                    "q": "Камераларға кепілдік беріле ме?",
                    "a": "Иә, біз орнататын барлық ресми жабдықтарға 1 жылдан 3 жылға дейін кепілдік және сервистік қолдау ұсынамыз."
                }
            ],
            "problems": [
                {
                    "problem": "Ескі камералардың сапасыздығынан түнде адамдар мен көлік нөмірлерінің көрінбеуі.",
                    "solution": "Түнгі түрлі-түсті көру жүйесі бар заманауи 4K IP-камераларды орнату.",
                    "benefit": "Нысанның тәулік бойы толық қауіпсіздігі."
                }
            ]
        },
        "en": {
            "title": "CCTV Video Surveillance & Biometric Access Control in Kazakhstan",
            "description": "Enterprise-grade IP video surveillance with AI video analytics, Face ID access control, automated turnstiles, and time-and-attendance management across Kazakhstan.",
            "keywords": "CCTV installation Almaty, access control systems Kazakhstan, Face ID turnstiles, biometric security, Face-ID turnstile access control, commercial 4K CCTV, LPR license plate barrier, HR time tracking integration",
            "features": [
                "High-definition IP cameras with edge AI (facial and license plate recognition)",
                "Contactless Face ID terminals and mobile Bluetooth/NFC credentials",
                "Automated time-tracking integration with corporate ERP and HR systems"
            ],
            "stages": [
                "Site survey and optical field-of-view modeling",
                "Network switch and storage server dimensioning",
                "Field cabling, camera mounting, and barrier installation",
                "User credential enrollment and security operator training"
            ],
            "faqs": [
                {
                    "q": "Can video be accessed remotely?",
                    "a": "Yes, securely via encrypted cloud mobile apps or central management desktop software."
                },
                {
                    "q": "What equipment manufacturers do you install?",
                    "a": "We install enterprise-grade platforms from Dahua, Hikvision, Sigur, Perco, Came, and Uniview with manufacturer warranties."
                }
            ],
            "problems": [
                {
                    "problem": "Stock theft or unauthorized perimeter intrusions masked by blurry analog footage and coverage blind spots.",
                    "solution": "Deploying commercial 4K ultra-wide IP cameras with advanced true WDR and low-light color imaging.",
                    "benefit": "Crystal-clear evidential identification of faces and vehicle plates day and night."
                }
            ]
        },
        "knowsAbout": [
            {
                "name": "Closed-circuit television",
                "sameAs": "https://www.wikidata.org/wiki/Q215705"
            },
            {
                "name": "Biometrics",
                "sameAs": "https://www.wikidata.org/wiki/Q178706"
            },
            {
                "name": "Access control",
                "sameAs": "https://www.wikidata.org/wiki/Q13410526"
            }
        ],
        "related_services": [
            "low-voltage-systems",
            "networks-smatv",
            "system-integration"
        ]
    },
    "sound-and-light": {
        "slug": "sound-and-light",
        "icon": "Speaker",
        "badge": {
            "ru": "Звук и свет",
            "kz": "Дыбыс және жарық",
            "en": "Pro Audio & Light"
        },
        "ru": {
            "title": "Профессиональный звук и сценический свет в Алматы",
            "description": "Акустический расчет и оснащение конференц-залов, концертных площадок, ресторанов, мечетей и ТРЦ. Линейные массивы, микрофонные парки, DSP-процессоры и сценический свет.",
            "keywords": "профессиональный звук Алматы, сценический свет, звуковое оборудование для ресторанов, акустический расчет, линейный массив Казахстан, фоновое озвучивание ресторанов, акустика 100V OBT, конференц-связь для залов, постановочный свет DMX",
            "features": [
                "Электроакустический расчет помещений для идеальной разборчивости речи",
                "Линейные массивы, сабвуферы, потолочная и настенная акустика",
                "Конференц-системы, синхронный перевод и радиомикрофоны",
                "Сценический динамический свет DMX и светодиодные LED-экраны"
            ],
            "stages": [
                "Акустические замеры зала и 3D-моделирование",
                "Подбор акустики, усилителей и процессоров",
                "Монтаж ферм, подвеса акустики и кабельных трасс",
                "Калибровка звукового тракта измерительными микрофонами"
            ],
            "faqs": [
                {
                    "q": "Делаете ли вы акустический расчет?",
                    "a": "Да, акустический расчет обязателен для предотвращения эха и достижения кристально чистой разборчивости речи."
                },
                {
                    "q": "Поставляете ли вы акустику OBT, которую можно увидеть в каталоге товаров?",
                    "a": "Да, INPAR является прямым дистрибьютором и интегратором профессиональных акустических систем OBT (усилители, настенные колонны, потолочные динамики) в Казахстане."
                }
            ],
            "problems": [
                {
                    "problem": "Плохая разборчивость речи, гул, эхо и неравномерная громкость в залах ресторанов или конференц-комнатах.",
                    "solution": "Компьютерное акустическое моделирование помещения, подбор диаграммы направленности колонок и точная настройка DSP-процессора.",
                    "benefit": "Кристально чистый звук, комфортный уровень громкости за каждым столом и отсутствие утомляемости гостей."
                }
            ]
        },
        "kz": {
            "title": "Кәсіби дыбыс және сахналық жарық",
            "description": "Конференц-залдар, мейрамханалар, мешіттер мен сауда орталықтарына арналған кәсіби акустика және динамикалық сахналық жарық жүйелері.",
            "keywords": "кәсіби дыбыс Алматы, сахналық жарық, мейрамханаға дыбыс, конференц жүйелер, мейрамханаға фондық дыбыс, OBT акустикасы Алматы, конференц залдарды жабдықтау, сахналық жарық DMX",
            "features": [
                "Сөз анықтығын қамтамасыз ететін акустикалық есептеу",
                "Конференц-байланыс және сапалы радиомикрофондар",
                "DMX сахналық динамикалық жарықтандыру"
            ],
            "stages": [
                "Бөлменің акустикасын өлшеу",
                "Акустикалық жүйелерді іріктеу және монтаждау",
                "Дыбыс процессорларын кәсіби баптау"
            ],
            "faqs": [
                {
                    "q": "Фондық дыбыс орнатасыздар ма?",
                    "a": "Иә, мейрамханалар мен дүкендерге арналған аймақтық 100V трансляциялық дыбыс жүйелерін орнатамыз."
                },
                {
                    "q": "Каталогтағы OBT акустикасын көтерме бағамен сатып алуға бола ма?",
                    "a": "Иә, біз OBT жабдықтарын Қазақстан бойынша тікелей жеткізуші болып табыламыз және көтерме бағамен ұсынамыз."
                }
            ],
            "problems": [
                {
                    "problem": "Залдағы жаңғырық пен дыбыстың бұзылуы.",
                    "solution": "Акустикалық есептеу жүргізу және DSP дыбыс процессорларын дәл баптау.",
                    "benefit": "Залдың әрбір нүктесінде таза және жағымды дыбыс."
                }
            ]
        },
        "en": {
            "title": "Professional Audio & Stage Lighting Systems in Kazakhstan",
            "description": "Acoustic design, supply, and installation for concert venues, auditoriums, conference centers, houses of worship, and commercial hospitality spaces.",
            "keywords": "pro audio Almaty, commercial sound systems Kazakhstan, line array speakers, architectural lighting, commercial background music 100V, restaurant acoustics, conference room AV systems, OBT audio distribution",
            "features": [
                "Computer-modeled acoustic simulation for optimal speech intelligibility",
                "Line arrays, distributed ceiling audio, and High-End stage amplification",
                "DMX moving heads, wash lights, and high-resolution indoor LED screens"
            ],
            "stages": [
                "Acoustic measurement and room reverberation modeling",
                "Rigging, cabling, and loudspeaker positioning",
                "Digital signal processing (DSP) alignment with calibrated microphones"
            ],
            "faqs": [
                {
                    "q": "Do you design background music systems for hospitality?",
                    "a": "Yes, we install multi-zone 100V distributed commercial background music systems with app-based volume control."
                },
                {
                    "q": "Do you supply OBT commercial audio hardware listed in your catalog?",
                    "a": "Yes, INPAR is a direct distributor and integrator of certified OBT commercial audio products in Kazakhstan."
                }
            ],
            "problems": [
                {
                    "problem": "Poor speech intelligibility, acoustic flutter echoes, and fatiguing sound levels in restaurants or halls.",
                    "solution": "Predictive acoustic mapping, targeted dispersion speaker selection, and calibrated DSP equalization.",
                    "benefit": "Warm, crystal-clear audio balance across every seating zone."
                }
            ]
        },
        "knowsAbout": [
            {
                "name": "Public address system",
                "sameAs": "https://www.wikidata.org/wiki/Q1340156"
            },
            {
                "name": "Acoustics",
                "sameAs": "https://www.wikidata.org/wiki/Q82811"
            }
        ],
        "related_services": [
            "fire-safety",
            "smart-home-knx",
            "low-voltage-systems"
        ]
    },
    "networks-smatv": {
        "slug": "networks-smatv",
        "icon": "Network",
        "badge": {
            "ru": "СКС & SMATV",
            "kz": "СКС & Желілер",
            "en": "Networks & SMATV"
        },
        "ru": {
            "title": "Информационные сети, СКС и SMATV (IPTV, Спутниковое ТВ) в Алматы",
            "description": "Проектирование и построение структурированных кабельных систем (СКС), оптоволокна (ВОЛС), бесшовного корпоративного Wi-Fi и гостиничного телевидения SMATV/IPTV.",
            "keywords": "монтаж СКС Алматы, корпоративный Wi-Fi, гостиничное телевидение SMATV, IPTV для отелей, оптические сети Казахстан, монтаж СКС Fluke тестирование, сварка оптоволокна ВОЛС, серверные шкафы 19 дюймов, телевидение IPTV для отелей",
            "features": [
                "Сертифицированные кабельные системы категорий 5e, 6, 6A, 7 с гарантией",
                "Сварка оптоволокна и тестирование линий сканером Fluke Networks",
                "Бесшовный роуминг Wi-Fi для офисов, отелей и складских терминалов",
                "Интерактивное гостиничное телевидение IPTV с брендированным меню"
            ],
            "stages": [
                "Радиообследование и аудит сетевых потребностей",
                "Проектирование серверных комнат и кроссовых шкафов",
                "Монтаж лотков, витой пары и оптоволокна",
                "Тестирование портов Fluke и настройка активного оборудования"
            ],
            "faqs": [
                {
                    "q": "Предоставляете ли вы протоколы Fluke?",
                    "a": "Да, на каждую смонтированную линию предоставляется официальный протокол сертификационного тестирования."
                },
                {
                    "q": "Проводите ли вы тестирование СКС профессиональными кабельными сканерами?",
                    "a": "Да, каждая смонтированная линия проходит проверку кабельным анализатором Fluke Networks с выдачей графических протоколов сертификации."
                }
            ],
            "problems": [
                {
                    "problem": "Обрывы связи и низкая скорость корпоративной сети из-за некачественных скруток и перегибов кабеля.",
                    "solution": "Монтаж сертифицированной СКС с соблюдением радиусов изгиба и обязательным тестированием приборами Fluke Networks.",
                    "benefit": "Гарантированная гигабитная скорость передачи данных и отсутствие потерь пакетов."
                }
            ]
        },
        "kz": {
            "title": "Ақпараттық желілер, СКС және SMATV (IPTV, Спутниктік ТВ)",
            "description": "Құрылымдалған кабельдік желілерді (СКС), талшықты-оптикалық байланыс желілерін (ВОЛС), үздіксіз Wi-Fi және қонақүйлерге арналған интерактивті теледидар жүйелерін құру.",
            "keywords": "СКС монтаждау Алматы, корпоративті Wi-Fi, қонақүй теледидары, оптика дәнекерлеу, СКС монтаж Fluke тестілеу, оптика дәнекерлеу, серверлік бөлмелер, қонақ үйге IPTV орнату",
            "features": [
                "5e, 6, 6A санатты сертификатталған СКС желілері",
                "Оптикалық талшықтарды кәсіби дәнекерлеу және Fluke сынағы",
                "Үздіксіз роумингі бар корпоративтік сенімді Wi-Fi"
            ],
            "stages": [
                "Желілік қажеттіліктерді талдау және жобалау",
                "Серверлік шкафтар мен кабельдерді орнату",
                "Белсенді желілік жабдықты баптау"
            ],
            "faqs": [
                {
                    "q": "Кепілдік бар ма?",
                    "a": "Иә, сертификатталған желілерге 15 жылға дейін жүйелік кепілдік беріледі."
                },
                {
                    "q": "Оптиканы дәнекерлеу қызметін көрсетесіздер ме?",
                    "a": "Иә, біз кәсіби жапондық дәнекерлеу аппараттарымен оптикалық кабельдерді сапалы дәнекерлейміз."
                }
            ],
            "problems": [
                {
                    "problem": "Сервердегі ретсіздік және интернет жылдамдығының төмендеуі.",
                    "solution": "Кәсіби СКС құру және Fluke аспабымен тестілеу.",
                    "benefit": "Тұрақты жоғары жылдамдықты желі және реттелген сервер."
                }
            ]
        },
        "en": {
            "title": "Data Networks, Structured Cabling & SMATV in Kazakhstan",
            "description": "Structured cabling systems (SCS Cat 5e/6/6A/7), fiber optic backbone links, seamless high-density enterprise Wi-Fi, and hospitality interactive SMATV/IPTV systems.",
            "keywords": "structured cabling Almaty, fiber optic installation Kazakhstan, enterprise Wi-Fi, hotel IPTV, Fluke certified structured cabling, fiber fusion splicing OTDR, telecom rack dressing, hospitality IPTV SMATV",
            "features": [
                "Certified Cat 6 / 6A / 7 structured cabling with manufacturer warranties",
                "Fiber optic fusion splicing and Fluke Networks certification reports",
                "High-density seamless enterprise Wi-Fi networks for offices, warehouses, and hotels"
            ],
            "stages": [
                "Wi-Fi predictive heatmapping and infrastructure capacity audit",
                "Server room and telecom closet CAD layout",
                "Cable pulling, patch panel termination, and fluke testing",
                "Core routing, switching, VLAN, and firewall configuration"
            ],
            "faqs": [
                {
                    "q": "Do you certify cabling with Fluke?",
                    "a": "Yes, every copper and fiber link is tested and certified with a formal Fluke Networks report."
                },
                {
                    "q": "Do you provide Fluke test certification reports?",
                    "a": "Yes, every installed drop is verified with Fluke Networks DTX/DSX analyzers with complete PDF pass reports."
                }
            ],
            "problems": [
                {
                    "problem": "Network connection drops and packet loss caused by substandard wiring terminations.",
                    "solution": "Installing certified structured cabling using strict bend-radius rules and mandatory Fluke Networks qualification.",
                    "benefit": "Guaranteed gigabit throughput and zero downtime for mission-critical IT services."
                }
            ]
        },
        "knowsAbout": [
            {
                "name": "Computer network",
                "sameAs": "https://www.wikidata.org/wiki/Q1301371"
            },
            {
                "name": "Fiber-optic communication",
                "sameAs": "https://www.wikidata.org/wiki/Q162"
            }
        ],
        "related_services": [
            "low-voltage-systems",
            "cctv-access-control",
            "system-integration"
        ]
    },
    "system-integration": {
        "slug": "system-integration",
        "icon": "Combine",
        "badge": {
            "ru": "Генеральный подряд",
            "kz": "Бас мердігерлік",
            "en": "Systems Integration"
        },
        "ru": {
            "title": "Системная интеграция слаботочных систем под ключ в Казахстане",
            "description": "Генеральный подряд по слаботочным системам. Объединение разрозненного оборудования (BMS, пожарная сигнализация, СКУД, CCTV, звук, мультимедиа) в единую слаженно работающую экосистему с централизованным управлением.",
            "keywords": "системная интеграция Алматы, генеральный подрядчик слаботочные сети Казахстан, комплексные инженерные системы, интеграция оборудования, генеральный подрядчик инжиниринг, интеграция слаботочки автоматики, пусконаладочные работы ПНР, сервисное ТО",
            "features": [
                "Единая точка ответственности за все слаботочные разделы объекта",
                "Бесшовная стыковка оборудования разных брендов по открытым протоколам",
                "Согласованная работа систем безопасности при пожаре и ЧС",
                "Снижение бюджета стройки за счет исключения дублирующих трасс",
                "Собственный штат квалифицированных инженеров и программистов"
            ],
            "stages": [
                "Комплексный аудит проекта и координация смежных разделов",
                "Разработка сводного проекта автоматизации и интеграции",
                "Поставка оборудования напрямую от заводов",
                "Шеф-монтаж, пусконаладка и интеграционные тесты систем",
                "Сдача объекта госкомиссии и службам технического надзора"
            ],
            "faqs": [
                {
                    "q": "Работаете ли вы по всему Казахстану?",
                    "a": "Да, мы реализуем масштабные проекты в Алматы, Астане, Шымкенте, Актобе, Туркестане и других городах РК."
                },
                {
                    "q": "Почему выгоднее нанять одного интегратора вместо десятка узких подрядчиков?",
                    "a": "Один генеральный интегратор несет полную ответственность за конечный результат, исключает несогласованность кабельных трасс и обеспечивает слаженную работу всех систем без взаимных обвинений субподрядчиков."
                }
            ],
            "problems": [
                {
                    "problem": "Инженерные системы здания (вентиляция, чиллеры, котельная, пожарка, электрика) работают автономно, не синхронизированы и конфликтуют друг с другом.",
                    "solution": "Комплексная интеграция всех разделов от INPAR: сведение всех протоколов и систем в единую интеллектуальную цифровую экосистему.",
                    "benefit": "Слаженная работа всех инженерных узлов, снижение энергозатрат до 30% и полное отсутствие аварийных несогласованностей."
                }
            ]
        },
        "kz": {
            "title": "Төменгі ток жүйелерінің кешенді интеграциясы",
            "description": "Ғимараттардың барлық инженерлік және әлсіз ток желілері бойынша бас мердігерлік. BMS, өрт дабылы, СКУД, бейнебақылау және мультимедианы бірыңғай цифрлық жүйеге біріктіру.",
            "keywords": "жүйелік интеграция Алматы, әлсіз ток бас мердігері Қазақстан, кешенді инженерлік жүйелер, инженерлік жүйелердің бас мердігері, кешенді интеграциялау, автоматика мен әлсіз токты біріктіру",
            "features": [
                "Нысанның барлық төменгі ток бөлімдері үшін бірыңғай жауапкершілік",
                "Әртүрлі өндірушілердің жабдықтарын үздіксіз біріктіру",
                "Құрылыс сметасын 20%-ға дейін оңтайландыру"
            ],
            "stages": [
                "Жобаны кешенді сараптау",
                "Интеграция сызбасын әзірлеу",
                "Жабдықтарды тікелей жеткізу және монтаждау",
                "Мемлекеттік комиссияға тапсыру"
            ],
            "faqs": [
                {
                    "q": "Қай қалаларда жұмыс істейсіздер?",
                    "a": "Алматы, Астана, Шымкент, Ақтөбе және бүкіл Қазақстан бойынша қызмет көрсетеміз."
                },
                {
                    "q": "Кешенді интеграция не үшін қажет?",
                    "a": "Ғимараттың барлық жүйелері өзара байланыста жұмыс істеп, апаттардың алдын алады және пайдалану шығындарын барынша азайтады."
                }
            ],
            "problems": [
                {
                    "problem": "Ғимараттағы желдету, жылыту және өрт жүйелерінің бөлек жұмыс істеуі және келіспеушілігі.",
                    "solution": "Барлық жүйелерді INPAR арқылы біртұтас цифрлық экожүйеге біріктіру.",
                    "benefit": "Жүйелердің мінсіз үйлесімді жұмысы және шығындарды 30% үнемдеу."
                }
            ]
        },
        "en": {
            "title": "End-to-End Systems Integration for Low-Voltage Infrastructure in Kazakhstan",
            "description": "Master technology integrator for Extra Low Voltage (ELV) and smart building systems. Unifying BMS, fire detection, CCTV, access control, and audio-visual into a cohesive smart facility ecosystem.",
            "keywords": "systems integrator Almaty, master systems integrator Kazakhstan, turnkey ELV contractor, MEP automation, master systems integrator, turnkey building engineering, commissioning agent, cross-system protocol integration",
            "features": [
                "Single point of responsibility for all building technology packages",
                "Seamless multi-vendor interoperability via open standards (BACnet, Modbus, KNX, DALI)",
                "Optimized construction budget by eliminating duplicate containment and cabling",
                "In-house engineering team with proven track record across Central Asia"
            ],
            "stages": [
                "Integrated multi-discipline project audit and clash detection",
                "Master integration architecture blueprinting",
                "Direct factory equipment procurement",
                "Commissioning, cause-and-effect testing, and client handover"
            ],
            "faqs": [
                {
                    "q": "Do you deliver projects across Kazakhstan?",
                    "a": "Yes, our engineers deliver projects in Almaty, Astana, Shymkent, Aktobe, Turkestan, and regionally."
                },
                {
                    "q": "Why hire a Master Systems Integrator (MSI) instead of isolated trade contractors?",
                    "a": "An MSI guarantees overall functionality, eliminates interface disputes, streamlines pathways, and delivers a unified building intelligence platform with single-point accountability."
                }
            ],
            "problems": [
                {
                    "problem": "Siloed building systems (HVAC, fire, chillers, power) operating independently and causing conflicting control cycles.",
                    "solution": "Comprehensive master system integration uniting all field equipment into a singular intelligent digital control plane.",
                    "benefit": "Flawless inter-system coordination, up to 30% reduction in utility waste, and zero contractor finger-pointing."
                }
            ]
        },
        "knowsAbout": [
            {
                "name": "Systems engineering",
                "sameAs": "https://www.wikidata.org/wiki/Q216353"
            },
            {
                "name": "Systems integrator",
                "sameAs": "https://www.wikidata.org/wiki/Q3244837"
            }
        ],
        "related_services": [
            "bms-dispatching",
            "industrial-automation",
            "low-voltage-systems"
        ]
    }
}


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
    Generate dynamic XML sitemap with all pages, services, products,
    and multi-lingual xhtml:link alternates (ru, kk, en, x-default).
    """
    products = Product.objects.filter(is_active=True).select_related('category').order_by('-updated_at')

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]

    def add_multilingual_urls(path_rel, priority, changefreq, image=None, lastmod=None):
        clean = path_rel.strip('/')
        # 3 URL paths: Default (RU) "", Kazakh "kz", English "en"
        ru_url = f"{BASE_URL}/{clean}" if clean else f"{BASE_URL}/"
        kz_url = f"{BASE_URL}/kz/{clean}" if clean else f"{BASE_URL}/kz"
        en_url = f"{BASE_URL}/en/{clean}" if clean else f"{BASE_URL}/en"

        locs = [
            ("ru", ru_url),
            ("kk", kz_url),
            ("en", en_url)
        ]

        for lang_code, loc in locs:
            xml_lines.append("  <url>")
            xml_lines.append(f"    <loc>{html.escape(loc)}</loc>")
            if lastmod:
                xml_lines.append(f"    <lastmod>{lastmod}</lastmod>")
            xml_lines.append(f"    <changefreq>{changefreq}</changefreq>")
            xml_lines.append(f"    <priority>{priority}</priority>")

            # Alternates for Google
            xml_lines.append(f'    <xhtml:link rel="alternate" hreflang="ru" href="{html.escape(ru_url)}"/>')
            xml_lines.append(f'    <xhtml:link rel="alternate" hreflang="kk" href="{html.escape(kz_url)}"/>')
            xml_lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{html.escape(en_url)}"/>')
            xml_lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{html.escape(ru_url)}"/>')

            if image:
                xml_lines.append("    <image:image>")
                xml_lines.append(f"      <image:loc>{html.escape(image['loc'])}</image:loc>")
                xml_lines.append(f"      <image:title>{html.escape(image['title'])}</image:title>")
                xml_lines.append("    </image:image>")

            xml_lines.append("  </url>")

    # 1. Main pages
    add_multilingual_urls("", "1.0", "daily")
    add_multilingual_urls("products", "0.9", "daily")
    add_multilingual_urls("projects", "0.8", "weekly")

    # 2. All 12 Services
    for slug in SERVICES_DATA.keys():
        add_multilingual_urls(f"services/{slug}", "0.9", "weekly")

    # 3. Products from DB
    for p in products:
        lastmod = p.updated_at.strftime('%Y-%m-%d') if p.updated_at else '2026-10-23'
        image_obj = None
        if p.main_image:
            image_url = f"{BASE_URL}{p.main_image.url}" if not p.main_image.url.startswith('http') else p.main_image.url
            image_obj = {"loc": image_url, "title": p.name}

        add_multilingual_urls(f"products/{p.id}", "0.8", "weekly", image=image_obj, lastmod=lastmod)

    xml_lines.append("</urlset>")
    return HttpResponse("\n".join(xml_lines), content_type="application/xml; charset=utf-8")


def _render_base_html(title, description, keywords, canonical, og_image, json_ld_list, body_content, lang="ru", path=""):
    """Render semantic HTML for bots with multi-lingual tags and alternates"""
    og_image = og_image or f"{BASE_URL}/assets/sticker-CGlHhmMq.png"
    json_ld_scripts = "\n".join([
        f'    <script type="application/ld+json">\n{json.dumps(schema, ensure_ascii=False, indent=2)}\n    </script>'
        for schema in json_ld_list
    ])

    # Strip lang from path for alternate calculation
    clean_path = path.strip('/')
    if clean_path.startswith(('kz/', 'en/')):
        clean_path = clean_path[3:]
    elif clean_path in ('kz', 'en'):
        clean_path = ''

    ru_url = f"{BASE_URL}/{clean_path}" if clean_path else f"{BASE_URL}/"
    kz_url = f"{BASE_URL}/kz/{clean_path}" if clean_path else f"{BASE_URL}/kz"
    en_url = f"{BASE_URL}/en/{clean_path}" if clean_path else f"{BASE_URL}/en"

    html_lang = "kk" if lang == "kz" else ("en" if lang == "en" else "ru")

    labels = {
        "ru": {
            "home": "Главная", "catalog": "Каталог", "projects": "Проекты", "services": "Услуги", "contact": "Контакты",
            "footer": "ТОО «INPAR.KZ» — Слаботочные системы, автоматизация зданий (BMS, DDC, MCC) и Умный дом KNX.",
            "addr": "Казахстан, г. Алматы, ЖК «Сарыарка», 1-й микрорайон, 68/4 | Тел: +7 (701) 995-42-17 | Email: info@inpar.kz"
        },
        "kz": {
            "home": "Басты бет", "catalog": "Каталог", "projects": "Жобалар", "services": "Қызметтер", "contact": "Байланыс",
            "footer": "«INPAR.KZ» ЖШС — Төменгі ток жүйелері, ғимараттарды автоматтандыру (BMS, DDC, MCC) және KNX Ақылды үй.",
            "addr": "Қазақстан, Алматы қ., «Сарыарқа» ТҮК, 1-ші ықшамаудан, 68/4 | Тел: +7 (701) 995-42-17 | Email: info@inpar.kz"
        },
        "en": {
            "home": "Home", "catalog": "Catalog", "projects": "Projects", "services": "Services", "contact": "Contact",
            "footer": "INPAR.KZ — Low-Voltage Systems, Industrial Automation (BMS, DDC, MCC) & KNX Smart Home.",
            "addr": "Kazakhstan, Almaty, Saryarka Complex, Microdistrict 1, 68/4 | Phone: +7 (701) 995-42-17 | Email: info@inpar.kz"
        }
    }.get(lang, "ru")

    prefix = f"/{lang}" if lang in ("kz", "en") else ""

    return f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description)}">
    <meta name="keywords" content="{html.escape(keywords)}">
    <link rel="canonical" href="{html.escape(canonical)}">

    <!-- Hreflang Alternates for Google Multi-Language Indexing -->
    <link rel="alternate" hreflang="ru" href="{html.escape(ru_url)}">
    <link rel="alternate" hreflang="kk" href="{html.escape(kz_url)}">
    <link rel="alternate" hreflang="en" href="{html.escape(en_url)}">
    <link rel="alternate" hreflang="x-default" href="{html.escape(ru_url)}">

    <!-- Open Graph -->
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
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
            background-color: #1A1D23;
            color: #E8E9ED;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1040px;
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
            margin-left: 18px;
            font-size: 14px;
        }}
        nav a:hover {{
            color: #3B82F6;
        }}
        .lang-switch {{
            margin-left: 20px;
            padding-left: 15px;
            border-left: 1px solid #333842;
        }}
        .lang-switch a {{
            color: #B8A276;
            margin-left: 8px;
            font-weight: bold;
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
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
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
            <a href="{BASE_URL}{prefix}/" class="logo">INPAR.KZ</a>
            <nav>
                <a href="{BASE_URL}{prefix}/">{labels['home']}</a>
                <a href="{BASE_URL}{prefix}/products">{labels['catalog']}</a>
                <a href="{BASE_URL}{prefix}/projects">{labels['projects']}</a>
                <a href="{BASE_URL}{prefix}/#services">{labels['services']}</a>
                <a href="{BASE_URL}{prefix}/#contact">{labels['contact']}</a>
                <span class="lang-switch">
                    <a href="{html.escape(ru_url)}">RU</a>
                    <a href="{html.escape(kz_url)}">KZ</a>
                    <a href="{html.escape(en_url)}">EN</a>
                </span>
            </nav>
        </header>

        {body_content}

        <footer>
            <p><strong>{labels['footer']}</strong></p>
            <p>{labels['addr']}</p>
            <p>© 2014–2026 INPAR.KZ. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>"""


def bot_render_view(request):
    """
    Renders fully structured semantic HTML for search crawlers in 3 languages (RU, KZ, EN)
    """
    path = request.GET.get('path', request.path)
    clean_path = path.strip('/')

    # Detect language from path prefix
    lang = "ru"
    route_path = clean_path
    if clean_path.startswith("kz/") or clean_path == "kz":
        lang = "kz"
        route_path = clean_path[3:] if clean_path.startswith("kz/") else ""
    elif clean_path.startswith("en/") or clean_path == "en":
        lang = "en"
        route_path = clean_path[3:] if clean_path.startswith("en/") else ""

    prefix = f"/{lang}" if lang in ("kz", "en") else ""

    # 1. Product Detail Page: /products/<id>
    product_match = re.search(r'^products/(\d+)$', route_path)
    if product_match:
        product_id = product_match.group(1)
        try:
            product = Product.objects.select_related('category').prefetch_related('characteristics', 'images').get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return HttpResponse("Product not found", status=404)

        rate = Decimal(str(get_usd_to_kzt_rate()))
        price_kzt = int(round(product.price_usd * rate)) if product.price_usd else 0
        wholesale_kzt = int(round(product.wholesale_price_usd * rate)) if product.wholesale_price_usd else 0

        title_tpl = {
            "ru": f"{product.name} — Купить в Алматы, цена, характеристики | INPAR.KZ",
            "kz": f"{product.name} — Сатып алу Алматы, бағасы, сипаттамасы | INPAR.KZ",
            "en": f"{product.name} — Buy in Almaty, Price, Specs | INPAR.KZ"
        }
        desc_tpl = {
            "ru": f"Купить {product.name} в Алматы. Цена: ₸{price_kzt:,}. {product.description or 'Оборудование для автоматизации и слаботочных систем.'} Доставка по Казахстану.",
            "kz": f"{product.name} Алматыда сатып алу. Бағасы: ₸{price_kzt:,}. {product.description or 'Автоматтандыру жабдықтары.'} Қазақстан бойынша жеткізу.",
            "en": f"Buy {product.name} in Kazakhstan. Price: ₸{price_kzt:,}. {product.description or 'Industrial automation & low voltage equipment.'} Official warranty."
        }

        title = title_tpl.get(lang, title_tpl["ru"])
        description = desc_tpl.get(lang, desc_tpl["ru"])
        keywords = f"{product.name}, купить {product.name}, {product.sku or ''}, слаботочные системы Алматы, автоматизация Казахстан"
        canonical = f"{BASE_URL}{prefix}/products/{product.id}"
        image_url = f"{BASE_URL}{product.main_image.url}" if product.main_image else f"{BASE_URL}/assets/sticker-CGlHhmMq.png"

        schema_product = {
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": product.name,
            "image": [image_url],
            "description": product.description or product.name,
            "sku": product.sku or f"INPAR-{product.id}",
            "brand": {"@type": "Brand", "name": "INPAR"},
            "offers": {
                "@type": "Offer",
                "url": canonical,
                "priceCurrency": "KZT",
                "price": str(price_kzt),
                "priceValidUntil": "2027-12-31",
                "itemCondition": "https://schema.org/NewCondition",
                "availability": "https://schema.org/InStock",
                "seller": {"@type": "Organization", "name": "INPAR.KZ"}
            }
        }

        char_rows = "".join([f"<tr><td><strong>{html.escape(c.name)}</strong></td><td>{html.escape(c.value)}</td></tr>" for c in product.characteristics.all()])

        cta_text = {
            "ru": "Заказать в WhatsApp",
            "kz": "WhatsApp арқылы тапсырыс беру",
            "en": "Order via WhatsApp"
        }.get(lang, "Order via WhatsApp")

        body_content = f"""
        <span class="badge">Каталог оборудования / Products</span>
        <h1>{html.escape(product.name)}</h1>
        {f'<p><strong>SKU / Артикул:</strong> {html.escape(product.sku)}</p>' if product.sku else ''}
        {f'<div class="price">₸{price_kzt:,} <span style="font-size: 16px; color: #9BA1AB; font-weight: normal;">($ {product.price_usd})</span></div>' if price_kzt > 0 else ''}
        {f'<p style="color: #60A5FA;">Оптом / Wholesale: <strong>₸{wholesale_kzt:,}</strong></p>' if wholesale_kzt > 0 else ''}

        <p><a href="https://wa.me/77019954217?text={html.escape('Здравствуйте! Интересует товар ' + product.name)}" class="btn">{cta_text}</a></p>

        <h2>Описание товара</h2>
        <p>{html.escape(product.description or 'Оборудование для системной интеграции, слаботочных систем и автоматизации.')}</p>

        {f'''<h2>Характеристики</h2>
        <table class="table">
            <thead><tr><th>Параметр</th><th>Значение</th></tr></thead>
            <tbody>{char_rows}</tbody>
        </table>''' if char_rows else ''}
        """

        return HttpResponse(_render_base_html(title, description, keywords, canonical, image_url, [schema_product], body_content, lang=lang, path=path), content_type="text/html; charset=utf-8")

    # 2. Service Detail Page: /services/<slug>
    service_match = re.search(r'^services/([a-z0-9-]+)$', route_path)
    if service_match:
        slug = service_match.group(1)
        if slug in SERVICES_DATA:
            service_root = SERVICES_DATA[slug]
            service_data = service_root.get(lang, service_root["ru"])
            badge_text = service_root["badge"].get(lang, service_root["badge"]["ru"])

            canonical = f"{BASE_URL}{prefix}/services/{slug}"
            title = f"{service_data['title']} | INPAR.KZ"
            description = service_data['description']
            keywords = service_data['keywords']

            schema_service = {
                "@context": "https://schema.org",
                "@type": "Service",
                "name": service_data['title'],
                "description": service_data['description'],
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
                "areaServed": {"@type": "Country", "name": "Kazakhstan"},
                "knowsAbout": [
                    {"@type": "DefinedTerm", "name": k["name"], "sameAs": k["sameAs"]}
                    for k in service_root.get("knowsAbout", [])
                ]
            }

            schema_faq = {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": faq["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": faq["a"]}
                    } for faq in service_data.get("faqs", [])
                ]
            }

            features_html = "".join([f"<li>{html.escape(f)}</li>" for f in service_data['features']])
            stages_html = "".join([f"<li>{html.escape(s)}</li>" for s in service_data['stages']])
            faqs_html = "".join([f"<p><strong>Q: {html.escape(faq['q'])}</strong><br>A: {html.escape(faq['a'])}</p>" for faq in service_data.get("faqs", [])])

            problems_html = ""
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
            }.get(lang, ("Задачи", "Возможности", "Этапы", "FAQ", "WhatsApp", "Связанные"))

            body_content = f"""
            <span class="badge">{html.escape(badge_text)}</span>
            <h1>{html.escape(service_data['title'])}</h1>
            <p style="font-size: 18px; color: #D1D5DB;">{html.escape(service_data['description'])}</p>
            <p><a href="https://wa.me/77019954217?text={html.escape('Интересует ' + service_data['title'])}" class="btn">{sec_titles[4]}</a></p>

            {f'''<h2>{sec_titles[0]}</h2>
            {problems_html}''' if problems_html else ''}

            <h2>{sec_titles[1]}</h2>
            <ul>{features_html}</ul>

            <h2>{sec_titles[1]}</h2>
            <ol>{stages_html}</ol>

            {f'''<h2>{sec_titles[2]}</h2>
            <div style="background-color: #252932; padding: 20px; border-radius: 8px; border: 1px solid #333842;">
                {faqs_html}
            </div>''' if faqs_html else ''}
            """

            return HttpResponse(_render_base_html(title, description, keywords, canonical, None, [schema_service, schema_faq], body_content, lang=lang, path=path), content_type="text/html; charset=utf-8")

    # 3. Products Catalog: /products
    if route_path == 'products':
        canonical = f"{BASE_URL}{prefix}/products"
        title_map = {
            "ru": "Каталог оборудования — Слаботочные системы, автоматизация, звук | INPAR.KZ",
            "kz": "Жабдықтар каталогы — Төменгі ток жүйелері, автоматтандыру, дыбыс | INPAR.KZ",
            "en": "Equipment Catalog — Low-Voltage, Automation & Audio Systems | INPAR.KZ"
        }
        desc_map = {
            "ru": "Каталог сертифицированного оборудования в Алматы: акустика, датчики, шкафы автоматики, контроллеры с доставкой по Казахстану.",
            "kz": "Алматыдағы сертификатталған жабдықтар каталогы: акустика, датчиктер, автоматика шкафтары, контроллерлер.",
            "en": "Catalog of certified engineering equipment in Kazakhstan: audio systems, DDC/MCC sensors, control panels."
        }
        title = title_map.get(lang, title_map["ru"])
        description = desc_map.get(lang, desc_map["ru"])
        keywords = "каталог оборудования умный дом, датчики BMS, акустика Алматы, слаботочное оборудование Казахстан"

        products = Product.objects.filter(is_active=True)[:40]
        items_html = ""
        for p in products:
            items_html += f"""
            <div class="card">
                <h3><a href="{BASE_URL}{prefix}/products/{p.id}">{html.escape(p.name)}</a></h3>
                {f'<p style="color: #9BA1AB; font-size: 13px;">SKU: {html.escape(p.sku)}</p>' if p.sku else ''}
                {f'<p style="color: #3B82F6; font-weight: bold;">$ {p.price_usd}</p>' if p.price_usd else ''}
                <p><a href="{BASE_URL}{prefix}/products/{p.id}">Подробнее / Details →</a></p>
            </div>
            """

        body_content = f"""
        <span class="badge">Каталог / Catalog</span>
        <h1>{title}</h1>
        <p>{description}</p>
        <div class="grid">{items_html}</div>
        """
        return HttpResponse(_render_base_html(title, description, keywords, canonical, None, [], body_content, lang=lang, path=path), content_type="text/html; charset=utf-8")

    # 4. Default: Homepage /
    canonical = f"{BASE_URL}{prefix}/" if prefix else f"{BASE_URL}/"
    home_meta = {
        "ru": {
            "title": "INPAR.KZ — Слаботочные системы, Индустриальная автоматизация, MCC, DDC и Умный дом в Алматы",
            "description": "ТОО «INPAR.KZ» с 2014 года в Казахстане: монтаж слаботочных систем, индустриальная автоматизация, сборка шкафов MCC и DDC, электрические щиты (ЩА, ЩУ, ВРУ) и Умный дом KNX.",
            "keywords": "слаботочные системы Алматы, индустриальные автоматизации, шкафы MCC, контроллеры DDC, электрические шкафы Алматы, сборка щитов автоматики, умный дом KNX Казахстан, АСУ ТП",
            "badge": "Engineering Excellence",
            "h1": "INPAR — Интеллектуальная автоматизация, слаботочные сети и шкафы MCC / DDC в Казахстане",
            "text": "Компания INPAR.KZ с 2014 года выполняет полный комплекс инжиниринга: слаботочные системы, индустриальная автоматизация технологических процессов (АСУ ТП), производство шкафов управления двигателями (MCC), прямое цифровое управление ОВиК (DDC), электрощитовое производство (ЩА, ЩУ, ГРЩ) и Умный дом стандарта KNX."
        },
        "kz": {
            "title": "INPAR.KZ — Төменгі ток жүйелері, Өндірістік автоматтандыру, MCC, DDC және Ақылды үй Алматыда",
            "description": "«INPAR.KZ» ЖШС 2014 жылдан бері Қазақстанда: төменгі ток желілері, өндірістік автоматтандыру (ТП ББЖ), MCC және DDC басқару шкафтары, электр қалқандары және KNX Ақылды үй.",
            "keywords": "төменгі ток жүйелері Алматы, өндірістік автоматтандыру, MCC басқару шкафтары, DDC контроллерлері, электр шкафтарын құрастыру, ақылды үй Қазақстан",
            "badge": "Инженерлік кемелдік",
            "h1": "INPAR — Төменгі ток желілері, өндірістік автоматтандыру және MCC / DDC шкафтары",
            "text": "2014 жылдан бері INPAR.KZ компаниясы Қазақстан бойынша төменгі ток желілерін, өндірістік автоматтандыруды, MCC қозғалтқыштарды басқару шкафтарын, DDC желдету автоматикасын және KNX Ақылды үй жүйелерін жобалап, кілтке дейін орнатады."
        },
        "en": {
            "title": "INPAR.KZ — Low-Voltage Systems, Industrial Automation, MCC & DDC Panels, Smart Home in Kazakhstan",
            "description": "INPAR.KZ engineering since 2014: turnkey Extra Low Voltage (ELV) systems, industrial process automation (SCADA/PLC), Motor Control Centers (MCC), DDC HVAC panels, switchgear, and KNX smart home.",
            "keywords": "low voltage systems Almaty, industrial automation Kazakhstan, MCC panels, DDC controllers, electrical enclosures Almaty, KNX smart home, SCADA PLC integration",
            "badge": "Engineering Excellence",
            "h1": "INPAR — Low-Voltage Engineering, Industrial Automation & MCC/DDC Control Panels",
            "text": "Since 2014, INPAR.KZ delivers comprehensive engineering: ELV systems, industrial process automation (PLC/SCADA), custom Motor Control Center (MCC) panel assembly, DDC climate controls, and KNX smart home automation across Kazakhstan."
        }
    }.get(lang, "ru")

    services_cards = ""
    for slug, s_root in SERVICES_DATA.items():
        s_data = s_root.get(lang, s_root["ru"])
        badge_text = s_root["badge"].get(lang, s_root["badge"]["ru"])
        services_cards += f"""
        <div class="card">
            <span class="badge">{html.escape(badge_text)}</span>
            <h3><a href="{BASE_URL}{prefix}/services/{slug}">{html.escape(s_data['title'])}</a></h3>
            <p style="font-size: 14px; color: #9BA1AB;">{html.escape(s_data['description'][:140])}...</p>
            <p><a href="{BASE_URL}{prefix}/services/{slug}">Подробнее / Learn more →</a></p>
        </div>
        """

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
    }

    body_content = f"""
    <span class="badge">{html.escape(home_meta['badge'])}</span>
    <h1>{html.escape(home_meta['h1'])}</h1>
    <p style="font-size: 18px; color: #D1D5DB;">{html.escape(home_meta['text'])}</p>
    <p><a href="https://wa.me/77019954217" class="btn">WhatsApp Консультация</a></p>

    <h2>Направления деятельности / Engineering Capabilities</h2>
    <div class="grid">
        {services_cards}
    </div>
    """

    return HttpResponse(_render_base_html(home_meta['title'], home_meta['description'], home_meta['keywords'], canonical, None, [schema_organization], body_content, lang=lang, path=path), content_type="text/html; charset=utf-8")
