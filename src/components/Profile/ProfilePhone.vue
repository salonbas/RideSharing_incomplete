// ProfilePhone.vue
<template>
  <div v-if="showField" class="relative">
    <div class="text-sm font-medium text-gray-500 mb-1">電話號碼</div>
    
    <div class="flex items-center justify-between">
      <div class="flex items-center" @click="togglePhoneVisibility">
        <!-- 手機圖標 -->
        <div 
          class="transition-opacity duration-300 cursor-pointer mr-2"
          :class="{ 'opacity-30': isPhoneVisible }"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
        </div>
        
        <!-- 電話號碼 -->
        <span 
          class="transition-opacity duration-300"
          :class="{ 'opacity-100': isPhoneVisible, 'opacity-0': !isPhoneVisible }"
        >
          {{ displayValue }}
        </span>
      </div>
      
      <button 
        v-if="editable" 
        @click="$emit('edit')"
        class="text-gray-400 hover:text-blue-500 transition ml-2"
        aria-label="編輯電話"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  phoneNumber: {
    type: String,
    default: ''
  },
  editable: {
    type: Boolean,
    default: false
  }
});

defineEmits(['edit']);

// 控制電話號碼顯示狀態
const isPhoneVisible = ref(false);

// 顯示邏輯：無值且不可編輯則不顯示整欄
const showField = computed(() => {
  return props.phoneNumber || props.editable;
});

// 顯示值：無值但可編輯顯示(未填寫)，否則顯示值
const displayValue = computed(() => {
  return props.phoneNumber || (props.editable ? '(未填寫)' : '');
});

// 切換電話顯示狀態
const togglePhoneVisibility = () => {
  if (props.phoneNumber) {
    isPhoneVisible.value = !isPhoneVisible.value;
  }
};
</script>
