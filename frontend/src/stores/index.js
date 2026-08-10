import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "../services/api";

export const useAuthStore = defineStore("auth", () => {
  const user = ref(null);
  const accessToken = ref(localStorage.getItem("access_token"));
  const refreshToken = ref(localStorage.getItem("refresh_token"));
  const isLoading = ref(false);

  const isAuthenticated = computed(() => !!accessToken.value);
  const isAdmin = computed(() => user.value?.is_staff === true);

  const login = async (username, password) => {
    isLoading.value = true;
    try {
      const response = await api.post("/auth/login/", { username, password });

      accessToken.value = response.data.access;
      refreshToken.value = response.data.refresh;
      user.value = response.data.user;

      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);
      localStorage.setItem("user", JSON.stringify(response.data.user));

      // Явно установить Authorization header для всех последующих запросов
      api.defaults.headers.common.Authorization = `Bearer ${response.data.access}`;

      return true;
    } catch (error) {
      console.error("Login error:", error);
      return false;
    } finally {
      isLoading.value = false;
    }
  };

  const logout = () => {
    user.value = null;
    accessToken.value = null;
    refreshToken.value = null;
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    // Удалить Authorization header при logout
    delete api.defaults.headers.common.Authorization;
  };

  const getMe = async () => {
    try {
      const response = await api.get("/auth/me/");
      user.value = response.data;
      localStorage.setItem("user", JSON.stringify(response.data));
    } catch (error) {
      console.error("Failed to get user info:", error);
      logout();
    }
  };

  const init = () => {
    const stored = localStorage.getItem("user");
    if (stored) {
      user.value = JSON.parse(stored);
    }
    
    const token = localStorage.getItem("access_token");
    if (token) {
      // Если токен существует в localStorage, убедись что он есть в API headers
      api.defaults.headers.common.Authorization = `Bearer ${token}`;
      accessToken.value = token;
    }
  };

  return {
    user,
    accessToken,
    refreshToken,
    isLoading,
    isAuthenticated,
    isAdmin,
    login,
    logout,
    getMe,
    init,
  };
});

export const useProductStore = defineStore("products", () => {
  const products = ref([]);
  const categories = ref([]);
  const currentProduct = ref(null);
  const isLoading = ref(false);
  const error = ref(null);

  const getProducts = async (params = {}) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await api.get("/products/", { params });
      products.value = response.data.results || response.data;
      return products.value;
    } catch (err) {
      error.value = err.message;
      return [];
    } finally {
      isLoading.value = false;
    }
  };

  const getProduct = async (id) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await api.get(`/products/${id}/`);
      currentProduct.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.message;
      return null;
    } finally {
      isLoading.value = false;
    }
  };

  const getCategories = async () => {
    try {
      const response = await api.get("/categories/");
      categories.value = response.data.results || response.data;
      return categories.value;
    } catch (err) {
      error.value = err.message;
      return [];
    }
  };

  const createProduct = async (productData) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await api.post("/products/", productData);
      products.value.push(response.data);
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateProduct = async (id, productData) => {
    isLoading.value = true;
    error.value = null;
    try {
      const response = await api.put(`/products/${id}/`, productData);
      const index = products.value.findIndex((p) => p.id === id);
      if (index >= 0) {
        products.value[index] = response.data;
      }
      return response.data;
    } catch (err) {
      error.value = err.response?.data?.detail || err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const deleteProduct = async (id) => {
    isLoading.value = true;
    error.value = null;
    try {
      await api.delete(`/products/${id}/`);
      products.value = products.value.filter((p) => p.id !== id);
      return true;
    } catch (err) {
      error.value = err.response?.data?.detail || err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  return {
    products,
    categories,
    currentProduct,
    isLoading,
    error,
    getProducts,
    getProduct,
    getCategories,
    createProduct,
    updateProduct,
    deleteProduct,
  };
});
