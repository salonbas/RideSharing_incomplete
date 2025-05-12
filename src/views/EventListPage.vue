// views/EventListPage.vue
<template>
  <div class="bg-gray-50 min-h-screen">
    <!-- 導航列 -->
    <NavBar />
    
    <div class="container mx-auto px-4 py-6">
      <!-- 頂部區域：創建活動按鈕 -->
      <div class="flex justify-between items-center mb-6">
        <h1 class="text-2xl font-bold text-gray-800">活動列表</h1>
        <button 
          @click="navigateToCreateEvent" 
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md transition duration-200 flex items-center"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          發起活動
        </button>
      </div>
      
      <!-- 篩選與排序 -->
      <EventFilterSort 
        @sort-change="handleSortChange" 
        @filter-change="handleFilterChange" 
      />
      
      <!-- 活動列表 -->
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500 mx-auto"></div>
        <p class="mt-2 text-gray-600">載入中...</p>
      </div>
      
      <div v-else-if="filteredEvents.length === 0" class="text-center py-12">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="mt-4 text-lg text-gray-600">沒有找到符合條件的活動</p>
      </div>
      
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
        <EventCard 
          v-for="event in eventsToDisplay" 
          :key="event.id" 
          :event-data="event"
          @show-profile="showProfile"
          @join-event="handleJoinEvent"
        />
      </div>
      
      <!-- 分頁 -->
      <PaginationBar 
        v-if="filteredEvents.length > 0"
        :total-pages="totalPages" 
        :current-page="currentPage" 
        @page-change="handlePageChange" 
        class="mt-8"
      />
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
            :is-self="false"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import NavBar from '../components/Layout/NavBar.vue';
import EventCard from '../components/Event/EventCard.vue';
import EventFilterSort from '../components/Event/EventFilterSort.vue';
import PaginationBar from '../components/Event/PaginationBar.vue';
import ProfileBox from '../components/Profile/ProfileBox.vue';

// 路由相關
const router = useRouter();
const route = useRoute();

// 頁面狀態
const loading = ref(true);
const events = ref([]);
const sortBy = ref('date-asc');
const filterType = ref('all');
const currentPage = ref(1);
const itemsPerPage = 9;

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
  
  // 模擬 API 載入
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

// 顯示個人資料
const showProfile = (organizer) => {
  selectedOrganizer.value = organizer;
  showProfileBox.value = true;
};

// 處理加入活動
const handleJoinEvent = (eventId) => {
  const isLoggedIn = true; // 假設已登入
  
  if (!isLoggedIn) {
    alert('請先登入再申請加入活動');
    return;
  }
  
  alert(`已申請加入活動 ID: ${eventId}`);
  // 在實際應用程式中這裡會呼叫 API
};

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

