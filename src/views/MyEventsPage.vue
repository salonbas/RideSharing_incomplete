// views/MyEventsPage.vue
<template>
  <div class="min-h-screen bg-black text-white">
    <div class="px-4 sm:px-6 md:px-12 lg:px-20 py-8">
      <div class="max-w-[85vw] mx-auto">
        <!-- 頂部區域：標題和統計 -->
        <div class="flex justify-between items-center mb-8">
          <div>
            <h1 class="text-4xl font-bold text-[#d1ad41] mb-2">我的活動</h1>
            <div class="flex gap-6 text-sm text-gray-300">
            </div>
          </div>
          <!-- 快捷按鈕 -->
          <div class="flex gap-3">
            <button @click="fetchMyEvents" :disabled="loading"
              class="px-4 py-2 bg-transparent border border-[#d1ad41] text-[#d1ad41] hover:bg-[#d1ad41] hover:text-black transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg">
              <svg v-if="loading" class="animate-spin h-4 w-4 inline mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
              {{ loading ? '載入中...' : '重新整理' }}
            </button>
            <router-link to="/create-event"
              class="px-4 py-2 bg-[#d1ad41] text-black hover:bg-[#b8941c] transition-colors duration-200 rounded-lg font-medium">
              + 創建活動
            </router-link>
          </div>
        </div>
        <!-- 活動分類標籤 -->
        <div class="flex gap-4 mb-6">
          <button @click="activeTab = 'all'"
            :class="['px-4 py-2 rounded-lg transition-all duration-200', activeTab === 'all' ? 'bg-[#d1ad41] text-black' : 'bg-transparent border border-gray-600 text-gray-300 hover:border-[#d1ad41] hover:text-[#d1ad41]']">
            全部活動 ({{ allMyEvents.length }})
          </button>
          <button @click="activeTab = 'organized'"
            :class="['px-4 py-2 rounded-lg transition-all duration-200', activeTab === 'organized' ? 'bg-[#d1ad41] text-black' : 'bg-transparent border border-gray-600 text-gray-300 hover:border-[#d1ad41] hover:text-[#d1ad41]']">
            我主辦的 ({{ organizedEvents.length }})
          </button>
          <button @click="activeTab = 'joined'"
            :class="['px-4 py-2 rounded-lg transition-all duration-200', activeTab === 'joined' ? 'bg-[#d1ad41] text-black' : 'bg-transparent border border-gray-600 text-gray-300 hover:border-[#d1ad41] hover:text-[#d1ad41]']">
            我參與的 ({{ joinedOnlyEvents.length }})
          </button>
        </div>
        <!-- 載入狀態 -->
        <div v-if="loading" class="text-center py-16">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-[#d1ad41] mx-auto mb-4"></div>
          <p class="text-[#d1ad41] text-lg">載入活動資料中...</p>
        </div>
        <!-- 空狀態 -->
        <div v-else-if="filteredEvents.length === 0" class="text-center py-16">
          <p class="text-xl text-gray-400 mb-2">{{ getEmptyMessage() }}</p>
          <p class="text-gray-500">{{ getEmptySubMessage() }}</p>
        </div>
        <!-- 活動列表 -->
        <div v-else class="min-h-[75vh] grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 auto-rows-fr gap-8 mt-6">
          <EventCard 
            v-for="event in filteredEvents" 
            :key="event.id" 
            :event-data="processEventData(event)"
            :currentUserId="currentUserId"
            :joinedEventIds="joinedEventIds" 
            @show-detail="openEventDetail" 
            @show-profile="showProfile"
            @join-event="handleJoinEvent" 
            @leave-event="handleLeaveEvent" 
            @cancel-event="handleCancelEvent" 
          />
        </div>
      </div>
      <!-- 活動詳情彈窗 -->
      <div v-if="selectedEvent" class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="selectedEvent = null">
        <div class="relative max-w-2xl w-full bg-gray-900 border border-[#d1ad41] rounded-xl overflow-hidden">
          <button @click="selectedEvent = null" class="absolute top-4 right-4 z-10 text-gray-400 hover:text-white bg-black/50 hover:bg-black/70 rounded-full p-2 transition-colors">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <EventDetail :eventData="selectedEvent" :currentUserId="currentUserId" :joinedEventIds="joinedEventIds"
            @join-event="handleJoinEvent" @leave-event="handleLeaveEvent" @cancel-event="handleCancelEvent"
            @show-profile="showProfile" />
        </div>
      </div>
      <!-- 個人資料浮動視窗 -->
      <div v-if="showProfileBox" class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 p-4" @click.self="showProfileBox = false">
        <div class="relative bg-gray-900 border border-[#d1ad41] rounded-xl shadow-xl max-w-md w-full">
          <button @click="showProfileBox = false" class="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <div class="p-1">
            <ProfileBox :user="selectedOrganizer" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useEventService } from '@/composables/useEvents'
