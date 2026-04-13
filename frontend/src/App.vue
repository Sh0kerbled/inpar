<script setup>
import Navbar from "./components/Navbar.vue";
import HeroSection from "./components/HeroSection.vue";
import ServicesSection from "./components/ServicesSection.vue";
import AboutSection from "./components/AboutSection.vue";
import PartnersSection from "./components/PartnersSection.vue";
import ContactSection from "./components/ContactSection.vue";
import AppFooter from "./components/AppFooter.vue";
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
