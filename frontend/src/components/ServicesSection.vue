<script setup>
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import {
  Building2,
  ShieldAlert,
  Cctv,
  Network,
  Speaker,
  Home,
  Combine,
  ArrowRight,
  Layers,
  Cpu,
  Box,
  Factory
} from "lucide-vue-next";

const { t, locale } = useI18n();

const servicesList = [
  {
    slug: "mcc-cabinets",
    icon: Layers,
    color: "#3B82F6",
    title: {
      ru: "Шкафы управления двигателями MCC и ЧРП",
      kz: "MCC қозғалтқыштарды басқару шкафтары мен ЖТ",
      en: "Motor Control Centers (MCC) & VFD Panels"
    },
    desc: {
      ru: "Сборка силовых шкафов MCC, щитов управления насосными станциями и двигателями с частотными преобразователями.",
      kz: "Жиілік түрлендіргіштері бар MCC күштік шкафтарын және сорғы станцияларын басқару қалқандарын құрастыру.",
      en: "Custom assembly of Motor Control Centers (MCC), pump stations, and variable frequency drive (VFD) cabinets."
    }
  },
  {
    slug: "ddc-automation",
    icon: Cpu,
    color: "#B8A276",
    title: {
      ru: "Шкафы и контроллеры DDC (ОВиК)",
      kz: "DDC басқару шкафтары мен контроллерлері",
      en: "Direct Digital Control (DDC) HVAC Panels"
    },
    desc: {
      ru: "Прямое цифровое управление вентиляцией, ИТП и климатом на базе свободно программируемых контроллеров.",
      kz: "Бағдарламаланатын DDC контроллерлері негізінде желдету және жылу пункттерін тікелей цифрлық басқару.",
      en: "Field programmable DDC controllers and automation panels for air handling units, heating, and chillers."
    }
  },
  {
    slug: "electrical-cabinets",
    icon: Box,
    color: "#EAB308",
    title: {
      ru: "Сборка электрошкафов (ЩА, ЩУ, ВРУ, ГРЩ)",
      kz: "Электр шкафтарын құрастыру (ЩА, ЩУ, ВРУ, ГРЩ)",
      en: "Custom Electrical Enclosures (MDB, LVSG)"
    },
    desc: {
      ru: "Сертифицированное электрощитовое производство в Алматы: сборка шкафов автоматики и распределения по схемам заказчика.",
      kz: "Алматыдағы жеке сертификатталған электрощит өндірісі: автоматика және тарату шкафтарын тапсырыспен жинау.",
      en: "Certified in-house electrical panel building: automation, distribution boards, and main switchgear."
    }
  },
  {
    slug: "industrial-automation",
    icon: Factory,
    color: "#EF4444",
    title: {
      ru: "Индустриальная автоматизация и АСУ ТП",
      kz: "Өндірістік автоматтандыру және АСУ ТП",
      en: "Industrial Automation & SCADA Systems"
    },
    desc: {
      ru: "Автоматизация технологических процессов производств, программирование промышленных ПЛК и разработка SCADA.",
      kz: "Технологиялық процестерді кешенді автоматтандыру, өндірістік ПЛК бағдарламалау және SCADA әзірлеу.",
      en: "Complete industrial process automation, PLC logic programming, and supervisory SCADA development."
    }
  },
  {
    slug: "low-voltage-systems",
    icon: Network,
    color: "#06B6D4",
    title: {
      ru: "Слаботочные системы под ключ",
      kz: "Төменгі ток жүйелері кілтке дейін",
      en: "Turnkey Low-Voltage (ELV) Systems"
    },
    desc: {
      ru: "Полный цикл проектирования и монтажа слаботочных сетей (СКС, СКУД, CCTV, АПС, СОУЭ) для зданий любого масштаба.",
      kz: "Кез келген ауқымдағы нысандарға арналған әлсіз ток желілерін (СКС, СКУД, өрт дабылы, дыбыс) толық жобалау және монтаждау.",
      en: "Comprehensive engineering and installation of all Extra Low Voltage building subsystems."
    }
  },
  {
    slug: "smart-home-knx",
    icon: Home,
    color: "#3B82F6",
    title: {
      ru: "Умный дом стандарта KNX/EIB",
      kz: "KNX стандартындағы Ақылды үй",
      en: "Smart Home KNX/EIB Automation"
    },
    desc: {
      ru: "Проектирование и интеграция домашней автоматизации KNX: освещение, шторы, климат, мультирум и безопасность.",
      kz: "KNX үй автоматикасын жобалау және интеграциялау: жарық, перделер, климат және қауіпсіздік.",
      en: "Premium residential automation engineered on the global KNX standard for lighting, climate, and AV."
    }
  },
  {
    slug: "bms-dispatching",
    icon: Building2,
    color: "#B8A276",
    title: {
      ru: "Диспетчеризация BMS",
      kz: "BMS диспетчерлеу",
      en: "BMS Building Dispatching"
    },
    desc: {
      ru: "Комплексное управление инженерными системами здания на единой платформе для снижения энергозатрат до 30%.",
      kz: "Энергия шығындарын 30%-ға дейін азайту үшін ғимарат жүйелерін бірыңғай платформаға біріктіру.",
      en: "Integrated building management platforms to monitor and optimize multi-system energy efficiency."
    }
  },
  {
    slug: "fire-safety",
    icon: ShieldAlert,
    color: "#D00000",
    title: {
      ru: "Пожарная безопасность (АПС/СОУЭ)",
      kz: "Өрт қауіпсіздігі (АПС/СОУЭ)",
      en: "Fire Safety & Evacuation (PA/VA)"
    },
    desc: {
      ru: "Адресная пожарная сигнализация, системы оповещения и управления эвакуацией 1-5 типов по нормам РК.",
      kz: "ҚР нормаларына сәйкес адрестік өрт дабылы және 1-5 үлгідегі хабарландыру жүйелері.",
      en: "Addressable fire detection and multi-zone voice alarm evacuation systems."
    }
  },
  {
    slug: "cctv-access-control",
    icon: Cctv,
    color: "#A8ADB5",
    title: {
      ru: "Видеонаблюдение и СКУД",
      kz: "Бейнебақылау және СКУД",
      en: "CCTV Surveillance & Access Control"
    },
    desc: {
      ru: "IP-видеонаблюдение высокой четкости с ИИ-аналитикой, Face ID терминалы доступа и турникеты.",
      kz: "Жасанды интеллектісі бар IP-бейнебақылау, Face ID биометриялық рұқсат бақылауы және турникеттер.",
      en: "AI-powered IP video analytics, biometric Face ID terminals, and turnstile perimeter access."
    }
  },
  {
    slug: "sound-and-light",
    icon: Speaker,
    color: "#B8A276",
    title: {
      ru: "Профессиональный звук и свет",
      kz: "Кәсіби дыбыс және жарық",
      en: "Pro Audio & Stage Lighting"
    },
    desc: {
      ru: "Акустический расчет, линейные массивы, микрофонные парки и сценический DMX свет для залов и сцен.",
      kz: "Залдар мен сахналарға арналған акустикалық есептеу, сызықтық массивтер және DMX жарық жүйелері.",
      en: "Acoustic simulations, line array sound systems, and intelligent DMX stage lighting."
    }
  },
  {
    slug: "networks-smatv",
    icon: Network,
    color: "#A8ADB5",
    title: {
      ru: "Информационные сети и SMATV",
      kz: "Ақпараттық желілер және SMATV",
      en: "Structured Cabling & SMATV"
    },
    desc: {
      ru: "СКС 5e/6/6A/7, оптоволоконные магистрали ВОЛС, бесшовный корпоративный Wi-Fi и гостиничное IPTV.",
      kz: "СКС желілері, оптика дәнекерлеу, үздіксіз Wi-Fi және қонақүйлерге арналған интерактивті IPTV.",
      en: "Enterprise Cat 6A/7 cabling, fiber optic links, high-density Wi-Fi, and interactive hotel IPTV."
    }
  },
  {
    slug: "system-integration",
    icon: Combine,
    color: "#3B82F6",
    title: {
      ru: "Системная интеграция под ключ",
      kz: "Жүйелік интеграция кілтке дейін",
      en: "Master Systems Integration"
    },
    desc: {
      ru: "Генеральный подряд по слаботочным системам: объединение разрозненного оборудования в единую экосистему.",
      kz: "Әлсіз ток желілері бойынша бас мердігерлік: барлық жабдықты бірыңғай экожүйеге біріктіру.",
      en: "Single-source master integration of low-voltage technology into a coordinated facility ecosystem."
    }
  }
];

