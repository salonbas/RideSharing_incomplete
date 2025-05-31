// views/EventListPage.vue
<template>
  <div class="min-h-screen bg-[#12150e] text-white">
    <div class="px-4 sm:px-6 md:px-12 lg:px-20 py-8">
      <div class="max-w-[85vw] mx-auto">
      <!-- 頂部區域：創建活動按鈕 -->
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-4xl font-bold text-[#d1ad41]">活動列表</h1>
          <EventFilterSort
            :initialSort="currentSort"
            :initialFilters="currentFilters"
            @sort-change="handleSortChange"
            @filter-change="handleFilterChange"
            @expand-toggle="handleExpandToggle"
          />
          <router-link
            :to="{ name: 'createEvent' }"
            class="btn group"
          >
          <span class="btn-text flex items-center">
            <span class="wave-char text-2xl mr-1 leading-none">+</span>
            <span class="wave-char">發</span>
            <span class="wave-char">起</span>
            <span class="wave-char">活</span>
            <span class="wave-char">動</span>
          </span>
          <svg viewBox="0 0 100 40" preserveAspectRatio="none">
            <rect x="3" y="3" width="94" height="34" rx="17" ry="17" />
          </svg>
        </router-link>
        </div>

        <!-- 活動列表 -->
        <div v-if="loading" class="text-center py-12">
          <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-[#d1ad41] mx-auto"></div>
          <p class="mt-2 text-[#d1ad41]">載入中...</p>
        </div>
        
        <div v-else-if="filteredEvents.length === 0" class="text-center py-12">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="mt-4 text-lg text-[#d1ad41]">沒有找到符合條件的活動</p>
        </div>
        
        <!-- 活動卡片 + 分頁按鈕區塊 -->
        <div v-else class="grid grid-cols-[1fr_auto] gap-4 mt-6">
          <!-- 左：卡片 -->
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 auto-rows-fr gap-8">
            <EventCard 
              v-for="event in eventsToDisplay" 
              :key="event.id" 
              :event-data="event"
              :currentUserId="currentUserId"
              :joinedEventIds="joinedEventIds"
              :play-animation="playAnim" 
              @show-detail="openEventDetail"
              @show-profile="showProfile"
              @join-event="handleJoinEvent"
              @leave-event="handleLeaveEvent"
              @cancel-event="handleCancelEvent"
            />
          </div>

          <!-- 右：上下頁按鈕 -->
          <div class="flex flex-col justify-center items-center space-y-8 relative">
            <!-- 下一頁 group -->
            <div class="relative group">
              <div
                @click="handlePageChange(currentPage + 1)"
                :class="{ 'opacity-30 pointer-events-none': currentPage === totalPages }"
                class="cursor-pointer transition-transform duration-200 ease-out hover:scale-110 hover:translate-x-1 hover:drop-shadow-[0_0_6px_#d1ad41]"
                style="
                  width: 0;
                  height: 0;
                  border-top: 24px solid transparent;
                  border-bottom: 24px solid transparent;
                  border-left: 28px solid white;
                "
              ></div>

              <div
                class="absolute top-[-550%] right-[15%] w-6 h-6 bg-[#d1ad41] rounded-full opacity-0 transition-all duration-500 group-hover:opacity-100 group-hover:translate-x-2"
              ></div>
            </div>

            <!-- 上一頁 group -->
            <div class="relative group">
              <div
                @click="handlePageChange(currentPage - 1)"
                :class="{ 'opacity-30 pointer-events-none': currentPage === 1 }"
                class="cursor-pointer transition-transform duration-200 ease-out hover:scale-110 hover:-translate-x-1 hover:drop-shadow-[0_0_6px_#d1ad41]"
                style="
                  width: 0;
                  height: 0;
                  border-top: 24px solid transparent;
                  border-bottom: 24px solid transparent;
                  border-right: 28px solid white;
                "
              ></div>

              <div
                class="absolute bottom-[-550%] left-[-4800%] w-6 h-6 bg-[#d1ad41] rounded-full opacity-0 transition-all duration-500 group-hover:opacity-100 group-hover:translate-x-2"
              ></div>
            </div>
          </div>
        </div>
      </div>
      <!-- 活動詳情彈窗 -->
      <div 
        v-if="selectedEvent" 
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        @click.self="selectedEvent = null"
      >
        <div class="relative max-w-2xl w-full mx-4">
          <button 
            @click="selectedEvent = null" 
            class="absolute top-4 right-4 z-10 text-white hover:text-gray-300 bg-black bg-opacity-50 rounded-full p-2"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <EventDetail 
            :eventData="selectedEvent"
            :currentUserId="currentUserId"
            :joinedEventIds="joinedEventIds"
            @join-event="handleJoinEvent"
            @leave-event="handleLeaveEvent"
            @cancel-event="handleCancelEvent"
            @show-profile="showProfile"
          />
        </div>
      </div>
      <!-- 個人資料浮動視窗 -->
      <div 
        v-if="showProfileBox" 
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        @click.self="showProfileBox = false"
      >
        <div class="relative bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
          <button 
            @click="showProfileBox = false" 
            class="absolute top-4 right-4 text-gray-500 hover:text-gray-700"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <div class="p-1">
            <ProfileBox 
              :user="selectedOrganizer" 
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useEventService } from '@/composables/useEvents'
import EventCard from '../components/Event/EventCard.vue'
import EventDetail from '../components/Event/EventDetail.vue'
import EventFilterSort from '../components/Event/EventFilterSort.vue'
import PaginationBar from '../components/Event/PaginationBar.vue'
import ProfileBox from '../components/Profile/ProfileBox.vue'

const eventService = useEventService()

const {
  joinedEventIds,
  initJoinedEvents,
  joinEvent,
  leaveEvent,
  cancelEvent,
  createEvent,
  getAllEvents,
  hasJoinedEvent
} = eventService


const playAnim = ref(false)

const auth = useAuthStore()
const currentUserId = auth.user?.id || 0
const selectedEvent = ref(null)

// 路由相關
const router = useRouter();
const route = useRoute();

// 頁面狀態
const loading = ref(true);
const events = ref([]);
const currentPage = ref(1);
const itemsPerPage = 8;

// 個人資料浮動視窗狀態
const showProfileBox = ref(false);
const selectedOrganizer = ref(null);

// 排序和篩選狀態
const currentSort = ref('spotsRemaining-desc');
const currentFilters = ref({
  hasAvailableSpots: false,
  withinWeek: false,
  withinMonth: false,
  cities: []
});

// 展開狀態（用於頁面效果）
const isFilterExpanded = ref(false);

// 從路由參數中獲取頁碼和篩選條件（如果有）
onMounted(() => {
  if (route.query.page) {
    currentPage.value = parseInt(route.query.page) || 1;
  }
  
  // 從路由恢復排序設定
  if (route.query.sort) {
    currentSort.value = route.query.sort;
  }
  
  // 從路由恢復篩選條件
  if (route.query.filters) {
    try {
      const parsedFilters = JSON.parse(decodeURIComponent(route.query.filters));
      currentFilters.value = { ...currentFilters.value, ...parsedFilters };
    } catch (e) {
      console.warn('無法解析篩選參數:', e);
    }
  }
  
  fetchEvents();
  fetchMyEvents();
});

// 監聽排序和篩選條件的變化，重置頁碼
watch([currentSort, currentFilters], () => {
  currentPage.value = 1;
  updateUrlParams();
}, { deep: true });

// 處理排序變更
const handleSortChange = (sortValue) => {
  currentSort.value = sortValue;
};

// 處理篩選變更
const handleFilterChange = (filters) => {
  currentFilters.value = { ...filters };
};

// 處理展開狀態變更
const handleExpandToggle = (isExpanded) => {
  isFilterExpanded.value = isExpanded;
  // 可以在這裡添加頁面背景模糊等效果
};

// 處理分頁變更
const handlePageChange = (page) => {
  playAnim.value = true
  currentPage.value = page;
  setTimeout(() => {
    playAnim.value = false  // 1秒後自動關閉，方便下次重播
  }, 2000)
  updateUrlParams();
  // 滾動到頂部
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
};

const showProfile = async (userId) => {
  try {
    const userData = await auth.getPublicUser(userId)
    selectedOrganizer.value = userData
    showProfileBox.value = true
  } catch (err) {
    console.error('載入 organizer 資料失敗:', err)
    alert('載入個人資料失敗')
  }
}

const openEventDetail = (eventId) => {
  selectedEvent.value = events.value.find(e => e.id === eventId)
}

// 處理加入活動
const handleJoinEvent = async (eventId) => {
  try {
    await eventService.joinEvent(eventId)
    alert('成功申請加入活動')
    
    // 重新載入資料
    await fetchEvents()
    await fetchMyEvents()
    
    // 如果詳情頁面開啟，更新詳情頁面的資料
    if (selectedEvent.value && selectedEvent.value.id === eventId) {
      selectedEvent.value = events.value.find(e => e.id === eventId)
    }
  } catch (err) {
    const msg = err?.response?.data?.error || err?.response?.data?.msg || err.message || '未知錯誤'
    alert(`申請失敗：${msg}`)
  }
}

// 處理退出活動
const handleLeaveEvent = async (eventId) => {
  try {
    await eventService.leaveEvent(eventId)
    alert('成功退出活動')
    
    // 重新載入資料
    await fetchEvents()
    await fetchMyEvents()
    
    // 如果詳情頁面開啟，更新詳情頁面的資料
    if (selectedEvent.value && selectedEvent.value.id === eventId) {
      selectedEvent.value = events.value.find(e => e.id === eventId)
    }
  } catch (err) {
    const msg = err?.response?.data?.error || err?.response?.data?.msg || err.message || '未知錯誤'
    alert(`退出失敗：${msg}`)
  }
}

// 處理取消活動
const handleCancelEvent = async (eventId) => {
  if (!confirm('確定要取消這個活動嗎？此操作無法復原。')) {
    return
  }

  try {
    await eventService.cancelEvent(eventId)
    alert('活動已成功取消')
    
    // 重新載入資料
    await fetchEvents()
    await fetchMyEvents()
    
    // 如果詳情頁面開啟且是被取消的活動，關閉詳情頁面
    if (selectedEvent.value && selectedEvent.value.id === eventId) {
      selectedEvent.value = null
    }
  } catch (err) {
    const msg = err?.response?.data?.error || err?.response?.data?.msg || err.message || '未知錯誤'
    alert(`取消失敗：${msg}`)
  }
}

// 更新 URL 參數
const updateUrlParams = () => {
  const query = {
    page: currentPage.value > 1 ? currentPage.value : undefined,
    sort: currentSort.value !== 'spotsRemaining-desc' ? currentSort.value : undefined
  };

  // 如果有篩選條件，將其序列化到 URL 中
  const hasFilters = currentFilters.value.hasAvailableSpots || 
                    currentFilters.value.withinWeek || 
                    currentFilters.value.withinMonth || 
                    currentFilters.value.cities.length > 0;
  
  if (hasFilters) {
    query.filters = encodeURIComponent(JSON.stringify(currentFilters.value));
  }

  router.replace({ query });
};

// 獲取日期範圍的輔助函數
const getDateRange = (type) => {
  const now = new Date();
  const endDate = new Date(now);
  
  if (type === 'week') {
    endDate.setDate(now.getDate() + 7);
  } else if (type === 'month') {
    endDate.setMonth(now.getMonth() + 1);
  }
  
  return { start: now, end: endDate };
};

// 檢查城市是否匹配
const checkCityMatch = (event, selectedCities) => {
  if (selectedCities.length === 0) return true;
  
  const fromCity = event.location?.from?.city || '';
  const toCity = event.location?.destination?.city || '';
  
  return selectedCities.some(city => 
    fromCity.includes(city) || toCity.includes(city)
  );
};

// 根據篩選條件過濾事件
const filteredEvents = computed(() => {
  let result = [...events.value];
  
  // 篩選有剩餘空位的活動
  if (currentFilters.value.hasAvailableSpots) {
    result = result.filter(event => event.spotsRemaining > 0);
  }
  
  // 篩選時間範圍
  if (currentFilters.value.withinWeek) {
    const { start, end } = getDateRange('week');
    result = result.filter(event => {
      const eventDate = new Date(event.date);
      return eventDate >= start && eventDate <= end;
    });
  } else if (currentFilters.value.withinMonth) {
    const { start, end } = getDateRange('month');
    result = result.filter(event => {
      const eventDate = new Date(event.date);
      return eventDate >= start && eventDate <= end;
    });
  }
  
  // 篩選城市
  if (currentFilters.value.cities.length > 0) {
    result = result.filter(event => checkCityMatch(event, currentFilters.value.cities));
  }
  
  // 排序
  result.sort((a, b) => {
    switch (currentSort.value) {
      case 'spotsRemaining-desc':
        return b.spotsRemaining - a.spotsRemaining;
      case 'spotsRemaining-asc':
        return a.spotsRemaining - b.spotsRemaining;
      case 'date-asc':
        return new Date(a.date) - new Date(b.date);
      case 'date-desc':
        return new Date(b.date) - new Date(a.date);
      case 'city-asc':
        const cityA = a.location?.from?.city || '';
        const cityB = b.location?.from?.city || '';
        return cityA.localeCompare(cityB);
      case 'city-desc':
        const cityA2 = a.location?.from?.city || '';
        const cityB2 = b.location?.from?.city || '';
        return cityB2.localeCompare(cityA2);
      case 'price-asc':
        return (a.price || 0) - (b.price || 0);
      case 'price-desc':
        return (b.price || 0) - (a.price || 0);
      default:
        return 0;
    }
  });
  
  console.log('篩選後剩餘event數量:', result.length);
  return result;
});

// 計算總頁數
const totalPages = computed(() => {
  return Math.ceil(filteredEvents.value.length / itemsPerPage);
});

// 當前頁面要顯示的事件
const eventsToDisplay = computed(() => {
  const startIndex = (currentPage.value - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  return filteredEvents.value.slice(startIndex, endIndex);
});

const fetchEvents = async () => {
  loading.value = true
  try {
    events.value = await eventService.getAllEvents()   // 注意：你需要把 getAllEvents() 寫進 useEvents.js
    console.log('✅ 活動資料已載入', events.value)
  } catch (err) {
    console.error('❌ 無法取得活動資料:', err)
  } finally {
    loading.value = false
  }
}

const fetchMyEvents = async () => {
  try {
    await eventService.initJoinedEvents()
  } catch (err) {
    console.error('❌ getMyEvents 發生錯誤', err)
  }
}

</script>