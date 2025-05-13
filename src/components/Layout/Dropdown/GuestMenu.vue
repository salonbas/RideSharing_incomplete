<template>
  <div class="relative w-10 h-10">
    <Listbox v-model="selected">
      <div class="relative">
        <ListboxButton class="w-10 h-10 rounded-full overflow-hidden border-2 border-gray-300 hover:ring-2 hover:ring-blue-500 transition">
          <img src="/default-avatar.png" alt="Guest Avatar" class="w-full h-full object-cover" />
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
            <ListboxOption
              v-for="item in pages"
              :key="item.path"
              :value="item"
              class="hover:bg-blue-100"
            >
              <RouterLink
                :to="item.path"
                class="block px-4 py-2 text-gray-700 hover:font-semibold"
              >
                {{ item.name }}
              </RouterLink>
            </ListboxOption>
          </ListboxOptions>
        </Transition>
      </div>
    </Listbox>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue'
import { RouterLink } from 'vue-router'

const pages = [
  { name: '登入', path: '/login' },
  { name: '建立帳號', path: '/create-password' }
]
const showUserMenu = ref(true)

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

const selected = ref(null)
</script>
