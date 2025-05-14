<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center">建立密碼</h2>

      <form @submit.prevent="handleSubmit">
        <div class="mb-4">
          <label for="password" class="block text-gray-700 font-semibold mb-2">新密碼</label>
          <input
            id="password"
            type="password"
            v-model="password"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="請輸入新密碼"
          />
        </div>

        <div class="mb-4">
          <label for="confirmPassword" class="block text-gray-700 font-semibold mb-2">再次輸入密碼</label>
          <input
            id="confirmPassword"
            type="password"
            v-model="confirmPassword"
            class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="請再次輸入密碼"
          />
        </div>

        <div v-if="errorMessage" class="mb-4 text-red-600 text-sm">
          {{ errorMessage }}
        </div>

        <button
          type="submit"
          class="w-full bg-blue-600 text-white font-semibold py-2 rounded-lg hover:bg-blue-700 transition duration-200"
        >
          建立密碼
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')
const router = useRouter()

function handleSubmit() {
  if (password.value.length < 8) {
    errorMessage.value = '密碼長度至少需 8 個字元'
    return
  }
  if (password.value !== confirmPassword.value) {
    errorMessage.value = '兩次輸入的密碼不一致'
    return
  }

  // 模擬密碼建立成功後導向登入頁
  alert('密碼建立成功！')
  router.push('/login')
}
</script>
