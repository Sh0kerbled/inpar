<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";

const { t, locale } = useI18n();
const router = useRouter();

const scrolled = ref(false);
const menuOpen = ref(false);

const handleScroll = () => {
  scrolled.value = window.scrollY > 20;
};

const setLocale = (lang) => {
  locale.value = lang;
  localStorage.setItem("user-locale", lang);
};

const navLinks = [
  { key: "services", href: "/#services" },
  { key: "about", href: "/#about" },
  { key: "partners", href: "/#partners" },
  { key: "contact", href: "/#contact" },
];

const langs = ["ru", "kz", "en"];

onMounted(() => window.addEventListener("scroll", handleScroll));
onUnmounted(() => window.removeEventListener("scroll", handleScroll));
</script>

<template>
  <nav
    :class="[
      'fixed top-0 left-0 right-0 z-50 px-6 lg:px-12 py-5 transition-all duration-500',
      scrolled
        ? 'bg-[#1A1D23]/90 backdrop-blur-md border-b border-[#333842]'
        : 'bg-transparent',
    ]"
  >
    <div class="max-w-7xl mx-auto flex justify-between items-center">
      <router-link
        to="/"
        class="text-2xl font-light tracking-tight text-[#E8E9ED] hover:text-white transition-colors duration-200"
      >
        INPAR
      </router-link>

      <div class="hidden md:flex items-center gap-8">
        <a
          v-for="link in navLinks"
          :key="link.key"
          :href="link.href"
          class="text-sm text-[#9BA1AB] hover:text-[#E8E9ED] tracking-wide transition-colors duration-200"
        >
          {{ t(`nav.${link.key}`) }}
        </a>

        <router-link
          to="/products"
          class="text-sm tracking-wide px-4 py-2 border border-[#333842] text-[#9BA1AB] hover:text-[#E8E9ED] hover:border-[#3B82F6]/50 transition-all duration-200"
        >
          {{ t("nav.catalog") }}
        </router-link>

        <div
          class="flex items-center gap-1 ml-2 border-l border-[#333842] pl-4"
        >
          <button
            v-for="lang in langs"
            :key="lang"
            @click="setLocale(lang)"
            :class="[
              'text-xs tracking-widest uppercase px-2 py-1 transition-colors duration-200',
              locale === lang
                ? 'text-[#B8A276]'
                : 'text-[#9BA1AB] hover:text-[#E8E9ED]',
            ]"
          >
            {{ lang }}
          </button>
        </div>
      </div>

      <button
        class="md:hidden text-[#9BA1AB] hover:text-[#E8E9ED] transition-colors duration-200"
        @click="menuOpen = !menuOpen"
      >
        <svg
          class="w-6 h-6"
          fill="none"
          stroke="currentColor"
          stroke-width="1.5"
          viewBox="0 0 24 24"
        >
          <path
            v-if="!menuOpen"
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5"
          />
          <path
            v-else
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>
    </div>

    <div
      v-if="menuOpen"
      class="md:hidden mt-4 pb-4 border-t border-[#333842] pt-4 flex flex-col gap-4"
    >
      <a
        v-for="link in navLinks"
        :key="link.key"
        :href="link.href"
        class="text-sm text-[#9BA1AB] hover:text-[#E8E9ED] tracking-wide transition-colors duration-200"
        @click="menuOpen = false"
      >
        {{ t(`nav.${link.key}`) }}
      </a>

      <router-link
        to="/products"
        class="text-sm tracking-wide text-[#9BA1AB] hover:text-[#E8E9ED] transition-colors duration-200"
        @click="menuOpen = false"
      >
        {{ t("nav.catalog") }}
      </router-link>

      <div class="flex items-center gap-2 pt-2 border-t border-[#333842]">
        <button
          v-for="lang in langs"
          :key="lang"
          @click="setLocale(lang)"
          :class="[
            'text-xs tracking-widest uppercase px-2 py-1 transition-colors duration-200',
            locale === lang
              ? 'text-[#B8A276]'
              : 'text-[#9BA1AB] hover:text-[#E8E9ED]',
          ]"
        >
          {{ lang }}
        </button>
      </div>
    </div>
  </nav>
</template>
