<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useProductStore } from "../stores/index";
import { useI18n } from "vue-i18n";
import { ArrowLeft, ShoppingCart, Tag, MessageCircle } from "lucide-vue-next";
import Navbar from "../components/Navbar.vue";
import api from "../services/api";
import { formatNiceKztPrice, calculateKztFromUsd } from "../services/price";

const route = useRoute();
const router = useRouter();
const productStore = useProductStore();
const { t } = useI18n();

const exchangeRate = ref(460);
const WHATSAPP_PHONE = "77001234567";

// Локальный флаг готовности страницы — ждём оба запроса
const isPageReady = ref(false);

onMounted(async () => {
  // Fetch курса и товара идут параллельно
  const rateRequest = api
    .get("/exchange-rate/")
    .then((res) => {
      exchangeRate.value = res.data.rate;
    })
    .catch((err) => {
      console.error("Failed to get exchange rate:", err);
    });

  const productRequest = productStore.getProduct(route.params.id);

  // Ждём оба запроса
  await Promise.all([rateRequest, productRequest]);

  isPageReady.value = true;
});

const product = computed(() => productStore.currentProduct);

const productPriceKzt = computed(() => {
  const p = product.value;
  if (!p) return "0";
  const rawPrice = p.price_kzt
    ? Number(p.price_kzt)
    : calculateKztFromUsd(p.price_usd, exchangeRate.value);
  return formatNiceKztPrice(rawPrice);
});

const whatsappLink = computed(() => {
  const current = product.value;
  if (!current) return "#";

  const message = t("catalog.whatsappMessage", {
    name: current.name,
    price: productPriceKzt.value,
    url: window.location.href,
  });

  return `https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(message)}`;
});
</script>

<template>
  <div class="min-h-screen bg-[#13151A] text-[#E8E9ED]">
    <Navbar />

    <div class="max-w-7xl mx-auto px-6 lg:px-12 pt-36 pb-20">
      <!-- Показываем загрузку пока НЕ готовы оба запроса -->
      <div v-if="!isPageReady" class="flex items-center justify-center py-32">
        <p class="text-[#9BA1AB] font-light">{{ t("catalog.loading") }}</p>
      </div>

      <div
        v-else-if="!product"
        class="flex flex-col items-center justify-center py-32 gap-4"
      >
        <p class="text-[#9BA1AB] font-light">{{ t("catalog.notFound") }}</p>
        <button
          @click="router.push('/products')"
          class="text-sm text-[#3B82F6] hover:text-[#60A5FA] transition-colors font-light"
        >
          ← {{ t("catalog.backToCatalog", "Вернуться в каталог") }}
        </button>
      </div>

      <div v-else>
        <button
          @click="router.push('/products')"
          class="flex items-center gap-2 text-sm text-[#9BA1AB] hover:text-[#E8E9ED] transition-colors duration-200 mb-12 font-light"
        >
          <ArrowLeft class="w-4 h-4" :stroke-width="1.5" />
          {{ t("catalog.title") }}
        </button>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16">
          <div
            class="aspect-square bg-[#1A1D23] border border-[#333842] overflow-hidden"
          >
            <img
              v-if="product.main_image"
              :src="product.main_image"
              :alt="product.name"
              class="w-full h-full object-cover"
            />
            <div
              v-else
              class="w-full h-full flex items-center justify-center text-[#9BA1AB]/30"
            >
              <ShoppingCart class="w-16 h-16" :stroke-width="1" />
            </div>
          </div>

          <div class="flex flex-col justify-center">
            <div
              v-if="product.category_name"
              class="flex items-center gap-2 mb-6"
            >
              <Tag class="w-3.5 h-3.5 text-[#B8A276]" :stroke-width="1.5" />
              <span
                class="text-xs text-[#B8A276] tracking-widest uppercase font-light"
              >
                {{ product.category_name }}
              </span>
            </div>

            <h1
              class="text-4xl lg:text-5xl font-light tracking-tight text-[#E8E9ED] mb-6"
            >
              {{ product.name }}
            </h1>

            <p
              class="text-[#9BA1AB] text-base leading-relaxed font-light mb-10"
            >
              {{ product.description }}
            </p>

            <div class="flex items-baseline gap-2 mb-6">
              <span class="text-4xl font-light text-[#3B82F6]">
                {{ productPriceKzt }}
              </span>
              <span class="text-xl text-[#9BA1AB]">₸</span>
            </div>

            <div class="mb-8">
              <span
                v-if="product.stock_quantity > 0"
                class="text-sm text-[#B8A276] font-light"
              >
                {{ t("catalog.inStock") }} {{ product.stock_quantity }} шт.
              </span>
              <span v-else class="text-sm text-[#9BA1AB]/50 font-light">
                {{ t("catalog.outOfStock") }}
              </span>
            </div>

            <a
              :href="whatsappLink"
              target="_blank"
              rel="noopener noreferrer"
              class="group inline-flex items-center justify-center gap-2.5 w-full sm:w-fit px-8 py-3.5 bg-[#25D366] hover:bg-[#20BD5A] text-[#0B140F] font-medium rounded-lg transition-all duration-200 active:scale-[0.98] mb-10"
            >
              <MessageCircle
                class="w-5 h-5 transition-transform duration-200 group-hover:scale-110"
                :stroke-width="2"
              />
              {{ t("catalog.contactWhatsapp", "Связаться в WhatsApp") }}
            </a>

            <div class="h-px bg-[#333842] mb-10" />

            <div v-if="product.characteristics?.length" class="space-y-3">
              <p
                class="text-xs text-[#9BA1AB] tracking-widest uppercase font-light mb-4"
              >
                {{ t("catalog.characteristics", "Характеристики") }}
              </p>
              <div
                v-for="char in product.characteristics"
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
