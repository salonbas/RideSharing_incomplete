<template>
  <div class="max-w-3xl mx-auto bg-white p-6 rounded-lg shadow-md">
    <h1 class="text-2xl font-bold mb-4">{{ event.title }}</h1>

    <div class="mb-4 text-gray-600">
      <p><strong>活動類型：</strong> {{ typeLabel }}</p>
      <p><strong>時間：</strong> {{ formattedDate }}</p>
      <p><strong>地點：</strong> {{ event.location }}</p>
      <p><strong>費用：</strong> {{ event.price === 0 ? '免費' : `$${event.price}` }}</p>
      <p><strong>剩餘名額：</strong> {{ event.spotsRemaining }}</p>
    </div>

    <div class="flex items-center space-x-4 mb-6">
      <img :src="event.organizer.avatar" alt="Avatar" class="w-12 h-12 rounded-full object-cover" />
      <div>
        <p class="text-gray-800 font-semibold">{{ event.organizer.nickname }}</p>
        <p class="text-sm text-gray-500">主辦人</p>
      </div>
    </div>

    <div>
      <h2 class="text-lg font-semibold mb-2">活動介紹</h2>
      <p class="text-gray-700 leading-relaxed whitespace-pre-wrap">
        {{ event.description || '主辦人尚未提供詳細介紹。' }}
      </p>
    </div>

    <div class="mt-6 flex justify-end">
      <button
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        @click="joinEvent"
        :disabled="event.spotsRemaining <= 0"
      >
        {{ event.spotsRemaining > 0 ? '申請加入活動' : '活動已額滿' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  event: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['join']);

// 日期格式
const formattedDate = computed(() => {
  const date = new Date(props.event.datetime);
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  return `${month}/${day} ${hours}:${minutes}`;
});

// 類型標籤
const typeLabel = computed(() => {
  switch (props.event.type) {
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

// 點擊加入事件
function joinEvent() {
  emit('join', props.event.id);
}
</script>
