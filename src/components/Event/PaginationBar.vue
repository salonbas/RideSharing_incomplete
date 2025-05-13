<!-- components/Event/PaginationBar.vue -->
<template>
  <div class="flex justify-center space-x-2 flex-wrap">
    <!-- 第一頁按鈕 -->
    <button
      @click="$emit('page-change', 1)"
      :disabled="currentPage === 1"
      class="px-3 py-2 border rounded-md"
      :class="currentPage === 1 ? 'bg-gray-300 text-gray-500' : 'bg-white text-gray-700 hover:bg-gray-200'"
    >
      First
    </button>

    <!-- 中間頁數 -->
    <button
      v-for="page in totalPages"
      :key="page"
      @click="$emit('page-change', page)"
      :class="[
        'px-3 py-2 border rounded-md',
        currentPage === page
          ? 'bg-blue-600 text-white'
          : 'bg-white text-gray-700 hover:bg-gray-200'
      ]"
    >
      {{ page }}{{ page === 1 ? 'st' : page === 2 ? 'nd' : page === 3 ? 'rd' : 'th' }} page
    </button>

    <!-- 最後一頁按鈕 -->
    <button
      @click="$emit('page-change', totalPages)"
      :disabled="currentPage === totalPages"
      class="px-3 py-2 border rounded-md"
      :class="currentPage === totalPages ? 'bg-gray-300 text-gray-500' : 'bg-white text-gray-700 hover:bg-gray-200'"
    >
      Last
    </button>
  </div>
</template>

<script setup>
defineProps({
  totalPages: Number,
  currentPage: Number
});
defineEmits(['page-change']);
</script>
