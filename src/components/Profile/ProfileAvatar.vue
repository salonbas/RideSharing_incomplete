// ProfileAvatar.vue
<template>
  <div class="relative">
    <!-- 頭像顯示 -->
    <div 
      class="w-24 h-24 rounded-full overflow-hidden bg-gray-200 flex items-center justify-center"
    >
      <img 
        v-if="avatar" 
        :src="avatar" 
        alt="用戶頭像" 
        class="w-full h-full object-cover"
      />
      <span v-else class="text-gray-400">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      </span>
    </div>
    
    <!-- 編輯按鈕 (可選) -->
    <button 
      v-if="editable" 
      @click="$emit('edit')"
      class="absolute bottom-0 right-0 bg-white rounded-full p-1 shadow-md hover:bg-gray-100 transition"
    >
      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
      </svg>
    </button>
  </div>
</template>

<script setup>
defineProps({
  avatar: {
    type: String,
    default: ''
  },
  editable: {
    type: Boolean,
    default: false
  }
});

defineEmits(['edit']);
</script>

// 用法示例
<template>
  <div class="p-4">
    <ProfileBox 
      :user="user" 
      :is-self="true"
      @edit="handleEdit"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ProfileBox from './components/ProfileBox.vue';

const user = ref({
  avatar: 'https://via.placeholder.com/150',
  nickname: '用戶小明',
  account: 'xiaoming123',
  instagram: '@xiaoming_insta',
  phoneNumber: '0912-345-678'
});

const handleEdit = ({ field }) => {
  console.log(`Editing field: ${field}`);
  // 這裡可以打開編輯對話框等等
};
</script>