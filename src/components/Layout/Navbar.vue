// components/Layout/Navbar.vue
<template>
  <nav class="bg-[#12150e] text-white shadow-md ">
    <div class="max-w-screen mx-auto px-20">
      <div class="flex justify-between items-center h-16">
        <!-- 左側 Logo 區 -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </router-link>
        </div>
        
        <!-- 中間導航區 -->
        <div class="hidden md:flex space-x-12 items-center">
          <router-link to="/" class="btn group">
            <span class="btn-text flex items-center">
              <span class="wave-char">首</span>
              <span class="wave-char">頁</span>
            </span>
            <svg viewBox="0 0 100 40" preserveAspectRatio="none">
              <rect x="3" y="3" width="94" height="34" rx="17" ry="17" />
            </svg>
          </router-link>
          <router-link to="/events" class="btn group">
            <span class="btn-text flex items-center">
              <span class="wave-char">活</span>
              <span class="wave-char">動</span>
              <span class="wave-char">列</span>
              <span class="wave-char">表</span>
            </span>
            <svg viewBox="0 0 100 40" preserveAspectRatio="none">
              <rect x="3" y="3" width="94" height="34" rx="17" ry="17" />
            </svg>
          </router-link>
        </div>
        <!-- 右側用戶區 -->
        <div class="flex items-center space-x-4">
          <!-- 頭相選單 -->
          <div class="relative" v-if="auth.isLoggedIn">
            <AccountMenu />
          </div>
          <div v-else class="flex items-center space-x-2">
            <GuestMenu />
          </div>

          
          <!-- 手機版選單先擱置 -->
          <button 
            @click="toggleMobileMenu" 
            class="md:hidden text-gray-500 hover:text-gray-700"
          >
          </button>
        </div>
      </div>
    </div>
    <hr class="border-t border-white/20" />
  </nav>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import AccountMenu from './Dropdown/AccountMenu.vue';
import GuestMenu from './Dropdown/GuestMenu.vue';
import { useAuthStore } from '@/stores/authStore';

const auth = useAuthStore();

const route = useRoute();

const showMobileMenu = ref(true);


// 切換手機版選單
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value;
};

// 檢查當前路由是否活躍
const isActive = (path) => {
  return route.path === path;
};

</script>

