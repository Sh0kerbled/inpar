<script setup>
import { ref, computed } from "vue";
import { useI18n } from "vue-i18n";
import {
  Building2,
  Flame,
  Key,
  Cctv,
  Lightbulb,
  Volume2,
  Network,
  Home,
  Car,
  Wifi,
  MonitorPlay,
  Phone,
  Wind,
  Users,
  ShieldAlert,
} from "lucide-vue-next";
import essentaimg from "./img/image 1.svg";
import khanshatyr from "./img/image 2.svg";
import afd from "./img/image 3.svg";
import intercontinental from "./img/image 4.svg";
import megaekat from "./img/image 5.svg";
import forum from "./img/image 6.svg";
import libya from "./img/image 7.svg";
import holiday from "./img/image 8.svg";
import shymmega from "./img/image 9.svg";
import expo from "./img/image 10.svg";
import millitary from "./img/image 11.svg";
import kairat from "./img/image 12.svg";
import mechet from "./img/image 13.svg";
import aktobemega from "./img/image 14.svg";
import kcell from "./img/image 15.svg";
import qyzylordacenter from "./img/image 16.svg";
import bnplaza from "./img/image 17.svg";
import Navbar from "@/components/Navbar.vue";

const { t } = useI18n();

const activeFilter = ref("all");

const filters = computed(() => [
  { key: "all", label: t("projects.filters.all") },
  { key: "hotel", label: t("projects.filters.hotel") },
  { key: "mall", label: t("projects.filters.mall") },
  { key: "office", label: t("projects.filters.office") },
  { key: "residential", label: t("projects.filters.residential") },
  { key: "public", label: t("projects.filters.public") },
]);

const systemIcons = computed(() => ({
  fire: { icon: Flame, label: t("projects.systems.fire"), color: "#D00000" },
  access: { icon: Key, label: t("projects.systems.access"), color: "#B8A276" },
  cctv: { icon: Cctv, label: t("projects.systems.cctv"), color: "#A8ADB5" },
  lighting: {
    icon: Lightbulb,
    label: t("projects.systems.lighting"),
    color: "#3B82F6",
  },
  audio: {
    icon: Volume2,
    label: t("projects.systems.audio"),
    color: "#B8A276",
  },
  network: {
    icon: Network,
    label: t("projects.systems.network"),
    color: "#A8ADB5",
  },
  smart: { icon: Home, label: t("projects.systems.smart"), color: "#3B82F6" },
  parking: {
    icon: Car,
    label: t("projects.systems.parking"),
    color: "#A8ADB5",
  },
  wifi: { icon: Wifi, label: t("projects.systems.wifi"), color: "#3B82F6" },
  tv: { icon: MonitorPlay, label: t("projects.systems.tv"), color: "#B8A276" },
  hvac: { icon: Wind, label: t("projects.systems.hvac"), color: "#A8ADB5" },
  conference: {
    icon: Users,
    label: t("projects.systems.conference"),
    color: "#3B82F6",
  },
  phone: { icon: Phone, label: t("projects.systems.phone"), color: "#B8A276" },
  security: {
    icon: ShieldAlert,
    label: t("projects.systems.security"),
    color: "#D00000",
  },
}));

