<script setup>
import { ref, reactive, onMounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore, useProductStore } from "../stores/index";
import {
  LogOut,
  Settings,
  Package,
  Plus,
  ArrowLeft,
  Upload,
  X,
  ChevronDown,
} from "lucide-vue-next";
import api from "../services/api";

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const productStore = useProductStore();
const categories = ref([]);
const error = ref("");
const imageFile = ref(null);
const imagePreview = ref(null);
const exchangeRate = ref(460);
const showCreateCategory = ref(false);
const newCategoryName = ref("");
const newCategoryError = ref("");
const isCreatingCategory = ref(false);

const isEditMode = !!route.params.id;

const form = reactive({
  name: "",
  description: "",
  price_usd: "",
  stock_quantity: "",
  category: "",
});

const priceKztPreview = computed(() => {
  if (!form.price_usd || form.price_usd === "") return 0;
  return (parseFloat(form.price_usd) * exchangeRate.value).toFixed(2);
});

const logout = () => {
  authStore.logout();
  router.push("/admin/login");
};

const handleImageChange = (e) => {
  const file = e.target.files[0];
  if (!file) return;
  imageFile.value = file;
  imagePreview.value = URL.createObjectURL(file);
};

const removeImage = () => {
  imageFile.value = null;
  imagePreview.value = null;
};

const createNewCategory = async () => {
  if (!newCategoryName.value.trim()) {
    newCategoryError.value = "Название категории не может быть пусто";
    return;
  }

  isCreatingCategory.value = true;
  newCategoryError.value = "";

  try {
    const response = await api.post("/categories/", {
      name: newCategoryName.value,
      description: "",
      is_active: true,
    });

    categories.value.push(response.data);
    form.category = response.data.id;
    showCreateCategory.value = false;
    newCategoryName.value = "";
  } catch (err) {
    newCategoryError.value =
      err.response?.data?.name?.[0] ||
      err.response?.data?.detail ||
      "Ошибка при создании категории";
  } finally {
    isCreatingCategory.value = false;
  }
};

