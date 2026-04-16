<script setup>
import {
  Building2,
  ShieldAlert,
  Cctv,
  Network,
  Speaker,
  Home,
  Combine,
} from "lucide-vue-next";

// Если нужно, добавьте переводы для этих строк в i18n
const services = [
  {
    icon: Building2,
    title: "BMS Диспетчеризация",
    description:
      "Комплексное управление зданием. Интеграция систем в общую платформу с единым веб-интерфейсом для снижения энергозатрат.",
    color: "#B8A276",
  },
  {
    icon: ShieldAlert,
    title: "Пожарная безопасность",
    description:
      "Интеллектуальные адресные пожарные панели и системы аварийного оповещения (PA) для объектов любого масштаба.",
    color: "#D00000",
  },
  {
    icon: Cctv,
    title: "Видеонаблюдение и СКУД",
    description:
      "NVR-системы, IP-биометрия и контроль доступа. Управление авторизованным доступом с интеграцией в пожарную сеть.",
    color: "#A8ADB5",
  },
  {
    icon: Home,
    title: "Умный дом (KNX/EIB)",
    description:
      "Проектирование и интеграция домашней автоматизации. Полный контроль освещения, климата и мультимедиа.",
    color: "#3B82F6",
  },
  {
    icon: Speaker,
    title: "Профессиональный звук и свет",
    description:
      "High-End акустика, линейные массивы, робот-освещение и LED-экраны для концертов, конференц-залов и коммерции.",
    color: "#B8A276",
  },
  {
    icon: Network,
    title: "Информационные сети и SMATV",
    description:
      "Проектирование сетевой инфраструктуры, IP-телефония и системы спутникового телевидения с контролем доступа к каналам.",
    color: "#A8ADB5",
  },
  {
    icon: Combine,
    title: "Системная интеграция",
    description:
      "Бесшовная интеграция оборудования различных производителей. Настройка, симуляция программ и техподдержка.",
    color: "#3B82F6",
  },
];
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
          <span class="text-[#B8A276] text-sm tracking-[0.15em] uppercase"
            >Core Services</span
          >
        </div>
        <h2 class="text-5xl font-light tracking-tight">Сферы деятельности</h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="(service, index) in services"
          :key="service.title"
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
              class="absolute inset-0 bg-gradient-to-br from-white/[0.03] to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"
            />

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
