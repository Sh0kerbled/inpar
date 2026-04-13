<script setup>
import { computed } from "vue";
import { useWindowScroll } from "@vueuse/core";
import ImageWithFallback from "./ImageWithFallback.vue";

const { y } = useWindowScroll();

const heroImageY = computed(() => `${y.value * 0.1}px`);
const heroOpacity = computed(() => Math.max(1 - y.value / 500, 0));
</script>

<template>
  <section class="relative h-screen flex items-center overflow-hidden pt-20">
    <div
      class="absolute inset-0 bg-gradient-to-br from-[#1A1D23] via-[#1A1D23]/95 to-[#252932]/80 z-10"
    />

    <div
      class="absolute inset-0 z-0"
      :style="{ transform: `translateY(${heroImageY})`, opacity: heroOpacity }"
    >
      <ImageWithFallback
        src="https://images.unsplash.com/photo-1760246964044-1384f71665b9?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxoaWdoLXRlY2glMjBtb2Rlcm4lMjBidWlsZGluZyUyMGFyY2hpdGVjdHVyZXxlbnwxfHx8fDE3NzYwNTc2NTB8MA&ixlib=rb-4.1.0&q=80&w=1080"
        alt="Modern high-tech building"
        customClass="w-full h-full object-cover opacity-40"
      />
    </div>

    <div class="relative z-20 max-w-7xl mx-auto px-6 lg:px-12 w-full">
      <div class="max-w-3xl">
        <div
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{
            opacity: 1,
            y: 0,
            transition: { duration: 800, delay: 200 },
          }"
          class="mb-6"
        >
          <div class="inline-flex items-center gap-3 mb-8">
            <span
              class="text-[#B8A276] text-sm tracking-[0.2em] uppercase font-light"
              >Engineering Excellence</span
            >
            <div
              class="h-px w-12 bg-gradient-to-r from-[#B8A276] to-transparent"
            />
          </div>

          <h1
            class="text-7xl lg:text-8xl font-light tracking-tight mb-6 leading-[0.95]"
          >
            <span class="block text-[#E8E9ED]">INPAR</span>
          </h1>
        </div>

        <p
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{
            opacity: 1,
            y: 0,
            transition: { duration: 800, delay: 400 },
          }"
          class="text-xl lg:text-2xl text-[#9BA1AB] mb-10 max-w-2xl font-light leading-relaxed"
        >
          Precision-engineered infrastructure solutions for complex technical
          environments.
        </p>

        <div
          v-motion
          :initial="{ opacity: 0, y: 30 }"
          :enter="{
            opacity: 1,
            y: 0,
            transition: { duration: 800, delay: 600 },
          }"
        >
          <button
            class="group relative px-8 py-4 bg-transparent border border-[#333842] text-[#E8E9ED] overflow-hidden transition-all duration-300 hover:border-[#3B82F6]"
          >
            <span class="relative z-10 tracking-wide">Explore Projects</span>
            <div
              class="absolute inset-0 bg-gradient-to-r from-[#3B82F6]/0 via-[#3B82F6]/10 to-[#3B82F6]/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-700"
            />
            <div
              class="absolute inset-0 border border-[#3B82F6]/0 group-hover:border-[#3B82F6]/50 transition-colors duration-300"
              style="box-shadow: 0 0 20px rgba(59, 130, 246, 0)"
            />
          </button>
        </div>
      </div>
    </div>

    <div
      class="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[#333842] to-transparent z-20"
    />
  </section>
</template>
