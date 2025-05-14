<template>
  <div class="relative" ref="menuRef">
    <img
      src="/default-avatar.png"
      alt="Guest Avatar"
      class="w-10 h-10 rounded-full border-2 border-gray-300 cursor-pointer hover:ring-2 hover:ring-blue-500 transition"
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
        <RouterLink
          v-for="item in pages"
          :key="item.path"
          :to="item.path"
          class="block px-4 py-2 text-sm text-gray-700 hover:bg-blue-100"
          @click="closeMenu"
        >
          {{ item.name }}
        </RouterLink>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { RouterLink } from 'vue-router'

const showMenu = ref(false)
const menuRef = ref(null)

const toggleMenu = () => {
  showMenu.value = !showMenu.value
}

const closeMenu = () => {
  showMenu.value = false
}

// 點擊外部關閉選單
const handleClickOutside = (event) => {
  if (menuRef.value && !menuRef.value.contains(event.target)) {
    showMenu.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

const pages = [
  { name: '登入', path: '/login' },
  { name: '建立帳號', path: '/create-password' }
]
</script>
