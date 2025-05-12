// ProfileBox.vue
<template>
  <div class="bg-white rounded-lg shadow-md p-6 max-w-lg mx-auto">
    <!-- 個人資料卡片標題 -->
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-xl font-semibold text-gray-800">個人資料</h2>
      <div v-if="isSelf">
        <button 
          @click="navigateToChangePassword" 
          class="text-sm px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition mr-2"
        >
          更改密碼
        </button>
      </div>
    </div>

    <div class="flex flex-col md:flex-row gap-6">
      <!-- 大頭照區域 -->
      <div class="flex-shrink-0">
        <ProfileAvatar 
          :avatar="user.avatar" 
          :editable="isSelf" 
          @edit="handleEditAvatar" 
        />
      </div>

      <!-- 資料欄位區域 -->
      <div class="flex-grow space-y-4">
        <ProfileField 
          label="暱稱" 
          :value="user.nickname" 
          :editable="isSelf"
          @edit="handleEdit('nickname')" 
        />
        
        <ProfileField 
          label="帳號" 
          :value="user.account" 
          :editable="isSelf"
          @edit="handleEdit('account')" 
        />
        
        <ProfileField 
          label="Instagram" 
          :value="user.instagram" 
          :editable="isSelf"
          @edit="handleEdit('instagram')" 
        />
        
        <ProfilePhone 
          :phone-number="user.phoneNumber" 
          :editable="isSelf"
          @edit="handleEdit('phoneNumber')" 
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import ProfileAvatar from './ProfileAvatar.vue';
import ProfileField from './ProfileField.vue';
import ProfilePhone from './ProfilePhone.vue';

// 定義 props
const props = defineProps({
  user: {
    type: Object,
    required: true,
    default: () => ({
      avatar: '',
      nickname: '',
      account: '',
      instagram: '',
      phoneNumber: ''
    })
  },
  isSelf: {
    type: Boolean,
    default: false
  }
});

// 定義 emit 事件
const emit = defineEmits(['update:user']);

// 路由導航
const router = useRouter();

// 處理更改密碼
const navigateToChangePassword = () => {
  router.push('/change-password');
};

// 處理編輯事件
const handleEdit = (field) => {
  // 這裡通常會打開編輯對話框或進入編輯模式
  // 但在此範例中我們只發出事件，通知父元件有編輯請求
  emit('edit', { field });
};

// 處理頭像編輯
const handleEditAvatar = () => {
  emit('edit', { field: 'avatar' });
};
</script>

