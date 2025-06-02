<!-- components/Event/EventFilterSort.vue -->
<template>
  <div class="relative">
    <!-- 主按鈕 -->
    <button
      @click="toggleExpanded"
      class="bg-black border border-yellow-400 rounded-lg px-6 py-3 text-yellow-400 font-medium hover:bg-gray-900 transition-all duration-300 ease-in-out focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:ring-opacity-50"
    >
      排序&篩選
    </button>

    <!-- 展開的面板 -->
    <transition
      name="expand"
      @enter="onEnter"
      @leave="onLeave"
    >
      <div
        v-if="isExpanded"
        class="absolute top-0 right-0 bg-black border border-yellow-400 rounded-lg shadow-2xl z-50 min-w-80"
        :style="{ transformOrigin: 'bottom right' }"
      >
        <div class="p-6 space-y-6">
          <!-- 標題 -->
          <div class="flex justify-between items-center">
            <h3 class="text-yellow-400 font-medium text-lg">排序&篩選</h3>
            <button
              @click="toggleExpanded"
              class="text-yellow-400 hover:text-white transition-colors"
            >
              ✕
            </button>
          </div>

          <!-- 排序選項 -->
          <div>
            <label class="block text-yellow-400 font-medium mb-3">排序方式</label>
            <div class="space-y-2">
              <label
                v-for="option in sortOptions"
                :key="option.value"
                class="flex items-center cursor-pointer group"
              >
                <input
                  type="radio"
                  :value="option.value"
                  v-model="localSortBy"
                  @change="emitSortChange"
                  class="sr-only"
                />
                <div class="w-4 h-4 border border-yellow-400 rounded-full mr-3 flex items-center justify-center group-hover:bg-yellow-400 group-hover:bg-opacity-20 transition-colors">
                  <div
                    v-if="localSortBy === option.value"
                    class="w-2 h-2 bg-yellow-400 rounded-full"
                  ></div>
                </div>
                <span class="text-white group-hover:text-yellow-400 transition-colors">
                  {{ option.label }}
                </span>
              </label>
            </div>
          </div>

          <!-- 篩選選項 -->
          <div>
            <label class="block text-yellow-400 font-medium mb-3">篩選條件</label>
            
            <!-- 基本篩選 -->
            <div class="space-y-3 mb-4">
              <label class="flex items-center cursor-pointer group">
                <input
                  type="checkbox"
                  v-model="localFilters.hasAvailableSpots"
                  @change="emitFilterChange"
                  class="sr-only"
                />
                <div class="w-4 h-4 border border-yellow-400 rounded mr-3 flex items-center justify-center group-hover:bg-yellow-400 group-hover:bg-opacity-20 transition-colors">
                  <div
                    v-if="localFilters.hasAvailableSpots"
                    class="w-2 h-2 bg-yellow-400"
                  ></div>
                </div>
                <span class="text-white group-hover:text-yellow-400 transition-colors">
                  有剩餘空位
                </span>
              </label>

              <label class="flex items-center cursor-pointer group">
                <input
                  type="checkbox"
                  v-model="localFilters.withinWeek"
                  @change="emitFilterChange"
                  class="sr-only"
                />
                <div class="w-4 h-4 border border-yellow-400 rounded mr-3 flex items-center justify-center group-hover:bg-yellow-400 group-hover:bg-opacity-20 transition-colors">
                  <div
                    v-if="localFilters.withinWeek"
                    class="w-2 h-2 bg-yellow-400"
                  ></div>
                </div>
                <span class="text-white group-hover:text-yellow-400 transition-colors">
                  一週內
                </span>
              </label>

              <label class="flex items-center cursor-pointer group">
                <input
                  type="checkbox"
                  v-model="localFilters.withinMonth"
                  @change="emitFilterChange"
                  class="sr-only"
                />
                <div class="w-4 h-4 border border-yellow-400 rounded mr-3 flex items-center justify-center group-hover:bg-yellow-400 group-hover:bg-opacity-20 transition-colors">
                  <div
                    v-if="localFilters.withinMonth"
                    class="w-2 h-2 bg-yellow-400"
                  ></div>
                </div>
                <span class="text-white group-hover:text-yellow-400 transition-colors">
                  一個月內
                </span>
              </label>
            </div>

            <!-- 城市篩選 -->
            <div>
              <h4 class="text-yellow-400 text-sm font-medium mb-2">城市</h4>
              <div class="grid grid-cols-3 gap-2 max-h-32 overflow-y-auto">
                <label
                  v-for="city in cities"
                  :key="city"
                  class="flex items-center cursor-pointer group text-sm"
                >
                  <input
                    type="checkbox"
                    :value="city"
                    v-model="localFilters.cities"
                    @change="emitFilterChange"
                    class="sr-only"
                  />
                  <div class="w-3 h-3 border border-yellow-400 rounded mr-2 flex items-center justify-center group-hover:bg-yellow-400 group-hover:bg-opacity-20 transition-colors flex-shrink-0">
                    <div
                      v-if="localFilters.cities.includes(city)"
                      class="w-1.5 h-1.5 bg-yellow-400"
                    ></div>
                  </div>
                  <span class="text-white group-hover:text-yellow-400 transition-colors truncate">
                    {{ city }}
                  </span>
                </label>
              </div>
            </div>
          </div>

          <!-- 清除篩選按鈕 -->
          <div class="pt-4 border-t border-yellow-400 border-opacity-30">
            <button
              @click="clearFilters"
              class="w-full bg-transparent border border-yellow-400 text-yellow-400 py-2 px-4 rounded hover:bg-yellow-400 hover:text-black transition-all duration-200"
            >
              清除所有篩選
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue';

