<template>
  <div class="min-h-screen bg-black text-[#FFD700]">
    <!-- 大頭照放大顯示 -->
    <div 
      v-if="showAvatarModal" 
      class="fixed inset-0 z-50 flex items-center justify-center"
      style="background-color: rgba(0, 0, 0, 0.8);"
      @click="showAvatarModal = false"
    >
      <div class="relative max-w-md max-h-96">
        <img 
          :src="userInfo.avatarUrl || '/default-avatar.png'" 
          alt="頭像"
          class="w-full h-full object-cover rounded-lg shadow-2xl border border-[#FFD700]"
          @click.stop
        >
        <button 
          @click="showAvatarModal = false"
          class="absolute top-4 right-4 w-8 h-8 bg-black bg-opacity-70 text-[#FFD700] rounded-full flex items-center justify-center hover:bg-opacity-90 border border-[#FFD700]"
        >
          ×
        </button>
      </div>
    </div>

    <div class="max-w-md mx-auto bg-black min-h-screen border-x border-gradient">
      <!-- 標題列 -->
      <div class="flex items-center justify-between p-4 border-b border-gradient">
        <h1 class="text-lg font-semibold text-left text-[#FFD700] font-sans">編輯個人檔案</h1>
        <button 
          @click="handleSave"
          :disabled="!hasChanges || isLoading"
          class="btn"
          :class="{ 'link-btn-disabled': !hasChanges || isLoading }"
        >
          <svg>
            <rect x="2" y="2" width="calc(100% - 4px)" height="calc(100% - 4px)" rx="8"/>
          </svg>
          {{ isLoading ? '儲存中...' : '儲存' }}
        </button>
      </div>

      <div class="p-4 space-y-6">
        <!-- 大頭照區域 -->
        <div class="flex items-center space-x-4">
          <div class="relative">
            <img 
              :src="userInfo.avatarUrl || '/default-avatar.png'" 
              alt="頭像"
              class="w-20 h-20 rounded-full object-cover cursor-pointer border-2 border-[#FFD700]"
              @click="showAvatarModal = true"
            >
          </div>
          <div class="flex-1">
            <h2 class="font-semibold text-lg text-[#FFD700] font-sans">{{ userInfo.username }}</h2>
            <button 
              @click="triggerFileUpload"
              class="btn mt-2"
            >
              <svg>
                <rect x="2" y="2" width="calc(100% - 4px)" height="calc(100% - 4px)" rx="8"/>
              </svg>
              更改大頭照
            </button>
            <input 
              ref="fileInput"
              type="file" 
              accept="image/*" 
              @change="handleAvatarUpload"
              class="hidden"
            >
          </div>
        </div>

        <!-- 表單欄位 -->
        <div class="space-y-4">
          <!-- 帳號 -->
          <div>
            <label class="block text-sm font-medium text-[#FFD700] mb-2 text-left font-sans">帳號</label>
            <input 
              v-model="editForm.username"
              type="text"
              class="input"
              placeholder="輸入帳號"
            >
          </div>

          <!-- 暱稱 -->
          <div>
            <label class="block text-sm font-medium text-[#FFD700] mb-2 text-left font-sans">暱稱</label>
            <input 
              v-model="editForm.nickname"
              type="text"
              class="input"
              placeholder="輸入暱稱"
            >
          </div>

          <!-- Instagram -->
          <div>
            <label class="block text-sm font-medium text-[#FFD700] mb-2 text-left font-sans">Instagram</label>
            <input 
              v-model="editForm.instagram"
              type="text"
              class="input"
              placeholder="輸入 Instagram 帳號"
            >
            <p class="text-xs text-[#FFD700aa] mt-1">你只能使用可行動電話帳號驗證過，請前往 Instagram 應用程式並驗證電子信箱或帳號，以便更新個人檔案中的 Instagram。</p>
          </div>

          <!-- Email -->
          <div>
            <label class="block text-sm font-medium text-[#FFD700] mb-2 text-left font-sans">Email</label>
            <input 
              v-model="editForm.email"
              type="email"
              class="input"
              placeholder="輸入電子信箱"
            >
          </div>

          <!-- 電話 -->
          <div>
            <label class="block text-sm font-medium text-[#FFD700] mb-2 text-left font-sans">電話</label>
            <input 
              v-model="editForm.phone"
              type="tel"
              class="input"
              placeholder="輸入電話號碼"
            >
          </div>

          <!-- 簡介 -->
          <div>
            <label class="block text-sm font-medium text-[#FFD700] mb-2 text-left font-sans">簡介</label>
            <textarea 
              v-model="editForm.bio"
              rows="4"
              class="input resize-none"
              placeholder="介紹一下自己..."
              maxlength="150"
            ></textarea>
            <div class="text-right text-xs text-[#FFD700aa] mt-1">
              {{ (editForm.bio || '').length }}/150
            </div>
          </div>
        </div>

        <!-- 更改密碼按鈕 -->
        <div class="pt-4 border-t border-gradient">
          <router-link 
            to="/new-password"
            class="btn w-full"
          >
            <svg>
              <rect x="2" y="2" width="calc(100% - 4px)" height="calc(100% - 4px)" rx="8"/>
            </svg>
            更改密碼
          </router-link>
        </div>

        <!-- 隱私設置提示 -->
        <div class="text-xs text-[#FFD700aa] text-center font-sans">
          其他使用者會在活動列表上看到你的資訊。
          <a href="#" class="text-[#FFD700] hover:underline">查看共用對象與隱私設置資訊政策</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/authStore'

