<template>
  <div class="min-h-screen bg-[#1A1D23] text-[#E8E9ED] py-24">
    <div class="max-w-3xl mx-auto px-6 lg:px-12">
      <div class="flex flex-col items-center justify-center gap-6 bg-[#13151A]/80 border border-[#333842] rounded-4xl p-10 shadow-[0_30px_90px_rgba(0,0,0,0.25)] transition-transform duration-500 hover:-translate-y-1">
        <div class="text-center">
          <p class="text-sm uppercase tracking-[0.35em] text-[#9BA1AB] mb-4">
            Страница не найдена
          </p>
          <h1 class="text-6xl font-semibold text-[#B8A276] mb-4">404</h1>
          <p class="text-lg text-[#E8E9ED] font-light leading-8">
            Такой страницы нет в каталоге. Возможно, ссылка устарела или вы просто ошиблись.
          </p>
        </div>

        <div class="grid gap-3 sm:grid-cols-2 w-full">
          <router-link
            to="/"
            class="inline-flex items-center justify-center rounded-3xl border border-[#3B82F6]/40 bg-[#1F2230] px-5 py-3 text-sm text-[#E8E9ED] transition hover:border-[#3B82F6] hover:bg-[#252B40]"
          >
            На главную
          </router-link>
          <router-link
            to="/products"
            class="inline-flex items-center justify-center rounded-3xl bg-[#B8A276] px-5 py-3 text-sm font-semibold text-[#13151A] transition hover:bg-[#A78A54]"
          >
            В каталог товаров
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>
