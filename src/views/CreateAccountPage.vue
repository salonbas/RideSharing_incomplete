<template>
  <div class="min-h-screen flex items-center justify-center bg-black text-[#FFD700]">
    <div class="w-full max-w-md md:max-w-lg lg:max-w-xl p-8 border rounded-lg shadow-xl bg-black border-gradient">
      <h2 class="text-3xl font-semibold mb-6 text-center font-sans">創建帳號</h2>
      <form @submit.prevent="handleRegister">
        <input
          type="text"
          v-model="username"
          placeholder="帳號（限英數10字內）"
          class="input mb-4"
        />
        <input
          type="password"
          v-model="password"
          placeholder="密碼（限英數8字內）"
          class="input mb-4"
        />
        <input
          type="email"
          v-model="email"
          placeholder="Email"
          class="input mb-4"
        />
        <button type="submit" class="btn w-full">註冊</button>
        <router-link to="/login" class="text-sm text-yellow-400 hover:underline block mt-3 text-center">
          已有帳號？點此登入
        </router-link>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const email = ref('')
const router = useRouter()

async function handleRegister() {
  const usernameValid = /^[A-Za-z0-9]{1,10}$/.test(username.value)
  const passwordValid = /^[A-Za-z0-9]{1,8}$/.test(password.value)
  const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)

  if (!usernameValid) {
    alert("帳號格式錯誤：限10字內，僅含英數")
    return
  }

  if (!passwordValid) {
    alert("密碼格式錯誤：限8字內，僅含英數")
    return
  }

  if (!emailValid) {
    alert("Email 格式錯誤")
    return
  }

  try {
    const res = await axios.post('http://localhost:5000/register', {
      username: username.value,
      password: password.value,
      email: email.value
    })
    alert('註冊成功！請登入')
    router.push('/login')
  } catch (err) {
    console.error('❌ 註冊失敗:', err)
    alert(err?.response?.data?.msg || '註冊失敗')
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

.input {
  @apply w-full px-4 py-2 border rounded;
  background-color: transparent;
  color: #FFD700;
  border-image: linear-gradient(to right, #fff, #FFD700) 1;
  font-family: 'Inter', sans-serif;
}

.input::placeholder {
  color: #FFD700aa;
}

.btn {
  @apply font-semibold py-2 px-4 rounded transition;
  background: linear-gradient(to right, #FFD700, #fff);
  color: #000;
  font-family: 'Inter', sans-serif;
}

h2 {
  font-family: 'Inter', sans-serif;
}

.border-gradient {
  border-width: 1px;
  border-image: linear-gradient(to right, #ffffff80, #FFD700) 1;
}
</style>
