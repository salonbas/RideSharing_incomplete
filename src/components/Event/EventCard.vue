// components/Event/EventCard.vue
<template>
  <div class="bg-white rounded-lg shadow-md overflow-hidden transition hover:shadow-lg">
    <!-- 活動類型標籤 -->
    <div class="bg-gray-100 px-4 py-2 flex items-center border-b">
      <div class="flex items-center">
        <!-- 活動類型圖示 -->
        <div class="p-1 rounded-md" :class="typeColorClass">
          <svg v-if="eventData.type === 'carpool'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h8m-8 5h8m-4 5v-5m4 5V7a4 4 0 00-8 0v10a4 4 0 108 0z" />
          </svg>
          <svg v-else-if="eventData.type === 'drink'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
          <svg v-else-if="eventData.type === 'sports'" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        </div>
        <span class="ml-2 text-sm font-medium">{{ typeLabel }}</span>
      </div>
      
      <h3 class="ml-2 text-sm font-semibold text-gray-700 truncate">{{ eventData.title }}</h3>
    </div>
    
    <div class="p-4">
      <!-- 主辦人資訊 -->
      <div class="flex items-center mb-4">
        <div
          class="h-10 w-10 rounded-full overflow-hidden cursor-pointer"
          @click="$emit('show-profile', eventData.organizer)"
        >
          <img 
            :src="eventData.organizer.avatar" 
            :alt="eventData.organizer.nickname"
            class="h-full w-full object-cover"
          />
        </div>
        <div class="ml-3">
          <div class="text-sm font-medium text-gray-800">{{ eventData.organizer.nickname }}</div>
          <div class="text-xs text-gray-500">主辦人</div>
        </div>
      </div>
      
      <!-- 活動資訊 -->
      <div class="space-y-2">
        <!-- 地點 -->
        <div class="flex items-center text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span>{{ eventData.location }}</span>
        </div>
        
        <!-- 時間 -->
        <div class="flex items-center text-sm">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
          <span>{{ formattedDate }}</span>
        </div>
        
        <!-- 價格與名額資訊 -->
        <div class="flex justify-between text-sm">
          <div class="flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ eventData.price === 0 ? '免費' : `$${eventData.price}` }}</span>
          </div>
          
          <div class="flex items-center" :class="spotsColorClass">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span>剩餘 {{ eventData.spotsRemaining }} 名額</span>
          </div>
        </div>
      </div>
      
      <!-- 申請加入按鈕 -->
      <button 
        class="mt-4 w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded-md transition duration-200 disabled:bg-gray-300 disabled:cursor-not-allowed"
        @click="$emit('join-event', eventData.id)"
        :disabled="eventData.spotsRemaining <= 0"
      >
        {{ eventData.spotsRemaining > 0 ? '申請加入' : '已額滿' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  eventData: {
    type: Object,
    required: true
  }
});

defineEmits(['show-profile', 'join-event']);

// 格式化日期與時間
const formattedDate = computed(() => {
  const date = new Date(props.eventData.datetime);
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  
  return `${month}/${day} ${hours}:${minutes}`;
});

// 計算活動類型標籤與顏色
const typeLabel = computed(() => {
  switch (props.eventData.type) {
    case 'carpool':
      return '共乘';
    case 'drink':
      return '飲酒';
    case 'sports':
      return '運動';
    default:
      return '活動';
  }
});

const typeColorClass = computed(() => {
  switch (props.eventData.type) {
    case 'carpool':
      return 'bg-green-100 text-green-600';
    case 'drink':
      return 'bg-blue-100 text-blue-600';
    case 'sports':
      return 'bg-orange-100 text-orange-600';
    default:
      return 'bg-gray-100 text-gray-600';
  }
});

// 名額顏色
const spotsColorClass = computed(() => {
  if (props.eventData.spotsRemaining <= 0) {
    return 'text-red-500';
  } else if (props.eventData.spotsRemaining <= 2) {
    return 'text-orange-500';
  } else {
    return 'text-green-500';
  }
});
</script>
