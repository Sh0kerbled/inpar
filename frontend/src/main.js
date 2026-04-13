import { createApp } from "vue";
import { MotionPlugin } from "@vueuse/motion";
import { createI18n } from "vue-i18n";
import App from "./App.vue";
import "./assets/main.css";

const messages = {
  en: {
    nav: {
      engineering: "Engineering",
      services: "Services",
      partners: "Partners",
      about: "About",
      contact: "Contact",
    },
  },
  ru: {
    nav: {
      engineering: "Инженерия",
      services: "Услуги",
      partners: "Партнеры",
      about: "О компании",
      contact: "Контакты",
    },
  },
  kz: {
    nav: {
      engineering: "Инженерия",
      services: "Қызметтер",
      partners: "Серіктестер",
      about: "Біз туралы",
      contact: "Байланыс",
    },
  },
};

const i18n = createI18n({
  legacy: false,
  locale: "en",
  fallbackLocale: "en",
  messages,
});

const app = createApp(App);
app.use(MotionPlugin);
app.use(i18n);
app.mount("#app");
