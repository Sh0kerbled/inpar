<script setup>
import { ref } from "vue";

const props = defineProps({
  src: {
    type: String,
    required: true,
  },
  alt: {
    type: String,
    required: true,
  },
  customClass: {
    type: String,
    default: "",
  },
});

const hasError = ref(false);
</script>

<template>
  <img
    v-if="!hasError"
    :src="src"
    :alt="alt"
    :class="customClass"
    @error="hasError = true"
  />
  <div v-else :class="['bg-[#252932]', customClass]"></div>
</template>