const projects = [
  {
    id: 1,
    name: "Almaty Esentai Ritz Carlton Hotel",
    location: "Алматы",
    type: "hotel",
    area: "325 000 м²",
    image: essentaimg,
    systems: ["fire", "access", "cctv", "lighting", "conference"],
  },
  {
    id: 2,
    name: "Astana Khan Shatyr Shopping Mall",
    location: "Астана",
    type: "mall",
    area: "110 000 м²",
    image: khanshatyr,
    systems: ["fire"],
  },
  {
    id: 3,
    name: "Almaty AFD Building",
    location: "Алматы",
    type: "office",
    image: afd,
    systems: ["access"],
  },
  {
    id: 4,
    name: "Almaty InterContinental Hotel",
    location: "Алматы",
    type: "hotel",
    image: intercontinental,
    systems: ["fire", "audio", "conference", "lighting"],
  },
  {
    id: 5,
    name: "Ekaterinburg MEGA Center",
    location: "Екатеринбург",
    type: "mall",
    image: megaekat,
    systems: ["fire", "cctv", "audio", "lighting"],
  },
  {
    id: 6,
    name: "Almaty Forum Shopping Mall",
    location: "Алматы",
    type: "mall",
    image: forum,
    systems: ["fire", "audio", "lighting"],
  },
  {
    id: 7,
    name: "Libya Tripoli El Nasr Hotel",
    location: "Триполи, Ливия",
    type: "hotel",
    image: libya,
    systems: ["fire", "access", "security", "cctv", "lighting"],
  },
  {
    id: 8,
    name: "Almaty Holiday INN Hotel",
    location: "Алматы",
    type: "hotel",
    image: holiday,
    systems: ["cctv", "access", "security", "audio"],
  },
  {
    id: 9,
    name: "Shymkent MEGA Center",
    location: "Шымкент",
    type: "mall",
    image: shymmega,
    systems: ["cctv", "access", "security", "audio", "parking"],
  },
  {
    id: 10,
    name: "Astana EXPO 2017",
    location: "Астана",
    type: "public",
    image: expo,
    systems: ["lighting", "fire"],
  },
  {
    id: 11,
    name: "Astana Military Academy",
    location: "Астана",
    type: "public",
    image: millitary,
    systems: ["lighting", "smart"],
  },
  {
    id: 12,
    name: "Almaty Beshagash KAIRAT Sport Complex",
    location: "Алматы",
    type: "public",
    image: kairat,
    systems: ["audio", "conference", "lighting", "smart", "tv"],
  },
  {
    id: 13,
    name: "Turkistan Hoca Ahmet Yesevi Religious Complex",
    location: "Туркестан",
    type: "public",
    image: mechet,
    systems: ["audio", "fire", "phone", "hvac"],
  },
  {
    id: 14,
    name: "Aktobe City Center Shopping Mall",
    location: "Актобе",
    type: "mall",
    image: aktobemega,
    systems: ["fire", "audio", "cctv", "network", "lighting", "hvac"],
  },
  {
    id: 15,
    name: "Almaty KCELL Administration Building",
    location: "Алматы",
    type: "office",
    image: kcell,
    systems: ["fire", "access", "cctv", "parking", "conference"],
  },
  {
    id: 16,
    name: "Qyzylorda Bastau Business Center",
    location: "Қызылорда",
    type: "office",
    image: qyzylordacenter,
    systems: ["fire", "cctv", "access", "conference", "audio", "hvac"],
  },
  {
    id: 17,
    name: "Almaty BN Plaza",
    location: "Алматы",
    type: "office",
    image: bnplaza,
    systems: ["audio"],
  },
  {
    id: 18,
    name: "Microsoft Almaty Main Office",
    location: "Алматы",
    type: "office",
    image:
      "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=800&q=80",
    systems: ["conference"],
  },
  {
    id: 19,
    name: "NARXOZ University",
    location: "Алматы",
    type: "public",
    image:
      "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=800&q=80",
    systems: ["audio", "conference", "lighting"],
  },
  {
    id: 20,
    name: "Almaty Orhun Medical Center",
    location: "Алматы",
    type: "public",
    image:
      "https://images.unsplash.com/photo-1586773860418-d37222d8fce3?w=800&q=80",
    systems: ["fire", "audio", "access", "network", "cctv"],
  },
  {
    id: 21,
    name: "Boroboe Golf Club VIP Villa",
    location: "Бурабай",
    type: "residential",
    image:
      "https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&q=80",
    systems: ["fire", "cctv", "network", "smart", "hvac"],
  },
  {
    id: 22,
    name: "Almaty Golf Club VIP Villa",
    location: "Алматы",
    type: "residential",
    image:
      "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&q=80",
    systems: ["fire", "cctv", "security", "smart", "audio", "wifi", "hvac"],
  },
  {
    id: 23,
    name: "Almaty Arman VIP Home",
    location: "Алматы",
    type: "residential",
    image:
      "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&q=80",
    systems: ["fire", "cctv", "smart", "audio", "wifi", "hvac"],
  },
  {
    id: 24,
    name: "Almaty Yubileyni Villa",
    location: "Алматы",
    type: "residential",
    image:
      "https://images.unsplash.com/photo-1613977257363-707ba9348227?w=800&q=80",
    systems: ["smart", "audio"],
  },
  {
    id: 25,
    name: "Shymkent Astana Motors",
    location: "Шымкент",
    type: "office",
    image:
      "https://images.unsplash.com/photo-1550355291-bbee04a92027?w=800&q=80",
    systems: ["cctv", "access", "security", "audio"],
  },
];

const filteredProjects = computed(() =>
  activeFilter.value === "all"
    ? projects
    : projects.filter((p) => p.type === activeFilter.value),
);
</script>