const handleSubmit = async () => {
  error.value = "";

  if (!form.price_usd || form.price_usd === "") {
    error.value = "Цена товара обязательна";
    return;
  }

  try {
    const formData = new FormData();
    formData.append("name", form.name);
    formData.append("description", form.description);
    formData.append("price_usd", form.price_usd);
    formData.append("stock_quantity", form.stock_quantity);
    formData.append("category", form.category);
    if (imageFile.value) {
      formData.append("main_image", imageFile.value);
    }

    if (isEditMode) {
      await api.patch(`/products/${route.params.id}/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
    } else {
      await api.post("/products/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
    }
    router.push("/admin/products");
  } catch (err) {
    error.value =
      err.response?.data?.detail ||
      JSON.stringify(err.response?.data) ||
      err.message ||
      "Ошибка при сохранении";
  }
};

onMounted(async () => {
  try {
    const rateResponse = await api.get("/exchange-rate/");
    exchangeRate.value = rateResponse.data.rate;
  } catch (err) {
    console.error("Failed to get exchange rate:", err);
  }

  categories.value = await productStore.getCategories();
  if (isEditMode) {
    const product = await productStore.getProduct(route.params.id);
    if (product) {
      form.name = product.name;
      form.description = product.description;
      form.price_usd = product.price_usd;
      form.stock_quantity = product.stock_quantity;
      form.category = product.category;
      if (product.main_image) {
        imagePreview.value = product.main_image;
      }
    }
  }
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
          class="flex items-center gap-3 px-4 py-3 text-sm text-[#9BA1AB] hover:text-[#E8E9ED] hover:bg-[#252932] transition-all duration-200 font-light"
        >
          <Package class="w-4 h-4" :stroke-width="1.5" />
          Товары
        </router-link>
        <router-link
          to="/admin/products/new"
          class="flex items-center gap-3 px-4 py-3 text-sm text-[#E8E9ED] bg-[#252932] border-l-2 border-[#B8A276] font-light"
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
      <div class="mb-10 flex items-center gap-4">
        <router-link
          to="/admin/products"
          class="text-[#9BA1AB] hover:text-[#E8E9ED] transition-colors"
        >
          <ArrowLeft class="w-5 h-5" :stroke-width="1.5" />
        </router-link>
        <h1 class="text-3xl font-light tracking-tight">
          {{ isEditMode ? "Редактировать товар" : "Новый товар" }}
        </h1>
      </div>

      <div class="max-w-2xl border border-[#333842] bg-[#1A1D23]/60 p-10">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div
            v-if="error"
            class="px-4 py-3 border border-red-500/30 bg-red-500/10 text-red-400 text-sm font-light"
          >
            {{ error }}
          </div>

          <div>
            >
            <label
              class="block text-xs text-[#9BA1AB] tracking-[0.15em] uppercase mb-3 font-light"
            >
              Название *
            </label>
            <input
              v-model="form.name"
              type="text"
              required
              class="w-full px-4 py-3 bg-[#13151A] border border-[#333842] text-[#E8E9ED] focus:outline-none focus:border-[#3B82F6] transition-colors duration-300 font-light"
            />
          </div>

          <div>
            >
            <label
              class="block text-xs text-[#9BA1AB] tracking-[0.15em] uppercase mb-3 font-light"
            >
              Описание
            </label>
            <textarea
              v-model="form.description"
              rows="4"
              class="w-full px-4 py-3 bg-[#13151A] border border-[#333842] text-[#E8E9ED] focus:outline-none focus:border-[#3B82F6] transition-colors duration-300 font-light resize-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label
                class="block text-xs text-[#9BA1AB] tracking-[0.15em] uppercase mb-3 font-light"
              >
                Цена (USD) *
              </label>
              <input
                v-model="form.price_usd"
                type="number"
                step="0.01"
                required
                class="w-full px-4 py-3 bg-[#13151A] border border-[#333842] text-[#E8E9ED] focus:outline-none focus:border-[#3B82F6] transition-colors duration-300 font-light"
              />
              <p
                v-if="priceKztPreview"
                class="text-xs text-[#B8A276] mt-2 font-light"
              >
                ≈ {{ priceKztPreview }} ₸
              </p>
            </div>
            <div>
              <label
                class="block text-xs text-[#9BA1AB] tracking-[0.15em] uppercase mb-3 font-light"
              >
                Количество *
              </label>
              <input
                v-model="form.stock_quantity"
                type="number"
                required
                class="w-full px-4 py-3 bg-[#13151A] border border-[#333842] text-[#E8E9ED] focus:outline-none focus:border-[#3B82F6] transition-colors duration-300 font-light"
              />
            </div>
          </div>

          <div>
            >
            <label
              class="block text-xs text-[#9BA1AB] tracking-[0.15em] uppercase mb-3 font-light"
            >
              Категория *
            </label>
            <div class="space-y-2">
              <select
                v-model="form.category"
                class="w-full px-4 py-3 bg-[#13151A] border border-[#333842] text-[#E8E9ED] focus:outline-none focus:border-[#3B82F6] transition-colors duration-300 font-light appearance-none cursor-pointer"
              >
                <option value="" disabled>Выберите категорию</option>
                <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                  {{ cat.name }}
                </option>
              </select>
              <button
                type="button"
                @click="showCreateCategory = !showCreateCategory"
                class="w-full flex items-center justify-center gap-2 px-4 py-2 text-xs text-[#9BA1AB] border border-[#333842] hover:border-[#3B82F6]/50 hover:text-[#3B82F6] transition-colors duration-300 font-light"
              >
                <Plus class="w-3.5 h-3.5" :stroke-width="1.5" />
                Создать новую категорию
              </button>

              <!-- Create category form -->
              <div
                v-if="showCreateCategory"
                class="space-y-3 p-4 border border-[#333842] bg-[#1A1D23]/60"
              >
                <div
                  v-if="newCategoryError"
                  class="px-3 py-2 bg-red-500/10 border border-red-500/30 text-red-400 text-xs font-light"
                >
                  {{ newCategoryError }}
                </div>
                <input
                  v-model="newCategoryName"
                  type="text"
                  placeholder="Название новой категории"
                  class="w-full px-4 py-3 bg-[#13151A] border border-[#333842] text-[#E8E9ED] placeholder-[#9BA1AB]/50 focus:outline-none focus:border-[#3B82F6] transition-colors duration-300 font-light text-sm"
                />
                <div class="flex gap-2">
                  <button
                    type="button"
                    @click="createNewCategory"
                    :disabled="isCreatingCategory"
                    class="flex-1 px-3 py-2 bg-[#3B82F6] text-white text-xs font-light hover:bg-[#3B82F6]/90 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {{ isCreatingCategory ? "Создание..." : "Создать" }}
                  </button>
                  <button
                    type="button"
                    @click="
                      showCreateCategory = false;
                      newCategoryName = '';
                      newCategoryError = '';
                    "
                    class="flex-1 px-3 py-2 text-[#9BA1AB] border border-[#333842] text-xs font-light hover:bg-[#333842]/50 transition-colors"
                  >
                    Отмена
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div>
            >
            <label
              class="block text-xs text-[#9BA1AB] tracking-[0.15em] uppercase mb-3 font-light"
            >
              Изображение
            </label>

            <!-- Preview -->
            <div
              v-if="imagePreview"
              class="relative mb-3 w-full aspect-video bg-[#13151A] border border-[#333842] overflow-hidden"
            >
              <img
                :src="imagePreview"
                alt="Preview"
                class="w-full h-full object-contain"
              />
              <button
                type="button"
                @click="removeImage"
                class="absolute top-3 right-3 p-1.5 bg-[#13151A]/80 border border-[#333842] text-[#9BA1AB] hover:text-red-400 hover:border-red-500/50 transition-all duration-200"
              >
                <X class="w-4 h-4" :stroke-width="1.5" />
              </button>
            </div>

            <!-- Upload zone -->
            <label
              v-else
              class="flex flex-col items-center justify-center w-full py-10 border border-dashed border-[#333842] hover:border-[#3B82F6]/50 cursor-pointer transition-colors duration-300 group"
            >
              <Upload
                class="w-8 h-8 text-[#9BA1AB]/50 group-hover:text-[#3B82F6]/70 mb-3 transition-colors duration-300"
                :stroke-width="1.5"
              />
              <span class="text-sm text-[#9BA1AB] font-light"
                >Нажмите для загрузки</span
              >
              <span class="text-xs text-[#9BA1AB]/50 font-light mt-1"
                >PNG, JPG, WEBP до 10MB</span
              >
              <input
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleImageChange"
              />
            </label>

            <!-- Заменить изображение если уже есть -->
            <label
              v-if="imagePreview"
              class="flex items-center gap-2 mt-2 text-xs text-[#9BA1AB] hover:text-[#3B82F6] cursor-pointer transition-colors duration-200 font-light"
            >
              <Upload class="w-3.5 h-3.5" :stroke-width="1.5" />
              Заменить изображение
              <input
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleImageChange"
              />
            </label>
          </div>

          <!-- Submit -->
          <div class="flex justify-end pt-4">
            <button
              type="submit"
              :disabled="productStore.isLoading"
              class="px-8 py-3 border border-[#3B82F6]/50 text-[#3B82F6] text-sm tracking-widest uppercase font-light hover:bg-[#3B82F6]/10 transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {{ productStore.isLoading ? "Сохранение..." : "Сохранить" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
