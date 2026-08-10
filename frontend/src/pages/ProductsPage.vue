<script setup>
import { ref, onMounted, computed } from "vue";
import { useI18n } from "vue-i18n";
import { Search, ShoppingCart } from "lucide-vue-next";
import { useProductStore } from "../stores/index";
import Navbar from "@/components/Navbar.vue";
import api from "../services/api";

const { t } = useI18n();
const productStore = useProductStore();

const searchQuery = ref("");
const selectedCategory = ref("");
const sortBy = ref("");
const categories = ref([]);
const exchangeRate = ref(null);

const displayExchangeRate = computed(() => {
  return exchangeRate.value ? Number(exchangeRate.value).toFixed(2) : "...";
});

const search = async () => {
  const params = {};
  if (searchQuery.value) params.search = searchQuery.value;
  if (selectedCategory.value) params.category = selectedCategory.value;
  if (sortBy.value) params.ordering = sortBy.value;
  await productStore.getProducts(params);
};

onMounted(async () => {
  try {
    const rateResponse = await api.get("/exchange-rate/");
    exchangeRate.value = rateResponse.data.rate;
  } catch (err) {
    console.error("Failed to get exchange rate:", err);
  }

  categories.value = await productStore.getCategories();
  await search();
});

const displayProducts = computed(() => productStore.products || []);

const getProductPriceKzt = (product) => {
  const usd = parseFloat(product.price_usd || 0);
  const rate = exchangeRate.value ? parseFloat(exchangeRate.value) : 0;
  const price = usd * rate;
  return price ? price.toFixed(2) : "0.00";
};
</script>