// 模擬 API 載入資料
const fetchEvents = () => {
  // 假資料
  setTimeout(() => {
    events.value = [
      {
        id: 1,
        type: 'carpool',
        title: '台北到花蓮共乘',
        location: '台北市',
        datetime: '2025-05-15T08:30:00',
        price: 350,
        spotsRemaining: 3,
        organizer: {
          id: 101,
          avatar: 'https://i.pravatar.cc/150?img=1',
          nickname: '阿德',
          account: 'driver_dave',
          instagram: '@dave_taipei',
          phoneNumber: '0912-345-678'
        }
      },
      {
        id: 2,
        type: 'drink',
        title: '週五微醺夜',
        location: '台北市',
        datetime: '2025-05-17T20:00:00',
        price: 500,
        spotsRemaining: 5,
        organizer: {
          id: 102,
          avatar: 'https://i.pravatar.cc/150?img=2',
          nickname: '小美',
          account: 'party_mei',
          instagram: '@mei_party',
          phoneNumber: '0923-456-789'
        }
      },
      {
        id: 3,
        type: 'sports',
        title: '籃球三對三',
        location: '新北市',
        datetime: '2025-05-14T18:00:00',
        price: 150,
        spotsRemaining: 1,
        organizer: {
          id: 103,
          avatar: 'https://i.pravatar.cc/150?img=3',
          nickname: '小偉',
          account: 'basketball_wei',
          instagram: '@wei_bball',
          phoneNumber: '0934-567-890'
        }
      },
      {
        id: 4,
        type: 'sports',
        title: '羽球友誼賽',
        location: '台中市',
        datetime: '2025-05-20T19:30:00',
        price: 200,
        spotsRemaining: 7,
        organizer: {
          id: 104,
          avatar: 'https://i.pravatar.cc/150?img=4',
          nickname: '小芳',
          account: 'badminton_fang',
          instagram: '@fang_sports',
          phoneNumber: '0945-678-901'
        }
      },
      {
        id: 5,
        type: 'carpool',
        title: '高雄到墾丁共乘',
        location: '高雄市',
        datetime: '2025-05-22T07:00:00',
        price: 250,
        spotsRemaining: 2,
        organizer: {
          id: 105,
          avatar: 'https://i.pravatar.cc/150?img=5',
          nickname: '阿明',
          account: 'drive_ming',
          instagram: '@ming_driver',
          phoneNumber: '0956-789-012'
        }
      },
      {
        id: 6,
        type: 'drink',
        title: '調酒品嚐會',
        location: '台南市',
        datetime: '2025-05-18T19:00:00',
        price: 650,
        spotsRemaining: 8,
        organizer: {
          id: 106,
          avatar: 'https://i.pravatar.cc/150?img=6',
          nickname: '小婷',
          account: 'cocktail_ting',
          instagram: '@ting_drinks',
          phoneNumber: '0967-890-123'
        }
      },
      {
        id: 7,
        type: 'sports',
        title: '晨跑團',
        location: '台北市',
        datetime: '2025-05-16T06:00:00',
        price: 0,
        spotsRemaining: 15,
        organizer: {
          id: 107,
          avatar: 'https://i.pravatar.cc/150?img=7',
          nickname: '教練',
          account: 'morning_runner',
          instagram: '@taipei_runners',
          phoneNumber: '0978-901-234'
        }
      },
      {
        id: 8,
        type: 'carpool',
        title: '台中到南投共乘',
        location: '台中市',
        datetime: '2025-05-19T09:30:00',
        price: 180,
        spotsRemaining: 1,
        organizer: {
          id: 108,
          avatar: 'https://i.pravatar.cc/150?img=8',
          nickname: '小強',
          account: 'driver_strong',
          instagram: '@strong_driver',
          phoneNumber: '0989-012-345'
        }
      },
      {
        id: 9,
        type: 'drink',
        title: '精釀啤酒品嚐',
        location: '新北市',
        datetime: '2025-05-21T18:30:00',
        price: 450,
        spotsRemaining: 4,
        organizer: {
          id: 109,
          avatar: 'https://i.pravatar.cc/150?img=9',
          nickname: '小軒',
          account: 'beer_xuan',
          instagram: '@xuan_beers',
          phoneNumber: '0990-123-456'
        }
      },
      {
        id: 10,
        type: 'sports',
        title: '瑜珈課程',
        location: '台北市',
        datetime: '2025-05-23T10:00:00',
        price: 300,
        spotsRemaining: 6,
        organizer: {
          id: 110,
          avatar: 'https://i.pravatar.cc/150?img=10',
          nickname: '瑜老師',
          account: 'yoga_teacher',
          instagram: '@yoga_taipei',
          phoneNumber: '0901-234-567'
        }
      },
      {
        id: 11,
        type: 'drink',
        title: '紅酒品嚐會',
        location: '台北市',
        datetime: '2025-05-25T19:00:00',
        price: 750,
        spotsRemaining: 9,
        organizer: {
          id: 111,
          avatar: 'https://i.pravatar.cc/150?img=11',
          nickname: '小紅',
          account: 'wine_hong',
          instagram: '@hong_wines',
          phoneNumber: '0912-345-678'
        }
      },
      {
        id: 12,
        type: 'carpool',
        title: '台北到宜蘭共乘',
        location: '台北市',
        datetime: '2025-05-26T14:00:00',
        price: 200,
        spotsRemaining: 2,
        organizer: {
          id: 112,
          avatar: 'https://i.pravatar.cc/150?img=12',
          nickname: '小李',
          account: 'driver_li',
          instagram: '@li_driver',
          phoneNumber: '0923-456-789'
        }
      }
    ];
    loading.value = false;
  }, 800); // 模擬載入延遲
};
</script>
