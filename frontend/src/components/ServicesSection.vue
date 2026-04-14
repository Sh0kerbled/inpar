<script setup>
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { Building2, Cog, Ruler, Zap } from "lucide-vue-next";

const { t } = useI18n();

const services = computed(() => [
  {
    icon: Building2,
    title: t("services.items.infrastructure.title"),
    description: t("services.items.infrastructure.desc"),
    color: "#B8A276",
  },
  {
    icon: Cog,
    title: t("services.items.integration.title"),
    description: t("services.items.integration.desc"),
    color: "#A8ADB5",
  },
  {
    icon: Ruler,
    title: t("services.items.design.title"),
    description: t("services.items.design.desc"),
    color: "#B8A276",
  },
  {
    icon: Zap,
    title: t("services.items.performance.title"),
    description: t("services.items.performance.desc"),
    color: "#3B82F6",
  },
]);
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
            {{ t("services.badge") }}
          </span>
        </div>
        <h2 class="text-5xl font-light tracking-tight">
          {{ t("services.title") }}
        </h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          v-for="(service, index) in services"
          :key="index"
          v-motion
          :initial="{ opacity: 0, y: 40 }"
          :visibleOnce="{
            opacity: 1,
            y: 0,
            transition: { duration: 600, delay: index * 100 },
          }"
          class="group relative transform transition-transform duration-300 hover:-translate-y-2"
        >
          <div
            class="relative h-full p-8 border border-[#333842] backdrop-blur-sm bg-gradient-to-br from-[#1A1D23]/40 to-[#252932]/20 transition-all duration-500 group-hover:border-[#3B82F6]/50"
          >
            <div
              class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500"
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
                class="text-xl mb-3 font-normal tracking-tight text-[#E8E9ED]"
              >
                {{ service.title }}
              </h3>
              <p class="text-[#9BA1AB] text-sm leading-relaxed font-light">
                {{ service.description }}
              </p>
            </div>

            <div
              class="absolute top-0 right-0 w-16 h-16 border-t border-r border-transparent group-hover:border-[#3B82F6]/30 transition-colors duration-500"
            />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
