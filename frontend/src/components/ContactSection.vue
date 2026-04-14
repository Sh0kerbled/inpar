<script setup>
import { ref, onMounted, watch } from "vue";
import { useI18n } from "vue-i18n";

const { t, locale } = useI18n();
const mapContainer = ref(null);
let dgMap = null;
let marker = null;

const initMap = () => {
  if (window.DG) {
    window.DG.then(() => {
      dgMap = window.DG.map(mapContainer.value, {
        center: [43.233071, 76.852412],
        zoom: 16,
        scrollWheelZoom: false,
        fullscreenControl: false,
      });

      marker = window.DG.marker([43.233071, 76.852412])
        .addTo(dgMap)
        .bindPopup(getPopupContent());
    });
  }
};

const getPopupContent = () => {
  return `<div style="color: #1A1D23; font-family: Inter, sans-serif;">
    <b>INPAR.KZ</b><br/>${t("contact.address")}
  </div>`;
};

watch(locale, () => {
  if (marker) {
    marker.setPopupContent(getPopupContent());
  }
});

onMounted(() => {
  if (!document.getElementById("2gis-loader")) {
    const script = document.createElement("script");
    script.id = "2gis-loader";
    script.src = "https://maps.api.2gis.ru/2.0/loader.js?pkg=full";
    script.onload = initMap;
    document.head.appendChild(script);
  } else {
    initMap();
  }
});
</script>

<template>
  <section
    id="contact"
    class="relative py-32 px-6 lg:px-12 border-t border-[#333842]"
  >
    <div class="max-w-7xl mx-auto">
      <div
        v-motion
        :initial="{ opacity: 0 }"
        :visibleOnce="{ opacity: 1, transition: { duration: 600 } }"
        class="mb-20"
      >
        <div class="flex items-center gap-4 mb-4">
          <div class="h-px w-8 bg-[#B8A276]" />
          <span class="text-[#B8A276] text-sm tracking-[0.15em] uppercase">{{
            t("contact.badge")
          }}</span>
        </div>
        <h2 class="text-5xl font-light tracking-tight">
          {{ t("contact.title") }}
        </h2>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <div
          v-motion
          :initial="{ opacity: 0, x: -40 }"
          :visibleOnce="{ opacity: 1, x: 0, transition: { duration: 800 } }"
          class="space-y-8"
        >
          <div class="group">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-1 h-8 bg-[#3B82F6]" />
              <h3 class="text-xl font-normal tracking-tight text-[#E8E9ED]">
                {{ t("contact.office") }}
              </h3>
            </div>
            <div class="pl-7">
              <p
                class="text-[#9BA1AB] font-light leading-relaxed whitespace-pre-line"
              >
                {{ t("contact.address").replace(/, /g, ",\n") }}
              </p>
            </div>
          </div>

          <div class="group">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-1 h-8 bg-[#B8A276]" />
              <h3 class="text-xl font-normal tracking-tight text-[#E8E9ED]">
                {{ t("contact.details") }}
              </h3>
            </div>
            <div class="pl-7 space-y-3">
              <div>
                <div
                  class="text-xs text-[#9BA1AB] tracking-wider uppercase mb-1"
                >
                  {{ t("contact.phone") }}
                </div>
                <a
                  href="tel:+77273923211"
                  class="text-[#E8E9ED] hover:text-[#3B82F6] transition-colors duration-300 font-light"
                  >+7 (727) 392 32 11</a
                >
              </div>
              <div>
                <div
                  class="text-xs text-[#9BA1AB] tracking-wider uppercase mb-1"
                >
                  {{ t("contact.email") }}
                </div>
                <a
                  href="mailto:info@inpar.kz"
                  class="text-[#E8E9ED] hover:text-[#3B82F6] transition-colors duration-300 font-light"
                  >info@inpar.kz</a
                >
              </div>
              <div>
                <div
                  class="text-xs text-[#9BA1AB] tracking-wider uppercase mb-1"
                >
                  {{ t("contact.hours") }}
                </div>
                <p class="text-[#E8E9ED] font-light">
                  {{ t("contact.weekdays") }}: 09:00 - 18:00
                </p>
              </div>
            </div>
          </div>
        </div>

        <div
          v-motion
          :initial="{ opacity: 0, x: 40 }"
          :visibleOnce="{ opacity: 1, x: 0, transition: { duration: 800 } }"
          class="relative h-[400px] border border-[#333842] bg-[#1A1D23]/60 overflow-hidden group p-2"
        >
          <div ref="mapContainer" class="w-full h-full relative z-10"></div>
          <div
            class="absolute inset-0 bg-gradient-to-br from-[#3B82F6]/5 to-[#B8A276]/5 pointer-events-none z-20"
          />
        </div>
      </div>
    </div>
  </section>
</template>
