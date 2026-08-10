<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/index";

const router = useRouter();
const authStore = useAuthStore();
const username = ref("");
const password = ref("");
const error = ref("");

const handleLogin = async () => {
  error.value = "";
  const success = await authStore.login(username.value, password.value);
  if (success) {
    router.push("/admin");
  } else {
    error.value = "Неверное имя пользователя или пароль";
  }
};
</script>

<template>
  <div class="min-h-screen bg-[#13151A] flex items-center justify-center px-6">
    <div class="w-full max-w-md">
      <div class="mb-10 text-center">
        <router-link
          to="/"
          class="text-2xl font-light tracking-tight text-[#E8E9ED] hover:text-white transition-colors duration-200"
        >
          INPAR
        </router-link>
        <div class="h-px w-12 bg-[#B8A276] mx-auto mt-4" />
      </div>

      <div
        class="border border-[#333842] bg-[#1A1D23]/60 backdrop-blur-sm p-10"
      >
        <h1 class="text-2xl font-light tracking-tight text-[#E8E9ED] mb-8">
          Панель администратора
        </h1>

        <form @submit.prevent="handleLogin" class="space-y-6">
          <div
            v-if="error"
            class="px-4 py-3 border border-red-500/30 bg-red-500/10 text-red-400 text-sm font-light"
          >
            {{ error }}
          </div>

          <div>
            <label
              class="block text-xs text-[#9BA1AB] tracking-[0.15em] uppercase mb-3 font-light"
            >
              Имя пользователя
            </label>
            <input
              v-model="username"
              type="text"
              required
              class="w-full px-4 py-3 bg-[#13151A] border border-[#333842] text-[#E8E9ED] placeholder-[#9BA1AB]/40 focus:outline-none focus:border-[#3B82F6] transition-colors duration-300 font-light"
            />
          </div>

          <div>
            <label
              class="block text-xs text-[#9BA1AB] tracking-[0.15em] uppercase mb-3 font-light"
            >
              Пароль
            </label>
            <input
              v-model="password"
              type="password"
              required
              class="w-full px-4 py-3 bg-[#13151A] border border-[#333842] text-[#E8E9ED] placeholder-[#9BA1AB]/40 focus:outline-none focus:border-[#3B82F6] transition-colors duration-300 font-light"
            />
          </div>

          <button
            type="submit"
            :disabled="authStore.isLoading"
            class="w-full py-3 border border-[#3B82F6]/50 text-[#3B82F6] text-sm tracking-widest uppercase font-light hover:bg-[#3B82F6]/10 transition-all duration-300 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            {{ authStore.isLoading ? "Вход..." : "Войти" }}
          </button>
        </form>
      </div>

      <p
        class="text-center text-xs text-[#9BA1AB]/40 mt-6 font-light tracking-wider"
      >
        Доступ только для авторизованных сотрудников
      </p>
    </div>
  </div>
</template>
