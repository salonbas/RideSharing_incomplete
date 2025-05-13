// stores/authStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const isLoggedIn = ref(false)

  function login() {
    isLoggedIn.value = true;
    alert('已登入！');
  }

  function logout() {
    isLoggedIn.value = false;
    alert('已登出！');
  }

  return { isLoggedIn, login, logout }
})
