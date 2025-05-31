// components/Event/EventCard.vue-router
<template>
  <div class="bg-black rounded-lg shadow-2xl border border-yellow-500 max-h-[90vh] overflow-y-auto">
    <!-- 頭部圖片區域 -->
    <div class="relative h-64 bg-gradient-to-r from-gray-900 via-yellow-900 to-black rounded-t-lg border-b border-yellow-500">
      <div class="absolute inset-0 bg-black bg-opacity-50 rounded-t-lg"></div>
      <div class="absolute bottom-4 left-6 text-yellow-400">
        <h1 class="text-3xl font-bold mb-2 text-yellow-300 drop-shadow-lg">{{ eventData.title || '活動詳情' }}</h1>
        <div class="flex items-center space-x-2">
          <span class="px-3 py-1 bg-yellow-600 bg-opacity-20 border border-yellow-500 rounded-full text-sm text-yellow-300">
            {{ eventData.type || '一般活動' }}
          </span>
          <span class="px-3 py-1 bg-yellow-600 bg-opacity-20 border border-yellow-500 rounded-full text-sm text-yellow-300">
            {{ eventData.price === 0 ? '免費' : `$${eventData.price}` }}
          </span>
        </div>
      </div>
    </div>

    <!-- 主要內容區域 -->
    <div class="p-6 bg-black">
      <!-- 主辦人信息 -->
      <div class="flex items-center mb-6 p-4 bg-gray-900 border border-yellow-600 rounded-lg">
        <div 
          class="w-16 h-16 rounded-full overflow-hidden cursor-pointer mr-4 border-2 border-yellow-500"
          @click="$emit('show-profile', eventData.organizer.id)"
        >
          <img
            :src="eventData.organizer.avatarUrl || '/default-avatar.png'"
            :alt="eventData.organizer.nickname"
            class="w-full h-full object-cover hover:scale-105 transition-transform"
          />
        </div>
        <div>
          <h3 class="text-lg font-semibold text-yellow-300">{{ eventData.organizer.nickname }}</h3>
          <p class="text-sm text-yellow-500">主辦人</p>
        </div>
      </div>

      <!-- 活動信息網格 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <!-- 時間信息 -->
        <div class="bg-gray-900 border border-yellow-600 p-4 rounded-lg">
          <h4 class="font-semibold text-yellow-300 mb-2 flex items-center">
            <svg class="w-5 h-5 mr-2 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            活動時間
          </h4>
          <p class="text-yellow-100">{{ formattedDateTime }}</p>
        </div>

        <!-- 人數信息 -->
        <div class="bg-gray-900 border border-yellow-600 p-4 rounded-lg">
          <h4 class="font-semibold text-yellow-300 mb-2 flex items-center">
            <svg class="w-5 h-5 mr-2 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
            </svg>
            參與人數
          </h4>
          <p class="text-yellow-100">
            已報名: {{ eventData.joinedSeats || 0 }} / {{ eventData.requiredSeats || 0 }} 人
            <span :class="spotsColorClass" class="ml-2 font-semibold">
              (剩餘 {{ eventData.spotsRemaining || 0 }} 名額)
            </span>
          </p>
        </div>
      </div>

      <!-- 路線信息 -->
      <div class="bg-gray-900 border border-yellow-600 p-4 rounded-lg mb-6">
        <h4 class="font-semibold text-yellow-300 mb-3 flex items-center">
          <svg class="w-5 h-5 mr-2 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
          </svg>
          行程路線
        </h4>
        <div class="flex items-center justify-between">
          <div class="text-center flex-1">
            <div class="font-semibold text-yellow-300">{{ eventData.location.from.city }}</div>
            <div class="text-sm text-yellow-200">{{ eventData.location.from.detail }}</div>
          </div>
          <div class="mx-4">
            <svg class="w-8 h-8 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
            </svg>
          </div>
          <div class="text-center flex-1">
            <div class="font-semibold text-yellow-300">{{ eventData.location.destination.city }}</div>
            <div class="text-sm text-yellow-200">{{ eventData.location.destination.detail }}</div>
          </div>
        </div>
      </div>

      <!-- 活動描述 -->
      <div v-if="eventData.description" class="mb-6">
        <h4 class="font-semibold text-yellow-300 mb-3">活動描述</h4>
        <div class="bg-gray-900 border border-yellow-600 p-4 rounded-lg">
          <p class="text-yellow-100 whitespace-pre-wrap">{{ eventData.description }}</p>
        </div>
      </div>

      <!-- 操作按鈕區域 -->
      <div class="flex flex-col sm:flex-row gap-3 pt-4 border-t border-yellow-600">
        <!-- 如果是主辦人，顯示取消活動按鈕 -->
        <button
          v-if="isOrganizer"
          @click="$emit('cancel-event', eventData.id)"
          class="flex-1 bg-red-900 border border-red-700 text-red-300 py-3 px-6 rounded-lg font-semibold hover:bg-red-800 hover:border-red-600 transition-colors duration-200 flex items-center justify-center"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
          </svg>
          取消活動
        </button>

        <!-- 如果不是主辦人，顯示加入/退出按鈕 -->
        <template v-else>
          <!-- 已加入的情況 -->
          <button
            v-if="hasJoined"
            @click="$emit('leave-event', eventData.id)"
            class="flex-1 bg-orange-900 border border-orange-700 text-orange-300 py-3 px-6 rounded-lg font-semibold hover:bg-orange-800 hover:border-orange-600 transition-colors duration-200 flex items-center justify-center"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
            </svg>
            退出活動
          </button>

          <!-- 未加入的情況 -->
          <button
            v-else
            @click="$emit('join-event', eventData.id)"
            :disabled="eventData.spotsRemaining <= 0"
            :class="joinButtonClass"
            class="flex-1 py-3 px-6 rounded-lg font-semibold transition-colors duration-200 flex items-center justify-center border"
          >
            <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
            </svg>
            {{ joinButtonText }}
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// Props
const props = defineProps({
  eventData: {
    type: Object,
    required: true
  },
  currentUserId: {
    type: Number,
    default: 0
  },
  joinedEventIds: {
    type: Array,
    default: () => []
  }
})

