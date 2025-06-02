// components/Event/EventCard.vue
<template>
  <div class="card-wrapper" @click="$emit('show-detail', eventData.id)">
    <div class="card-inner group">
      <!-- 馬賽克動畫遮罩 -->
      <div v-if="playAnimation" ref="overlayRef" class="mosaic-overlay">
        <canvas ref="mosaicCanvas" class="mosaic-canvas"></canvas>
      </div>
      
      <!-- 正面 -->
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
            <div class="text-sm text-blue-400 mt-1 cursor-pointer" @click.stop="openInstagram">
              IG: {{ eventData.organizer.instagram }}
            </div>
          </div>
        </div>

        <div class="flex-1 flex">
        <!-- 下半部：資訊 3:1 -->
        <div class="w-3/4 space-y-1 text-base text-gray-300 flex flex-col justify-center items-start pl-4 group-hover:text-[#1a1a1a]">
          <div>時間／ {{ formattedDate }}</div>
          <div>金額／ {{ eventData.price === 0 ? '免費' : `$${eventData.price}` }}</div>
          <div>地點／ {{ eventData.location.from.city }} {{ eventData.location.from.detail }}<br />
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
            <span class="btn-text whitespace-nowrap group-hover:text-[#1a1a1a]">
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
            <div class="text-xl font-semibold truncate group-hover:text-[#1a1a1a]">
              {{ eventData.organizer.nickname }}
            </div>
            <div class="text-sm text-blue-400 mt-1 cursor-pointer" @click.stop="openInstagram">
              IG: {{ eventData.organizer.instagram }}
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
              <span class="font-medium w-12">時間／</span>
              <span class="ml-2">{{ formattedDate }}</span>
            </div>
            <div class="flex items-center">
              <span class="font-medium w-12">人數／</span>
              <span class="ml-2">{{ eventData.joinedSeats }}/{{ eventData.requiredSeats }}</span>
            </div>
            <div class="flex items-center">
              <span class="font-medium w-12">費用／</span>
              <span class="ml-2">{{ eventData.price === 0 ? '免費' : `$${eventData.price}` }}</span>
            </div>
            <div class="flex items-start">
              <span class="font-medium w-12 mt-0.5">備註／</span>
              <span class="ml-2 mt-0.5 leading-relaxed">{{ eventData.description || '無特殊說明' }}</span>
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
              <span class="btn-text whitespace-nowrap group-hover:text-[#1a1a1a]">
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
import { ref, computed, watch, nextTick, onMounted } from 'vue'
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
  if (isOrganizer.value) return "取消"
  if (isJoined.value) return "退出"
  return "卡"
})

const btnClass = computed(() => {
  if (!props.eventData) return "btn bg-[#12150e]"

  if (isOrganizer.value) {
    return "btn bg-[#12150e] text-orange-500"
  }

  if (isJoined.value) {
    return "btn bg-[#12150e] text-green-400"
  }

  return "btn bg-[#12150e]"
})

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

const spotsColorClass = computed(() => {
  const remaining = props.eventData?.spotsRemaining || 0
  if (remaining <= 0) return 'text-red-500'
  if (remaining <= 2) return 'text-orange-500'
  return 'text-green-500'
})

const typeLabel = computed(() => {
  switch (props.eventData.type) {
    case 'carpool': return '共乘'
    case 'party': return 'party'
    case 'sex': return 'Netflix and chill'
    default: return '活動'
  }
})

const handleButtonClick = () => {
  if (isOrganizer.value) {
    emit('cancel-event', props.eventData.id)
  } else if (isJoined.value) {
    emit('leave-event', props.eventData.id)
  } else {
    emit('join-event', props.eventData.id)
  }
}

// 馬賽克動畫相關
const overlayRef = ref(null)
const mosaicCanvas = ref(null)

// 監聽 props 變化
watch(() => props.playAnimation, (newVal) => {
  if (newVal) {
    nextTick(() => {
      runMosaicAnimation()
    })
  }
})

function runMosaicAnimation() {
  if (!overlayRef.value || !mosaicCanvas.value) return
  
  const canvas = mosaicCanvas.value
  const ctx = canvas.getContext('2d')
  const overlay = overlayRef.value
  
  // 設置 canvas 尺寸
  const rect = overlay.getBoundingClientRect()
  canvas.width = rect.width
  canvas.height = rect.height
  
  // 馬賽克參數
  let pixelSize = 20 // 初始像素塊大小
  const minPixelSize = 1 // 最小像素塊大小
  
  // 生成隨機顏色的馬賽克
  function drawMosaic(size) {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    
    for (let x = 0; x < canvas.width; x += size) {
      for (let y = 0; y < canvas.height; y += size) {
        // 生成隨機灰度色彩作為馬賽克塊
        const gray = Math.floor(Math.random() * 100 + 50) // 50-150 的灰度
        ctx.fillStyle = `rgba(${gray}, ${gray}, ${gray}, 0.6)`
        ctx.fillRect(x, y, size, size)
      }
    }
  }
  
  // GSAP 動畫時間軸
  const tl = gsap.timeline()
  
  // 初始狀態：顯示馬賽克
  tl.set(overlay, { opacity: 1 })
    .call(() => drawMosaic(pixelSize))
    
  // 馬賽克像素逐漸變小直到消失
  tl.to({}, {
    duration: 1.5,
    ease: 'power2.out',
    onUpdate: function() {
      const progress = this.progress()
      // 像素大小從 20 縮小到 1
      const currentPixelSize = pixelSize - (pixelSize - minPixelSize) * progress
      drawMosaic(Math.max(currentPixelSize, minPixelSize))
      
      // 同時降低透明度
      overlay.style.opacity = 1 - progress * 0.8
    }
  })
  
  // 最後完全淡出
  tl.to(overlay, {
    opacity: 0,
    duration: 0.3,
    ease: 'power2.out',
    onComplete: () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
    }
  })
}
const openInstagram = () => {
  if (!props.eventData?.organizer?.instagram) return;
  const igAccount = props.eventData.organizer.instagram.replace('@', '');
  const url = `https://www.instagram.com/${igAccount}/`;
  window.open(url, "_blank");
};
</script>

<style scoped>
.mosaic-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 50;
  background: rgba(0, 0, 0, 0.2);
}

.mosaic-canvas {
  width: 100%;
  height: 100%;
  display: block;
}

/* 原有的 card-wrapper, card-inner 等樣式保持不變 */
</style>