<template>
  <Navbar />
  <div class="min-h-screen bg-[#1A1D23] text-[#E8E9ED] py-20">
    <div class="max-w-7xl mx-auto px-6 lg:px-12">
      <div
        v-motion
        :initial="{ opacity: 0, y: -20 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 600 } }"
        class="mb-16 text-center"
      >
        <div class="inline-flex items-center gap-3 mb-4">
          <div class="h-px w-6 bg-linear-to-r from-transparent to-[#B8A276]" />
          <span
            class="text-[#B8A276] text-xs tracking-[0.15em] uppercase font-light"
          >
            {{ t("catalog.badge") }}
          </span>
          <div class="h-px w-6 bg-linear-to-l from-transparent to-[#B8A276]" />
        </div>
        <h1 class="text-5xl lg:text-6xl font-light tracking-tight mb-4">
          {{ t("catalog.title") }}
        </h1>
        <p class="text-[#9BA1AB] text-lg font-light max-w-2xl mx-auto">
          {{ t("catalog.description") }}
        </p>
      </div>

      <div
        v-motion
        :initial="{ opacity: 0, y: 20 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 600, delay: 100 } }"
        class="mb-16"
      >
        <div
          class="bg-[#13151A]/70 border border-[#333842] backdrop-blur-sm p-8 space-y-6"
        >
          <div
            class="flex flex-col gap-3 p-4 rounded-3xl border border-[#3B82F6]/10 bg-[#1A1D23]/70"
          >
            <p
              class="text-xs text-[#9BA1AB] uppercase tracking-[0.25em] font-light"
            >
              Курс USD → KZT
            </p>
            <div class="flex flex-wrap items-center gap-3">
              <span class="text-2xl font-semibold text-[#B8A276]">
                ₸{{ displayExchangeRate }}
              </span>
              <span class="text-sm text-[#9BA1AB]">за 1 USD</span>
            </div>
          </div>
          <div>
            <label
              class="block text-xs text-[#9BA1AB] tracking-[0.15em] uppercase mb-3 font-light"
            >
              {{ t("catalog.search") }}
            </label>
            <div class="relative">
              <Search
                class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-[#9BA1AB]"
              />
              <input
                v-model="searchQuery"
                type="text"
                :placeholder="t('catalog.searchPlaceholder')"
                class="w-full pl-12 pr-4 py-3 bg-[#1A1D23]/60 border border-[#333842] text-[#E8E9ED] placeholder-[#9BA1AB]/50 focus:outline-none focus:border-[#3B82F6] transition-colors duration-300 font-light"
                @keyup.enter="search"
              />
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label
                class="block text-xs text-[#9BA1AB] tracking-[0.15em] uppercase mb-3 font-light"
              >
                {{ t("catalog.category") }}
              </label>
              <select
                v-model="selectedCategory"
                class="w-full px-4 py-3 bg-[#1A1D23]/60 border border-[#333842] text-[#E8E9ED] focus:outline-none focus:border-[#3B82F6] transition-colors duration-300 font-light appearance-none cursor-pointer"
                @change="search"
              >
                <option value="">{{ t("catalog.allCategories") }}</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                  {{ cat.name }}
                </option>
              </select>
            </div>

            <div>
              <label
                class="block text-xs text-[#9BA1AB] tracking-[0.15em] uppercase mb-3 font-light"
              >
                {{ t("catalog.sorting") }}
              </label>
              <select
                v-model="sortBy"
                class="w-full px-4 py-3 bg-[#1A1D23]/60 border border-[#333842] text-[#E8E9ED] focus:outline-none focus:border-[#3B82F6] transition-colors duration-300 font-light appearance-none cursor-pointer"
                @change="search"
              >
                <option value="">{{ t("catalog.sortDefault") }}</option>
                <option value="price">{{ t("catalog.sortPriceAsc") }}</option>
                <option value="-price">{{ t("catalog.sortPriceDesc") }}</option>
                <option value="name">{{ t("catalog.sortName") }}</option>
                <option value="-created_at">{{ t("catalog.sortNew") }}</option>
              </select>
            </div>

            <div class="flex items-end">
              <button
                @click="search"
                class="w-full group relative px-6 py-3 bg-transparent border border-[#333842] text-[#E8E9ED] overflow-hidden transition-all duration-300 hover:border-[#3B82F6] focus:outline-none font-light"
              >
                <div
                  class="absolute inset-0 bg-linear-to-r from-[#3B82F6]/0 via-[#3B82F6]/10 to-[#3B82F6]/0 -translate-x-full group-hover:translate-x-full transition-transform duration-700"
                />
                <span class="relative z-10">{{ t("catalog.search") }}</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div
        v-if="productStore.isLoading"
        class="flex items-center justify-center py-20"
      >
        <div class="text-[#9BA1AB] text-center">
          <p class="font-light">{{ t("catalog.loading") }}</p>
        </div>
      </div>

      <div
        v-else-if="displayProducts.length === 0"
        class="flex items-center justify-center py-20"
      >
        <div class="text-center">
          <p class="text-[#9BA1AB] font-light">{{ t("catalog.notFound") }}</p>
        </div>
      </div>

      <div
        v-else
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
      >
        <RouterLink
          v-for="(product, index) in displayProducts"
          :key="product.id"
          :to="`/products/${product.id}`"
          v-motion
          :initial="{ opacity: 0, y: 20 }"
          :visibleOnce="{
            opacity: 1,
            y: 0,
            transition: { duration: 400, delay: index * 50 },
          }"
          class="group relative"
        >
          <div
            class="h-full bg-linear-to-br from-[#1A1D23]/40 to-[#252932]/20 border border-[#333842] backdrop-blur-sm overflow-hidden transition-all duration-300 hover:-translate-y-2 hover:border-[#3B82F6]/50 hover:shadow-2xl hover:shadow-[#3B82F6]/10"
          >
            <div class="aspect-square bg-[#1A1D23]/60 overflow-hidden relative">
              <img
                v-if="product.main_image"
                :src="product.main_image"
                :alt="product.name"
                class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
              />
              <div
                v-else
                class="w-full h-full flex items-center justify-center text-[#9BA1AB]/50"
              >
                <ShoppingCart class="w-12 h-12" />
              </div>

              <div
                v-if="product.category_name"
                class="absolute top-4 left-4 px-3 py-1 bg-[#B8A276]/20 border border-[#B8A276]/50 text-[#B8A276] text-xs font-light tracking-wider"
              >
                {{ product.category_name }}
              </div>
            </div>

            <!-- Content -->
            <div class="p-6">
              <!-- Product Name -->
              <h3
                class="text-lg font-light tracking-tight mb-2 text-[#E8E9ED] line-clamp-2 group-hover:text-[#B8A276] transition-colors duration-300"
              >
                {{ product.name }}
              </h3>

              <p class="text-sm text-[#9BA1AB] mb-4 line-clamp-2 font-light">
                {{ product.description || t("catalog.premiumQuality") }}
              </p>

              <div
                class="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-4 backdrop-blur-sm"
              >
                <div class="space-y-1">
                  <!-- Основная цена в тенге -->
                  <p class="text-2xl tracking-tight text-[#B8A276]">
                    ₸{{ getProductPriceKzt(product) }}
                  </p>
                  <!-- Эквивалент в долларах снизу -->
                  <p class="text-sm font-medium text-zinc-400">
                    ${{ product.price_usd }}
                  </p>
                </div>
              </div>

              <div
                v-if="product.stock_quantity"
                class="text-xs text-[#B8A276] font-light tracking-wide"
              >
                {{ t("catalog.inStock") }} {{ product.stock_quantity }}
              </div>
              <div
                v-else
                class="text-xs text-[#9BA1AB]/50 font-light tracking-wide"
              >
                {{ t("catalog.outOfStock") }}
              </div>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>
  </div>
</template>
