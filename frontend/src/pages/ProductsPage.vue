<script setup>
import { ref, onMounted, computed } from "vue";
import { useI18n } from "vue-i18n";
import {
  Search,
  ShoppingCart,
  TrendingUp,
  Package,
  ChevronDown,
  X,
} from "lucide-vue-next";
import { useProductStore } from "../stores/index";
import Navbar from "@/components/Navbar.vue";
import api from "../services/api";
import { formatNiceKztFromUsd } from "../services/price";

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

const resetFilters = async () => {
  searchQuery.value = "";
  selectedCategory.value = "";
  sortBy.value = "";
  await search();
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
  if (!product) return "0";
  return formatNiceKztFromUsd(product.price_usd, exchangeRate.value);
};
</script>

<template>
  <Navbar />
  <div
    class="min-h-screen bg-[#1A1D23] text-[#E8E9ED] py-20 relative overflow-hidden"
  >
    <div
      class="pointer-events-none absolute -top-40 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-[#3B82F6]/5 rounded-full blur-3xl"
    />
    <div
      class="pointer-events-none absolute bottom-0 right-0 w-[400px] h-[400px] bg-[#B8A276]/5 rounded-full blur-3xl"
    />

    <div class="max-w-7xl mx-auto px-6 lg:px-12 relative">
      <div
        v-motion
        :initial="{ opacity: 0, y: -24 }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: { duration: 700, ease: 'easeOut' },
        }"
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
        :initial="{ opacity: 0, y: 24 }"
        :enter="{
          opacity: 1,
          y: 0,
          transition: { duration: 700, delay: 150, ease: 'easeOut' },
        }"
        class="mb-16"
      >
        <div
          class="bg-[#13151A]/80 border border-[#333842] backdrop-blur-sm rounded-2xl shadow-xl shadow-black/20 overflow-hidden"
        >
          <div
            class="flex flex-col lg:flex-row lg:items-center gap-4 p-6 border-b border-[#333842]/70"
          >
            <div
              class="flex items-center gap-3 shrink-0 px-4 py-2.5 rounded-xl border border-[#3B82F6]/15 bg-[#1A1D23]/70"
            >
              <TrendingUp class="w-4 h-4 text-[#B8A276] shrink-0" />
              <div class="flex items-baseline gap-1.5 whitespace-nowrap">
                <span
                  v-motion
                  :initial="{ opacity: 0, y: -4 }"
                  :enter="{ opacity: 1, y: 0, transition: { duration: 300 } }"
                  :key="displayExchangeRate"
                  class="text-base font-semibold text-[#B8A276]"
                >
                  ₸{{ displayExchangeRate }}
                </span>
                <span class="text-xs text-[#9BA1AB]">/ 1 USD</span>
              </div>
            </div>

            <div class="relative flex-1">
              <Search
                class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-[#9BA1AB] pointer-events-none"
              />
              <input
                v-model="searchQuery"
                type="text"
                :placeholder="t('catalog.searchPlaceholder')"
                class="w-full pl-12 pr-32 py-3.5 bg-[#1A1D23]/60 border border-[#333842] text-[#E8E9ED] placeholder-[#9BA1AB]/50 rounded-xl focus:outline-none focus:border-[#3B82F6] focus:ring-2 focus:ring-[#3B82F6]/20 transition-all duration-300 font-light text-base"
                @keyup.enter="search"
              />
              <button
                @click="search"
                class="absolute right-1.5 top-1/2 -translate-y-1/2 px-5 py-2 bg-[#3B82F6] hover:bg-[#3B82F6]/90 text-white text-sm font-medium rounded-lg transition-colors duration-200 active:scale-[0.97]"
              >
                {{ t("catalog.search") }}
              </button>
            </div>
          </div>

          <div class="flex flex-wrap items-center gap-3 p-6">
            <div class="relative group">
              <select
                v-model="selectedCategory"
                class="peer appearance-none pl-4 pr-9 py-2.5 bg-[#1A1D23]/60 border border-[#333842] text-[#E8E9ED] rounded-full focus:outline-none focus:border-[#3B82F6] focus:ring-1 focus:ring-[#3B82F6]/30 transition-all duration-200 font-light text-sm cursor-pointer hover:border-[#3B82F6]/40 min-w-[170px]"
                :class="
                  selectedCategory ? 'border-[#B8A276]/50 text-[#B8A276]' : ''
                "
                @change="search"
              >
                <option value="" class="bg-[#1A1D23] text-[#E8E9ED]">
                  {{ t("catalog.allCategories") }}
                </option>
                <option
                  v-for="cat in categories"
                  :key="cat.id"
                  :value="cat.id"
                  class="bg-[#1A1D23] text-[#E8E9ED]"
                >
                  {{ cat.name }}
                </option>
              </select>
              <ChevronDown
                class="absolute right-3.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none transition-transform duration-200 peer-focus:rotate-180"
                :class="selectedCategory ? 'text-[#B8A276]' : 'text-[#9BA1AB]'"
              />
            </div>

            <div class="relative group">
              <select
                v-model="sortBy"
                class="peer appearance-none pl-4 pr-9 py-2.5 bg-[#1A1D23]/60 border border-[#333842] text-[#E8E9ED] rounded-full focus:outline-none focus:border-[#3B82F6] focus:ring-1 focus:ring-[#3B82F6]/30 transition-all duration-200 font-light text-sm cursor-pointer hover:border-[#3B82F6]/40 min-w-[170px]"
                :class="sortBy ? 'border-[#B8A276]/50 text-[#B8A276]' : ''"
                @change="search"
              >
                <option value="" class="bg-[#1A1D23] text-[#E8E9ED]">
                  {{ t("catalog.sortDefault") }}
                </option>
                <option value="price" class="bg-[#1A1D23] text-[#E8E9ED]">
                  {{ t("catalog.sortPriceAsc") }}
                </option>
                <option value="-price" class="bg-[#1A1D23] text-[#E8E9ED]">
                  {{ t("catalog.sortPriceDesc") }}
                </option>
                <option value="name" class="bg-[#1A1D23] text-[#E8E9ED]">
                  {{ t("catalog.sortName") }}
                </option>
                <option value="-created_at" class="bg-[#1A1D23] text-[#E8E9ED]">
                  {{ t("catalog.sortNew") }}
                </option>
              </select>
              <ChevronDown
                class="absolute right-3.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 pointer-events-none transition-transform duration-200 peer-focus:rotate-180"
                :class="sortBy ? 'text-[#B8A276]' : 'text-[#9BA1AB]'"
              />
            </div>

            <button
              v-if="searchQuery || selectedCategory || sortBy"
              v-motion
              :initial="{ opacity: 0, scale: 0.9 }"
              :enter="{ opacity: 1, scale: 1, transition: { duration: 200 } }"
              @click="resetFilters"
              class="flex items-center gap-1.5 pl-3 pr-4 py-2.5 rounded-full border border-[#333842] text-[#9BA1AB] hover:text-[#E8E9ED] hover:border-[#3B82F6]/40 text-sm font-light transition-all duration-200 ml-1"
            >
              <X class="w-3.5 h-3.5" />
              {{ t("catalog.resetFilters", "Сбросить фильтры") }}
            </button>
          </div>
        </div>
      </div>

      <div
        v-if="productStore.isLoading"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
      >
        <div
          v-for="n in 8"
          :key="n"
          v-motion
          :initial="{ opacity: 0 }"
          :enter="{ opacity: 1, transition: { duration: 400, delay: n * 40 } }"
          class="rounded-2xl border border-[#333842] bg-[#1A1D23]/40 overflow-hidden"
        >
          <div class="aspect-square bg-[#252932]/60 animate-pulse" />
          <div class="p-6 space-y-3">
            <div class="h-4 bg-[#252932]/60 rounded animate-pulse w-3/4" />
            <div class="h-3 bg-[#252932]/40 rounded animate-pulse w-full" />
            <div
              class="h-10 bg-[#252932]/40 rounded-xl animate-pulse w-2/3 mt-4"
            />
          </div>
        </div>
      </div>

      <div
        v-else-if="displayProducts.length === 0"
        v-motion
        :initial="{ opacity: 0, scale: 0.95 }"
        :enter="{ opacity: 1, scale: 1, transition: { duration: 500 } }"
        class="flex items-center justify-center py-24"
      >
        <div class="text-center flex flex-col items-center gap-4">
          <Package class="w-10 h-10 text-[#9BA1AB]/40" />
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
          :initial="{ opacity: 0, y: 28, scale: 0.96 }"
          :visibleOnce="{
            opacity: 1,
            y: 0,
            scale: 1,
            transition: {
              duration: 500,
              delay: Math.min(index * 60, 400),
              ease: 'easeOut',
            },
          }"
          class="group relative"
        >
          <div
            class="h-full bg-linear-to-br from-[#1A1D23]/40 to-[#252932]/20 border border-[#333842] backdrop-blur-sm overflow-hidden rounded-2xl transition-all duration-500 ease-out hover:-translate-y-2 hover:scale-[1.015] hover:border-[#3B82F6]/50 hover:shadow-2xl hover:shadow-[#3B82F6]/10"
          >
            <div class="aspect-square bg-[#1A1D23]/60 overflow-hidden relative">
              <img
                v-if="product.main_image"
                :src="product.main_image"
                :alt="product.name"
                class="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-110"
              />
              <div
                v-else
                class="w-full h-full flex items-center justify-center text-[#9BA1AB]/50 transition-transform duration-500 group-hover:scale-105"
              >
                <ShoppingCart class="w-12 h-12" />
              </div>

              <div
                class="absolute inset-0 bg-linear-to-t from-[#13151A]/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500"
              />

              <div
                v-if="product.category_name"
                class="absolute top-4 left-4 px-3 py-1 bg-[#B8A276]/20 border border-[#B8A276]/50 text-[#B8A276] text-xs font-light tracking-wider rounded-full backdrop-blur-sm"
              >
                {{ product.category_name }}
              </div>
            </div>

            <div class="p-6">
              <h3
                class="text-lg font-light tracking-tight mb-2 text-[#E8E9ED] line-clamp-2 group-hover:text-[#B8A276] transition-colors duration-300"
              >
                {{ product.name }}
              </h3>

              <p class="text-sm text-[#9BA1AB] mb-4 line-clamp-2 font-light">
                {{ product.description || t("catalog.premiumQuality") }}
              </p>

              <div
                class="rounded-2xl border border-zinc-800 bg-zinc-900/50 p-4 backdrop-blur-sm transition-colors duration-300 group-hover:border-[#3B82F6]/20"
              >
                <div class="space-y-1">
                  <p
                    class="text-2xl tracking-tight text-[#B8A276] transition-transform duration-300 group-hover:scale-105 origin-left"
                  >
                    ₸{{ getProductPriceKzt(product) }}
                  </p>
                  <p class="text-sm font-medium text-zinc-400">
                    ${{ product.price_usd }}
                  </p>
                </div>
              </div>

              <div
                v-if="product.stock_quantity"
                class="text-xs text-[#B8A276] font-light tracking-wide mt-3 flex items-center gap-1.5"
              >
                <span
                  class="w-1.5 h-1.5 rounded-full bg-[#B8A276] animate-pulse"
                />
                {{ t("catalog.inStock") }} {{ product.stock_quantity }}
              </div>
              <div
                v-else
                class="text-xs text-[#9BA1AB]/50 font-light tracking-wide mt-3"
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
