<script setup>
import { ref, computed } from "vue";
import { useI18n } from "vue-i18n";
import { ChevronDown, Menu, X } from "lucide-vue-next";
import { onClickOutside } from "@vueuse/core";

const { t, locale } = useI18n();

const languages = [
  { code: "en", label: "ENG" },
  { code: "ru", label: "RU" },
  { code: "kz", label: "KZ" },
];

const navKeys = ["services", "about", "partners", "contact"];

const isLangOpen = ref(false);
const isMobileMenuOpen = ref(false);
const langDropdownRef = ref(null);

const currentLangLabel = computed(() => {
  return languages.find((l) => l.code === locale.value)?.label;
});

onClickOutside(langDropdownRef, () => {
  isLangOpen.value = false;
});

const setLang = (code) => {
  locale.value = code;
  isLangOpen.value = false;
};

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
};

const scrollToSection = (id) => {
  isMobileMenuOpen.value = false;
  const element = document.getElementById(id);

  if (element) {
    const navbarHeight = 80;
    const elementPosition = element.getBoundingClientRect().top;
    const offsetPosition = elementPosition + window.pageYOffset - navbarHeight;

    window.scrollTo({
      top: offsetPosition,
      behavior: "smooth",
    });
  }
};
</script>

<template>
  <nav
    class="fixed top-0 left-0 right-0 z-50 border-b border-[#333842]/50 bg-[#1A1D23]/80 backdrop-blur-xl"
  >
    <div class="max-w-7xl mx-auto px-6 lg:px-12">
      <div class="flex items-center justify-between h-20">
        <div
          v-motion
          :initial="{ opacity: 0, x: -20 }"
          :enter="{ opacity: 1, x: 0, transition: { duration: 600 } }"
          class="flex items-center gap-3"
        >
          <div class="text-2xl font-light tracking-tight text-[#E8E9ED]">
            INPAR
          </div>
          <div class="h-4 w-px bg-[#B8A276]" />
          <span
            class="text-xs text-[#9BA1AB] tracking-[0.15em] uppercase font-light"
          >
            {{ t("nav.engineering") }}
          </span>
        </div>

        <div
          v-motion
          :initial="{ opacity: 0, y: -10 }"
          :enter="{
            opacity: 1,
            y: 0,
            transition: { duration: 600, delay: 100 },
          }"
          class="hidden md:flex items-center gap-8"
        >
          <button
            v-for="(key, index) in navKeys"
            :key="key"
            @click="scrollToSection(key)"
            v-motion
            :initial="{ opacity: 0, y: -10 }"
            :enter="{
              opacity: 1,
              y: 0,
              transition: { duration: 400, delay: 200 + index * 100 },
            }"
            class="text-sm text-[#9BA1AB] hover:text-[#E8E9ED] transition-colors duration-300 tracking-wide relative group focus:outline-none"
          >
            {{ t(`nav.${key}`) }}
            <span
              class="absolute -bottom-1 left-0 w-0 h-px bg-gradient-to-r from-[#3B82F6] to-[#B8A276] group-hover:w-full transition-all duration-300"
            />
          </button>
        </div>

        <div
          v-motion
          :initial="{ opacity: 0, x: 20 }"
          :enter="{
            opacity: 1,
            x: 0,
            transition: { duration: 600, delay: 200 },
          }"
          class="flex items-center gap-4"
        >
          <div class="relative" ref="langDropdownRef">
            <button
              @click="isLangOpen = !isLangOpen"
              class="flex items-center gap-2 px-4 py-2 border border-[#333842] bg-[#1A1D23]/60 hover:border-[#3B82F6]/50 transition-all duration-300 group"
            >
              <span class="text-sm text-[#E8E9ED] tracking-wider font-light">
                {{ currentLangLabel }}
              </span>
              <ChevronDown
                class="w-4 h-4 text-[#9BA1AB] transition-transform duration-300"
                :style="{
                  transform: isLangOpen ? 'rotate(180deg)' : 'rotate(0deg)',
                }"
              />
            </button>

            <transition
              enter-active-class="transition duration-200 ease-out"
              enter-from-class="transform -translate-y-2 opacity-0"
              enter-to-class="transform translate-y-0 opacity-100"
              leave-active-class="transition duration-150 ease-in"
              leave-from-class="transform translate-y-0 opacity-100"
              leave-to-class="transform -translate-y-2 opacity-0"
            >
              <div
                v-if="isLangOpen"
                class="absolute top-full mt-2 right-0 min-w-[100px] border border-[#333842] bg-[#1A1D23]/95 backdrop-blur-xl overflow-hidden"
              >
                <button
                  v-for="(lang, index) in languages"
                  :key="lang.code"
                  @click="setLang(lang.code)"
                  v-motion
                  :initial="{ opacity: 0, x: -10 }"
                  :enter="{
                    opacity: 1,
                    x: 0,
                    transition: { duration: 200, delay: index * 50 },
                  }"
                  :class="[
                    'w-full px-4 py-3 text-left text-sm tracking-wider transition-all duration-200',
                    locale === lang.code
                      ? 'bg-[#3B82F6]/10 text-[#3B82F6] border-l-2 border-[#3B82F6]'
                      : 'text-[#9BA1AB] hover:bg-[#333842]/30 hover:text-[#E8E9ED] border-l-2 border-transparent',
                  ]"
                >
                  {{ lang.label }}
                </button>
              </div>
            </transition>
          </div>

          <button
            @click="toggleMobileMenu"
            class="md:hidden p-2 text-[#9BA1AB] hover:text-[#E8E9ED] transition-colors"
          >
            <Menu v-if="!isMobileMenuOpen" class="w-6 h-6" />
            <X v-else class="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>

    <transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="transform -translate-y-full opacity-0"
      enter-to-class="transform translate-y-0 opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="transform translate-y-0 opacity-100"
      leave-to-class="transform -translate-y-full opacity-0"
    >
      <div
        v-if="isMobileMenuOpen"
        class="absolute top-full left-0 right-0 border-b border-[#333842]/50 bg-[#1A1D23]/95 backdrop-blur-xl md:hidden"
      >
        <div class="px-6 py-4 flex flex-col gap-4">
          <button
            v-for="key in navKeys"
            :key="key"
            @click="scrollToSection(key)"
            class="text-sm text-[#9BA1AB] hover:text-[#E8E9ED] hover:pl-2 transition-all duration-300 tracking-wide py-2 border-b border-[#333842]/30 last:border-0 text-left focus:outline-none"
          >
            {{ t(`nav.${key}`) }}
          </button>
        </div>
      </div>
    </transition>
  </nav>
</template>
