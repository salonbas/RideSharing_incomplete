<template>
  <div class="flex flex-col items-center space-y-4">
    <!-- 下一頁 -->
    <button
      @click="$emit('page-change', currentPage + 1)"
      :disabled="currentPage === totalPages"
      class="text-white text-3xl px-3 transition hover:text-yellow-400 disabled:opacity-30 disabled:cursor-not-allowed"
      aria-label="Next page"
    >
      &rarr;
    </button>

    <!-- 上一頁 -->
    <button
      @click="$emit('page-change', currentPage - 1)"
      :disabled="currentPage === 1"
      class="text-white text-3xl px-3 transition hover:text-yellow-400 disabled:opacity-30 disabled:cursor-not-allowed"
      aria-label="Previous page"
    >
      &larr;
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
