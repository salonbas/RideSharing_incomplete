<template>
  <div class="min-h-screen flex items-center justify-center bg-black text-[#FFD700]">
    <div class="p-[2px] rounded-xl bg-gradient-to-br from-yellow-400 via-orange-400 to-yellow-600 w-full max-w-2xl mx-auto shadow-[0_0_12px_rgba(255,191,0,0.4)] mt-8 mb-8">
      <div class="bg-[#0d0d0d] rounded-xl px-6 md:px-10 py-10 text-[#e4c35d] space-y-6">
        <h2 class="text-4xl font-bold tracking-wide text-center text-yellow-300 font-serif drop-shadow-[0_1px_3px_rgba(255,191,0,0.3)]">發起活動</h2>
        
        <form @submit.prevent="handleCreateEvent">
          <!-- 活動標題 -->
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2 text-left">活動標題</label>
            <input
              type="text"
              v-model="eventData.title"
              placeholder="請輸入活動標題"
              class="input"
              required
            />
          </div>

          <!-- 活動描述 -->
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2 text-left">活動描述</label>
            <textarea
              v-model="eventData.description"
              placeholder="請描述活動內容..."
              class="input resize-none h-20"
              required
            ></textarea>
          </div>

          <!-- 活動類型 -->
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2 text-left">活動類型</label>
            <select v-model="eventData.type" class="input" required>
              <option value="">請選擇活動類型</option>
              <option value="carpool">共乘</option>
              <option value="party">喝酒</option>
              <option value="sex">Netfilx and cill</option>
              <option value="else">其他</option>
            </select>
          </div>

          <!-- 活動日期 -->
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2 text-left">活動日期</label>
            <input
              type="date"
              v-model="eventData.date"
              class="input"
              required
            />
          </div>

          <!-- 需求人數 -->
          <div class="mb-4">
            <label class="block text-sm font-medium mb-2 text-left">需求人數</label>
            <input
              type="number"
              v-model="eventData.requiredSeats"
              placeholder="請輸入需求人數"
              class="input"
              min="1"
              required
            />
          </div>

          <!-- 地點選擇區域 -->
          <div class="mb-4">
            <div class="grid grid-cols-2 gap-4">
              <!-- 出發地區域 -->
              <div>
                <label class="block text-sm font-medium mb-2 text-left">出發地</label>
                <!-- 出發地台灣地圖 -->
                <div class="mb-2">
                  <BottonSvg @select="handleFromCitySelect" />
                </div>
                <input
                  type="text"
                  v-model="eventData.fromCity"
                  placeholder="城市"
                  class="input mb-2"
                />
                <input
                  type="text"
                  v-model="eventData.fromDetail"
                  placeholder="詳細地點"
                  class="input"
                />
              </div>

              <!-- 目的地區域 -->
              <div>
                <label class="block text-sm font-medium mb-2 text-left">目的地</label>
                <!-- 目的地台灣地圖 -->
                <div class="mb-2">
                  <BottonSvg @select="handleToCitySelect" />
                </div>
                <input
                  type="text"
                  v-model="eventData.toCity"
                  placeholder="城市"
                  class="input mb-2"
                />
                <input
                  type="text"
                  v-model="eventData.toDetail"
                  placeholder="詳細地點"
                  class="input"
                />
              </div>
            </div>
          </div>

          <!-- 聯絡方式 -->
          <div class="mb-6">
            <label class="block text-sm font-medium mb-2 text-left">希望的聯絡方式</label>
            <select v-model="eventData.contactMethod" class="input" required>
              <option value="">請選擇聯絡方式</option>
              <option value="line">LINE</option>
              <option value="instagram">Instagram</option>
              <option value="phone">電話</option>
              <option value="email">Email</option>
            </select>
          </div>

          <!-- 按鈕區域 -->
          <div class="flex gap-4">
            <button 
              type="button" 
              @click="handleCancel"
              class="flex-1 bg-gray-600 hover:bg-gray-700 text-white py-2 rounded transition font-semibold"
            >
              取消
            </button>
            <button 
              type="submit" 
              class="btn flex-1"
            >
              發起活動
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import BottonSvg from '@/components/Event/BottonSvg.vue'
import { useEventService } from '@/composables/useEvents'

// 取得 router & 事件服務
const router = useRouter()
const eventService = useEventService()

// 活動表單資料
const eventData = reactive({
  title: '',
  description: '',
  type: '',
  date: '',
  requiredSeats: 1,
  fromCity: '',
  fromDetail: '',
  toCity: '',
  toDetail: '',
  contactMethod: ''
})

// 出發地選擇器處理
const handleFromCitySelect = (cityName) => {
  eventData.fromCity = cityName
}

// 目的地選擇器處理
const handleToCitySelect = (cityName) => {
  eventData.toCity = cityName
}

// 取消按鈕返回上一頁
const handleCancel = () => {
  router.go(-1)
}

// 重置表單
const resetForm = () => {
  eventData.title = ''
  eventData.description = ''
  eventData.type = ''
  eventData.date = ''
  eventData.requiredSeats = 1
  eventData.fromCity = ''
  eventData.fromDetail = ''
  eventData.toCity = ''
  eventData.toDetail = ''
  eventData.contactMethod = ''
}

// 發起活動送出
const handleCreateEvent = async () => {
  if (!eventData.title || !eventData.description || !eventData.type || 
      !eventData.date || !eventData.requiredSeats || !eventData.contactMethod) {
    alert('請填寫所有必填欄位')
    return
  }

  try {
    const response = await eventService.createEvent(eventData)
    console.log("✅ 活動創建成功:", response)
    alert("活動創建成功！")
    resetForm()
    router.push({ name: 'events' }) // ✅ 這裡路由跳轉可依照你自己實際命名
  } catch (error) {
    console.error("❌ 活動創建失敗:", error)
    alert("活動創建失敗，請稍後再試")
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

.input {
  @apply w-full px-4 py-2 border rounded;
  background-color: transparent;
  color: #FFD700;
  font-family: 'Inter', sans-serif;
  font-size: 0.875rem;
  border: 1px solid rgba(255, 215, 0, 0.4);
  font-family: 'Inter', sans-serif;
}

.input::placeholder {
  color: rgba(255, 215, 0, 0.5);
}

.input:focus {
  outline: none;
  border-color: #FFD700;
  box-shadow: 0 0 0 2px rgba(255, 215, 0, 0.3);
}

/* 修正 select 和 textarea 的樣式 */
select.input {
  appearance: none;
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23FFD700' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
}

select.input option {
  background-color: #000;
  color: #FFD700;
}

textarea.input {
  resize: vertical;
  min-height: 5rem;
}

.btn {
  @apply font-semibold py-2 px-4 rounded transition;
  background: linear-gradient(to right, #FFD700, #fff);
  color: #000;
  font-family: 'Inter', sans-serif;
}

.btn:hover {
  opacity: 0.9;
}

h2 {
  font-family: 'Inter', sans-serif;
}

.border-gradient {
  border-width: 1px;
  border-image: linear-gradient(to right, #ffffff80, #FFD700) 1;
}

label {
  font-family: 'Inter', sans-serif;
}
</style>