const props = defineProps({
  initialSort: {
    type: String,
    default: 'spotsRemaining-desc'
  },
  initialFilters: {
    type: Object,
    default: () => ({
      hasAvailableSpots: false,
      withinWeek: false,
      withinMonth: false,
      cities: []
    })
  }
});

const emit = defineEmits(['sort-change', 'filter-change', 'expand-toggle']);

const isExpanded = ref(false);
const localSortBy = ref(props.initialSort);
const localFilters = reactive({
  hasAvailableSpots: props.initialFilters.hasAvailableSpots,
  withinWeek: props.initialFilters.withinWeek,
  withinMonth: props.initialFilters.withinMonth,
  cities: [...props.initialFilters.cities]
});

const sortOptions = [
  { value: 'spotsRemaining-desc', label: '剩餘名額（多到少）' },
  { value: 'spotsRemaining-asc', label: '剩餘名額（少到多）' },
  { value: 'date-asc', label: '日期（近到遠）' },
  { value: 'date-desc', label: '日期（遠到近）' },
  { value: 'city-asc', label: '城市（A-Z）' },
  { value: 'city-desc', label: '城市（Z-A）' },
  { value: 'price-asc', label: '價格（低到高）' },
  { value: 'price-desc', label: '價格（高到低）' }
];

const cities = [
  '臺北', '新北', '桃園', '臺中', '臺南', '高雄',
  '宜蘭', '新竹', '苗栗', '彰化', '南投', '雲林',
  '嘉義', '屏東', '臺東', '花蓮', '澎湖', '基隆'
];

// 監聽 props 的變化
watch(() => props.initialSort, (newValue) => {
  localSortBy.value = newValue;
});

watch(() => props.initialFilters, (newValue) => {
  Object.assign(localFilters, newValue);
  localFilters.cities = [...newValue.cities];
}, { deep: true });

// 切換展開狀態
const toggleExpanded = () => {
  isExpanded.value = !isExpanded.value;
  emit('expand-toggle', isExpanded.value);
};

// 發送排序變更事件
const emitSortChange = () => {
  emit('sort-change', localSortBy.value);
};

// 發送篩選變更事件
const emitFilterChange = () => {
  emit('filter-change', { ...localFilters });
};

// 清除所有篩選
const clearFilters = () => {
  localFilters.hasAvailableSpots = false;
  localFilters.withinWeek = false;
  localFilters.withinMonth = false;
  localFilters.cities = [];
  emitFilterChange();
};

// 動畫鉤子
const onEnter = (el) => {
  el.style.transform = 'scale(0)';
  el.style.opacity = '0';
  el.offsetHeight; // 強制重繪
  el.style.transition = 'all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
  el.style.transform = 'scale(1)';
  el.style.opacity = '1';
};

const onLeave = (el) => {
  el.style.transition = 'all 0.2s ease-in-out';
  el.style.transform = 'scale(0)';
  el.style.opacity = '0';
};
</script>

<style scoped>
/* 自定義滾動條樣式 */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #fbbf24;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #f59e0b;
}

.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  transform: scale(0);
}
</style>