<template>
  <Navbar />
  <div class="min-h-screen bg-[#1A1D23]">
    <section class="relative py-32 px-6 lg:px-12">
      <div class="max-w-7xl mx-auto">
        <div
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :visibleOnce="{ opacity: 1, y: 0, transition: { duration: 700 } }"
          class="mb-16"
        >
          <div class="flex items-center gap-4 mb-4">
            <div class="h-px w-8 bg-[#B8A276]" />
            <span
              class="text-[#B8A276] text-sm tracking-[0.15em] uppercase font-light"
            >
              {{ t("projects.badge") }}
            </span>
          </div>
          <div
            class="flex flex-col lg:flex-row lg:items-end lg:justify-between gap-6"
          >
            <h2 class="text-5xl font-light tracking-tight text-[#E8E9ED]">
              {{ t("projects.title") }}
            </h2>
            <div class="flex items-center gap-3">
              <span class="text-4xl font-light text-[#B8A276]"
                >{{ projects.length }}+</span
              >
              <span
                class="text-[#9BA1AB] text-sm max-w-[140px] leading-relaxed font-light"
              >
                {{ t("projects.countLabel") }}
              </span>
            </div>
          </div>
        </div>

        <!-- Filters -->
        <div class="flex flex-wrap gap-2 mb-12">
          <button
            v-for="filter in filters"
            :key="filter.key"
            @click="activeFilter = filter.key"
            class="relative px-5 py-2 text-sm tracking-wide border transition-all duration-300"
            :class="
              activeFilter === filter.key
                ? 'border-[#B8A276] text-[#B8A276] bg-[#B8A276]/5'
                : 'border-[#333842] text-[#9BA1AB] hover:border-[#3B82F6]/50 hover:text-[#E8E9ED]'
            "
          >
            {{ filter.label }}
          </button>
        </div>

        <!-- Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <Transition
            v-for="(project, index) in filteredProjects"
            :key="project.id"
            name="project-card"
          >
            <div
              v-motion
              :initial="{ opacity: 0, y: 50, scale: 0.9 }"
              :visibleOnce="{
                opacity: 1,
                y: 0,
                scale: 1,
                transition: { duration: 500, delay: (index % 9) * 50, easing: 'cubic-bezier(0.34, 1.56, 0.64, 1)' },
              }"
              class="group relative flex flex-col border border-[#333842] bg-gradient-to-br from-[#1A1D23]/60 to-[#252932]/30 overflow-hidden transition-all duration-500 hover:border-[#B8A276]/40"
            >
            <!-- Image -->
            <div class="relative h-52 overflow-hidden">
              <img
                :src="project.image"
                :alt="project.name"
                loading="lazy"
                width="800"
                height="450"
                class="w-full h-full object-cover opacity-60 group-hover:opacity-80 group-hover:scale-105 transition-all duration-700"
              />
              <div
                class="absolute inset-0 bg-gradient-to-t from-[#1A1D23] via-[#1A1D23]/30 to-transparent pointer-events-none"
              />
              <div class="absolute top-4 left-4">
                <span
                  class="inline-flex items-center px-3 py-1 bg-[#1A1D23]/80 border border-[#333842] text-[#A8ADB5] text-xs tracking-wide uppercase backdrop-blur-sm"
                >
                  {{ project.location }}
                </span>
              </div>
              <div v-if="project.area" class="absolute top-4 right-4">
                <span
                  class="inline-flex items-center px-3 py-1 bg-[#B8A276]/15 border border-[#B8A276]/30 text-[#B8A276] text-xs"
                >
                  {{ project.area }}
                </span>
              </div>
            </div>

            <!-- Info -->
            <div class="flex flex-col flex-1 p-6">
              <h3
                class="text-lg font-normal tracking-tight text-[#E8E9ED] mb-4 leading-snug group-hover:text-white transition-colors duration-300"
              >
                {{ project.name }}
              </h3>
              <div class="flex flex-wrap gap-2 mt-auto">
                <div
                  v-for="sysKey in project.systems"
                  :key="sysKey"
                  class="inline-flex items-center gap-1.5 px-2.5 py-1 border border-[#333842] bg-[#252932]/60"
                >
                  <component
                    :is="systemIcons[sysKey]?.icon"
                    class="w-3 h-3 flex-shrink-0"
                    :style="{ color: systemIcons[sysKey]?.color }"
                    :stroke-width="2"
                  />
                  <span class="text-[#9BA1AB] text-xs font-light">
                    {{ systemIcons[sysKey]?.label }}
                  </span>
                </div>
              </div>
            </div>

            <div
              class="absolute top-0 right-0 w-16 h-16 border-t border-r border-transparent group-hover:border-[#B8A276]/30 transition-colors duration-500 pointer-events-none"
            />
            </div>
          </Transition>
        </div>

        <!-- Empty -->
        <div
          v-if="filteredProjects.length === 0"
          class="flex flex-col items-center justify-center py-24 text-[#9BA1AB]"
        >
          <Building2 class="w-12 h-12 mb-4 text-[#333842]" :stroke-width="1" />
          <p class="text-lg font-light">{{ t("projects.empty") }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.project-card-enter-active {
  transition: all 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.project-card-leave-active {
  transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.project-card-enter-from {
  opacity: 0;
  transform: translateY(50px) scale(0.85);
  filter: blur(4px);
}

.project-card-leave-to {
  opacity: 0;
  transform: translateY(-100px) scale(0.75) rotateX(10deg);
  filter: blur(6px);
}

@keyframes smoothEntry {
  from {
    opacity: 0;
    transform: translateY(50px) scale(0.85);
    filter: blur(4px);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0px);
  }
}
</style>
