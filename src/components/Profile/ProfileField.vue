// ProfileField.vue
<template>
  <div v-if="showField" class="group relative">
    <div class="flex items-center justify-between">
      <div class="flex-grow">
        <div class="text-sm font-medium text-gray-500 mb-1">{{ label }}</div>
        <div class="text-base text-gray-800">
          {{ displayValue }}
        </div>
      </div>
      
      <button 
        v-if="editable" 
        @click="$emit('edit')"
        class="text-gray-400 hover:text-blue-500 transition ml-2"
        aria-label="編輯"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  label: {
    type: String,
    required: true
  },
  value: {
    type: String,
    default: ''
  },
  editable: {
    type: Boolean,
    default: false
  }
});

defineEmits(['edit']);

// 顯示邏輯：無值且不可編輯則不顯示整欄，有值或可編輯則顯示
const showField = computed(() => {
  return props.value || props.editable;
});

// 顯示值：無值但可編輯顯示(未填寫)，否則顯示值
const displayValue = computed(() => {
  return props.value || (props.editable ? '(未填寫)' : '');
});
</script>

