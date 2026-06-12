<template>
  <div class="relative flex items-center gap-2">
    <span class="text-sm font-semibold text-slate-700 select-none">{{ authStore.user?.givenName?.[0] || authStore.user?.username || 'Usuário' }}</span>
    <button @click="isOpen = !isOpen" class="relative z-10 block h-12 w-12 rounded-xl overflow-hidden focus:outline-none transition-transform active:scale-95 cursor-pointer">
      <img src="/logousuario.png" alt="User Logo" class="h-full w-full object-cover">
    </button>

    <div v-if="isOpen" @click="isOpen = false" class="fixed inset-0 h-full w-full z-10"></div>

    <div v-if="isOpen" class="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-2xl z-20 border border-gray-100 overflow-hidden transform origin-top-right transition-all">
      <div class="p-5">
        <div class="flex items-center space-x-4">
          <div class="flex-shrink-0">
            <div class="h-18 w-18 rounded-xl bg-gray-100 flex items-center justify-center border border-gray-200 overflow-hidden">
              <img src="/logousuario.png" alt="User Logo" class="h-full w-full object-cover">
            </div>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-lg font-bold text-gray-900 leading-tight break-words">
              {{ authStore.user?.givenName?.[0] || authStore.user?.username || 'Usuário' }}
            </p>
            <p class="text-sm text-gray-500 break-all mt-0.5">
              {{ authStore.user?.userPrincipalName?.[0] || authStore.user?.username }}
            </p>
          </div>
        </div>
      </div>
      
      <div class="border-t border-gray-100 bg-gray-55/50">
        <div class="p-5 space-y-4 text-sm">
          <div class="flex items-start">
            <BriefcaseIcon class="h-5 w-5 mr-3 text-gray-400 shrink-0 mt-0.5" />
            <div class="flex-1">
              <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">Cargo</p>
              <p class="text-gray-800 font-medium leading-snug">{{ authStore.user?.title?.[0] || 'Não Informado' }}</p>
            </div>
          </div>
          <div class="flex items-start">
            <BuildingOffice2Icon class="h-5 w-5 mr-3 text-gray-400 shrink-0 mt-0.5" />
            <div class="flex-1">
              <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">Setor</p>
              <p class="text-gray-800 font-medium leading-snug">{{ authStore.user?.department?.[0] || 'Não Informado' }}</p>
            </div>
          </div>
          <div class="flex items-start">
            <IdentificationIcon class="h-5 w-5 mr-3 text-gray-400 shrink-0 mt-0.5" />
            <div class="flex-1">
              <p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider mb-0.5">Matrícula</p>
              <p class="text-gray-800 font-medium leading-snug">{{ authStore.user?.employeeNumber?.[0] || 'Não Informado' }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="border-t border-gray-100 bg-gray-100/50">
        <a href="#" @click.prevent="handleLogout" class="flex items-center justify-center px-4 py-3.5 text-sm font-semibold text-red-650 hover:bg-red-50 hover:text-red-750 transition duration-150 ease-in-out">
          <ArrowLeftOnRectangleIcon class="h-5 w-5 mr-2" />
          <span>Sair</span>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ArrowLeftOnRectangleIcon, BriefcaseIcon, BuildingOffice2Icon, IdentificationIcon } from '@heroicons/vue/24/outline';
import { useAuthStore } from '../stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const isOpen = ref(false);

const handleLogout = async () => {
  await authStore.logout(router);
};

// Close dropdown on navigation
watch(() => route.path, () => {
  isOpen.value = false;
});
</script>
