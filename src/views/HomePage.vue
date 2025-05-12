<template>
  <MainLayout>
    <NavBar />
    <div class="px-4 py-8 max-w-6xl mx-auto">
      <h1 class="text-2xl font-bold mb-4">探索最熱門的影片 🎥</h1>
      <p class="mb-8 text-gray-600">這裡是展示你最愛內容的地方，快來找看看有什麼好看的影片吧！</p>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <VideoCard
          v-for="video in paginatedVideos"
          :key="video.id"
          :videoData="video"
        />
      </div>

      <div class="flex justify-center mt-8 space-x-4">
        <button
          class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded"
          @click="prevPage"
          :disabled="currentPage === 1"
        >
          上一頁
        </button>
        <button
          class="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded"
          @click="nextPage"
          :disabled="endIndex >= videoDataList.length"
        >
          下一頁
        </button>
      </div>
    </div>
    <Footer />
  </MainLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import MainLayout from '@/components/Layout/MainLayout.vue'
import NavBar from '@/components/Layout/NavBar.vue'
import Footer from '@/components/Layout/Footer.vue'
import VideoCard from '@/components/Video/VideoCard.vue'

const videoDataList = ref(
  Array.from({ length: 15 }).map((_, i) => ({
    id: i + 1,
    title: `示範影片標題 #${i + 1}`,
    thumbnail: `https://placehold.co/400x225?text=Thumbnail+${i + 1}`,
    description: '這是一段示範影片的簡短說明文字，內容精彩豐富。',
    uploaderAvatar: `https://i.pravatar.cc/150?img=${i + 1}`,
    uploadDate: '2024-01-01',
    likes: Math.floor(Math.random() * 1000),
    views: Math.floor(Math.random() * 10000),
  }))
)

const currentPage = ref(1)
const pageSize = 6

const startIndex = computed(() => (currentPage.value - 1) * pageSize)
const endIndex = computed(() => currentPage.value * pageSize)
const paginatedVideos = computed(() =>
  videoDataList.value.slice(startIndex.value, endIndex.value)
)

const prevPage = () => currentPage.value--
const nextPage = () => currentPage.value++
</script>