const currentLang = computed(() => locale.value || "ru");

const services = computed(() => {
  const l = currentLang.value;
  return servicesList.map((item) => ({
    slug: item.slug,
    icon: item.icon,
    color: item.color,
    title: item.title[l] || item.title.ru,
    description: item.desc[l] || item.desc.ru
  }));
});

const sectionBadge = computed(() => {
  const l = currentLang.value;
  return l === "kz" ? "Негізгі қызметтер" : (l === "en" ? "Core Engineering" : "Основные услуги");
});

const sectionTitle = computed(() => {
  const l = currentLang.value;
  return l === "kz" ? "Инженерлік мүмкіндіктер" : (l === "en" ? "Engineering Capabilities" : "Направления и возможности");
});

const learnMoreText = computed(() => {
  const l = currentLang.value;
  return l === "kz" ? "Толық ақпарат" : (l === "en" ? "Learn more" : "Подробнее об услуге");
});

const getServiceLink = (slug) => {
  const l = currentLang.value;
  return l === "ru" ? `/services/${slug}` : `/${l}/services/${slug}`;
};
</script>

<template>
  <section id="services" class="relative py-32 px-6 lg:px-12">
    <div class="max-w-7xl mx-auto">
      <div
        v-motion
        :initial="{ opacity: 0 }"
        :visibleOnce="{ opacity: 1, transition: { duration: 600 } }"
        class="mb-20"
      >
        <div class="flex items-center gap-4 mb-4">
          <div class="h-px w-8 bg-[#B8A276]" />
          <span class="text-[#B8A276] text-sm tracking-[0.15em] uppercase">
            {{ sectionBadge }}
          </span>
        </div>
        <h2 class="text-4xl md:text-5xl font-light tracking-tight text-white">
          {{ sectionTitle }}
        </h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="(service, index) in services"
          :key="service.slug"
          v-motion
          :initial="{ opacity: 0, y: 40 }"
          :visibleOnce="{
            opacity: 1,
            y: 0,
            transition: { duration: 500, delay: (index % 3) * 100 },
          }"
          class="group relative transform transition-transform duration-300 hover:-translate-y-2"
        >
          <div
            class="relative h-full p-8 border border-[#333842] backdrop-blur-sm bg-gradient-to-br from-[#1A1D23]/40 to-[#252932]/20 transition-all duration-500 group-hover:border-[#3B82F6]/50 rounded-xl flex flex-col justify-between"
          >
            <div
              class="absolute inset-0 bg-gradient-to-br from-white/[0.03] to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-xl pointer-events-none"
            />
            <div
              class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 rounded-xl pointer-events-none"
              :style="{ boxShadow: `inset 0 0 60px ${service.color}15` }"
            />
            <div class="relative z-10">
              <component
                :is="service.icon"
                class="w-8 h-8 mb-6 transition-colors duration-300"
                :style="{ color: service.color }"
                :stroke-width="1.5"
              />
              <h3
                class="text-xl mb-3 font-normal tracking-tight text-[#E8E9ED] group-hover:text-white transition-colors"
              >
                {{ service.title }}
              </h3>
              <p class="text-[#9BA1AB] text-sm leading-relaxed font-light mb-6">
                {{ service.description }}
              </p>
            </div>

            <div class="relative z-10 pt-2 border-t border-[#333842]/40">
              <router-link
                :to="getServiceLink(service.slug)"
                class="inline-flex items-center gap-2 text-xs uppercase tracking-wider text-[#B8A276] hover:text-[#3B82F6] transition-colors font-medium"
              >
                {{ learnMoreText }}
                <ArrowRight class="w-3.5 h-3.5 transition-transform group-hover:translate-x-1" />
              </router-link>
            </div>

            <div
              class="absolute top-0 right-0 w-16 h-16 border-t border-r border-transparent group-hover:border-[#3B82F6]/30 transition-colors duration-500 rounded-tr-xl pointer-events-none"
            />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
