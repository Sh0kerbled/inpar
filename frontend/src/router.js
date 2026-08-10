import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "./stores/index.js";
import { defineAsyncComponent } from "vue";

const HomePage = defineAsyncComponent(() => import("./pages/HomePage.vue"));
const ProductsPage = defineAsyncComponent(
  () => import("./pages/ProductsPage.vue"),
);
const ProductDetailPage = defineAsyncComponent(
  () => import("./pages/ProductDetailPage.vue"),
);
const AdminLoginPage = defineAsyncComponent(
  () => import("./pages/AdminLoginPage.vue"),
);
const AdminDashboard = defineAsyncComponent(
  () => import("./pages/AdminDashboard.vue"),
);
const AdminProductsPage = defineAsyncComponent(
  () => import("./pages/AdminProductsPage.vue"),
);
const AdminProductForm = defineAsyncComponent(
  () => import("./pages/AdminProductForm.vue"),
);
const ProjectsPage = defineAsyncComponent(
  () => import("./pages/ProjectsPage.vue"),
);
const NotFoundPage = defineAsyncComponent(
  () => import("./pages/NotFoundPage.vue"),
);

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomePage,
    meta: { layout: "landing" },
  },
  {
    path: "/projects",
    name: "Projects",
    component: ProjectsPage,
    meta: { layout: "landing" },
  },
  {
    path: "/products",
    name: "Products",
    component: ProductsPage,
    meta: { layout: "app" },
  },
  {
    path: "/products/:id",
    name: "ProductDetail",
    component: ProductDetailPage,
  },
  {
    path: "/admin/login",
    name: "AdminLogin",
    component: AdminLoginPage,
  },
  {
    path: "/admin",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/products",
    name: "AdminProducts",
    component: AdminProductsPage,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/products/new",
    name: "AdminProductNew",
    component: AdminProductForm,
    meta: { requiresAuth: true },
  },
  {
    path: "/admin/products/:id/edit",
    name: "AdminProductEdit",
    component: AdminProductForm,
    meta: { requiresAuth: true },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: NotFoundPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    if (to.hash) {
      return {
        el: to.hash,
        behavior: "smooth",
      };
    }
    return { top: 0 };
  },
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  if (to.meta.requiresAuth) {
    if (authStore.isAuthenticated && authStore.isAdmin) {
      next();
    } else {
      next("/admin/login");
    }
  } else {
    next();
  }
});

export default router;
