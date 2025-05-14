<template>
  <div class="relative" ref="menuRef">
    <img
      :src="user.avatarUrl"
      alt="User Avatar"
      class="w-10 h-10 rounded-full border-2 border-blue-500 cursor-pointer hover:ring-2 hover:ring-blue-300 transition"
      @click="toggleMenu"
    />

    <Transition
      enter="transition duration-100 ease-out"
      enter-from="transform scale-95 opacity-0"
      enter-to="transform scale-100 opacity-100"
      leave="transition duration-75 ease-in"
      leave-from="transform scale-100 opacity-100"
      leave-to="transform scale-95 opacity-0"
    >
      <div
        v-if="showMenu"
        class="absolute right-0 mt-2 w-40 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 z-50"
      >
        <RouterLink to="/profile" class="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-100" @click="closeMenu">
          個人資料
        </RouterLink>
        <button
          class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-100"
          @click="handleLogout"
        >
          登出
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useClickOutside } from '@vueuse/core'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const auth = useAuthStore()

const showMenu = ref(false)
const menuRef = ref(null)
useClickOutside(menuRef, () => (showMenu.value = false))

const toggleMenu = () => (showMenu.value = !showMenu.value)
const closeMenu = () => (showMenu.value = false)

const handleLogout = () => {
  auth.logout()
  closeMenu()
  router.push('/')
}

// 模擬資料，請改成從 store 傳入
const user = {
  name: '阿明',
  avatarUrl: '/user-avatar.png'
}
</script>