// Emits
defineEmits([
  'join-event',
  'leave-event',
  'cancel-event',
  'show-profile'
])

// 計算屬性
const isOrganizer = computed(() => {
  return props.eventData.organizer?.id === props.currentUserId
})

const hasJoined = computed(() => {
  return props.joinedEventIds.includes(props.eventData.id)
})

const spotsColorClass = computed(() => {
  const remaining = props.eventData.spotsRemaining || 0
  if (remaining <= 0) return 'text-red-400'
  if (remaining <= 2) return 'text-orange-400'
  return 'text-emerald-400'
})

const joinButtonClass = computed(() => {
  const remaining = props.eventData.spotsRemaining || 0
  if (remaining <= 0) {
    return 'bg-gray-800 border-gray-600 text-gray-500 cursor-not-allowed'
  }
  return 'bg-yellow-900 border-yellow-600 text-yellow-300 hover:bg-yellow-800 hover:border-yellow-500'
})

const joinButtonText = computed(() => {
  const remaining = props.eventData.spotsRemaining || 0
  if (remaining <= 0) return '名額已滿'
  return '申請加入'
})

const formattedDateTime = computed(() => {
  if (!props.eventData.datetime) return '時間待定'
  
  try {
    const date = new Date(props.eventData.datetime)
    return date.toLocaleString('zh-TW', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      weekday: 'long',
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch (error) {
    return props.eventData.datetime
  }
})
// 活動類型標籤
const typeLabel = computed(() => {
  switch (props.eventData.type) {
    case 'carpool': return '共乘'
    case 'party': return 'party'
    case 'sex': return 'Netflix and chill'
    default: return '活動'
  }
})
</script>

<style scoped>
/* 自定義滾動條樣式 - 黑金主題 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #1f1f1f;
  border-radius: 4px;
  border: 1px solid #d4af37;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #d4af37, #b8860b);
  border-radius: 4px;
  border: 1px solid #8b7355;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #ffd700, #daa520);
}

/* 響應式調整 */
@media (max-width: 640px) {
  .grid-cols-1.md\:grid-cols-2 {
    grid-template-columns: 1fr;
  }
}

/* 添加微妙的發光效果 */
.border-yellow-500 {
  box-shadow: 0 0 5px rgba(212, 175, 55, 0.3);
}

.border-yellow-600 {
  box-shadow: 0 0 3px rgba(212, 175, 55, 0.2);
}

/* 按鈕hover效果增強 */
button:hover {
  box-shadow: 0 0 8px rgba(212, 175, 55, 0.4);
}

/* 標題文字發光效果 */
h1.text-yellow-300 {
  text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
}
</style>