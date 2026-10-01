<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore, useProductStore } from "../stores/index";
import {
  Plus,
  Pencil,
  Trash2,
  LogOut,
  Settings,
  Package,
  FileSpreadsheet,
  Download,
  Upload,
  Search,
  X,
  CheckCircle2,
  AlertCircle,
  FileUp,
  FolderTree,
  CheckSquare,
  Square,
  Check,
  Layers,
  ArrowRight,
} from "lucide-vue-next";
import api from "../services/api";
import { formatNiceKztPrice, calculateKztFromUsd } from "../services/price";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const productStore = useProductStore();
const exchangeRate = ref(460);

const searchQuery = ref("");
const selectedCategory = ref("");
const categories = ref([]);

// Чекбоксы и массовые действия
const selectedIds = ref([]);
const bulkTargetCategoryId = ref("");
const isBulkProcessing = ref(false);

// Модальное окно импорта
const showImportModal = ref(false);
const importFile = ref(null);
const importCategory = ref("");
const importCurrency = ref("KZT");
const isImporting = ref(false);
const importError = ref("");
const importResult = ref(null);
const isDownloadingTemplate = ref(false);

// Модальное окно управления категориями
const showCategoryModal = ref(false);
const newCatName = ref("");
const newCatDesc = ref("");
const isCreatingCat = ref(false);
const editingCatId = ref(null);
const editingCatName = ref("");
const catActionError = ref("");

const logout = () => {
  authStore.logout();
  router.push("/admin/login");
};

const deleteProduct = async (id) => {
  if (confirm("Удалить этот товар?")) {
    try {
      await productStore.deleteProduct(id);
      selectedIds.value = selectedIds.value.filter((item) => item !== id);
    } catch (error) {
      alert("Ошибка: " + error);
    }
  }
};

const clearUncategorized = async () => {
  if (
    confirm(
      `Удалить все ${uncategorizedCount.value} товаров без категории? Это поможет очистить ошибочно импортированные позиции.`
    )
  ) {
    try {
      await productStore.clearUncategorizedProducts();
      selectedIds.value = [];
      alert("Товары без категории удалены");
    } catch (error) {
      alert("Ошибка: " + error);
    }
  }
};

