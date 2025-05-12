<template>
  <div class="rounded-xl overflow-hidden shadow-md transition transform hover:scale-105 bg-white">
    <router-link :to="`/video/${videoData.id}`">
      <img :src="videoData.thumbnail" alt="Thumbnail" class="w-full h-48 object-cover" />
    </router-link>
    <div class="p-4">
      <div class="flex items-center space-x-3 mb-2">
        <img
          :src="videoData.uploaderAvatar"
          alt="Uploader"
          class="w-8 h-8 rounded-full cursor-pointer"
          @click.stop="toggleProfile"
        />
        <span class="text-sm text-gray-600">{{ videoData.uploadDate }}</span>
      </div>
      <h3 class="text-lg font-semibold">{{ videoData.title }}</h3>
      <p class="text-sm text-gray-700 line-clamp-2">{{ videoData.description }}</p>
      <div class="flex items-center text-sm text-gray-500 mt-2 space-x-4">
        <div class="flex items-center space-x-1">
          <i class="i-lucide-heart" /> <span>{{ videoData.likes }}</span>
        </div>
        <div class="flex items-center space-x-1">
          <i class="i-lucide-eye" /> <span>{{ videoData.views }}</span> 
        </div>
      </div>
    </div>

    <ProfileBox v-if="showProfile" @close="showProfile = false" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { defineProps } from 'vue'
import ProfileBox from '@/components/Profile/ProfileBox.vue'

const props = defineProps({
  videoData: Object
})

const showProfile = ref(false)
const toggleProfile = () => {
  showProfile.value = !showProfile.value
}
</script>
