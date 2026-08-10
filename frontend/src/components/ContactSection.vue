<script setup>
import { ref, onMounted, watch, onUnmounted } from "vue";
import { useI18n } from "vue-i18n";

const { t, locale } = useI18n();
const mapContainer = ref(null);
let dgMap = null;
let marker = null;
let mapInitialized = false;

const companyCoords = [43.233071, 76.852412];

const getPopupContent = () => {
  return `
    <div style="
      color: #1A1D23; 
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      padding: 10px;
      text-align: center;
    ">
      <div style="font-weight: 600; color: #ffffff; font-size: 13px;">INPAR.KZ</div>
    </div>
  `;
};

const initMap = () => {
  if (!mapContainer.value) return;

  try {
    window.DG.then(function () {
      if (!mapInitialized && mapContainer.value) {
        const isMobile = window.innerWidth < 768;
        const zoom = isMobile ? 15 : 16;

        dgMap = window.DG.map(mapContainer.value, {
          center: companyCoords,
          zoom: zoom,
          scrollWheelZoom: false,
          fullscreenControl: true,
          fullscreenControlPosition: "topright",
          trafficControl: false,
        });

        marker = window.DG.marker(companyCoords, {
          title: "INPAR.KZ Office",
        })
          .addTo(dgMap)
          .bindPopup(getPopupContent(), {
            closeButton: true,
            maxWidth: 280,
          })
          .openPopup();

        marker.on("click", function () {
          marker.openPopup();
        });

        mapInitialized = true;
      }
    });
  } catch (error) {
    console.error("Error initializing 2GIS map:", error);
  }
};

watch(locale, () => {
  if (marker && mapInitialized) {
    marker.setPopupContent(getPopupContent());
    marker.openPopup();
  }
});

const handleResize = () => {
  if (dgMap && mapContainer.value) {
    dgMap.invalidateSize();
  }
};

onMounted(() => {
  if (!window.DG && !document.getElementById("2gis-loader")) {
    const script = document.createElement("script");
    script.id = "2gis-loader";
    script.src = "https://maps.api.2gis.ru/2.0/loader.js?pkg=full";
    script.async = true;
    script.onload = initMap;
    script.onerror = () => {
      console.error("Failed to load 2GIS API");
    };
    document.head.appendChild(script);
  } else if (window.DG) {
    setTimeout(initMap, 100);
  }

  window.addEventListener("resize", handleResize);
});

onUnmounted(() => {
  window.removeEventListener("resize", handleResize);
  if (dgMap) {
    dgMap.off();
    dgMap = null;
    marker = null;
    mapInitialized = false;
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
          class="relative h-[500px] md:h-[400px] border border-[#333842] bg-[#1A1D23]/60 overflow-hidden group rounded"
        >
          <div ref="mapContainer" class="w-full h-full" />
          <div
            class="absolute inset-0 bg-linear-to-br from-[#3B82F6]/5 to-[#B8A276]/5 pointer-events-none z-20"
          />
        </div>
      </div>
    </div>
  </section>
</template>