import EventCard from '../components/Event/EventCard.vue'
import EventDetail from '../components/Event/EventDetail.vue'
import ProfileBox from '../components/Profile/ProfileBox.vue'

const eventService = useEventService()
const auth = useAuthStore()
const router = useRouter()

const { joinedEventIds } = eventService
const currentUserId = auth.user?.id || 0

// 頁面狀態
const loading = ref(true)
const activeTab = ref('all') // 'all', 'organized', 'joined'
const selectedEvent = ref(null)

// 活動資料
const organizedEvents = ref([]) // 我主辦的活動
const joinedEvents = ref([])    // 我參與的活動

// 個人資料浮動視窗狀態
const showProfileBox = ref(false)
const selectedOrganizer = ref(null)

// 計算屬性
const allMyEvents = computed(() => {
  // 合併所有活動，避免重複
  const eventMap = new Map()
  
  organizedEvents.value.forEach(event => {
    eventMap.set(event.id, { ...event, isOrganizer: true })
  })
  
  joinedEvents.value.forEach(event => {
    if (!eventMap.has(event.id)) {
      eventMap.set(event.id, { ...event, isOrganizer: false })
    }
  })
  
  return Array.from(eventMap.values()).sort((a, b) => new Date(a.date) - new Date(b.date))
})

const joinedOnlyEvents = computed(() => {
  return joinedEvents.value.filter(event => 
    !organizedEvents.value.some(orgEvent => orgEvent.id === event.id)
  )
})

const filteredEvents = computed(() => {
  switch (activeTab.value) {
    case 'organized':
      return organizedEvents.value.sort((a, b) => new Date(a.date) - new Date(b.date))
    case 'joined':
      return joinedOnlyEvents.value.sort((a, b) => new Date(a.date) - new Date(b.date))
    default:
      return allMyEvents.value
  }
})

// 處理事件資料格式，確保與 EventCard 組件預期的格式一致
const processEventData = (event) => {
  // 確保事件資料結構符合 EventCard 的預期
  const processedEvent = {
    ...event,
    // 確保 organizer 欄位存在
    organizer: event.organizer || {
      id: event.organizer_id || event.userId,
      nickname: event.organizer_name || event.organizerName || '未知用戶',
      avatarUrl: event.organizer_avatar || event.avatarUrl || '/default-avatar.png'
    },
    // 確保 location 欄位存在且格式正確
    location: event.location || {
      from: {
        city: event.from_city || event.fromCity || '',
        detail: event.from_detail || event.fromDetail || ''
      },
      destination: {
        city: event.destination_city || event.destinationCity || '',
        detail: event.destination_detail || event.destinationDetail || ''
      }
    },
    // 確保數字欄位存在
    joinedSeats: event.joinedSeats || event.joined_seats || 0,
    requiredSeats: event.requiredSeats || event.required_seats || 1,
    spotsRemaining: event.spotsRemaining || event.spots_remaining || 
                   (event.requiredSeats || event.required_seats || 1) - (event.joinedSeats || event.joined_seats || 0),
    price: event.price || 0,
    // 確保其他欄位存在
    date: event.date || event.eventDate,
    description: event.description || '',
    type: event.type || event.eventType || 'rideshare'
  }

  console.log('處理後的事件資料:', processedEvent)
  return processedEvent
}

// 工具函數
const isOrganizer = (event) => {
  return event.organizer_id === currentUserId || event.isOrganizer
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-TW', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit',
    weekday: 'short'
  })
}

const getEventStatus = (event) => {
  const now = new Date()
  const eventDate = new Date(event.date)
  const joinedSeats = event.joinedSeats || 0
  const requiredSeats = event.requiredSeats || 1
  
  if (eventDate < now) {
    return { text: '已結束', color: 'bg-gray-600 text-gray-300' }
  } else if (joinedSeats >= requiredSeats) {
    return { text: '已額滿', color: 'bg-red-600/80 text-white' }
  } else {
    return { text: '招募中', color: 'bg-blue-600/80 text-white' }
  }
}

