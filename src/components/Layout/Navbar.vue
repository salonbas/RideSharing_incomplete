// components/Layout/Navbar.vue
<template>
  <nav class="bg-[#12150e] text-white shadow-md ">
    <div class="max-w-screen mx-auto px-20">
      <div class="flex justify-between items-center h-16 relative">
        <!-- 左側 Logo 區 -->
        <div class="flex items-center">
          <!-- <img src="@/assets/logo.png" alt="Logo" class="h-[40px] w-[40px] sm:h-[8vh] sm:w-auto" /> -->
          <router-link to="/" class="flex items-center">
            <img src="@/assets/englishlogo.png" alt="首頁" class="h-[40px] w-[40px] sm:h-[10vh] sm:w-auto object-contain" />
          </router-link>
        </div>
        
        <!-- 中間導航區 -->
        <div class="absolute left-1/2 -translate-x-1/2 hidden md:flex space-x-12 items-center">
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