const deleteAllProducts = async () => {
  const total = productStore.products.length;
  if (!total) return;
  if (
    confirm(
      `ВНИМАНИЕ! Вы собираетесь удалить ВСЕ ${total} товаров из каталога.\nЭто действие нельзя отменить.\nПродолжить?`
    )
  ) {
    try {
      await productStore.bulkDeleteProducts({ all: true });
      selectedIds.value = [];
      alert("Все товары каталога успешно удалены");
    } catch (err) {
      alert("Ошибка при удалении: " + err);
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

const getProductWholesalePriceKzt = (product) => {
  if (!product || product.wholesale_price_usd == null) return null;
  const rawPrice = product.wholesale_price_kzt
    ? Number(product.wholesale_price_kzt)
    : calculateKztFromUsd(product.wholesale_price_usd, exchangeRate.value);
  return formatNiceKztPrice(rawPrice);
};

// Фильтрация товаров
const filteredProducts = computed(() => {
  let list = productStore.products || [];
  if (selectedCategory.value === "uncategorized") {
    list = list.filter(
      (p) => !p.category || p.category_name === "Без категории"
    );
  } else if (selectedCategory.value) {
    list = list.filter((p) => String(p.category) === String(selectedCategory.value));
  }

  if (searchQuery.value.trim()) {
    const q = searchQuery.value.trim().toLowerCase();
    list = list.filter(
      (p) =>
        (p.name && p.name.toLowerCase().includes(q)) ||
        (p.sku && p.sku.toLowerCase().includes(q)) ||
        (p.description && p.description.toLowerCase().includes(q))
    );
  }
  return list;
});

const uncategorizedCount = computed(() => {
  return (productStore.products || []).filter(
    (p) => !p.category || p.category_name === "Без категории"
  ).length;
});

// Чекбоксы: выбор всех отфильтрованных товаров
const isAllSelected = computed(() => {
  if (!filteredProducts.value.length) return false;
  return filteredProducts.value.every((p) => selectedIds.value.includes(p.id));
});

const toggleSelectAll = () => {
  if (isAllSelected.value) {
    const currentFilteredIds = new Set(filteredProducts.value.map((p) => p.id));
    selectedIds.value = selectedIds.value.filter((id) => !currentFilteredIds.has(id));
  } else {
    const set = new Set(selectedIds.value);
    filteredProducts.value.forEach((p) => set.add(p.id));
    selectedIds.value = Array.from(set);
  }
};

const toggleSelectProduct = (id) => {
  const index = selectedIds.value.indexOf(id);
  if (index > -1) {
    selectedIds.value.splice(index, 1);
  } else {
    selectedIds.value.push(id);
  }
};

// Массовое удаление выбранных товаров
const handleBulkDelete = async () => {
  const count = selectedIds.value.length;
  if (!count) return;

  if (confirm(`Удалить выбранные товары (${count} шт.)?`)) {
    isBulkProcessing.value = true;
    try {
      await productStore.bulkDeleteProducts({ ids: selectedIds.value });
      selectedIds.value = [];
    } catch (err) {
      alert("Ошибка при массовом удалении: " + err);
    } finally {
      isBulkProcessing.value = false;
    }
  }
};

// Массовое назначение категории
const handleBulkSetCategory = async () => {
  const count = selectedIds.value.length;
  if (!count) return;

  isBulkProcessing.value = true;
  try {
    const catId = bulkTargetCategoryId.value ? Number(bulkTargetCategoryId.value) : null;
    await productStore.bulkSetCategory({
      ids: selectedIds.value,
      categoryId: catId,
    });
    selectedIds.value = [];
    bulkTargetCategoryId.value = "";
    categories.value = await productStore.getCategories();
  } catch (err) {
    alert("Ошибка при назначении категории: " + err);
  } finally {
    isBulkProcessing.value = false;
  }
};

// --- Управление категориями ---
const openCategoryManager = () => {
  catActionError.value = "";
  editingCatId.value = null;
  newCatName.value = "";
  newCatDesc.value = "";
  showCategoryModal.value = true;
};

const handleCreateCategory = async () => {
  if (!newCatName.value.trim()) {
    catActionError.value = "Введите название категории";
    return;
  }

  isCreatingCat.value = true;
  catActionError.value = "";
  try {
    await productStore.createCategory({
      name: newCatName.value.trim(),
      description: newCatDesc.value.trim(),
    });
    newCatName.value = "";
    newCatDesc.value = "";
    categories.value = await productStore.getCategories();
  } catch (err) {
    catActionError.value = err.message || "Ошибка при создании";
  } finally {
    isCreatingCat.value = false;
  }
};

const startEditCategory = (cat) => {
  editingCatId.value = cat.id;
  editingCatName.value = cat.name;
};

const cancelEditCategory = () => {
  editingCatId.value = null;
  editingCatName.value = "";
};

const saveEditCategory = async (catId) => {
  if (!editingCatName.value.trim()) return;
  try {
    await productStore.updateCategory(catId, { name: editingCatName.value.trim() });
    editingCatId.value = null;
    categories.value = await productStore.getCategories();
  } catch (err) {
    alert("Ошибка при переименовании: " + err);
  }
};

const handleDeleteCategory = async (cat) => {
  const msg = `Удалить категорию "${cat.name}"?\nВсе товары из этой категории автоматически перейдут в "Без категории".`;
  if (confirm(msg)) {
    try {
      await productStore.deleteCategory(cat.id);
      categories.value = await productStore.getCategories();
    } catch (err) {
      alert("Ошибка при удалении: " + err);
    }
  }
};

// --- Импорт Excel ---
const handleFileSelect = (e) => {
  const file = e.target.files?.[0];
  if (file) {
    importFile.value = file;
    importError.value = "";
    importResult.value = null;
  }
};

const handleDrop = (e) => {
  e.preventDefault();
  const file = e.dataTransfer?.files?.[0];
  if (file && (file.name.endsWith(".xlsx") || file.name.endsWith(".xls"))) {
    importFile.value = file;
    importError.value = "";
    importResult.value = null;
  } else {
    importError.value = "Пожалуйста, выберите файл в формате .xlsx или .xls";
  }
};

const handleDownloadTemplate = async () => {
  isDownloadingTemplate.value = true;
  try {
    await productStore.downloadExcelTemplate();
  } catch (err) {
    alert("Не удалось скачать шаблон: " + (err.message || err));
  } finally {
    isDownloadingTemplate.value = false;
  }
};

const submitImport = async () => {
  if (!importFile.value) {
    importError.value = "Выберите Excel-файл для загрузки";
    return;
  }

  isImporting.value = true;
  importError.value = "";
  importResult.value = null;

  try {
    const res = await productStore.importExcel(
      importFile.value,
      importCategory.value || null,
      importCurrency.value
    );
    importResult.value = res;
    categories.value = await productStore.getCategories();
  } catch (err) {
    importError.value =
      err.response?.data?.errors?.[0] ||
      err.response?.data?.error ||
      err.message ||
      "Ошибка при импорте";
  } finally {
    isImporting.value = false;
  }
};

const closeImportModal = () => {
  showImportModal.value = false;
  importFile.value = null;
  importCategory.value = "";
  importError.value = "";
  importResult.value = null;
};

onMounted(async () => {
  try {
    const rateResponse = await api.get("/exchange-rate/");
    exchangeRate.value = rateResponse.data.rate;
  } catch (err) {
    console.error("Failed to get exchange rate:", err);
  }

  categories.value = await productStore.getCategories();
  await productStore.getProducts();

  if (route.query.manageCategories) {
    openCategoryManager();
  }
});
</script>

<template>
  <div class="min-h-screen bg-[#13151A] text-[#E8E9ED]">
    <!-- Боковое меню -->
    <div
      class="fixed top-0 left-0 h-full w-64 bg-[#1A1D23] border-r border-[#333842] flex flex-col z-40"
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
        <button
          @click="openCategoryManager"
          class="w-full flex items-center gap-3 px-4 py-3 text-sm text-[#9BA1AB] hover:text-[#E8E9ED] hover:bg-[#252932] transition-all duration-200 font-light text-left"
        >
          <FolderTree class="w-4 h-4 text-[#B8A276]" :stroke-width="1.5" />
          Категории
        </button>
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

    <!-- Основной контент -->
    <div class="ml-64 p-10">
      <!-- Шапка страницы -->
      <div
        class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 mb-8"
      >
        <div>
          <h1 class="text-3xl font-light tracking-tight">Товары</h1>
          <p class="text-[#9BA1AB] text-sm mt-1 font-light flex items-center flex-wrap gap-2">
            <span>{{ productStore.products.length }} позиций в каталоге</span>
            <span
              v-if="uncategorizedCount > 0"
              class="inline-flex items-center gap-1.5 text-amber-400 text-xs px-2.5 py-0.5 rounded-full border border-amber-500/30 bg-amber-500/10"
            >
              <span>{{ uncategorizedCount }} без категории</span>
              <button
                @click="clearUncategorized"
                class="text-red-400 hover:text-red-300 underline font-medium cursor-pointer ml-1"
                title="Удалить все ошибочные/некатегоризованные позиции"
              >
                (очистить их)
              </button>
            </span>
          </p>
        </div>

        <div class="flex flex-wrap items-center gap-3">
          <!-- Управление категориями -->
          <button
            @click="openCategoryManager"
            class="flex items-center gap-2 px-4 py-2.5 bg-[#B8A276]/10 border border-[#B8A276] text-[#B8A276] hover:bg-[#B8A276]/20 text-sm font-medium tracking-wide transition-all duration-300 rounded shadow-sm"
            title="Управление категориями: создание, переименование, удаление"
          >
            <FolderTree class="w-4 h-4 text-[#B8A276]" :stroke-width="1.8" />
            <span>Категории ({{ categories.length }})</span>
          </button>

          <!-- Скачать шаблон -->
          <button
            @click="handleDownloadTemplate"
            :disabled="isDownloadingTemplate"
            class="flex items-center gap-2 px-4 py-2.5 border border-[#333842] text-[#9BA1AB] hover:text-[#E8E9ED] hover:border-[#3B82F6]/50 text-sm font-light tracking-wide transition-all duration-300 disabled:opacity-50 rounded"
            title="Скачать образец таблицы Excel для заполнения"
          >
            <Download class="w-4 h-4" :stroke-width="1.5" />
            <span>Шаблон Excel</span>
          </button>

          <!-- Импорт Excel -->
          <button
            @click="showImportModal = true"
            class="flex items-center gap-2 px-4 py-2.5 border border-[#3B82F6]/50 text-[#3B82F6] hover:bg-[#3B82F6]/10 text-sm font-light tracking-wide transition-all duration-300 rounded"
          >
            <FileSpreadsheet class="w-4 h-4" :stroke-width="1.5" />
            <span>Импорт из Excel</span>
          </button>

          <!-- Новый товар -->
          <router-link
            to="/admin/products/new"
            class="flex items-center gap-2 px-5 py-2.5 bg-[#B8A276] hover:bg-[#B8A276]/90 text-[#13151A] text-sm font-medium tracking-wide transition-all duration-300 rounded"
          >
            <Plus class="w-4 h-4" :stroke-width="2" />
            <span>Новый товар</span>
          </router-link>
        </div>
      </div>

      <!-- Фильтры и поиск -->
      <div
        class="mb-4 flex flex-col sm:flex-row items-center justify-between gap-4 bg-[#1A1D23]/60 p-4 border border-[#333842] rounded-t"
      >
        <!-- Поиск -->
        <div class="relative flex-1 w-full">
          <Search
            class="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-[#9BA1AB]"
          />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Поиск по названию или артикулу (SKU)..."
            class="w-full pl-10 pr-4 py-2.5 bg-[#13151A] border border-[#333842] text-[#E8E9ED] text-sm placeholder-[#9BA1AB]/50 focus:outline-none focus:border-[#3B82F6] transition-colors font-light rounded"
          />
          <button
            v-if="searchQuery"
            @click="searchQuery = ''"
            class="absolute right-3 top-1/2 -translate-y-1/2 text-[#9BA1AB] hover:text-[#E8E9ED]"
          >
            <X class="w-3.5 h-3.5" />
          </button>
        </div>

        <!-- Фильтр по категории -->
        <div class="w-full sm:w-64">
          <select
            v-model="selectedCategory"
            class="w-full px-3.5 py-2.5 bg-[#13151A] border border-[#333842] text-[#E8E9ED] text-sm focus:outline-none focus:border-[#3B82F6] transition-colors font-light appearance-none cursor-pointer rounded"
          >
            <option value="">Все категории</option>
            <option
              v-if="uncategorizedCount > 0"
              value="uncategorized"
              class="text-amber-400 font-medium"
            >
              ⚠️ Без категории ({{ uncategorizedCount }})
            </option>
            <option v-for="cat in categories" :key="cat.id" :value="cat.id">
              {{ cat.name }} ({{ cat.products_count ?? 0 }})
            </option>
          </select>
        </div>
      </div>

      <!-- Панель массовых действий (всегда видна над таблицей для удобства) -->
      <div
        class="mb-6 p-3.5 bg-[#1A1D23] border border-[#333842] rounded flex flex-wrap items-center justify-between gap-3"
      >
        <div class="flex items-center gap-2.5 flex-wrap">
          <!-- Кнопка Выбрать все -->
          <button
            @click="toggleSelectAll"
            class="flex items-center gap-1.5 px-3 py-1.5 bg-[#252932] hover:bg-[#2e333e] border border-[#333842] text-xs font-light rounded transition-colors text-[#E8E9ED] cursor-pointer"
          >
            <component :is="isAllSelected ? CheckSquare : Square" class="w-3.5 h-3.5 text-[#3B82F6]" />
            <span>{{ isAllSelected ? 'Снять выделение' : 'Выбрать все (' + filteredProducts.length + ')' }}</span>
          </button>

          <span
            v-if="selectedIds.length > 0"
            class="text-xs text-[#3B82F6] font-medium bg-[#3B82F6]/15 border border-[#3B82F6]/30 px-2.5 py-1 rounded"
          >
            Выбрано: {{ selectedIds.length }} позиций
          </span>
          <span v-else class="text-xs text-[#9BA1AB] font-light hidden md:inline">
            ← Отметьте чекбоксами товары для удаления или смены категории
          </span>
        </div>

        <div class="flex items-center gap-2 flex-wrap">
          <!-- Массовое назначение категории (активно если выбраны товары) -->
          <div v-if="selectedIds.length > 0" class="flex items-center gap-1.5">
            <select
              v-model="bulkTargetCategoryId"
              class="px-2.5 py-1.5 bg-[#13151A] border border-[#333842] text-xs text-white rounded outline-none focus:border-[#3B82F6]"
            >
              <option value="" disabled>Назначить категорию...</option>
              <option value="none">Без категории</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
            <button
              @click="handleBulkSetCategory"
              :disabled="!bulkTargetCategoryId || isBulkProcessing"
              class="px-3 py-1.5 bg-[#3B82F6] hover:bg-[#3B82F6]/90 text-white text-xs font-medium rounded transition-colors disabled:opacity-40 cursor-pointer"
            >
              Применить
            </button>
          </div>

          <!-- Кнопка удаления выбранных товаров -->
          <button
            @click="handleBulkDelete"
            :disabled="selectedIds.length === 0 || isBulkProcessing"
            :class="[
              'flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded transition-colors',
              selectedIds.length > 0
                ? 'bg-red-500/20 hover:bg-red-500/30 text-red-400 border border-red-500/50 cursor-pointer'
                : 'text-[#9BA1AB]/40 border border-[#333842]/40 cursor-not-allowed opacity-50'
            ]"
            title="Удалить отмеченные товары"
          >
            <Trash2 class="w-3.5 h-3.5" />
            <span>Удалить выбранные {{ selectedIds.length > 0 ? `(${selectedIds.length})` : '' }}</span>
          </button>

          <!-- Разделитель -->
          <div class="h-4 w-px bg-[#333842] hidden sm:block"></div>

          <!-- Кнопка удаления ВСЕХ товаров -->
          <button
            v-if="productStore.products.length > 0"
            @click="deleteAllProducts"
            class="flex items-center gap-1 px-3 py-1.5 text-xs text-red-400 hover:text-red-300 hover:bg-red-500/10 border border-red-500/30 rounded transition-colors cursor-pointer"
            title="Очистить абсолютно весь каталог"
          >
            <Trash2 class="w-3.5 h-3.5" />
            <span>Удалить ВСЕ товары ({{ productStore.products.length }})</span>
          </button>
        </div>
      </div>

      <!-- Loading -->
      <div
        v-if="productStore.isLoading && !productStore.products.length"
        class="py-20 text-center text-[#9BA1AB] font-light"
      >
        Загрузка...
      </div>

      <!-- Empty -->
      <div
        v-else-if="filteredProducts.length === 0"
        class="py-20 text-center text-[#9BA1AB] font-light border border-[#333842] bg-[#1A1D23]/30"
      >
        <p>Товары не найдены</p>
        <p class="text-xs text-[#9BA1AB]/60 mt-1">
          Попробуйте сбросить фильтры или добавить товары
        </p>
      </div>

      <!-- Table -->
      <div v-else class="border border-[#333842] overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="border-b border-[#333842] bg-[#1A1D23]/80">
              <!-- Чекбокс Выбрать все -->
              <th class="w-16 px-3 py-4 text-center">
                <label class="inline-flex items-center gap-1.5 cursor-pointer" title="Выбрать все отфильтрованные товары">
                  <input
                    type="checkbox"
                    :checked="isAllSelected"
                    @change="toggleSelectAll"
                    class="w-4 h-4 rounded border-[#333842] bg-[#13151A] text-[#3B82F6] focus:ring-0 cursor-pointer accent-[#3B82F6]"
                  />
                  <span class="text-[10px] text-[#9BA1AB] font-medium uppercase select-none">Все</span>
                </label>
              </th>
              <th
                class="px-6 py-4 text-xs text-[#9BA1AB] tracking-widest uppercase font-light"
              >
                Товар / Артикул
              </th>
              <th
                class="px-6 py-4 text-xs text-[#9BA1AB] tracking-widest uppercase font-light"
              >
                Категория
              </th>
              <th
                class="px-6 py-4 text-right text-xs text-[#9BA1AB] tracking-widest uppercase font-light"
              >
                Розница
              </th>
              <th
                class="px-6 py-4 text-right text-xs text-[#9BA1AB] tracking-widest uppercase font-light"
              >
                Опт
              </th>
              <th
                class="px-6 py-4 text-right text-xs text-[#9BA1AB] tracking-widest uppercase font-light"
              >
                Остаток
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
              v-for="product in filteredProducts"
              :key="product.id"
              :class="[
                'border-b border-[#333842] transition-colors duration-150',
                selectedIds.includes(product.id)
                  ? 'bg-[#3B82F6]/10'
                  : 'hover:bg-[#1A1D23]/40'
              ]"
            >
              <!-- Чекбокс строки -->
              <td class="px-4 py-4 text-center">
                <input
                  type="checkbox"
                  :checked="selectedIds.includes(product.id)"
                  @change="toggleSelectProduct(product.id)"
                  class="w-4 h-4 rounded border-[#333842] bg-[#13151A] text-[#3B82F6] focus:ring-0 cursor-pointer accent-[#3B82F6]"
                />
              </td>

              <!-- Название и SKU -->
              <td class="px-6 py-4">
                <div class="text-sm text-[#E8E9ED] font-light line-clamp-2">
                  {{ product.name }}
                </div>
                <div
                  v-if="product.sku"
                  class="text-xs text-[#9BA1AB] font-mono mt-1"
                >
                  Код: {{ product.sku }}
                </div>
              </td>

              <!-- Категория -->
              <td class="px-6 py-4">
                <span
                  v-if="!product.category_name || product.category_name === 'Без категории'"
                  class="inline-flex items-center gap-1 px-2.5 py-1 border border-amber-500/40 bg-amber-500/10 text-amber-400 text-xs font-light tracking-wide rounded cursor-pointer hover:border-amber-400"
                  @click="openCategoryManager"
                  title="Нажмите для управления категориями"
                >
                  <span>Без категории</span>
                </span>
                <span
                  v-else
                  class="px-2 py-1 border border-[#B8A276]/30 text-[#B8A276] text-xs font-light tracking-wide rounded"
                >
                  {{ product.category_name }}
                </span>
              </td>

              <!-- Розничная цена -->
              <td class="px-6 py-4 text-right whitespace-nowrap">
                <div class="text-sm text-[#E8E9ED] font-light">
                  ${{ product.price_usd }}
                </div>
                <div class="text-xs text-[#B8A276] font-light mt-0.5">
                  ≈ {{ getProductPriceKzt(product) }} ₸
                </div>
              </td>

              <!-- Оптовая цена -->
              <td class="px-6 py-4 text-right whitespace-nowrap">
                <div
                  v-if="product.wholesale_price_usd != null"
                  class="space-y-0.5"
                >
                  <div class="text-sm text-[#3B82F6] font-light">
                    ${{ product.wholesale_price_usd }}
                  </div>
                  <div class="text-xs text-[#3B82F6]/80 font-light">
                    ≈ {{ getProductWholesalePriceKzt(product) }} ₸
                  </div>
                  <div class="text-[10px] text-[#9BA1AB] font-light">
                    от {{ product.min_wholesale_quantity || 1 }} шт.
                  </div>
                </div>
                <span v-else class="text-xs text-[#9BA1AB]/40 font-light">
                  —
                </span>
              </td>

              <!-- Остаток на складе -->
              <td class="px-6 py-4 text-right whitespace-nowrap">
                <span
                  :class="[
                    'px-2 py-1 text-xs font-light rounded',
                    product.stock_quantity > 0
                      ? 'border border-[#3B82F6]/30 text-[#3B82F6] bg-[#3B82F6]/5'
                      : 'border border-red-500/30 text-red-400 bg-red-500/5',
                  ]"
                >
                  {{ product.stock_quantity }} шт.
                </span>
              </td>

              <!-- Действия -->
              <td class="px-6 py-4 whitespace-nowrap">
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

    <!-- Модальное окно управления категориями -->
    <div
      v-if="showCategoryModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-xs p-4"
    >
      <div
        class="w-full max-w-2xl bg-[#1A1D23] border border-[#333842] shadow-2xl overflow-hidden flex flex-col max-h-[90vh]"
      >
        <!-- Шапка -->
        <div
          class="flex items-center justify-between px-6 py-4 border-b border-[#333842] bg-[#13151A]"
        >
          <div class="flex items-center gap-2.5">
            <FolderTree class="w-5 h-5 text-[#B8A276]" :stroke-width="1.5" />
            <h2 class="text-lg font-light text-[#E8E9ED]">
              Управление категориями
            </h2>
          </div>
          <button
            @click="showCategoryModal = false"
            class="text-[#9BA1AB] hover:text-white transition-colors"
          >
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Ошибка -->
        <div
          v-if="catActionError"
          class="mx-6 mt-4 p-3 bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-light"
        >
          {{ catActionError }}
        </div>

        <!-- Форма добавления новой категории -->
        <div class="p-6 border-b border-[#333842] bg-[#13151A]/50">
          <div class="text-xs uppercase tracking-wider text-[#9BA1AB] mb-3 font-light">
            Создать новую категорию
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-3">
            <input
              v-model="newCatName"
              type="text"
              placeholder="Название (например: Освещение)"
              class="w-full px-3.5 py-2.5 bg-[#13151A] border border-[#333842] text-sm text-[#E8E9ED] focus:outline-none focus:border-[#3B82F6]"
            />
            <input
              v-model="newCatDesc"
              type="text"
              placeholder="Описание (опционально)"
              class="w-full px-3.5 py-2.5 bg-[#13151A] border border-[#333842] text-sm text-[#E8E9ED] focus:outline-none focus:border-[#3B82F6]"
            />
          </div>
          <button
            @click="handleCreateCategory"
            :disabled="!newCatName.trim() || isCreatingCat"
            class="flex items-center gap-2 px-4 py-2 bg-[#B8A276] hover:bg-[#B8A276]/90 text-[#13151A] text-xs font-medium rounded transition-colors disabled:opacity-40"
          >
            <Plus class="w-3.5 h-3.5" />
            <span>{{ isCreatingCat ? "Создание..." : "Добавить категорию" }}</span>
          </button>
        </div>

        <!-- Список категорий -->
        <div class="p-6 flex-1 overflow-y-auto space-y-3">
          <div class="text-xs uppercase tracking-wider text-[#9BA1AB] font-light">
            Существующие категории ({{ categories.length }})
          </div>

          <div
            v-if="categories.length === 0"
            class="py-10 text-center text-[#9BA1AB] font-light text-sm"
          >
            Категорий пока нет
          </div>

          <div
            v-for="cat in categories"
            :key="cat.id"
            class="flex items-center justify-between gap-3 p-3.5 bg-[#13151A] border border-[#333842] rounded hover:border-[#333842]/80 transition-colors"
          >
            <!-- Редактирование на месте -->
            <div v-if="editingCatId === cat.id" class="flex-1 flex items-center gap-2">
              <input
                v-model="editingCatName"
                type="text"
                class="flex-1 px-3 py-1.5 bg-[#1A1D23] border border-[#3B82F6] text-sm text-white focus:outline-none rounded"
                @keyup.enter="saveEditCategory(cat.id)"
                @keyup.esc="cancelEditCategory"
                autofocus
              />
              <button
                @click="saveEditCategory(cat.id)"
                class="px-3 py-1.5 bg-[#3B82F6] text-white text-xs font-medium rounded hover:bg-[#3B82F6]/90"
              >
                Сохранить
              </button>
              <button
                @click="cancelEditCategory"
                class="px-2.5 py-1.5 border border-[#333842] text-[#9BA1AB] text-xs hover:text-white rounded"
              >
                Отмена
              </button>
            </div>

            <!-- Обычное отображение -->
            <div v-else class="flex-1">
              <div class="flex items-center gap-2">
                <span class="text-sm font-medium text-[#E8E9ED]">{{ cat.name }}</span>
                <span class="text-xs text-[#B8A276] px-2 py-0.5 rounded-full border border-[#B8A276]/30 bg-[#B8A276]/10">
                  {{ cat.products_count ?? 0 }} товаров
                </span>
              </div>
              <p v-if="cat.description" class="text-xs text-[#9BA1AB] mt-0.5 line-clamp-1">
                {{ cat.description }}
              </p>
            </div>

            <div v-if="editingCatId !== cat.id" class="flex items-center gap-2">
              <button
                @click="startEditCategory(cat)"
                class="p-1.5 text-[#9BA1AB] hover:text-[#3B82F6] transition-colors"
                title="Переименовать"
              >
                <Pencil class="w-4 h-4" />
              </button>
              <button
                @click="handleDeleteCategory(cat)"
                class="p-1.5 text-[#9BA1AB] hover:text-red-400 transition-colors"
                title="Удалить категорию"
              >
                <Trash2 class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <!-- Подвал -->
        <div class="px-6 py-4 border-t border-[#333842] bg-[#13151A] flex justify-end">
          <button
            @click="showCategoryModal = false"
            class="px-5 py-2 text-sm text-[#9BA1AB] hover:text-white transition-colors font-light"
          >
            Закрыть
          </button>
        </div>
      </div>
    </div>

    <!-- Модальное окно импорта из Excel -->
    <div
      v-if="showImportModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-xs p-4"
    >
      <div
        class="w-full max-w-xl bg-[#1A1D23] border border-[#333842] shadow-2xl overflow-hidden"
      >
        <!-- Шапка модалки -->
        <div
          class="flex items-center justify-between px-6 py-4 border-b border-[#333842] bg-[#13151A]"
        >
          <div class="flex items-center gap-2.5">
            <FileSpreadsheet class="w-5 h-5 text-[#3B82F6]" :stroke-width="1.5" />
            <h2 class="text-lg font-light text-[#E8E9ED]">
              Импорт товаров из Excel
            </h2>
          </div>
          <button
            @click="closeImportModal"
            class="text-[#9BA1AB] hover:text-white transition-colors"
          >
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Тело модалки -->
        <div class="p-6 space-y-5">
          <!-- Ошибка -->
          <div
            v-if="importError"
            class="flex items-start gap-2.5 p-3.5 bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-light"
          >
            <AlertCircle class="w-4 h-4 shrink-0 mt-0.5" />
            <div>{{ importError }}</div>
          </div>

          <!-- Результат импорта -->
          <div
            v-if="importResult"
            class="p-4 bg-[#13151A] border border-[#333842] space-y-3"
          >
            <div class="flex items-center gap-2 text-emerald-400 text-sm font-medium">
              <CheckCircle2 class="w-4 h-4" />
              <span>Импорт успешно завершен!</span>
            </div>
            <div class="grid grid-cols-3 gap-2 pt-2 text-center text-xs">
              <div class="p-2 border border-[#333842] bg-[#1A1D23]">
                <div class="text-[#9BA1AB]">Создано</div>
                <div class="text-base font-semibold text-emerald-400 mt-1">
                  {{ importResult.created }}
                </div>
              </div>
              <div class="p-2 border border-[#333842] bg-[#1A1D23]">
                <div class="text-[#9BA1AB]">Обновлено</div>
                <div class="text-base font-semibold text-[#3B82F6] mt-1">
                  {{ importResult.updated }}
                </div>
              </div>
              <div class="p-2 border border-[#333842] bg-[#1A1D23]">
                <div class="text-[#9BA1AB]">Обработано строк</div>
                <div class="text-base font-semibold text-[#E8E9ED] mt-1">
                  {{ importResult.total_rows }}
                </div>
              </div>
            </div>

            <!-- Замечания по строкам если были -->
            <div
              v-if="importResult.errors && importResult.errors.length"
              class="mt-3 p-3 border border-amber-500/30 bg-amber-500/10 text-xs text-amber-300 space-y-1 max-h-36 overflow-y-auto"
            >
              <div class="font-medium mb-1">Замечания при обработке:</div>
              <div v-for="(err, idx) in importResult.errors" :key="idx">
                • {{ err }}
              </div>
            </div>
          </div>

          <!-- Зона загрузки файла -->
          <div
            v-if="!importResult"
            class="space-y-4"
          >
            <div>
              <label
                class="block text-xs text-[#9BA1AB] tracking-widest uppercase mb-2 font-light"
              >
                Категория для товаров без категории
              </label>
              <select
                v-model="importCategory"
                class="w-full px-3.5 py-2.5 bg-[#13151A] border border-[#333842] text-[#E8E9ED] text-sm focus:outline-none focus:border-[#3B82F6] font-light appearance-none"
              >
                <option value="">Без категории (автоматически)</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                  {{ cat.name }}
                </option>
              </select>
              <p class="text-[11px] text-[#9BA1AB]/70 mt-1">
                Если в файле колонка категории отсутствует или пустая, товары будут назначены в выбранную категорию или в «Без категории».
              </p>
            </div>

            <!-- Валюта цен в файле -->
            <div>
              <label
                class="block text-xs text-[#9BA1AB] tracking-widest uppercase mb-2 font-light"
              >
                Валюта цен в файле
              </label>
              <div class="grid grid-cols-2 gap-3">
                <label
                  :class="[
                    'flex flex-col p-3 border cursor-pointer text-xs font-light transition-all rounded',
                    importCurrency === 'KZT'
                      ? 'border-[#3B82F6] bg-[#3B82F6]/15 text-white shadow-xs'
                      : 'border-[#333842] text-[#9BA1AB] hover:border-[#333842]/80 bg-[#13151A]'
                  ]"
                >
                  <div class="flex items-center gap-2">
                    <input type="radio" value="KZT" v-model="importCurrency" class="accent-[#3B82F6]" />
                    <span class="font-medium text-[#E8E9ED]">₸ Тенге (KZT)</span>
                  </div>
                  <span class="text-[10px] text-[#9BA1AB] mt-1 pl-5">
                    Автоконвертация в USD по курсу
                  </span>
                </label>

                <label
                  :class="[
                    'flex flex-col p-3 border cursor-pointer text-xs font-light transition-all rounded',
                    importCurrency === 'USD'
                      ? 'border-[#3B82F6] bg-[#3B82F6]/15 text-white shadow-xs'
                      : 'border-[#333842] text-[#9BA1AB] hover:border-[#333842]/80 bg-[#13151A]'
                  ]"
                >
                  <div class="flex items-center gap-2">
                    <input type="radio" value="USD" v-model="importCurrency" class="accent-[#3B82F6]" />
                    <span class="font-medium text-[#E8E9ED]">$ Доллары (USD)</span>
                  </div>
                  <span class="text-[10px] text-[#9BA1AB] mt-1 pl-5">
                    Цены уже в долларах США
                  </span>
                </label>
              </div>
            </div>

            <!-- Drag & drop area -->
            <div
              @dragover.prevent
              @drop="handleDrop"
              class="relative border-2 border-dashed border-[#333842] hover:border-[#3B82F6]/50 bg-[#13151A] p-6 text-center cursor-pointer transition-colors"
            >
              <input
                type="file"
                accept=".xlsx, .xls"
                @change="handleFileSelect"
                class="absolute inset-0 opacity-0 cursor-pointer w-full h-full"
              />
              <div class="flex flex-col items-center justify-center space-y-2 pointer-events-none">
                <FileUp class="w-8 h-8 text-[#3B82F6]" :stroke-width="1.5" />
                <p class="text-sm text-[#E8E9ED] font-light">
                  <span v-if="importFile" class="font-medium text-[#3B82F6]">
                    {{ importFile.name }}
                  </span>
                  <span v-else>
                    Нажмите для выбора файла или перетащите сюда
                  </span>
                </p>
                <p class="text-xs text-[#9BA1AB]/60">
                  Поддерживаются файлы Excel (.xlsx, .xls)
                </p>
              </div>
            </div>

            <!-- Подсказка и ссылка на шаблон -->
            <div class="flex items-center justify-between text-xs text-[#9BA1AB] pt-2">
              <span>Нужен правильный формат колонок?</span>
              <button
                type="button"
                @click="handleDownloadTemplate"
                class="text-[#3B82F6] hover:underline flex items-center gap-1"
              >
                <Download class="w-3.5 h-3.5" />
                Скачать образец таблицы
              </button>
            </div>
          </div>
        </div>

        <!-- Подвал модалки -->
        <div
          class="flex items-center justify-end gap-3 px-6 py-4 border-t border-[#333842] bg-[#13151A]"
        >
          <button
            type="button"
            @click="closeImportModal"
            class="px-4 py-2 text-sm text-[#9BA1AB] hover:text-white transition-colors font-light"
          >
            {{ importResult ? "Закрыть" : "Отмена" }}
          </button>
          <button
            v-if="!importResult"
            type="button"
            @click="submitImport"
            :disabled="!importFile || isImporting"
            class="flex items-center gap-2 px-5 py-2 bg-[#3B82F6] hover:bg-[#3B82F6]/90 text-white text-sm font-medium tracking-wide transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          >
            <Upload class="w-4 h-4" />
            <span>{{ isImporting ? "Импорт..." : "Загрузить товары" }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
