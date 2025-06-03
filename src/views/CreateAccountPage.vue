<template>
  <div class="min-h-screen flex items-center justify-center bg-black text-[#FFD700] relative">
    <div class="sky" ref="skyRef"></div>
    <div class="w-full max-w-md md:max-w-lg lg:max-w-xl p-8 border rounded-lg shadow-xl bg-black border-gradient z-10">
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
  <Wave class="force-bottom-right" />
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import Wave from '@/components/Layout/Small/Wave.vue'

const username = ref('')
const password = ref('')
const email = ref('')
const router = useRouter()
const authStore = useAuthStore()

const skyRef = ref(null)

onMounted(async () => {
  await nextTick()
  const sky = skyRef.value
  if (!sky) return

  // 產生星星
  for (let i = 0; i < 200; i++) {
    const star = document.createElement('div')
    star.classList.add('star')
    star.style.top = `${Math.random() * 100}%`
    star.style.left = `${Math.random() * 100}%`
    const size = Math.random() * 2 + 1
    star.style.width = `${size}px`
    star.style.height = `${size}px`
    const duration = 1.5 + Math.random() * 2
    const delay = Math.random() * 2
    star.style.animationDuration = `${duration}s`
    star.style.animationDelay = `${delay}s`
    sky.appendChild(star)
  }

  // 🌠 流星
  setInterval(() => {
    if (Math.random() < 0.6) {
      const meteor = document.createElement('div')
      meteor.classList.add('shooting-star')
      meteor.style.top = `${Math.random() * 80}%`
      meteor.style.left = `-${Math.random() * 200 + 50}px`
      meteor.style.width = `${100 + Math.random() * 60}px`
      sky.appendChild(meteor)
      setTimeout(() => meteor.remove(), 3500)
    }
  }, 2000)
})

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
    await authStore.register({
      username: username.value,
      password: password.value,
      email: email.value
    })
    alert('註冊成功！請登入')
    router.push('/login')
  } catch (err) {
    console.error('註冊失敗:', err)
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

<style>
.sky {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.star {
  position: absolute;
  background: white;
  border-radius: 50%;
  opacity: 0;
  animation: twinkle 2s infinite ease-in-out alternate;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.1; }
  50% { opacity: 1; }
}

.shooting-star {
  position: absolute;
  width: 140px;
  height: 2px;
  background: linear-gradient(to left, white, rgba(255, 255, 255, 0));
  opacity: 0;
  animation: shoot 3s ease-out forwards;
  z-index: 20;
  pointer-events: none;
  transform: rotate(35deg);
}

@keyframes shoot {
  0% { transform: translate(0, 0) rotate(35deg); opacity: 0; }
  10% { opacity: 1; }
  100% { transform: translate(800px, 400px) rotate(35deg); opacity: 0; }
}
</style>