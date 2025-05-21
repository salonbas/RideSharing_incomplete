//src\views\LoginPage.vue
<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="w-full max-w-sm p-6 bg-white rounded shadow">
      <h2 class="text-2xl font-bold mb-4">Login</h2>
      <form @submit.prevent="handleLogin"> 
        <input v-model="username" type="text" placeholder="帳號" class="input mb-3" />
        <input v-model="password" type="password" class="input mb-3" />
        <button type="submit" class="btn w-full">Login</button>
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
import { ref } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const auth = useAuthStore()
const router = useRouter()

async function handleLogin() {
  console.log('🚀 handleLogin triggered')
  try {
    const res = await axios.post('http://localhost:5000/login', {
      username: username.value,
      password: password.value
    })
    console.log(auth.login.toString())

    const { token, user } = res.data
    auth.login(user, token)
    auth.login(user, token)

    console.log('✅ login() 執行完畢')
    console.log('auth.isLoggedIn:', auth.isLoggedIn)
    console.log('auth.user:', auth.user)
    console.log('auth.token:', auth.token)

    console.log('✅ 登入成功，準備導向首頁')
    router.push('/')
  } catch (err) {
    console.error('❌ 登入失敗:', err)
    alert('登入失敗')
  }
}

</script>