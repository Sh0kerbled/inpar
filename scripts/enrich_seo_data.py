# scripts/enrich_seo_data.py
# Enriching SERVICES_DATA with Knowledge Graph entities, Problem-Solution matrices, and conversational FAQs

ENRICHMENTS = {
    "mcc-cabinets": {
        "knowsAbout": [
            {"name": "Motor Control Center", "sameAs": "https://www.wikidata.org/wiki/Q175185"},
            {"name": "Variable-frequency drive", "sameAs": "https://www.wikidata.org/wiki/Q1055745"},
            {"name": "Motor soft starter", "sameAs": "https://www.wikidata.org/wiki/Q1760467"}
        ],
        "related_services": ["electrical-cabinets", "bms-dispatching", "industrial-automation"],
        "ru": {
            "keywords": ", защита насоса от гидроудара, автоматизация КНС ХВС, плавный пуск насосов, шкафы Danfoss Schneider ABB",
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
            ],
            "faqs": [
                {
                    "q": "Как шкаф MCC защищает от гидроударов в водопроводе?",
                    "a": "Частотный преобразователь плавно изменяет частоту тока (от 0 до 50 Гц), исключая резкий скачок давления в трубах при старте и останове насосных агрегатов."
                },
                {
                    "q": "Можно ли подключить шкаф управления MCC к общей системе SCADA или диспетчеризации здания?",
                    "a": "Да, наши шкафы комплектуются интерфейсами RS-485 Modbus RTU, Ethernet Modbus TCP или Profinet для передачи всех параметров (ток, давление, аварии, наработка моточасов) на пульт диспетчера."
                }
            ]
        },
        "kz": {
            "keywords": ", гидросоққыдан қорғау, сорғыларды автоматтандыру, жұмсақ іске қосу шкафы, сорғы станциялары",
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
            ],
            "faqs": [
                {
                    "q": "MCC шкафтары сорғыларды қалай қорғайды?",
                    "a": "Жиілік түрлендіргіш қозғалтқышты бірқалыпты іске қосады, құбырлардағы қысымның күрт көтерілуін жояды және фазалардың қисаюын бақылайды."
                }
            ]
        },
        "en": {
            "keywords": ", water hammer prevention, pump soft starters, industrial MCC panels, motor protection relays",
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
            ],
            "faqs": [
                {
                    "q": "Can your MCC panels integrate with third-party BMS or SCADA platforms?",
                    "a": "Yes, we integrate Modbus RTU/TCP, BACnet, and Profinet communication cards to stream operating currents, pressures, and diagnostic fault codes to any supervisory station."
                }
            ]
        }
    },

    "ddc-automation": {
        "knowsAbout": [
            {"name": "Direct digital control", "sameAs": "https://www.wikidata.org/wiki/Q5271878"},
            {"name": "HVAC control system", "sameAs": "https://www.wikidata.org/wiki/Q5635832"},
            {"name": "Building automation", "sameAs": "https://www.wikidata.org/wiki/Q629239"}
        ],
        "related_services": ["bms-dispatching", "mcc-cabinets", "electrical-cabinets"],
        "ru": {
            "keywords": ", защита калорифера от замерзания, шкафы автоматики вентиляции, приводы Belimo 0-10V, контроллеры Segnetics Carel, автоматика ИТП",
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
            ],
            "faqs": [
                {
                    "q": "Как DDC защищает калорифер от разморозки при внезапном отключении электричества?",
                    "a": "При пропадании питания привод воздушной заслонки с возвратной пружиной немедленно захлопывается, а клапан теплоносителя открывается на 100%, предотвращая доступ ледяного уличного воздуха к водяным трубкам."
                },
                {
                    "q": "Контроллеры каких производителей вы используете в сборке DDC?",
                    "a": "Мы используем надежные контроллеры Segnetics (Pixel, Matrix), Carel, Siemens Desigo, Danfoss и ОВЕН в зависимости от технического задания и бюджета заказчика."
                }
            ]
        },
        "kz": {
            "keywords": ", калориферді қатып қалудан қорғау, желдету автоматикасы шкафы, Belimo жетектері, DDC контроллерлері",
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
            ],
            "faqs": [
                {
                    "q": "DDC жүйесі калориферді қатып қалудан қалай сақтайды?",
                    "a": "Жүйе кері қайтқан су температурасын үнемі бақылап, апаттық жағдайда сыртқы ауа қақпағын жауып, жылу клапанын толық ашады."
                }
            ]
        },
        "en": {
            "keywords": ", HVAC frost protection, air handling unit control panel, Belimo valve actuators, DDC AHU controllers",
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
            ],
            "faqs": [
                {
                    "q": "How does DDC protect against coil freeze during utility power loss?",
                    "a": "Spring-return damper actuators instantly close against incoming sub-zero air while hot water modulating valves default to 100% open."
                }
            ]
        }
    },

    "electrical-cabinets": {
        "knowsAbout": [
            {"name": "Electric switchboard", "sameAs": "https://www.wikidata.org/wiki/Q1141753"},
            {"name": "Distribution board", "sameAs": "https://www.wikidata.org/wiki/Q1411516"},
            {"name": "Automatic transfer switch", "sameAs": "https://www.wikidata.org/wiki/Q4826573"}
        ],
        "related_services": ["mcc-cabinets", "industrial-automation", "low-voltage-systems"],
        "ru": {
            "keywords": ", сборка щитов по схеме, шкаф АВР на генератор, ВРУ ГРЩ с паспортом, сертификаты технадзор электрощиты",
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
            ],
            "faqs": [
                {
                    "q": "Предоставляются ли сертификаты и паспорта на готовые шкафы?",
                    "a": "Каждый шкаф проходит заводские испытания и отгружается с паспортом изделия, схемой соединений, гарантийным талоном и сертификатом соответствия ЕАС."
                },
                {
                    "q": "Каковы сроки производства электрощитов ВРУ и ГРЩ?",
                    "a": "Сборка стандартных щитов занимает от 5 до 12 рабочих дней, сложных ГРЩ до 4000А с АВР — от 15 до 25 дней."
                }
            ]
        },
        "kz": {
            "keywords": ", бірсызықты схема бойынша жинау, АВР генератор қалқаны, ВРУ ГРЩ паспорты, техқадағалау сертификаттары",
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
            ],
            "faqs": [
                {
                    "q": "Қалқандарға ресми сертификат беріле ме?",
                    "a": "Иә, барлық қалқандар зауыттық сынақтан өтіп, ЕАС сәйкестік сертификатымен және паспортымен тапсырылады."
                }
            ]
        },
        "en": {
            "keywords": ", custom SLD switchboard, ATS generator panels, MDB switchgear passports, certified electrical panels Kazakhstan",
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
            ],
            "faqs": [
                {
                    "q": "Do your switchgear panels include test documentation and warranty?",
                    "a": "Yes, every panel is supplied with full factory test reports, SLDs, serial passports, and an official multi-year warranty."
                }
            ]
        }
    },

    "industrial-automation": {
        "knowsAbout": [
            {"name": "Industrial control system", "sameAs": "https://www.wikidata.org/wiki/Q211050"},
            {"name": "Programmable logic controller", "sameAs": "https://www.wikidata.org/wiki/Q173491"},
            {"name": "SCADA", "sameAs": "https://www.wikidata.org/wiki/Q211050"}
        ],
        "related_services": ["mcc-cabinets", "bms-dispatching", "system-integration"],
        "ru": {
            "keywords": ", модернизация станков ПЛК, разработка SCADA систем, программирование Siemens Schneider ОВЕН, АСУ ТП цеха",
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
            ],
            "faqs": [
                {
                    "q": "С какими промышленными контроллерами (ПЛК) вы работаете?",
                    "a": "Мы разрабатываем ПО для Siemens Simatic, Schneider Electric (Modicon), ОВЕН, Delta, Mitsubishi Electric, Wecon и других платформ."
                },
                {
                    "q": "Возможна ли поэтапная модернизация завода без полной остановки производства?",
                    "a": "Да, мы разрабатываем стратегию параллельной сборки и переключения узлов в технологические «окна» или межсменные интервалы, чтобы минимизировать простои."
                }
            ]
        },
        "kz": {
            "keywords": ", станоктарды жаңғырту ПЛК, SCADA диспетчерлеу, өндірісті автоматтандыру, өндірістік желілер",
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
            ],
            "faqs": [
                {
                    "q": "Өндірісті тоқтатпай жаңғыртуға бола ма?",
                    "a": "Иә, біз жаңа шкафтарды алдын ала дайындап, ауыстыруды демалыс немесе техникалық үзілістер кезінде жүргіземіз."
                }
            ]
        },
        "en": {
            "keywords": ", PLC programming Siemens Schneider Owen, SCADA system development, factory machine retrofit, process automation",
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
            ],
            "faqs": [
                {
                    "q": "Can you modernize machinery without stopping ongoing plant operations?",
                    "a": "Yes, we build and test new control enclosures offsite and perform rapid cutovers during planned maintenance shifts."
                }
            ]
        }
    },

    "low-voltage-systems": {
        "knowsAbout": [
            {"name": "Extra-low voltage", "sameAs": "https://www.wikidata.org/wiki/Q1255858"},
            {"name": "Structured cabling", "sameAs": "https://www.wikidata.org/wiki/Q1363294"},
            {"name": "Access control", "sameAs": "https://www.wikidata.org/wiki/Q13410526"},
            {"name": "Fire alarm system", "sameAs": "https://www.wikidata.org/wiki/Q1365389"}
        ],
        "related_services": ["cctv-access-control", "networks-smatv", "fire-safety"],
        "ru": {
            "keywords": ", слаботочка под ключ Алматы, монтаж СКС СКУД видеонаблюдение, подрядчик слаботочных систем, оптоволокно ВОЛС",
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
            ],
            "faqs": [
                {
                    "q": "Какие слаботочные системы вы монтируете под ключ?",
                    "a": "Мы выполняем полный комплекс: СКС, ВОЛС, IP-видеонаблюдение, СКУД, адресную пожарную сигнализацию (АПС), систему оповещения и управления эвакуацией (СОУЭ), домофонию и фоновый звук."
                },
                {
                    "q": "Предоставляете ли вы исполнительную документацию для технадзора и ДЧС?",
                    "a": "Да, мы оформляем полный комплект исполнительных чертежей, кабельных журналов, актов скрытых работ и протоколов замеров изоляции."
                }
            ]
        },
        "kz": {
            "keywords": ", слаботочка кілтке дейін, әлсіз токты желілер монтаж, СКС кабель тарту, СКУД турникет Face-ID",
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
            ],
            "faqs": [
                {
                    "q": "Қандай нысандармен жұмыс істейсіздер?",
                    "a": "Кеңселер, қоймалар, логистикалық орталықтар, бизнес-орталықтар, зауыттар мен көпқабатты тұрғын үй кешендері."
                }
            ]
        },
        "en": {
            "keywords": ", turnkey ELV contractor, structured cabling installation, access control CCTV integration, commercial low voltage",
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
            ],
            "faqs": [
                {
                    "q": "Do you provide as-built documentation for building commissioning authorities?",
                    "a": "Yes, we produce complete as-built CAD drawings, cable schedules, Fluke test certificates, and compliance declarations."
                }
            ]
        }
    },

    "smart-home-knx": {
        "knowsAbout": [
            {"name": "KNX (standard)", "sameAs": "https://www.wikidata.org/wiki/Q1889"},
            {"name": "Home automation", "sameAs": "https://www.wikidata.org/wiki/Q2818960"},
            {"name": "Lighting control system", "sameAs": "https://www.wikidata.org/wiki/Q1842844"}
        ],
        "related_services": ["bms-dispatching", "electrical-cabinets", "sound-and-light"],
        "ru": {
            "keywords": ", умный дом проводной knx, выключатели knx Zennio Jung ABB, сценарии умный дом, управление светом DALI",
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
            ],
            "faqs": [
                {
                    "q": "Почему для коттеджа или большой квартиры выбирают проводной KNX, а не беспроводные системы?",
                    "a": "KNX — это промышленный европейский стандарт с децентрализованной шиной: если откажет один прибор, остальные продолжат работать. Он не забивает Wi-Fi эфир, не зависит от облачных серверов и работает стабильно десятилетиями."
                },
                {
                    "q": "Можно ли управлять умным домом KNX с iPhone через приложение 'Дом' (Apple HomeKit)?",
                    "a": "Да, мы устанавливаем сертифицированные шлюзы, позволяющие управлять светом, шторами, сценариями и климатом через Apple HomeKit, Siri, Google Assistant и Яндекс Алису."
                }
            ]
        },
        "kz": {
            "keywords": ", сымды KNX ақылды үй, DALI жарық басқару, ақылды үй сценарийлері, коттеджге ақылды үй бағасы",
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
            ],
            "faqs": [
                {
                    "q": "KNX Ақылды үйінің қарапайым жүйелерден айырмашылығы неде?",
                    "a": "Бұл еуропалық өндірістік стандарт. Ол интернетке немесе орталық серверге тәуелді емес, сондықтан ешқашан ілінбейді және өте ұзақ қызмет етеді."
                }
            ]
        },
        "en": {
            "keywords": ", hardwired KNX automation, DALI-2 architectural lighting, Apple HomeKit KNX, luxury smart home Kazakhstan",
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
            ],
            "faqs": [
                {
                    "q": "Can I control my KNX home using Apple HomeKit and Siri?",
                    "a": "Yes, we integrate certified bidirectional bridges allowing native control via Apple HomeKit, Siri voice commands, and Apple Watch widgets."
                }
            ]
        }
    },

    "bms-dispatching": {
        "knowsAbout": [
            {"name": "Building management system", "sameAs": "https://www.wikidata.org/wiki/Q629239"},
            {"name": "BACnet", "sameAs": "https://www.wikidata.org/wiki/Q795493"},
            {"name": "Modbus", "sameAs": "https://www.wikidata.org/wiki/Q1130095"}
        ],
        "related_services": ["ddc-automation", "mcc-cabinets", "system-integration"],
        "ru": {
            "keywords": ", диспетчеризация зданий BMS, автоматизация ИТП котельных, протоколы BACnet Modbus, энергосбережение зданий",
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
            ],
            "faqs": [
                {
                    "q": "Можно ли подключить к BMS оборудование разных производителей?",
                    "a": "Да, BMS строится на открытых международных протоколах BACnet, Modbus, KNX, что позволяет объединить приточки одного бренда, чиллеры другого и насосы третьего в единую систему."
                }
            ]
        },
        "kz": {
            "keywords": ", BMS жүйелері Алматы, ғимаратты диспетчерлеу, BACnet Modbus хаттамалары, энергия үнемдеу",
            "problems": [
                {
                    "problem": "Апат болған кезде инженерлердің кеш хабардар болуы.",
                    "solution": "Диспетчерлік мониторинг және Telegram арқылы лезде ескерту.",
                    "benefit": "Апаттарды алғашқы минуттарда жедел жою."
                }
            ],
            "faqs": [
                {
                    "q": "BMS жүйесі қандай үнем береді?",
                    "a": "Жылыту мен электр қуатын тек қажет уақытта тұтыну арқылы коммуналдық шығындарды 20-30% төмендетеді."
                }
            ]
        },
        "en": {
            "keywords": ", BMS dispatching Kazakhstan, BACnet IP Modbus supervisory, building energy optimization, central plant monitoring",
            "problems": [
                {
                    "problem": "Facility teams unaware of equipment failures until tenant comfort complaints escalate.",
                    "solution": "Continuous automated BMS telemetry streaming telemetry and instantaneous engineer notification.",
                    "benefit": "Proactive resolution of equipment malfunctions before tenant impact or structural damage occurs."
                }
            ],
            "faqs": [
                {
                    "q": "Can legacy chillers and third-party panels be bridged into the BMS?",
                    "a": "Yes, we integrate open standard protocol gateways (BACnet, Modbus, SNMP) to bring multi-vendor hardware into a unified operator workstation."
                }
            ]
        }
    },

    "fire-safety": {
        "knowsAbout": [
            {"name": "Fire alarm system", "sameAs": "https://www.wikidata.org/wiki/Q1365389"},
            {"name": "Smoke detector", "sameAs": "https://www.wikidata.org/wiki/Q189578"}
        ],
        "related_services": ["low-voltage-systems", "sound-and-light", "bms-dispatching"],
        "ru": {
            "keywords": ", сдача АПС в ДЧС, монтаж пожарной сигнализации, речевое оповещение СОУЭ 1-5 типов, обслуживание пожарки",
            "problems": [
                {
                    "problem": "Риск штрафов, приостановки деятельности объекта или отказа ввода в эксплуатацию инспекцией ДЧС.",
                    "solution": "Лицензированный монтаж сертифицированного оборудования строго по СН РК с полным пакетом исполнительных актов.",
                    "benefit": "Безупречная приемка объекта инспекцией пожарного надзора с первого раза."
                }
            ],
            "faqs": [
                {
                    "q": "Имеет ли ваша компания лицензию на монтаж пожарной сигнализации?",
                    "a": "Да, у нас есть все государственные лицензии и квалифицированные специалисты для проектирования, монтажа и обслуживания систем пожарной безопасности в РК."
                }
            ]
        },
        "kz": {
            "keywords": ", өрт дабылын монтаждау, ТЖД тапсыру, СОУЭ құлақтандыру жүйесі, өрт қауіпсіздігі лицензия",
            "problems": [
                {
                    "problem": "ТЖД инспекциясының айыппұл салу немесе нысанды қабылдамау қаупі.",
                    "solution": "ҚР нормаларына сай ресми лицензиямен сапалы монтаждау.",
                    "benefit": "Нысанды өрт қауіпсіздігі органдарына кедергісіз тапсыру."
                }
            ],
            "faqs": [
                {
                    "q": "Құжаттарды ТЖД-ға тапсыруға көмектесесіздер ме?",
                    "a": "Иә, толық атқарушылық сызбалар мен актілерді дайындап, инспекцияның қабылдауына дейін сүйемелдейміз."
                }
            ]
        },
        "en": {
            "keywords": ", fire alarm certification Kazakhstan, emergency voice evacuation PAVA, addressable fire detection, life safety",
            "problems": [
                {
                    "problem": "Risk of regulatory shutdown and failure to pass mandatory state fire safety inspections.",
                    "solution": "Turnkey licensed installation of certified fire equipment with comprehensive testing protocols.",
                    "benefit": "Guaranteed first-time inspection acceptance by emergency authorities."
                }
            ],
            "faqs": [
                {
                    "q": "Do you hold state licenses for fire safety engineering?",
                    "a": "Yes, INPAR holds all required state certifications and licensing for fire safety and emergency evacuation engineering in Kazakhstan."
                }
            ]
        }
    },

    "cctv-access-control": {
        "knowsAbout": [
            {"name": "Closed-circuit television", "sameAs": "https://www.wikidata.org/wiki/Q215705"},
            {"name": "Biometrics", "sameAs": "https://www.wikidata.org/wiki/Q178706"},
            {"name": "Access control", "sameAs": "https://www.wikidata.org/wiki/Q13410526"}
        ],
        "related_services": ["low-voltage-systems", "networks-smatv", "system-integration"],
        "ru": {
            "keywords": ", СКУД турникеты Face-ID, видеонаблюдение для склада, распознавание автономеров шлагбаум, учет рабочего времени 1С",
            "problems": [
                {
                    "problem": "Хищения на складе или в торговом зале из-за 'слепых зон' и плохого качества старых аналоговых камер.",
                    "solution": "Установка профессиональных IP-камер 4K с ультрашироким углом обзора, WDR и ночной цветной подсветкой (ColorVu/FullColor).",
                    "benefit": "100% покрытие территории и детализированное видео лиц и номеров даже в полной темноте."
                }
            ],
            "faqs": [
                {
                    "q": "Какое оборудование вы используете для видеонаблюдения и СКУД?",
                    "a": "Мы работаем с официальными поставщиками Dahua, Hikvision, Sigur, Perco, Came, Uniview и предоставляем заводскую гарантию."
                }
            ]
        },
        "kz": {
            "keywords": ", СКУД Face-ID орнату, көлік нөмірін танитын шлагбаум, бейнебақылау камералары 4K, қойма күзеті",
            "problems": [
                {
                    "problem": "Ескі камералардың сапасыздығынан түнде адамдар мен көлік нөмірлерінің көрінбеуі.",
                    "solution": "Түнгі түрлі-түсті көру жүйесі бар заманауи 4K IP-камераларды орнату.",
                    "benefit": "Нысанның тәулік бойы толық қауіпсіздігі."
                }
            ],
            "faqs": [
                {
                    "q": "Камераларға кепілдік беріле ме?",
                    "a": "Иә, біз орнататын барлық ресми жабдықтарға 1 жылдан 3 жылға дейін кепілдік және сервистік қолдау ұсынамыз."
                }
            ]
        },
        "en": {
            "keywords": ", Face-ID turnstile access control, commercial 4K CCTV, LPR license plate barrier, HR time tracking integration",
            "problems": [
                {
                    "problem": "Stock theft or unauthorized perimeter intrusions masked by blurry analog footage and coverage blind spots.",
                    "solution": "Deploying commercial 4K ultra-wide IP cameras with advanced true WDR and low-light color imaging.",
                    "benefit": "Crystal-clear evidential identification of faces and vehicle plates day and night."
                }
            ],
            "faqs": [
                {
                    "q": "What equipment manufacturers do you install?",
                    "a": "We install enterprise-grade platforms from Dahua, Hikvision, Sigur, Perco, Came, and Uniview with manufacturer warranties."
                }
            ]
        }
    },

    "sound-and-light": {
        "knowsAbout": [
            {"name": "Public address system", "sameAs": "https://www.wikidata.org/wiki/Q1340156"},
            {"name": "Acoustics", "sameAs": "https://www.wikidata.org/wiki/Q82811"}
        ],
        "related_services": ["fire-safety", "smart-home-knx", "low-voltage-systems"],
        "ru": {
            "keywords": ", фоновое озвучивание ресторанов, акустика 100V OBT, конференц-связь для залов, постановочный свет DMX",
            "problems": [
                {
                    "problem": "Плохая разборчивость речи, гул, эхо и неравномерная громкость в залах ресторанов или конференц-комнатах.",
                    "solution": "Компьютерное акустическое моделирование помещения, подбор диаграммы направленности колонок и точная настройка DSP-процессора.",
                    "benefit": "Кристально чистый звук, комфортный уровень громкости за каждым столом и отсутствие утомляемости гостей."
                }
            ],
            "faqs": [
                {
                    "q": "Поставляете ли вы акустику OBT, которую можно увидеть в каталоге товаров?",
                    "a": "Да, INPAR является прямым дистрибьютором и интегратором профессиональных акустических систем OBT (усилители, настенные колонны, потолочные динамики) в Казахстане."
                }
            ]
        },
        "kz": {
            "keywords": ", мейрамханаға фондық дыбыс, OBT акустикасы Алматы, конференц залдарды жабдықтау, сахналық жарық DMX",
            "problems": [
                {
                    "problem": "Залдағы жаңғырық пен дыбыстың бұзылуы.",
                    "solution": "Акустикалық есептеу жүргізу және DSP дыбыс процессорларын дәл баптау.",
                    "benefit": "Залдың әрбір нүктесінде таза және жағымды дыбыс."
                }
            ],
            "faqs": [
                {
                    "q": "Каталогтағы OBT акустикасын көтерме бағамен сатып алуға бола ма?",
                    "a": "Иә, біз OBT жабдықтарын Қазақстан бойынша тікелей жеткізуші болып табыламыз және көтерме бағамен ұсынамыз."
                }
            ]
        },
        "en": {
            "keywords": ", commercial background music 100V, restaurant acoustics, conference room AV systems, OBT audio distribution",
            "problems": [
                {
                    "problem": "Poor speech intelligibility, acoustic flutter echoes, and fatiguing sound levels in restaurants or halls.",
                    "solution": "Predictive acoustic mapping, targeted dispersion speaker selection, and calibrated DSP equalization.",
                    "benefit": "Warm, crystal-clear audio balance across every seating zone."
                }
            ],
            "faqs": [
                {
                    "q": "Do you supply OBT commercial audio hardware listed in your catalog?",
                    "a": "Yes, INPAR is a direct distributor and integrator of certified OBT commercial audio products in Kazakhstan."
                }
            ]
        }
    },

    "networks-smatv": {
        "knowsAbout": [
            {"name": "Computer network", "sameAs": "https://www.wikidata.org/wiki/Q1301371"},
            {"name": "Fiber-optic communication", "sameAs": "https://www.wikidata.org/wiki/Q162"}
        ],
        "related_services": ["low-voltage-systems", "cctv-access-control", "system-integration"],
        "ru": {
            "keywords": ", монтаж СКС Fluke тестирование, сварка оптоволокна ВОЛС, серверные шкафы 19 дюймов, телевидение IPTV для отелей",
            "problems": [
                {
                    "problem": "Обрывы связи и низкая скорость корпоративной сети из-за некачественных скруток и перегибов кабеля.",
                    "solution": "Монтаж сертифицированной СКС с соблюдением радиусов изгиба и обязательным тестированием приборами Fluke Networks.",
                    "benefit": "Гарантированная гигабитная скорость передачи данных и отсутствие потерь пакетов."
                }
            ],
            "faqs": [
                {
                    "q": "Проводите ли вы тестирование СКС профессиональными кабельными сканерами?",
                    "a": "Да, каждая смонтированная линия проходит проверку кабельным анализатором Fluke Networks с выдачей графических протоколов сертификации."
                }
            ]
        },
        "kz": {
            "keywords": ", СКС монтаж Fluke тестілеу, оптика дәнекерлеу, серверлік бөлмелер, қонақ үйге IPTV орнату",
            "problems": [
                {
                    "problem": "Сервердегі ретсіздік және интернет жылдамдығының төмендеуі.",
                    "solution": "Кәсіби СКС құру және Fluke аспабымен тестілеу.",
                    "benefit": "Тұрақты жоғары жылдамдықты желі және реттелген сервер."
                }
            ],
            "faqs": [
                {
                    "q": "Оптиканы дәнекерлеу қызметін көрсетесіздер ме?",
                    "a": "Иә, біз кәсіби жапондық дәнекерлеу аппараттарымен оптикалық кабельдерді сапалы дәнекерлейміз."
                }
            ]
        },
        "en": {
            "keywords": ", Fluke certified structured cabling, fiber fusion splicing OTDR, telecom rack dressing, hospitality IPTV SMATV",
            "problems": [
                {
                    "problem": "Network connection drops and packet loss caused by substandard wiring terminations.",
                    "solution": "Installing certified structured cabling using strict bend-radius rules and mandatory Fluke Networks qualification.",
                    "benefit": "Guaranteed gigabit throughput and zero downtime for mission-critical IT services."
                }
            ],
            "faqs": [
                {
                    "q": "Do you provide Fluke test certification reports?",
                    "a": "Yes, every installed drop is verified with Fluke Networks DTX/DSX analyzers with complete PDF pass reports."
                }
            ]
        }
    },

    "system-integration": {
        "knowsAbout": [
            {"name": "Systems engineering", "sameAs": "https://www.wikidata.org/wiki/Q216353"},
            {"name": "Systems integrator", "sameAs": "https://www.wikidata.org/wiki/Q3244837"}
        ],
        "related_services": ["bms-dispatching", "industrial-automation", "low-voltage-systems"],
        "ru": {
            "keywords": ", генеральный подрядчик инжиниринг, интеграция слаботочки автоматики, пусконаладочные работы ПНР, сервисное ТО",
            "problems": [
                {
                    "problem": "Инженерные системы здания (вентиляция, чиллеры, котельная, пожарка, электрика) работают автономно, не синхронизированы и конфликтуют друг с другом.",
                    "solution": "Комплексная интеграция всех разделов от INPAR: сведение всех протоколов и систем в единую интеллектуальную цифровую экосистему.",
                    "benefit": "Слаженная работа всех инженерных узлов, снижение энергозатрат до 30% и полное отсутствие аварийных несогласованностей."
                }
            ],
            "faqs": [
                {
                    "q": "Почему выгоднее нанять одного интегратора вместо десятка узких подрядчиков?",
                    "a": "Один генеральный интегратор несет полную ответственность за конечный результат, исключает несогласованность кабельных трасс и обеспечивает слаженную работу всех систем без взаимных обвинений субподрядчиков."
                }
            ]
        },
        "kz": {
            "keywords": ", инженерлік жүйелердің бас мердігері, кешенді интеграциялау, автоматика мен әлсіз токты біріктіру",
            "problems": [
                {
                    "problem": "Ғимараттағы желдету, жылыту және өрт жүйелерінің бөлек жұмыс істеуі және келіспеушілігі.",
                    "solution": "Барлық жүйелерді INPAR арқылы біртұтас цифрлық экожүйеге біріктіру.",
                    "benefit": "Жүйелердің мінсіз үйлесімді жұмысы және шығындарды 30% үнемдеу."
                }
            ],
            "faqs": [
                {
                    "q": "Кешенді интеграция не үшін қажет?",
                    "a": "Ғимараттың барлық жүйелері өзара байланыста жұмыс істеп, апаттардың алдын алады және пайдалану шығындарын барынша азайтады."
                }
            ]
        },
        "en": {
            "keywords": ", master systems integrator, turnkey building engineering, commissioning agent, cross-system protocol integration",
            "problems": [
                {
                    "problem": "Siloed building systems (HVAC, fire, chillers, power) operating independently and causing conflicting control cycles.",
                    "solution": "Comprehensive master system integration uniting all field equipment into a singular intelligent digital control plane.",
                    "benefit": "Flawless inter-system coordination, up to 30% reduction in utility waste, and zero contractor finger-pointing."
                }
            ],
            "faqs": [
                {
                    "q": "Why hire a Master Systems Integrator (MSI) instead of isolated trade contractors?",
                    "a": "An MSI guarantees overall functionality, eliminates interface disputes, streamlines pathways, and delivers a unified building intelligence platform with single-point accountability."
                }
            ]
        }
    }
}
