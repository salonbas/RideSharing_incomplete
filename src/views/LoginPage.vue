<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="w-full max-w-sm p-6 bg-white rounded shadow">
      <h2 class="text-2xl font-bold mb-4">Login</h2>
      <form>
        <input type="email" placeholder="Email" class="input mb-3" />
        <input type="password" placeholder="Password" class="input mb-3" />
        <button @click="handleLogin" type="submit" class="btn w-full">Login</button>
        <router-link to="/forgot-password" class="text-sm text-blue-600 hover:underline block mt-2">Forgot Password?</router-link>
      </form>
    </div>
  </div>
</template>

<style scoped>
.input {
  @apply w-full px-3 py-2 border rounded;
}
.btn {
  @apply bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded;
}
</style>

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