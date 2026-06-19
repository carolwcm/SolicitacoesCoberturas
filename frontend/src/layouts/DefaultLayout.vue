<template>
  <div class="relative h-screen overflow-hidden md:flex">
    <!-- Mobile Menu -->
    <div class="bg-paper-sidebar text-gray-100 flex justify-between md:hidden shrink-0">
      <router-link to="/" class="block p-4 text-white font-bold">Hospital Curativos</router-link>
      <button @click="sidebarOpen = !sidebarOpen" class="p-4 focus:outline-none focus:bg-paper-active-link">
        <Bars3Icon class="h-6 w-6" />
      </button>
    </div>

    <!-- Sidebar -->
    <aside :class="{ '-translate-x-full': !sidebarOpen }" class="bg-paper-sidebar text-gray-100 w-64 flex flex-col justify-between py-7 px-4 absolute inset-y-0 left-0 transform md:relative md:translate-x-0 transition duration-200 ease-in-out z-20 h-full shrink-0">
      <div class="space-y-6">
        <div @click="() => router.push('/')" class="cursor-pointer flex items-center justify-center px-1 py-1">
          <img src="/woundflow.png" alt="WoundFlow Logo" class="w-full max-h-24 object-contain rounded-xl">
        </div>
        <div class="my-6">
          <div class="border-t border-white border-opacity-20"></div>
        </div>

        <nav class="space-y-2">
          <router-link v-if="authStore.isAuthenticated" to="/solicitacoes" class="flex items-center space-x-2 py-2.5 px-4 rounded transition duration-200 hover:bg-paper-active-link hover:text-white">
            <ClipboardDocumentCheckIcon class="h-6 w-6" />
            <span>Painel</span>
          </router-link>

          <router-link v-if="authStore.isAuthenticated" to="/relatorios" class="flex items-center space-x-2 py-2.5 px-4 rounded transition duration-200 hover:bg-paper-active-link hover:text-white">
            <ChartBarIcon class="h-6 w-6" />
            <span>Relatórios</span>
          </router-link>
        </nav>
      </div>

      <!-- Logo HC no canto inferior da barra lateral -->
      <div class="mt-auto pt-4 border-t border-white border-opacity-20 flex items-center justify-center px-2">
        <img src="/hc_logo.jpg" alt="Hospital Logo" class="w-full max-h-14 object-contain rounded-lg opacity-85 hover:opacity-100 transition-opacity">
      </div>
    </aside>

    <!-- Content -->
    <div class="flex-1 flex flex-col bg-paper-bg overflow-y-auto h-full">
      <main class="flex-1">
        <div class="container py-4 md:py-6">
          <router-view />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import {
  ShieldCheckIcon,
  Bars3Icon,
  ClipboardDocumentCheckIcon,
  ChartBarIcon,
} from '@heroicons/vue/24/outline';
import { useAuthStore } from '../stores/auth';

const sidebarOpen = ref(false);
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

// Close sidebar on route change
watch(() => route.path, () => {
  sidebarOpen.value = false;
});
</script>