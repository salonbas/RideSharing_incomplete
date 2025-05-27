// views/EventListPage.vue
<template>
  <div class="min-h-screen bg-[#12150e] text-white">
    <div class="px-4 sm:px-6 md:px-12 lg:px-20 py-8">
      <div class="max-w-[85vw] mx-auto">
      <!-- 頂部區域：創建活動按鈕 -->
        <div class="flex justify-between items-center mb-6">
          <h1 class="text-4xl font-bold text-[#d1ad41]">活動列表</h1>
          <button 
            @click="navigateToCreateEvent" 
            class="bg-[#d1ad41] hover:bg-[#a08432e7] text-[#1c1e10] px-6 py-3 rounded-md transition duration-200 flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
            </svg>
            發起活動
          </button>
        </div>
        
        <!-- 篩選與排序 -->
        <!-- <EventFilterSort 
          @sort-change="handleSortChange" 
          @filter-change="handleFilterChange" 
        /> -->
        
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
        
        <div v-else class="min-h-[75vh] grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 auto-rows-fr gap-8 mt-6">
          <EventCard 
            v-for="event in eventsToDisplay" 
            :key="event.id" 
            :event-data="event"
            @show-profile="showProfile"
            @join-event="handleJoinEvent"
          />
        </div>
        
        <!-- 分頁 -->
        <div class="fixed top-1/2 right-4 -translate-y-1/2 z-50 flex flex-col items-center space-y-2">
          <PaginationBar 
            v-if="filteredEvents.length > 0"
            :total-pages="totalPages" 
            :current-page="currentPage" 
            @page-change="handlePageChange" 
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
import axios from 'axios'
import NavBar from '../components/Layout/NavBar.vue'
import EventCard from '../components/Event/EventCard.vue'
import EventFilterSort from '../components/Event/EventFilterSort.vue'
import PaginationBar from '../components/Event/PaginationBar.vue'
import ProfileBox from '../components/Profile/ProfileBox.vue'

// 路由相關
const router = useRouter();
const route = useRoute();

// 頁面狀態
const loading = ref(true);
const events = ref([]);
const sortBy = ref('date-asc');
const filterType = ref('all');
const currentPage = ref(1);
const itemsPerPage = 8;

// 個人資料浮動視窗狀態
const showProfileBox = ref(false);
const selectedOrganizer = ref(null);

// 從路由參數中獲取頁碼和篩選條件（如果有）
onMounted(() => {
  if (route.query.page) {
    currentPage.value = parseInt(route.query.page) || 1;
  }
  
  if (route.query.type) {
    filterType.value = route.query.type;
  }
  
  if (route.query.sort) {
    sortBy.value = route.query.sort;
  }
  
  fetchEvents();
});

// 監聽過濾條件的變化，重置頁碼
watch([sortBy, filterType], () => {
  currentPage.value = 1;
  updateUrlParams();
});

// 處理排序變更
const handleSortChange = (sort) => {
  sortBy.value = sort;
};

// 處理篩選變更
const handleFilterChange = (filter) => {
  filterType.value = filter;
};

// 處理分頁變更
const handlePageChange = (page) => {
  currentPage.value = page;
  updateUrlParams();
  // 滾動到頂部
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
};

const showProfile = async (userId) => {
  try {
    const res = await axios.get(`http://localhost:5000/users/${userId}`)
    selectedOrganizer.value = res.data
    showProfileBox.value = true
  } catch (err) {
    console.error('載入 organizer 資料失敗:', err)
    alert('載入個人資料失敗')
  }
}

// 處理加入活動
const auth = useAuthStore()
const handleJoinEvent = async (eventId) => {
  console.log("申請加入活動", eventId)
  console.log("token:", auth.token)

  if (!auth.isLoggedIn) {
    alert('請先登入再申請加入活動')
    return
  }

  try {
    const formattedEventId = typeof eventId === 'string' ? parseInt(eventId, 10) : eventId

    const response = await auth.joinEvent(formattedEventId)

    console.log('加入成功:', response)
    alert('成功申請加入活動')

    // 重新取得活動資料（你需自行實作 fetchEvents()）
    await fetchEvents?.()
  } catch (err) {
    console.error('加入活動錯誤:', err)

    const msg =
      err?.response?.data?.error ||
      err?.response?.data?.msg ||
      err.message ||
      '未知錯誤'

    alert(`申請失敗：${msg}`)
  }
}

// 導航到創建活動頁面
const navigateToCreateEvent = () => {
  router.push('/event/create');
};

// 更新 URL 參數
const updateUrlParams = () => {
  router.replace({
    query: {
      page: currentPage.value,
      type: filterType.value !== 'all' ? filterType.value : undefined,
      sort: sortBy.value !== 'date-asc' ? sortBy.value : undefined
    }
  });
};

// 根據篩選條件過濾事件
const filteredEvents = computed(() => {
  let result = [...events.value];
  
  if (filterType.value !== 'all') {
    result = result.filter(event => event.type === filterType.value);
  }
  
  // 排序
  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'date-asc':
        return new Date(a.datetime) - new Date(b.datetime);
      case 'date-desc':
        return new Date(b.datetime) - new Date(a.datetime);
      case 'price-asc':
        return a.price - b.price;
      case 'price-desc':
        return b.price - a.price;
      case 'spots-asc':
        return a.spotsRemaining - b.spotsRemaining;
      case 'spots-desc':
        return b.spotsRemaining - a.spotsRemaining;
      default:
        return 0;
    }
  });
  console.log('篩選後剩餘event數量:', result.length)

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
    const res = await axios.get('http://localhost:5000/events')
    events.value = res.data
  } catch (err) {
    console.error('❌ 無法取得活動資料:', err)
  } finally {
    loading.value = false
  }
  console.log('✅ 活動資料已載入', events.value)
}
</script>