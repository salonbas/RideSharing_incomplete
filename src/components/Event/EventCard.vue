// components/Event/EventCard.vue
<template>
  <div
    class="w-full bg-white/10 backdrop-blur-sm border border-white/20 text-white rounded-[28px] shadow-md hover:scale-[1.02] transition px-6 py-4 flex items-center justify-between gap-4"
  >
    <!-- 🧑 頭像 -->
    <div
      class="flex-shrink-0 h-14 w-14 rounded-full overflow-hidden cursor-pointer"
      @click="$emit('show-profile', eventData.organizer)"
    >
      <img
        :src="eventData.organizer.avatar"
        :alt="eventData.organizer.nickname"
        class="h-full w-full object-cover"
      />
    </div>

    <!-- 📍 中間資訊（地點、時間） -->
    <div class="flex-1 min-w-0">
      <div class="text-lg font-semibold truncate">
        {{ eventData.title }}
      </div>
      <div class="text-sm text-gray-300 truncate">
        {{ eventData.location }} ｜ {{ formattedDate }}
      </div>
    </div>

    <!-- 💰 費用 / 剩餘人數 / 按鈕 -->
    <div class="text-right space-y-1">
      <div class="text-sm">
        💰 {{ eventData.price === 0 ? '免費' : `$${eventData.price}` }}
      </div>
      <div :class="['text-sm', spotsColorClass]">
        剩餘 {{ eventData.spotsRemaining }} 人
      </div>
      <button
        class="text-sm mt-1 bg-blue-500 hover:bg-blue-400 text-white px-3 py-1 rounded-full font-semibold disabled:bg-gray-500 disabled:cursor-not-allowed"
        @click="$emit('join-event', eventData.id)"
        :disabled="eventData.spotsRemaining <= 0"
      >
        {{ eventData.spotsRemaining > 0 ? '搭車' : '額滿' }}
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
