<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useProductStore } from "../stores/index";
import { useI18n } from "vue-i18n";
import { ArrowLeft, ShoppingCart, Tag } from "lucide-vue-next";
import Navbar from "../components/Navbar.vue";
import api from "../services/api";

const route = useRoute();
const router = useRouter();
const productStore = useProductStore();
const { t } = useI18n();
const exchangeRate = ref(460);

onMounted(async () => {
  // Получить текущий курс доллара
  try {
    const rateResponse = await api.get("/exchange-rate/");
    exchangeRate.value = rateResponse.data.rate;
  } catch (err) {
    console.error("Failed to get exchange rate:", err);
    // Используем значение по умолчанию (460)
  }

  await productStore.getProduct(route.params.id);
});

const product = productStore.currentProduct;

const getProductPriceKzt = () => {
  if (!product || !product.price_kzt) {
    if (!product || !product.price_usd) return 0;
    // Fallback: если price_kzt не пришел с API, считаем сами
    return (product.price_usd * exchangeRate.value).toFixed(0);
  }
  return product.price_kzt;
};
</script>

<template>
  <div class="min-h-screen bg-[#13151A] text-[#E8E9ED]">
    <Navbar />

    <div class="max-w-7xl mx-auto px-6 lg:px-12 pt-36 pb-20">
      <!-- Loading -->
      <div
        v-if="productStore.isLoading"
        class="flex items-center justify-center py-32"
      >
        <p class="text-[#9BA1AB] font-light">{{ t("catalog.loading") }}</p>
      </div>

      <!-- Not found -->
      <div
        v-else-if="!productStore.currentProduct"
        class="flex flex-col items-center justify-center py-32 gap-4"
      >
        <p class="text-[#9BA1AB] font-light">{{ t("catalog.notFound") }}</p>
        <button
          @click="router.push('/products')"
          class="text-sm text-[#3B82F6] hover:text-[#60A5FA] transition-colors font-light"
        >
          ← Вернуться в каталог
        </button>
      </div>

      <!-- Product -->
      <div v-else>
        <!-- Back -->
        <button
          @click="router.push('/products')"
          class="flex items-center gap-2 text-sm text-[#9BA1AB] hover:text-[#E8E9ED] transition-colors duration-200 mb-12 font-light"
        >
          <ArrowLeft class="w-4 h-4" :stroke-width="1.5" />
          {{ t("catalog.title") }}
        </button>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16">
          <!-- Image -->
          <div
            class="aspect-square bg-[#1A1D23] border border-[#333842] overflow-hidden"
          >
            <img
              v-if="productStore.currentProduct.main_image"
              :src="productStore.currentProduct.main_image"
              :alt="productStore.currentProduct.name"
              class="w-full h-full object-cover"
            />
            <div
              v-else
              class="w-full h-full flex items-center justify-center text-[#9BA1AB]/30"
            >
              <ShoppingCart class="w-16 h-16" :stroke-width="1" />
            </div>
          </div>

          <!-- Info -->
          <div class="flex flex-col justify-center">
            <!-- Category -->
            <div
              v-if="productStore.currentProduct.category_name"
              class="flex items-center gap-2 mb-6"
            >
              <Tag class="w-3.5 h-3.5 text-[#B8A276]" :stroke-width="1.5" />
              <span
                class="text-xs text-[#B8A276] tracking-widest uppercase font-light"
              >
                {{ productStore.currentProduct.category_name }}
              </span>
            </div>

            <h1
              class="text-4xl lg:text-5xl font-light tracking-tight text-[#E8E9ED] mb-6"
            >
              {{ productStore.currentProduct.name }}
            </h1>

            <p
              class="text-[#9BA1AB] text-base leading-relaxed font-light mb-10"
            >
              {{ productStore.currentProduct.description }}
            </p>

            <!-- Price -->
            <div class="flex items-baseline gap-2 mb-6">
              <span class="text-4xl font-light text-[#3B82F6]">
                {{ getProductPriceKzt() }}
              </span>
              <span class="text-xl text-[#9BA1AB]">₸</span>
            </div>

            <!-- Stock -->
            <div class="mb-10">
              <span
                v-if="productStore.currentProduct.stock_quantity > 0"
                class="text-sm text-[#B8A276] font-light"
              >
                {{ t("catalog.inStock") }}
                {{ productStore.currentProduct.stock_quantity }} шт.
              </span>
              <span v-else class="text-sm text-[#9BA1AB]/50 font-light">
                {{ t("catalog.outOfStock") }}
              </span>
            </div>

            <!-- Divider -->
            <div class="h-px bg-[#333842] mb-10" />

            <!-- Characteristics -->
            <div
              v-if="productStore.currentProduct.characteristics?.length"
              class="space-y-3"
            >
              <p
                class="text-xs text-[#9BA1AB] tracking-widest uppercase font-light mb-4"
              >
                Характеристики
              </p>
              <div
                v-for="char in productStore.currentProduct.characteristics"
                :key="char.id"
                class="flex justify-between items-center py-3 border-b border-[#333842]/50"
              >
                <span class="text-sm text-[#9BA1AB] font-light">{{
                  char.name
                }}</span>
                <span class="text-sm text-[#E8E9ED] font-light">{{
                  char.value
                }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
