<script setup>
import { useI18n } from "vue-i18n";
const { t } = useI18n();

const currentYear = new Date().getFullYear();
</script>

<template>
  <footer class="relative py-12 px-6 lg:px-12 border-t border-[#333842]">
    <div
      class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6"
    >
      <div class="text-2xl font-light tracking-tight text-[#E8E9ED]">INPAR</div>
      <div class="text-sm text-[#9BA1AB] font-light">
        © {{ currentYear }} INPAR Engineering. {{ t("footer.description") }}
      </div>
    </div>
  </footer>
</template>
