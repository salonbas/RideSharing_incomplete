<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-b from-yellow-300 to-black">
    <div class="w-full max-w-md md:max-w-lg lg:max-w-xl p-8 bg-white rounded-lg shadow-xl">
      <h2 class="text-3xl font-semibold mb-6 text-center font-sans">登入</h2>
      <form @submit.prevent="handleLogin">
        <input type="email" placeholder="Email" class="input mb-4" />
        <input type="password" placeholder="Password" class="input mb-4" />
        <button type="submit" class="btn w-full">登入</button>
        <router-link to="/forgot-password" class="text-sm text-blue-600 hover:underline block mt-3 text-center">
          忘記密碼？
        </router-link>
      </form>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

function handleLogin() {
  auth.login()
  router.push('/')
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

.input {
  @apply w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-400;
  font-family: 'Inter', sans-serif;
}

.btn {
  @apply bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded transition;
  font-family: 'Inter', sans-serif;
}

h2 {
  font-family: 'Inter', sans-serif;
}
</style>
