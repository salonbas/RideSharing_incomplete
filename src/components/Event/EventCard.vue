// components/Event/EventCard.vue
<template>
  <div class="card-wrapper" @click="$emit('show-detail', eventData.id)">
    <div class="card-inner group">
        <div v-if="playAnimation" ref="overlayRef" class="absolute inset-0 bg-black/30 pointer-events-none z-50"></div>
      <!-- 正面 -->
      <!-- 動畫遮罩 -->
      <div class="card-face card-front">
        <div class="flex-1 flex mb-2">
          <!-- 上半部：頭像 + 主辦人與路線 -->
          <div class="w-1/2 h-full flex items-center justify-center p-6">
            <!-- 🧑 頭像 -->
            <div
              class="h-full aspect-square rounded-full overflow-hidden cursor-pointer"
              @click="$emit('show-profile', eventData.organizer.id)"
            >
            <img
            :src="eventData.organizer.avatarUrl || '/default-avatar.png'"
            :alt="eventData.organizer.nickname"
            class="h-full w-full object-cover"
            />
            </div>
          </div>
          <!-- 👤 名字 + 路線 -->
          <div class="w-1/2 flex flex-col justify-center items-center pl-2 ">
            <div class="text-xl font-semibold truncate group-hover:text-[#1a1a1a]">
              {{ eventData.organizer.nickname }}
            </div>
            <div class="text-sm text-gray-300 w-full break-words whitespace-normal group-hover:text-[#1a1a1a]">
              {{ eventData.location.from.city }} {{ eventData.location.from.detail }}
              →
              {{ eventData.location.destination.city }} {{ eventData.location.destination.detail }}
            </div>
          </div>
        </div>

        <div class="flex-1 flex">
        <!-- 下半部：資訊 3:1 -->
        <div class="w-3/4 space-y-1 text-sm text-gray-300 flex flex-col justify-center items-start pl-4 group-hover:text-[#1a1a1a]">
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
            :class="btnClass"
            @click="$emit('join-event', eventData.id)"
            :disabled="isOrganizer || eventData.spotsRemaining <= 0"
          >
            <span class="btn-text group-hover:text-[#1a1a1a]">
              {{ btnText }}
            </span>
            <svg viewBox="0 0 100 40" preserveAspectRatio="none">
              <rect x="3" y="3" width="94" height="34" rx="17" ry="17" />
            </svg>
          </button>
          </div>
        </div>
      </div>
      <!-- 背面 -->
      <div class="card-face card-back">
        <div class="flex-1 flex mb-2">
          <!-- 上半部：頭像 + 主辦人與活動類型 -->
          <div class="w-1/2 h-full flex items-center justify-center p-6">
            <!-- 🧑 頭像 (稍大一些) -->
            <div
              class="h-full aspect-square rounded-full overflow-hidden cursor-pointer border-2 border-[#d1ad41]"
              @click.stop="$emit('show-profile', eventData.organizer.id)"
            >
              <img
                :src="eventData.organizer.avatarUrl || '/default-avatar.png'"
                :alt="eventData.organizer.nickname"
                class="h-full w-full object-cover"
              />
            </div>
          </div>
          <!-- 👤 名字 + 活動類型 -->
          <div class="w-1/2 flex flex-col justify-center items-center pl-2">
            <div class="text-xl font-semibold truncate group-hover:text-[#1a1a1a] mb-2">
              {{ eventData.organizer.nickname }}
            </div>
            <div class="bg-[#d1ad41] text-black px-3 py-1 rounded text-sm font-medium">
              {{ typeLabel }}
            </div>
          </div>
        </div>

        <div class="flex-1 flex">
          <!-- 下半部：詳細資訊 3:1 -->
          <div class="w-3/4 space-y-2 text-sm text-gray-300 flex flex-col justify-center items-start pl-4 group-hover:text-[#1a1a1a]">
            <div class="flex items-center">
              <span class="font-medium w-12">時間</span>
              <span class="ml-2">{{ formattedDate }}</span>
            </div>
            <div class="flex items-center">
              <span class="font-medium w-12">人數</span>
              <span class="ml-2">{{ eventData.joinedSeats }}/{{ eventData.requiredSeats }}</span>
            </div>
            <div class="flex items-center">
              <span class="font-medium w-12">費用</span>
              <span class="ml-2">{{ eventData.price === 0 ? '免費' : `$${eventData.price}` }}</span>
            </div>
            <div class="flex items-start">
              <span class="font-medium w-12 mt-0.5">備註</span>
              <span class="ml-2 text-xs leading-relaxed">{{ eventData.description || '無特殊說明' }}</span>
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
              :class="btnClass"
              @click.stop="handleButtonClick"
              :disabled="eventData.spotsRemaining <= 0 && !isOrganizer && !isJoined"
            >
              <span class="btn-text group-hover:text-[#1a1a1a]">
                {{ btnText }}
              </span>
              <svg viewBox="0 0 100 40" preserveAspectRatio="none">
                <rect x="3" y="3" width="94" height="34" rx="17" ry="17" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { format } from 'date-fns'
