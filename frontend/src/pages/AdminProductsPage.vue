<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore, useProductStore } from "../stores/index";
import {
  Plus,
  Pencil,
  Trash2,
  LogOut,
  Settings,
  Package,
} from "lucide-vue-next";
import api from "../services/api";
import { formatNiceKztPrice, calculateKztFromUsd } from "../services/price";

const router = useRouter();
const authStore = useAuthStore();
const productStore = useProductStore();
const exchangeRate = ref(460);

const logout = () => {
  authStore.logout();
  router.push("/admin/login");
};

const deleteProduct = async (id) => {
  if (confirm("Удалить товар?")) {
    try {
      await productStore.deleteProduct(id);
    } catch (error) {
      alert("Ошибка: " + error);
    }
  }
};

const getProductPriceKzt = (product) => {
  if (!product) return "0";
  const rawPrice = product.price_kzt
    ? Number(product.price_kzt)
    : calculateKztFromUsd(product.price_usd, exchangeRate.value);
  return formatNiceKztPrice(rawPrice);
};

onMounted(async () => {
  try {
    const rateResponse = await api.get("/exchange-rate/");
    exchangeRate.value = rateResponse.data.rate;
  } catch (err) {
    console.error("Failed to get exchange rate:", err);
  }

  await productStore.getProducts();
});
</script>

<template>
  <div class="min-h-screen bg-[#13151A] text-[#E8E9ED]">
    <div
      class="fixed top-0 left-0 h-full w-64 bg-[#1A1D23] border-r border-[#333842] flex flex-col z-50"
    >
      <div class="px-8 py-8 border-b border-[#333842]">
        <router-link
          to="/"
          class="text-xl font-light tracking-tight text-[#E8E9ED] hover:text-white transition-colors"
        >
          INPAR
        </router-link>
        <p
          class="text-xs text-[#9BA1AB] mt-1 tracking-widest uppercase font-light"
        >
          Admin Panel
        </p>
      </div>

      <nav class="flex-1 px-4 py-6 space-y-1">
        <router-link
          to="/admin"
          class="flex items-center gap-3 px-4 py-3 text-sm text-[#9BA1AB] hover:text-[#E8E9ED] hover:bg-[#252932] transition-all duration-200 font-light"
        >
          <Settings class="w-4 h-4" :stroke-width="1.5" />
          Обзор
        </router-link>
        <router-link
          to="/admin/products"
          class="flex items-center gap-3 px-4 py-3 text-sm text-[#E8E9ED] bg-[#252932] border-l-2 border-[#3B82F6] transition-all duration-200 font-light"
        >
          <Package class="w-4 h-4" :stroke-width="1.5" />
          Товары
        </router-link>
        <router-link
          to="/admin/products/new"
          class="flex items-center gap-3 px-4 py-3 text-sm text-[#9BA1AB] hover:text-[#E8E9ED] hover:bg-[#252932] transition-all duration-200 font-light"
        >
          <Plus class="w-4 h-4" :stroke-width="1.5" />
          Добавить товар
        </router-link>
      </nav>

      <div class="px-4 py-6 border-t border-[#333842] space-y-3">
        <div class="px-4 py-3">
          <p class="text-xs text-[#9BA1AB] font-light">Вы вошли как</p>
          <p class="text-sm text-[#E8E9ED] font-light mt-0.5">
            {{ authStore.user?.username }}
          </p>
        </div>
        <button
          @click="logout"
          class="w-full flex items-center gap-3 px-4 py-3 text-sm text-[#9BA1AB] hover:text-red-400 hover:bg-red-500/10 transition-all duration-200 font-light"
        >
          <LogOut class="w-4 h-4" :stroke-width="1.5" />
          Выйти
        </button>
      </div>
    </div>

    <div class="ml-64 p-10">
      <div class="flex items-center justify-between mb-10">
        <div>
          <h1 class="text-3xl font-light tracking-tight">Товары</h1>
          <p class="text-[#9BA1AB] text-sm mt-1 font-light">
            {{ productStore.products.length }} позиций в каталоге
          </p>
        </div>
        <router-link
          to="/admin/products/new"
          class="flex items-center gap-2 px-5 py-2.5 border border-[#B8A276]/50 text-[#B8A276] text-sm font-light tracking-wide hover:bg-[#B8A276]/10 transition-all duration-300"
        >
          <Plus class="w-4 h-4" :stroke-width="1.5" />
          Новый товар
        </router-link>
      </div>

      <!-- Loading -->
      <div
        v-if="productStore.isLoading"
        class="py-20 text-center text-[#9BA1AB] font-light"
      >
        Загрузка...
      </div>

      <!-- Empty -->
      <div
        v-else-if="productStore.products.length === 0"
        class="py-20 text-center text-[#9BA1AB] font-light"
      >
        Товаров пока нет
      </div>

      <!-- Table -->
      <div v-else class="border border-[#333842]">
        <table class="w-full">
          <thead>
            <tr class="border-b border-[#333842] bg-[#1A1D23]/60">
              <th
                class="px-6 py-4 text-left text-xs text-[#9BA1AB] tracking-widest uppercase font-light"
              >
                Название
              </th>
              <th
                class="px-6 py-4 text-left text-xs text-[#9BA1AB] tracking-widest uppercase font-light"
              >
                Категория
              </th>
              <th
                class="px-6 py-4 text-right text-xs text-[#9BA1AB] tracking-widest uppercase font-light"
              >
                Цена
              </th>
              <th
                class="px-6 py-4 text-right text-xs text-[#9BA1AB] tracking-widest uppercase font-light"
              >
                Кол-во
              </th>
              <th
                class="px-6 py-4 text-center text-xs text-[#9BA1AB] tracking-widest uppercase font-light"
              >
                Действия
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="product in productStore.products"
              :key="product.id"
              class="border-b border-[#333842] hover:bg-[#1A1D23]/40 transition-colors duration-200"
            >
              <td class="px-6 py-4 text-sm text-[#E8E9ED] font-light">
                {{ product.name }}
              </td>
              <td class="px-6 py-4">
                <span
                  class="px-2 py-1 border border-[#B8A276]/30 text-[#B8A276] text-xs font-light tracking-wide"
                >
                  {{ product.category_name || `ID: ${product.category}` }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <div class="text-sm text-[#E8E9ED] font-light">
                  ${{ product.price_usd }}
                </div>
                <div class="text-xs text-[#B8A276] font-light mt-1">
                  ≈ {{ getProductPriceKzt(product) }} ₸
                </div>
              </td>
              <td class="px-6 py-4 text-right">
                <span
                  :class="[
                    'px-2 py-1 text-xs font-light',
                    product.stock_quantity > 0
                      ? 'border border-[#3B82F6]/30 text-[#3B82F6]'
                      : 'border border-red-500/30 text-red-400',
                  ]"
                >
                  {{ product.stock_quantity }}
                </span>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center justify-center gap-3">
                  <router-link
                    :to="`/admin/products/${product.id}/edit`"
                    class="flex items-center gap-1.5 text-xs text-[#9BA1AB] hover:text-[#3B82F6] transition-colors font-light"
                  >
                    <Pencil class="w-3.5 h-3.5" :stroke-width="1.5" />
                    Изменить
                  </router-link>
                  <button
                    @click="deleteProduct(product.id)"
                    class="flex items-center gap-1.5 text-xs text-[#9BA1AB] hover:text-red-400 transition-colors font-light"
                  >
                    <Trash2 class="w-3.5 h-3.5" :stroke-width="1.5" />
                    Удалить
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>
