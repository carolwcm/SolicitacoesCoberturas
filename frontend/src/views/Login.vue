<template>
  <div v-if="showSplash" class="fixed inset-0 z-50 flex flex-col items-center justify-center bg-slate-900 select-none">
    <div class="max-w-lg p-6 flex flex-col items-center">
      <img src="/woundflowentrada.png" alt="WoundFlow Entrada" class="max-h-[75vh] w-auto object-contain rounded-2xl shadow-2xl mb-8">
      <div class="flex items-center gap-3 text-white font-semibold text-lg">
        <svg class="animate-spin h-6 w-6 text-indigo-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>Carregando Painel WoundFlow...</span>
      </div>
    </div>
  </div>

  <div v-else class="w-full h-screen flex items-center justify-center bg-slate-100 p-2 md:p-6 overflow-hidden">
    <!-- Responsive Image Overlay wrapper maintaining image aspect ratio -->
    <div class="relative w-full max-w-[1280px] aspect-[1280/876] bg-cover bg-no-repeat bg-center shadow-2xl rounded-3xl overflow-hidden" style="background-image: url('/telalogin.png')">
      
      <!-- Form with absolute layout mapping the input fields exactly -->
      <form @submit.prevent="handleLogin" class="absolute inset-0">
        
        <!-- User field overlay with real interactive styling -->
        <div class="absolute" style="left: 7.2%; top: 46.8%; width: 31.0%; height: 5.8%;">
          <div class="relative w-full h-full flex items-center">
            <span class="absolute left-4 text-[#009688]">
              <svg class="w-5 h-5 md:w-6 md:h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </span>
            <input 
              v-model="username" 
              type="text" 
              placeholder="Usuário"
              class="w-full h-full bg-white border border-[#d1dbf0] rounded-xl pl-12 pr-4 text-slate-800 placeholder-[#94a3b8] focus:border-[#103F8A] focus:outline-none transition-colors font-semibold text-sm md:text-base"
              id="username"
              autocomplete="username"
              required
            >
          </div>
        </div>

        <!-- Password field overlay with real interactive styling -->
        <div class="absolute" style="left: 7.2%; top: 54.4%; width: 31.0%; height: 5.8%;">
          <div class="relative w-full h-full flex items-center">
            <span class="absolute left-4 text-[#009688]">
              <svg class="w-5 h-5 md:w-6 md:h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </span>
            <input 
              v-model="password" 
              :type="passwordFieldType" 
              placeholder="Senha"
              class="w-full h-full bg-white border border-[#d1dbf0] rounded-xl pl-12 pr-12 text-slate-800 placeholder-[#94a3b8] focus:border-[#103F8A] focus:outline-none transition-colors font-semibold text-sm md:text-base"
              id="password"
              autocomplete="current-password"
              required
            >
            <button 
              type="button" 
              @click="togglePasswordVisibility" 
              class="absolute right-4 text-slate-400 hover:text-slate-600 transition-colors cursor-pointer flex items-center"
            >
              <component :is="passwordFieldType === 'password' ? EyeIcon : EyeSlashIcon" class="h-5 w-5 md:h-6 md:w-6" />
            </button>
          </div>
        </div>

        <!-- Checkbox overlay -->
        <div class="absolute flex items-center gap-2" style="left: 7.2%; top: 62.1%; width: 31.0%; height: 3.5%;">
          <input 
            v-model="rememberMe" 
            type="checkbox" 
            id="rememberMe"
            class="w-4 h-4 md:w-5 md:h-5 rounded border-[#d1dbf0] text-[#103F8A] focus:ring-[#103F8A] cursor-pointer"
          >
          <label for="rememberMe" class="text-xs md:text-sm text-[#64748b] font-semibold cursor-pointer select-none">
            Lembrar de mim
          </label>
        </div>

        <!-- Submit Button Overlay -->
        <div class="absolute" style="left: 7.2%; top: 67.0%; width: 31.0%; height: 5.8%;">
          <button 
            type="submit" 
            :disabled="loading" 
            class="w-full h-full rounded-xl bg-[#103F8A] hover:bg-[#0c316c] text-white font-bold cursor-pointer transition-all active:scale-[0.98] flex items-center justify-center text-sm md:text-base shadow-sm"
          >
            Entrar
          </button>
        </div>

      </form>

      <!-- Error Toast (Floating Bottom-Left) -->
      <div 
        v-if="error" 
        class="absolute bottom-6 left-6 max-w-sm bg-rose-50 border border-rose-200 text-rose-800 px-4 py-3 rounded-2xl shadow-xl flex items-start gap-2 animate-fade-in z-30"
      >
        <strong class="font-bold text-sm">Erro:</strong>
        <span class="text-sm font-medium">{{ error }}</span>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { EyeIcon, EyeSlashIcon } from '@heroicons/vue/24/outline';

const username = ref('');
const password = ref('');
const rememberMe = ref(false);
const error = ref('');
const loading = ref(false);
const passwordVisible = ref(false);
const showSplash = ref(false);

const router = useRouter();
const authStore = useAuthStore();

const passwordFieldType = computed(() => passwordVisible.value ? 'text' : 'password');

const togglePasswordVisibility = () => {
  passwordVisible.value = !passwordVisible.value;
};

const handleLogin = async () => {
  loading.value = true;
  error.value = '';
  try {
    await authStore.login(username.value, password.value, rememberMe.value);
    showSplash.value = true;
    await new Promise(resolve => setTimeout(resolve, 4000));
    await router.push('/solicitacoes');
  } catch (e: any) {
    error.value = e.response?.data?.detail || e.message || 'An unknown error occurred';
  } finally {
    loading.value = false;
  }
};
</script>