import { gsap } from 'gsap'

const showAvatarModal = ref(false)

const props = defineProps({
  eventData: {
    type: Object,
    required: true,
    default: () => ({})
  },
  currentUserId: {
    type: Number,
    required: false,
    default: null
  },
  joinedEventIds: {
    type: Array,
    required: false,
    default: () => []
  },
  playAnimation: { 
    type: Boolean, 
    required: false, 
    default: false 
  } 
})

const emit = defineEmits(['show-profile', 'join-event', 'leave-event', 'cancel-event', 'show-detail'])

const isOrganizer = computed(() => {
  if (!props.eventData?.organizer?.id || !props.currentUserId) return false
  return props.currentUserId === props.eventData.organizer.id
})

const isJoined = computed(() => {
  if (!props.eventData?.id || !props.joinedEventIds) return false
  return props.joinedEventIds.includes(props.eventData.id)
})

const btnText = computed(() => {
  if (isOrganizer.value) return "取消活動"
  if (isJoined.value) return "退出"
  return "卡"
})

const btnClass = computed(() => {
  if (!props.eventData) return "btn bg-[#12150e]"
  if (isOrganizer.value || isJoined.value) return "btn btn-secondary bg-[#12150e]"
  return "btn bg-[#12150e]"
})


// 格式化日期與時間 - 添加安全檢查
const formattedDate = computed(() => {
  if (!props.eventData?.date) return '時間未定'
  
  try {
    const date = new Date(props.eventData.date)
    if (isNaN(date.getTime())) return '時間格式錯誤'
    
    const month = date.getMonth() + 1
    const day = date.getDate()
    const hours = date.getHours().toString().padStart(2, '0')
    const minutes = date.getMinutes().toString().padStart(2, '0')
    return `${month}/${day} ${hours}:${minutes}`
  } catch (error) {
    return '時間格式錯誤'
  }
})

// 名額顏色 class - 添加安全檢查
const spotsColorClass = computed(() => {
  const remaining = props.eventData?.spotsRemaining || 0
  if (remaining <= 0) return 'text-red-500'
  if (remaining <= 2) return 'text-orange-500'
  return 'text-green-500'
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

// 處理背面按鈕點擊事件
const handleButtonClick = () => {
  if (isOrganizer.value) {
    emit('cancel-event', props.eventData.id)
  } else if (isJoined.value) {
    emit('leave-event', props.eventData.id)
  } else {
    emit('join-event', props.eventData.id)
  }
}
const overlayRef = ref(null)

// 監聽 props 變化
watch(() => props.playAnimation, (newVal) => {
  if (newVal) {
    nextTick(() => {
      runAnimation()
    })
  }
})

function runAnimation() {
  if (!overlayRef.value) return
  
  gsap.timeline()
    .set(overlayRef.value, {
      opacity: 1,
      backdropFilter: 'blur(20px)',
      scale: 1.05
    })
    .to(overlayRef.value, {
      opacity: 0,
      backdropFilter: 'blur(0px)',
      scale: 1,
      duration: 1.2,
      ease: 'power2.out'
    })
}
</script>