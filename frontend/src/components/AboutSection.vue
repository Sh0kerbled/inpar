<script setup>
const stats = [
  { label: "Projects Delivered", value: "450+", unit: "" },
  { label: "Countries", value: "23", unit: "" },
  { label: "Technical Staff", value: "180", unit: "" },
  { label: "Uptime Guarantee", value: "99.9", unit: "%" },
];
</script>

<template>
  <section
    id="about"
    class="relative py-32 px-6 lg:px-12 border-t border-[#333842]"
  >
    <div class="max-w-7xl mx-auto">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
        <div
          v-motion
          :initial="{ opacity: 0, x: -40 }"
          :visibleOnce="{ opacity: 1, x: 0, transition: { duration: 800 } }"
        >
          <div class="flex items-center gap-4 mb-6">
            <div class="h-px w-8 bg-[#A8ADB5]" />
            <span class="text-[#A8ADB5] text-sm tracking-[0.15em] uppercase"
              >About INPAR</span
            >
          </div>
          <h2 class="text-5xl font-light tracking-tight mb-6">
            Engineering at Scale
          </h2>
          <p class="text-[#9BA1AB] text-lg leading-relaxed font-light mb-8">
            Delivering mission-critical infrastructure with uncompromising
            precision across industrial, commercial, and public sectors.
          </p>
        </div>

        <div
          v-motion
          :initial="{ opacity: 0, x: 40 }"
          :visibleOnce="{ opacity: 1, x: 0, transition: { duration: 800 } }"
          class="grid grid-cols-2 gap-6"
        >
          <div
            v-for="(stat, index) in stats"
            :key="stat.label"
            v-motion
            :initial="{ opacity: 0, scale: 0.9 }"
            :visibleOnce="{
              opacity: 1,
              scale: 1,
              transition: { duration: 500, delay: index * 100 },
            }"
            class="p-6 border border-[#333842] bg-[#1A1D23]/60"
          >
            <div class="text-4xl font-light mb-2 tracking-tight">
              <span class="text-[#E8E9ED]">{{ stat.value }}</span>
              <span class="text-[#B8A276] text-2xl">{{ stat.unit }}</span>
            </div>
            <div class="text-[#9BA1AB] text-sm tracking-wide uppercase">
              {{ stat.label }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
