<script setup>
import { onMounted, ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore, useProductStore } from "../stores/index";
import { Package, Tag, LogOut, Settings, Plus, List } from "lucide-vue-next";
import api from "../services/api";

const router = useRouter();
const authStore = useAuthStore();
const productStore = useProductStore();
const categories = ref([]);
const exchangeRate = ref(460);

const totalProducts = computed(() => productStore.products.length);
const inStock = computed(() =>
  productStore.products.filter((p) => p.stock_quantity > 0).length,
);
const totalValueUsd = computed(() => {
  const sum = productStore.products.reduce(
    (acc, product) => acc + parseFloat(product.price_usd || 0),
    0,
  );
  return sum.toFixed(2);
});
const totalValueKzt = computed(() => {
  const sum = productStore.products.reduce(
    (acc, product) => acc + parseFloat(product.price_usd || 0) * exchangeRate.value,
    0,
  );
  return sum.toFixed(2);
});

const logout = () => {
  authStore.logout();
  router.push("/admin/login");
};

onMounted(async () => {
  try {
    const rateResponse = await api.get("/exchange-rate/");
    exchangeRate.value = rateResponse.data.rate;
  } catch (err) {
    console.error("Failed to get exchange rate:", err);
  }

  await productStore.getProducts();
  categories.value = await productStore.getCategories();
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
          active-class="text-[#E8E9ED] bg-[#252932] border-l-2 border-[#3B82F6]"
        >
          <Settings class="w-4 h-4" :stroke-width="1.5" />
          Обзор
        </router-link>

        <router-link
          to="/admin/products"
          class="flex items-center gap-3 px-4 py-3 text-sm text-[#9BA1AB] hover:text-[#E8E9ED] hover:bg-[#252932] transition-all duration-200 font-light"
          active-class="text-[#E8E9ED] bg-[#252932] border-l-2 border-[#3B82F6]"
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
      <div class="mb-10">
        <h1 class="text-3xl font-light tracking-tight">Обзор</h1>
        <p class="text-[#9BA1AB] text-sm mt-1 font-light">
          Добро пожаловать, {{ authStore.user?.username }}
        </p>
      </div>

      <div class="grid grid-cols-4 gap-6 mb-10">
        <div class="p-6 border border-[#333842] bg-[#1A1D23]/60">
          <p
            class="text-xs text-[#9BA1AB] tracking-widest uppercase font-light mb-3"
          >
            Всего товаров
          </p>
          <p class="text-4xl font-light text-[#E8E9ED]">{{ totalProducts }}</p>
        </div>
        <div class="p-6 border border-[#333842] bg-[#1A1D23]/60">
          <p
            class="text-xs text-[#9BA1AB] tracking-widest uppercase font-light mb-3"
          >
            В наличии
          </p>
          <p class="text-4xl font-light text-[#3B82F6]">{{ inStock }}</p>
        </div>
        <div class="p-6 border border-[#333842] bg-[#1A1D23]/60">
          <p
            class="text-xs text-[#9BA1AB] tracking-widest uppercase font-light mb-3"
          >
            Категорий
          </p>
          <p class="text-4xl font-light text-[#B8A276]">
            {{ categories.length }}
          </p>
        </div>
        <div class="p-6 border border-[#333842] bg-[#1A1D23]/60">
          <p
            class="text-xs text-[#9BA1AB] tracking-widest uppercase font-light mb-3"
          >
            Стоимость товаров
          </p>
          <p class="text-xl font-light text-[#E8E9ED]">
            ${{ totalValueUsd }}
          </p>
          <p class="text-sm text-[#B8A276] mt-2 font-light">
            ≈ {{ totalValueKzt }} ₸
          </p>
          <p class="text-xs text-[#9BA1AB] mt-1 font-light">
            Курс: 1 USD = {{ exchangeRate }} ₸
          </p>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-2 gap-6">
        <router-link
          to="/admin/products"
          class="group p-6 border border-[#333842] bg-[#1A1D23]/60 hover:border-[#3B82F6]/50 transition-all duration-300 flex items-center gap-4"
        >
          <List
            class="w-6 h-6 text-[#9BA1AB] group-hover:text-[#3B82F6] transition-colors"
            :stroke-width="1.5"
          />
          <div>
            <p class="text-sm text-[#E8E9ED] font-light">Список товаров</p>
            <p class="text-xs text-[#9BA1AB] font-light mt-0.5">
              Управление каталогом
            </p>
          </div>
        </router-link>

        <router-link
          to="/admin/products/new"
          class="group p-6 border border-[#333842] bg-[#1A1D23]/60 hover:border-[#B8A276]/50 transition-all duration-300 flex items-center gap-4"
        >
          <Plus
            class="w-6 h-6 text-[#9BA1AB] group-hover:text-[#B8A276] transition-colors"
            :stroke-width="1.5"
          />
          <div>
            <p class="text-sm text-[#E8E9ED] font-light">Новый товар</p>
            <p class="text-xs text-[#9BA1AB] font-light mt-0.5">
              Добавить в каталог
            </p>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>
