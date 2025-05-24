//src\views\LoginPage.vue
<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-b from-yellow-300 to-black">
    <div class="w-full max-w-md md:max-w-lg lg:max-w-xl p-8 bg-white rounded-lg shadow-xl">
      <h2 class="text-3xl font-semibold mb-6 text-center font-sans">登入</h2>
        <form @submit.prevent="handleLogin">
          <input
            type="text"
            v-model="username"
            placeholder="username"
            class="input mb-4"
          />
          <input
          type="password"
          v-model="password"
          placeholder="Password"
          class="input mb-4"
          />
          <button type="submit" class="btn w-full">登入</button>
          <router-link to="/forgot-password" class="text-sm text-blue-600 hover:underline block mt-3 text-center">
            忘記密碼？
          </router-link>
          <router-link to="/create-password" class="text-sm text-blue-600 hover:underline block mt-3 text-center">
           創建帳號
          </router-link>
        </form>
    </div>
  </div>
</template>

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

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

.input {
  @apply w-full px-4 py-2 border border-gray-300 rounded;
  font-family: 'Inter', sans-serif;
}

.input:focus {
  outline: none;
  border-color: #60a5fa;
  box-shadow: 0 0 0 2px rgba(96, 165, 250, 0.5); /* Optional */
}

.btn {
  @apply bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded transition;
  font-family: 'Inter', sans-serif;
}

h2 {
  font-family: 'Inter', sans-serif;
}
</style>