// 初始化
const authStore = useAuthStore()
const { user, token } = storeToRefs(authStore)

// 響應式資料
const isLoading = ref(false)
const showAvatarModal = ref(false)
const fileInput = ref(null)

const userInfo = reactive({
  id: null,
  username: '',
  nickname: '',
  avatarUrl: '',
  instagram: '',
  email: '',
  phone: '',
  bio: ''
})

const editForm = reactive({
  username: '',
  nickname: '',
  instagram: '',
  email: '',
  phone: '',
  bio: ''
})

const originalForm = ref({})

// 計算屬性
const hasChanges = computed(() => {
  return Object.keys(editForm).some(key => 
    editForm[key] !== originalForm.value[key]
  )
})

// 方法
const loadUserInfo = async () => {
  try {
    isLoading.value = true
    const response = await authStore.getProfile()
    
    // 更新 userInfo
    Object.assign(userInfo, response)
    
    // 更新編輯表單
    Object.assign(editForm, {
      username: response.username || '',
      nickname: response.nickname || '',
      instagram: response.instagram || '',
      email: response.email || '',
      phone: response.phone || '',
      bio: response.bio || ''
    })
    
    // 保存原始資料
    originalForm.value = { ...editForm }
    
  } catch (error) {
    // 如果 store 中有使用者資料，使用它作為備用
    if (user.value) {
      Object.assign(userInfo, {
        id: user.value.id,
        username: user.value.username || '',
        nickname: user.value.nickname || '',
        avatarUrl: user.value.avatarUrl || '',
        instagram: user.value.instagram || '',
        email: user.value.email || '',
        phone: user.value.phone || '',
        bio: user.value.bio || ''
      })
      
      Object.assign(editForm, {
        username: userInfo.username,
        nickname: userInfo.nickname,
        instagram: userInfo.instagram,
        email: userInfo.email,
        phone: userInfo.phone,
        bio: userInfo.bio
      })
      
      originalForm.value = { ...editForm }
    }
  } finally {
    isLoading.value = false
  }
}

const handleSave = async () => {
  if (!hasChanges.value || isLoading.value) return

  isLoading.value = true
  try {
    const response = await authStore.updateProfile(editForm)
    
    // 更新本地資料
    Object.assign(userInfo, response.user)
    originalForm.value = { ...editForm }
    
  } catch (error) {
    // 錯誤處理已在 authStore 中統一處理
  } finally {
    isLoading.value = false
  }
}

