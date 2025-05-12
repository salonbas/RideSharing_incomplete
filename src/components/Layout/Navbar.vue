// components/Layout/NavBar.vue
<template>
  <nav class="bg-white shadow-md">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center h-16">
        <!-- 左側 Logo 區 -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            <span class="ml-2 text-xl font-bold text-gray-800">活動平台</span>
          </router-link>
        </div>
        
        <!-- 中間導航區 -->
        <div class="hidden md:flex space-x-8 items-center">
          <router-link 
            to="/" 
            class="text-gray-600 hover:text-blue-600 transition-colors"
            :class="{ 'text-blue-600 font-medium': isActive('/') }"
          >
            首頁
          </router-link>
          <router-link 
            to="/events" 
            class="text-gray-600 hover:text-blue-600 transition-colors"
            :class="{ 'text-blue-600 font-medium': isActive('/events') }"
          >
            活動列表
          </router-link>
          <router-link 
            to="/my-events" 
            class="text-gray-600 hover:text-blue-600 transition-colors"
            :class="{ 'text-blue-600 font-medium': isActive('/my-events') }"
          >
            我的活動
          </router-link>
        </div>
        
        <!-- 右側用戶區 -->
        <div class="flex items-center space-x-4">
          <!-- 搜尋按鈕 -->
          <button class="text-gray-500 hover:text-gray-700">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </button>
          
          <!-- 通知按鈕 -->
          <button class="text-gray-500 hover:text-gray-700 relative">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
            <!-- 通知徽章 -->
            <span class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-4 w-4 flex items-center justify-center">
              3
            </span>
          </button>
          
          <!-- 已登入使用者 -->
          <div class="relative" v-if="isLoggedIn">
            <div 
              @click="toggleUserMenu" 
              class="flex items-center cursor-pointer"
            >
              <img 
                src="https://i.pravatar.cc/150?img=1" 
                alt="用戶頭像" 
                class="h-8 w-8 rounded-full object-cover border-2 border-gray-200"
              />
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </div>
            
            <!-- 下拉選單 -->
            <div 
              v-if="showUserMenu" 
              class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10"
            >
              <router-link 
                to="/profile" 
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                個人資料
              </router-link>
              <router-link 
                to="/my-events" 
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                我的活動
              </router-link>
              <router-link 
                to="/settings" 
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                設定
              </router-link>
              <div class="border-t border-gray-100 my-1"></div>
              <button 
                @click="logout" 
                class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
              >
                登出
              </button>
            </div>
          </div>
          
          <!-- 未登入 -->
          <div v-else class="flex items-center space-x-2">
            <router-link 
              to="/login" 
              class="px-4 py-2 text-sm text-blue-600 hover:text-blue-700"
            >
              登入
            </router-link>
            <router-link 
              to="/register" 
              class="px-4 py-2 text-sm bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              註冊
            </router-link>
          </div>
          
          <!-- 手機版選單按鈕 -->
          <button 
            @click="toggleMobileMenu" 
            class="md:hidden text-gray-500 hover:text-gray-700"
          >
            <svg v-if="!showMobileMenu" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
      
      <!-- 手機選單 -->
      <div v-if="showMobileMenu" class="md:hidden pb-3 border-t border-gray-200 mt-2">
        <div class="pt-2 space-y-1">
          <router-link 
            to="/" 
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-50"
            :class="{ 'bg-gray-50 text-blue-600': isActive('/') }"
          >
            首頁
          </router-link>
          <router-link 
            to="/events" 
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-50"
            :class="{ 'bg-gray-50 text-blue-600': isActive('/events') }"
          >
            活動列表
          </router-link>
          <router-link 
            to="/my-events" 
            class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:bg-gray-50"
            :class="{ 'bg-gray-50 text-blue-600': isActive('/my-events') }"
          >
            我的活動
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

// 用戶選單狀態
const showUserMenu = ref(false);
const showMobileMenu = ref(false);

// 假設使用者已登入
const isLoggedIn = ref(true);

// 切換用戶選單
const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value;
};

// 切換手機版選單
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value;
};

// 登出
const logout = () => {
  // 在實際應用中，這裡會處理登出邏輯
  isLoggedIn.value = false;
  showUserMenu.value = false;
};

// 檢查當前路由是否活躍
const isActive = (path) => {
  return route.path === path;
};

// 點擊文檔其他區域關閉選單
// (這裡是簡化版，實際應用可能需要更複雜的邏輯)
if (typeof window !== 'undefined') {
  window.addEventListener('click', (event) => {
    const target = event.target;
    if (!target.closest('.user-menu') && showUserMenu.value) {
      showUserMenu.value = false;
    }
  });
}
</script>