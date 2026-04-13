<script setup>
const partners = [
  "TECHCORP",
  "VERTEX",
  "AXIOM",
  "STELLAR",
  "QUANTUM",
  "NEXUS",
  "TITAN",
  "ZENITH",
  "PULSE",
  "APEX",
  "PRIME",
  "CORE",
];
</script>

<template>
  <section
    id="partners"
    class="relative py-32 px-6 lg:px-12 border-t border-[#333842]"
  >
    <div class="max-w-7xl mx-auto">
      <div
        v-motion
        :initial="{ opacity: 0 }"
        :visibleOnce="{ opacity: 1, transition: { duration: 600 } }"
        class="text-center mb-16"
      >
        <div class="inline-flex items-center gap-4 mb-4">
          <div class="h-px w-8 bg-[#A8ADB5]" />
          <span class="text-[#A8ADB5] text-sm tracking-[0.15em] uppercase"
            >Trusted By</span
          >
          <div class="h-px w-8 bg-[#A8ADB5]" />
        </div>
        <h2 class="text-4xl font-light tracking-tight">Industry Partners</h2>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-8">
        <div
          v-for="(partner, index) in partners"
          :key="partner"
          v-motion
          :initial="{ opacity: 0, scale: 0.8 }"
          :visibleOnce="{
            opacity: 1,
            scale: 1,
            transition: { duration: 400, delay: index * 50 },
          }"
          class="flex items-center justify-center p-6 border border-[#333842]/50 bg-[#1A1D23]/40 hover:border-[#3B82F6]/30 hover:scale-105 transition-all duration-300 group"
        >
          <span
            class="text-[#A8ADB5] text-sm font-light tracking-[0.2em] group-hover:text-[#E8E9ED] transition-colors duration-300"
          >
            {{ partner }}
          </span>
        </div>
      </div>
    </div>
  </section>
</template>