const triggerFileUpload = () => {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

const handleAvatarUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  // 檢查檔案類型
  if (!file.type.startsWith('image/')) {
    console.error('請選擇圖片檔案')
    return
  }

  // 檢查檔案大小 (5MB)
  if (file.size > 5 * 1024 * 1024) {
    console.error('圖片檔案不能超過 5MB')
    return
  }

  try {
    isLoading.value = true
    const response = await authStore.updateAvatar(file)
    
    // 更新本地頭像
    userInfo.avatarUrl = response.avatarUrl
    
  } catch (error) {
    // 錯誤處理已在 authStore 中統一處理
  } finally {
    isLoading.value = false
    // 清空 input
    if (event.target) {
      event.target.value = ''
    }
  }
}

// 重置表單
const resetForm = () => {
  Object.assign(editForm, originalForm.value)
}

// 生命週期
onMounted(async () => {
  await loadUserInfo()
})

// 暴露給模板使用
defineExpose({
  loadUserInfo,
  resetForm
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

.input {
  @apply w-full px-4 py-2 border rounded mb-4;
  background-color: transparent;
  color: #FFD700;
  border-image: linear-gradient(to right, #fff, #FFD700) 1;
  font-family: 'Inter', sans-serif;
  outline: none;
  transition: all 0.3s ease;
}

.input::placeholder {
  color: #FFD700aa;
}

.input:focus {
  border-image: linear-gradient(to right, #FFD700, #fff) 1;
  box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.2);
}

.btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1.5rem;
  color: #000;
  font-weight: 700;
  background: linear-gradient(to right, #FFD700, #fff);
  border: 2px solid transparent;
  border-radius: 8px;
  transition: all 0.3s ease;
  line-height: 1.5;
  letter-spacing: 1px;
  font-size: 1rem;
  cursor: pointer;
  overflow: hidden;
  z-index: 1;
  text-decoration: none;
  font-family: 'Inter', sans-serif;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, #FFD700, #fff);
  z-index: -1;
  transition: all 0.3s ease;
  opacity: 0;
}

.btn:hover {
  color: #000;
  border-color: #FFD700;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
}

.btn:hover::before {
  opacity: 1;
}

.btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(255, 215, 0, 0.2);
}

.btn:disabled,
.link-btn-disabled:disabled {
  background: #6b7280;
  cursor: not-allowed;
  opacity: 0.6;
  color: #9ca3af;
  border-color: #6b7280;
  transform: none;
  box-shadow: none;
}

.btn:disabled::before,
.link-btn-disabled:disabled::before {
  opacity: 0;
}

.btn:disabled:hover,
.link-btn-disabled:disabled:hover {
  transform: none;
  box-shadow: none;
}

.btn svg {
  position: absolute;
  top: 2px;
  left: 2px;
  width: calc(100% - 4px);
  height: calc(100% - 4px);
  fill: none;
  stroke: #FFD700;
  stroke-width: 2;
  stroke-dasharray: 0;
  stroke-dashoffset: 0;
  z-index: -2;
  pointer-events: none;
  opacity: 0;
}

.btn:hover svg {
  opacity: 1;
  stroke-dasharray: 300;
  animation: border-animate 0.6s ease-in-out;
}

@keyframes border-animate {
  0% {
    stroke-dasharray: 0 300;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 150 150;
    stroke-dashoffset: -150;
  }
  100% {
    stroke-dasharray: 300 0;
    stroke-dashoffset: -300;
  }
}

.btn:disabled svg,
.link-btn-disabled:disabled svg {
  stroke: #9ca3af;
  opacity: 0;
}

.border-gradient {
  border-width: 1px;
  border-image: linear-gradient(to right, #ffffff80, #FFD700) 1;
}

h1, h2 {
  font-family: 'Inter', sans-serif;
}

/* 自定義滾動條 */
.min-h-screen::-webkit-scrollbar {
  width: 6px;
}

.min-h-screen::-webkit-scrollbar-track {
  background: #1a1a1a;
}

.min-h-screen::-webkit-scrollbar-thumb {
  background: #FFD700;
  border-radius: 3px;
}

.min-h-screen::-webkit-scrollbar-thumb:hover {
  background: #e6c200;
}
</style>

