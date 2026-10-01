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

const productWholesalePriceKzt = computed(() => {
  const p = product.value;
  if (!p || p.wholesale_price_usd == null) return null;
  const rawPrice = p.wholesale_price_kzt
    ? Number(p.wholesale_price_kzt)
    : calculateKztFromUsd(p.wholesale_price_usd, exchangeRate.value);
  return formatNiceKztPrice(rawPrice);
});

const whatsappLink = computed(() => {
  const current = product.value;
  if (!current) return "#";

  let priceInfo = `₸${productPriceKzt.value}`;
  if (productWholesalePriceKzt.value) {
    priceInfo += ` | Опт от ${current.min_wholesale_quantity || 1} шт.: ₸${productWholesalePriceKzt.value}`;
  }

  const message = t("catalog.whatsappMessage", {
    name: current.name,
    price: priceInfo,
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
            <!-- Badges: Category, SKU, Wholesale -->
            <div class="flex flex-wrap items-center gap-3 mb-6">
              <div
                v-if="product.category_name && product.category_name !== 'Без категории'"
                class="flex items-center gap-1.5 px-3 py-1 bg-[#B8A276]/15 border border-[#B8A276]/40 text-[#B8A276] text-xs font-light tracking-wider rounded-full"
              >
                <Tag class="w-3.5 h-3.5" :stroke-width="1.5" />
                <span>{{ product.category_name }}</span>
              </div>

              <div
                v-if="product.sku"
                class="px-3 py-1 bg-[#1A1D23] border border-[#333842] text-[#9BA1AB] text-xs font-mono rounded-full"
              >
                Арт: {{ product.sku }}
              </div>

              <div
                v-if="product.wholesale_price_usd"
                class="px-3 py-1 bg-[#3B82F6]/15 border border-[#3B82F6]/50 text-[#60A5FA] text-xs font-medium tracking-wide rounded-full flex items-center gap-1.5"
              >
                <span class="w-1.5 h-1.5 rounded-full bg-[#3B82F6] animate-pulse"></span>
                <span>Доступен опт</span>
              </div>
            </div>

            <h1
              class="text-4xl lg:text-5xl font-light tracking-tight text-[#E8E9ED] mb-6"
            >
              {{ product.name }}
            </h1>

            <p
              class="text-[#9BA1AB] text-base leading-relaxed font-light mb-8"
            >
              {{ product.description || t("catalog.premiumQuality") }}
            </p>

            <!-- Розничная цена -->
            <div class="mb-4">
              <span class="text-xs text-[#9BA1AB] uppercase tracking-wider block font-light mb-1">
                Розничная цена
              </span>
              <div class="flex items-baseline gap-3">
                <div class="flex items-baseline gap-1">
                  <span class="text-4xl font-light text-[#B8A276]">
                    {{ productPriceKzt }}
                  </span>
                  <span class="text-xl text-[#B8A276]/80 font-light">₸</span>
                </div>
                <span class="text-sm font-medium text-zinc-400">
                  ${{ product.price_usd }}
                </span>
              </div>
            </div>

            <!-- Блок оптовой цены (если есть) -->
            <div
              v-if="product.wholesale_price_usd"
              class="mb-6 p-4 rounded-xl border border-[#3B82F6]/40 bg-[#3B82F6]/10 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-lg shadow-[#3B82F6]/5"
            >
              <div>
                <div class="flex items-center gap-2">
                  <span class="w-2 h-2 rounded-full bg-[#3B82F6] animate-pulse"></span>
                  <span class="text-xs uppercase tracking-wider text-[#60A5FA] font-medium">
                    Оптовая цена
                  </span>
                </div>
                <p class="text-xs text-[#9BA1AB] mt-1 font-light">
                  При заказе от <strong class="text-[#E8E9ED]">{{ product.min_wholesale_quantity || 1 }} шт.</strong>
                </p>
              </div>
              <div class="text-left sm:text-right">
                <div class="text-2xl font-light text-[#E8E9ED]">
                  {{ productWholesalePriceKzt }} <span class="text-base text-[#9BA1AB]">₸</span>
                </div>
                <div class="text-xs text-[#60A5FA] font-light">
                  ${{ product.wholesale_price_usd }} / шт.
                </div>
              </div>
            </div>

            <!-- Наличие на складе (всего) -->
            <div class="mb-8">
              <div
                v-if="product.stock_quantity > 0"
                class="flex items-center gap-2 text-sm text-[#B8A276] font-light"
              >
                <span class="w-2 h-2 rounded-full bg-[#B8A276] animate-pulse"></span>
                <span>{{ t("catalog.totalStock", "В наличии на складе:") }} <strong>{{ product.stock_quantity }} {{ t("catalog.pieces", "шт.") }}</strong></span>
              </div>
              <div v-else class="flex items-center gap-2 text-sm text-[#9BA1AB]/60 font-light">
                <span class="w-2 h-2 rounded-full bg-[#9BA1AB]/40"></span>
                <span>{{ t("catalog.outOfStock") }}</span>
              </div>
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
