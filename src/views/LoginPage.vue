<template>
  <div class="min-h-screen flex items-center justify-center bg-black text-[#FFD700] overflow-hidden relative">
    <!-- 🌌 星空背景 -->
    <div class="sky" ref="skyRef"></div>

    <!-- 登入框 - 使用金色渐变边框样式 -->
    <div class="p-[1px] rounded-xl bg-gradient-to-br from-yellow-400 via-orange-400 to-yellow-600 w-full max-w-md md:max-w-lg shadow-[0_0_12px_rgba(255,191,0,0.4)] mx-4 z-10">
      <div class="bg-[#0d0d0d] rounded-xl px-6 md:px-10 py-10 text-[#e4c35d] space-y-6">
        <h2 class="text-4xl font-bold tracking-wide text-center text-yellow-300 font-serif drop-shadow-[0_1px_3px_rgba(255,191,0,0.3)]">登入</h2>
        
        <form @submit.prevent="handleLogin">
          <div class="mb-4">
            <input
              type="text"
              v-model="username"
              placeholder="使用者名稱"
              class="input"
              required
            />
          </div>
          
          <div class="mb-6">
            <input
              type="password"
              v-model="password"
              placeholder="密碼"
              class="input"
              required
            />
          </div>
          
          <button type="submit" class="login-btn w-full" @click="createRipple($event)">
            登入
          </button>
          
          <div class="text-center mt-4 space-y-2">
            <router-link to="/create-account" class="link block">
              創建帳號
            </router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
  <Wave class="force-bottom-right" />
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import Wave from '@/components/Layout/Small/Wave.vue';

const username = ref('')
const password = ref('')
const skyRef = ref(null)
const auth = useAuthStore()
const router = useRouter()

// 🌠 星空與流星
onMounted(async () => {
  await nextTick()

  const sky = skyRef.value
  if (!sky) {
    console.warn('❌ skyRef 為 null，請檢查是否正確綁定 ref')
    return
  }

  // ⭐ 建立星星
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

  // 🌠 流星效果
  setInterval(() => {
    if (Math.random() < 0.6) {
      const meteor = document.createElement('div')
      meteor.classList.add('shooting-star')

      meteor.style.top = `${Math.random() * 80}%`
      meteor.style.left = `-${Math.random() * 200 + 50}px`
      meteor.style.width = `${100 + Math.random() * 60}px`

      skyRef.value.appendChild(meteor)
      setTimeout(() => meteor.remove(), 3500)
    }
  }, 2000)
})

// 🌀 Ripple 效果
function createRipple(event) {
  const button = event.currentTarget
  const ripple = document.createElement('span')
  const diameter = Math.max(button.clientWidth, button.clientHeight)
  const radius = diameter / 2

  ripple.style.width = ripple.style.height = `${diameter}px`
  ripple.style.left = `${event.clientX - button.getBoundingClientRect().left - radius}px`
  ripple.style.top = `${event.clientY - button.getBoundingClientRect().top - radius}px`
  ripple.classList.add('ripple')

  const existing = button.querySelector('.ripple')
  if (existing) existing.remove()

  button.appendChild(ripple)
  ripple.addEventListener('animationend', () => ripple.remove())
}

async function handleLogin() {
  try {
    await auth.loginUser({
      username: username.value,
      password: password.value
    })
    router.push('/')
  } catch (err) {
    console.error('❌ 登入失敗:', err)
    alert(err?.response?.data?.msg || '登入失敗，請確認帳號密碼')
  }
}

</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

/* 📄 輸入框樣式 */
.input {
  @apply w-full px-4 py-2 border rounded;
  background-color: transparent;
  color: #FFD700;
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  border: 1px solid rgba(255, 215, 0, 0.4);
}

.input::placeholder {
  color: rgba(255, 215, 0, 0.5);
}

.input:focus {
  outline: none;
  border-color: #FFD700;
  box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.3);
}

/* 🔵 登入按鈕 */
.login-btn {
  @apply font-semibold py-2 px-4 transition;
  border-radius: 12px;
  background: linear-gradient(145deg, #1a1a1a 0%, #0d0d0d 50%, #1a1a1a 100%);
  border: 1px solid;
  border-image: linear-gradient(145deg, #B8860B 0%, #FFD700 50%, #B8860B 100%) 1;
  color: #FFD700 !important;
  font-family: 'Inter', sans-serif;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4), 
              inset 0 1px 0 rgba(255, 215, 0, 0.1), 
              inset 0 -1px 0 rgba(0, 0, 0, 0.5),
              0 0 20px rgba(255, 215, 0, 0.1);
  text-shadow: 0 0 4px rgba(255, 215, 0, 0.3);
}

.login-btn:hover {
  background: linear-gradient(145deg, #262626 0%, #1a1a1a 50%, #262626 100%);
  transform: scale(1.02);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.6), 
              inset 0 1px 0 rgba(255, 215, 0, 0.2), 
              inset 0 -1px 0 rgba(0, 0, 0, 0.7),
              0 0 30px rgba(255, 215, 0, 0.2);
  text-shadow: 0 0 6px rgba(255, 215, 0, 0.5);
}

/* 🌊 Ripple 特效 */
.ripple {
  position: absolute;
  border-radius: 50%;
  transform: scale(0);
  animation: ripple-animation 600ms linear;
  background-color: rgba(255, 255, 255, 0.6);
  pointer-events: none;
}
@keyframes ripple-animation {
  to {
    transform: scale(4);
    opacity: 0;
  }
}

/* 🌌 星空背景 */
.sky {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

/* ⭐ 星星 */
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

/* 🌠 流星 */
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
  0% {
    transform: translate(0, 0) rotate(35deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  100% {
    transform: translate(800px, 400px) rotate(35deg);
    opacity: 0;
  }
}

/* 標題字體 */
h2 {
  font-family: 'Inter', sans-serif;
}

/* 链接样式 */
.link {
  color: #FFD700;
  text-decoration: none;
  font-size: 0.875rem;
  font-family: 'Inter', sans-serif;
}
.link:hover {
  text-decoration: underline;
  opacity: 0.8;
}
</style>