const getEmptyMessage = () => {
  switch (activeTab.value) {
    case 'organized':
      return '您還沒有創建任何活動'
    case 'joined':
      return '您還沒有參與任何活動'
    default:
      return '您還沒有任何活動記錄'
  }
}

const getEmptySubMessage = () => {
  switch (activeTab.value) {
    case 'organized':
      return '點擊右上角的「創建活動」按鈕來發起您的第一個活動吧！'
    case 'joined':
      return '快去瀏覽並參與其他人舉辦的精彩活動吧！'
    default:
      return '開始創建或參與活動來豐富您的活動體驗！'
  }
}

// 事件處理
const fetchMyEvents = async () => {
  loading.value = true
  try {
    const res = await auth.getMyEvents()
    console.log('🟢 getMyEvents 成功：', res)

    organizedEvents.value = Array.isArray(res.organized) ? res.organized : []
    joinedEvents.value = Array.isArray(res.joined) ? res.joined : []
    
    // 更新已加入活動的 ID 列表
    joinedEventIds.value = joinedEvents.value.map(e => e.id)
    
    console.log('✅ 我的活動資料已載入', {
      organized: organizedEvents.value.length,
      joined: joinedEvents.value.length,
      organizedSample: organizedEvents.value[0],
      joinedSample: joinedEvents.value[0]
    })
  } catch (err) {
    console.error('❌ getMyEvents 發生錯誤', err)
    organizedEvents.value = []
    joinedEvents.value = []
    joinedEventIds.value = []
    
    // 友善的錯誤提示
    const errorMsg = err.message || '載入活動失敗，請稍後再試'
    alert(errorMsg)
  } finally {
    loading.value = false
  }
}

const openEventDetail = (eventId) => {
  // 修復：從 filteredEvents 中找到對應的事件，並處理資料格式
  const event = filteredEvents.value.find(e => e.id === eventId)
  selectedEvent.value = event ? processEventData(event) : null
}

const showProfile = async (userId) => {
  try {
    const userData = await auth.getPublicUser(userId)
    selectedOrganizer.value = userData
    showProfileBox.value = true
  } catch (err) {
    console.error('載入個人資料失敗:', err)
    alert('載入個人資料失敗')
  }
}

// 處理加入活動
const handleJoinEvent = async (eventId) => {
  try {
    await eventService.joinEvent(eventId)
    alert('成功申請加入活動')
    await fetchMyEvents()
    
    if (selectedEvent.value && selectedEvent.value.id === eventId) {
      const updatedEvent = filteredEvents.value.find(e => e.id === eventId)
      selectedEvent.value = updatedEvent ? processEventData(updatedEvent) : null
    }
  } catch (err) {
    const msg = err?.response?.data?.error || err?.response?.data?.msg || err.message || '未知錯誤'
    alert(`申請失敗：${msg}`)
  }
}

// 處理退出活動
const handleLeaveEvent = async (eventId) => {
  if (!confirm('確定要退出這個活動嗎？')) return
  
  try {
    await eventService.leaveEvent(eventId)
    alert('成功退出活動')
    await fetchMyEvents()
    
    if (selectedEvent.value && selectedEvent.value.id === eventId) {
      const updatedEvent = filteredEvents.value.find(e => e.id === eventId)
      selectedEvent.value = updatedEvent ? processEventData(updatedEvent) : null
    }
  } catch (err) {
    const msg = err?.response?.data?.error || err?.response?.data?.msg || err.message || '未知錯誤'
    alert(`退出失敗：${msg}`)
  }
}

// 處理取消活動
const handleCancelEvent = async (eventId) => {
  if (!confirm('確定要取消這個活動嗎？此操作無法復原。')) return

  try {
    await eventService.cancelEvent(eventId)
    alert('活動已成功取消')
    await fetchMyEvents()
    
    if (selectedEvent.value && selectedEvent.value.id === eventId) {
      selectedEvent.value = null
    }
  } catch (err) {
    const msg = err?.response?.data?.error || err?.response?.data?.msg || err.message || '未知錯誤'
    alert(`取消失敗：${msg}`)
  }
}

// 生命週期
onMounted(() => {
  fetchMyEvents()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>