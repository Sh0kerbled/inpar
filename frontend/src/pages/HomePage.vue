<script setup>
import { onMounted } from "vue";
import Navbar from "../components/Navbar.vue";
import HeroSection from "../components/HeroSection.vue";
import ServicesSection from "../components/ServicesSection.vue";
import AboutSection from "../components/AboutSection.vue";
import PartnersSection from "../components/PartnersSection.vue";
import ContactSection from "../components/ContactSection.vue";
import AppFooter from "../components/AppFooter.vue";
import { updateSEO } from "../utils/seo";

onMounted(() => {
  updateSEO({
    title: "INPAR.KZ — Системная интеграция, Умный дом KNX и BMS в Алматы",
    description: "Компания INPAR.KZ с 2014 года выполняет проектирование, монтаж и интеграцию слаботочных систем, автоматизации зданий (BMS), пожарной безопасности и умных домов KNX в Казахстане.",
    keywords: "умный дом Алматы, KNX Казахстан, BMS диспетчеризация, пожарная сигнализация, видеонаблюдение, СКУД, профессиональный звук, слаботочные системы, INPAR",
    url: "https://inpar.kz/"
  });
});
</script>

<template>
  <div
    class="min-h-screen bg-[#1A1D23] text-[#E8E9ED] font-['Inter',sans-serif] overflow-x-hidden"
  >
    <Navbar />
    <HeroSection />
    <ServicesSection />
    <AboutSection />
    <PartnersSection />
    <ContactSection />
    <AppFooter />
  </div>
</template>
