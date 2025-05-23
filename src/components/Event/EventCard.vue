// components/Event/EventCard.vue
<template>
  <div
    class="w-full h-[40vh] bg-white/10 backdrop-blur-sm text-white rounded-[28px] shadow-md hover:scale-[1.02] transition p-4 flex flex-col"
  >
    <div class="flex-1 flex mb-2">
      <!-- 上半部：頭像 + 主辦人與路線 -->
      <div class="w-1/2 h-full flex items-center justify-center p-6">
        <!-- 🧑 頭像 -->
        <div
          class="h-full aspect-square rounded-full overflow-hidden cursor-pointer"
          @click="$emit('show-profile', eventData.organizer.id)"
        >
          <img
            :src="eventData.organizer.avatar"
            :alt="eventData.organizer.nickname"
            class="h-full w-full object-cover"
          />
        </div>
      </div>
      <!-- 👤 名字 + 路線 -->
      <div class="w-1/2 flex flex-col justify-center items-center pl-2">
        <div class="text-xl font-semibold truncate">
            {{ eventData.organizer.nickname }}
          </div>
          <div class="text-sm text-gray-300 w-full break-words whitespace-normal">
            {{ eventData.location.from.city }} {{ eventData.location.from.detail }}
            →
            {{ eventData.location.destination.city }} {{ eventData.location.destination.detail }}
          </div>
      </div>
    </div>

      <div class="flex-1 flex">
      <!-- 下半部：資訊 3:1 -->
      <div class="w-3/4 space-y-1 text-sm text-gray-300 flex flex-col justify-center items-start pl-4">
          <div>時間： {{ formattedDate }}</div>
          <div>金額： {{ eventData.price === 0 ? '免費' : `$${eventData.price}` }}</div>
          <div>地點： {{ eventData.location.from.city }} {{ eventData.location.from.detail }}
                    →
                  {{ eventData.location.destination.city }} {{ eventData.location.destination.detail }}
          </div>
      </div>
      <!-- 右側 1 欄 -->
      <div class="w-1/4 flex flex-col justify-end">
          <div
            class="text-xs mb-0 font-semibold"
            :class="spotsColorClass"
            >
              剩 {{ eventData.spotsRemaining }} 人
          </div>
          <button
            class="link-btn link-btn-disabled border-animate"
            @click="$emit('join-event', eventData.id)"
            :disabled="eventData.spotsRemaining <= 0"
          >
            {{ eventData.spotsRemaining > 0 ? '卡' : '不能卡' }}
          </button>
        </div>
      </div>
  </div>
</template>
<script setup>
import { computed } from 'vue'
import { format } from 'date-fns'

// 解構 props（避免一直 props.eventData）
const { eventData } = defineProps({
  eventData: {
    type: Object,
    required: true
  }
})

// 定義 emit 事件
defineEmits(['show-profile', 'join-event'])

// ✅ 格式化日期與時間（修正成 eventData.date）
const formattedDate = computed(() => {
  const date = new Date(eventData.date) // ← 修正這行
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  return `${month}/${day} ${hours}:${minutes}`
})

// ✅ 活動類型標籤
const typeLabel = computed(() => {
  switch (eventData.type) {
    case 'carpool': return '共乘'
    case 'drink': return '飲酒'
    case 'sports': return '運動'
    default: return '活動'
  }
})

// ✅ 活動類型色系 class
const typeColorClass = computed(() => {
  switch (eventData.type) {
    case 'carpool': return 'bg-green-100 text-green-600'
    case 'drink': return 'bg-blue-100 text-blue-600'
    case 'sports': return 'bg-orange-100 text-orange-600'
    default: return 'bg-gray-100 text-gray-600'
  }
})

// ✅ 名額顏色 class
const spotsColorClass = computed(() => {
  if (eventData.spotsRemaining <= 0) return 'text-red-500'
  if (eventData.spotsRemaining <= 2) return 'text-orange-500'
  return 'text-green-500'
})
</script>
