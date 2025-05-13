<template>
  <div class="relative w-10 h-10">
    <Listbox v-model="selected">
      <div class="relative">
        <ListboxButton class="w-10 h-10 rounded-full overflow-hidden border-2 border-blue-500 hover:ring-2 hover:ring-blue-300 transition">
          <img :src="user.avatarUrl" alt="User Avatar" class="w-full h-full object-cover" />
        </ListboxButton>

        <Transition
          enter="transition duration-100 ease-out"
          enter-from="transform scale-95 opacity-0"
          enter-to="transform scale-100 opacity-100"
          leave="transition duration-75 ease-in"
          leave-from="transform scale-100 opacity-100"
          leave-to="transform scale-95 opacity-0"
        >
          <ListboxOptions class="absolute right-0 mt-2 w-40 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-50">
            <ListboxOption :value="'profile'">
              <RouterLink to="/profile" class="block px-4 py-2 text-gray-700 hover:bg-blue-100">個人資料</RouterLink>
            </ListboxOption>
            <ListboxOption :value="'logout'">
              <button @click="handleLogout" class="w-full text-left px-4 py-2 text-red-600 hover:bg-red-100">登出</button>
            </ListboxOption>
          </ListboxOptions>
        </Transition>
      </div>
    </Listbox>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { defineEmits } from 'vue'
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'

// 模擬使用者資料
const user = {
  name: '阿明',
  avatarUrl: '/user-avatar.png'
}

const selected = ref(null)
const auth = useAuthStore()
const router = useRouter()

const emit = defineEmits(['logout'])

function handleLogout() {
  auth.logout()
  router.push('/')
}
</script>
