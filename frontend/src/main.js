import { createApp } from "vue";
import { MotionPlugin } from "@vueuse/motion";
import { createI18n } from "vue-i18n";
import App from "./App.vue";
import "./assets/main.css";

const getRuntimeLocale = () => {
  const savedLocale = localStorage.getItem("user-locale");
  return savedLocale || "ru";
};

const messages = {
  en: {
    nav: {
      engineering: "Engineering",
      services: "Services",
      partners: "Partners",
      about: "About",
      contact: "Contact",
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
    },
    about: {
      badge: "About INPAR Company",
      title: "Engineering at scale",
      description:
        "Delivering critical infrastructure with uncompromising precision across the industrial, commercial, and public sectors.",
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
  },
  ru: {
    nav: {
      engineering: "Engineering",
      services: "Услуги",
      partners: "Партнеры",
      about: "О компании",
      contact: "Контакты",
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
    },
    about: {
      badge: "О компании INPAR",
      title: "Инженерия в масштабе",
      description:
        "Поставка критически важной инфраструктуры с бескомпромиссной точностью в промышленном, коммерческом и государственном секторах.",
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
  },
  kz: {
    nav: {
      engineering: "Engineering",
      services: "Қызметтер",
      partners: "Серіктестер",
      about: "Біз туралы",
      contact: "Байланыс",
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
    },
    about: {
      badge: "INPAR компаниясы туралы",
      title: "Кең ауқымды инженерия",
      description:
        "Өнеркәсіптік, коммерциялық және мемлекеттік секторларда аса маңызды инфрақұрылымды мінсіз дәлдікпен қамтамасыз ету.",
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
      address: "«Сарыарқа» ТҮ, 1-ші ықшамаудан, 68/4, Алматы, Қазақстан",
    },
    footer: {
      description: "Жоғары дәлдіктегі инфрақұрылымдық шешімдер.",
    },
  },
};

const i18n = createI18n({
  legacy: false,
  locale: getRuntimeLocale(),
  fallbackLocale: "en",
  messages,
});

const app = createApp(App);
app.use(MotionPlugin);
app.use(i18n);
app.mount("#app");
