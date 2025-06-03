<template>
  <div class="relative" ref="menuRef">
    <img
      :src="user?.avatarUrl || '/default-avatar.png'"
      alt="User Avatar"
      class="w-10 h-10 rounded-full border-2 border-[#d1ad41] cursor-pointer hover:ring-2 hover:ring-[#d1ad41]/50 transition"
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
        class="absolute right-0 mt-2 w-44 rounded-xl bg-[#12150e] shadow-lg border border-[#d1ad41]/30 z-50"
      >
        <RouterLink
          to="/profile"
          class="block px-4 py-3 text-sm text-white hover:bg-[#d1ad41]/20 transition"
          @click="closeMenu"
        >
          個人資料
        </RouterLink>
        <RouterLink
          to="/my-events"
          class="block px-4 py-3 text-sm text-white hover:bg-[#d1ad41]/20 transition"
          @click="closeMenu"
        >
          我的活動
        </RouterLink>
        <button
          class="w-full text-left px-4 py-3 text-sm text-red-400 hover:bg-red-600/30 transition"
          @click="handleLogout"
        >
          登出
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

const router = useRouter()
const auth = useAuthStore()

const user = ref(null)
const showMenu = ref(false)
const menuRef = ref(null)

const toggleMenu = () => {
  showMenu.value = !showMenu.value
}

const closeMenu = () => {
  showMenu.value = false
}

const handleLogout = () => {
  auth.logout()
  closeMenu()
  router.push('/')
}

const handleClickOutside = (event) => {
  if (menuRef.value && !menuRef.value.contains(event.target)) {
    closeMenu()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

onMounted(async () => {
  try {
    const data = await auth.getProfile()
    user.value = data
  } catch (err) {
    console.error('無法取得使用者資料:', err)
  }
})
</script>