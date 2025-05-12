
// components/Event/EventFilterSort.vue
<template>
  <div class="bg-white rounded-lg shadow-sm p-4 flex flex-col sm:flex-row gap-4">
    <!-- 排序 -->
    <div class="flex-1">
      <label for="sortBy" class="block text-sm font-medium text-gray-700 mb-1">排序方式</label>
      <select
        id="sortBy"
        v-model="localSortBy"
        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
        @change="emitSortChange"
      >
        <option value="date-asc">時間（由近到遠）</option>
        <option value="date-desc">時間（由遠到近）</option>
        <option value="price-asc">價格（由低到高）</option>
        <option value="price-desc">價格（由高到低）</option>
        <option value="spots-asc">名額（由少到多）</option>
        <option value="spots-desc">名額（由多到少）</option>
      </select>
    </div>
    
    <!-- 篩選 -->
    <div class="flex-1">
      <label for="filterType" class="block text-sm font-medium text-gray-700 mb-1">活動類型</label>
      <select
        id="filterType"
        v-model="localFilterType"
        class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
        @change="emitFilterChange"
      >
        <option value="all">全部類型</option>
        <option value="carpool">共乘</option>
        <option value="drink">飲酒</option>
        <option value="sports">運動</option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  initialSort: {
    type: String,
    default: 'date-asc'
  },
  initialFilter: {
    type: String,
    default: 'all'
  }
});

const emit = defineEmits(['sort-change', 'filter-change']);

const localSortBy = ref(props.initialSort);
const localFilterType = ref(props.initialFilter);

// 監聽 props 的變化，以保持與父組件的同步
watch(() => props.initialSort, (newValue) => {
  localSortBy.value = newValue;
});

watch(() => props.initialFilter, (newValue) => {
  localFilterType.value = newValue;
});

// 發送排序變更事件
const emitSortChange = () => {
  emit('sort-change', localSortBy.value);
};

// 發送篩選變更事件
const emitFilterChange = () => {
  emit('filter-change', localFilterType.value);
};
</script>
