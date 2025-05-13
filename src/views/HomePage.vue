<template>
  <MainLayout>
    <LogoPart/>
    <div class="px-4 py-8 max-w-6xl mx-auto">
      <h1 class="text-2xl font-bold mb-4">探索最熱門的影片 🎥</h1>
      <p class="mb-8 text-gray-600">這裡是展示你最愛內容的地方，快來找看看有什麼好看的影片吧！</p>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <VideoCard :videoData="videoDataList[0]" />
        <VideoCard :videoData="videoDataList[1]" />
      </div>
    </div>
    <Footer />
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/components/Layout/MainLayout.vue'
import Footer from '@/components/Layout/Footer.vue'
import VideoCard from '@/components/Video/VideoCard.vue'
import LogoPart from '../components/Layout/LogoPart.vue'

const videoDataList = [
  {
    title: '歡迎使用揪揪GO',
    thumbnail: 'https://via.placeholder.com/640x360.png?text=Video+1',
    url: 'https://www.w3schools.com/html/mov_bbb.mp4'
  },
  {
    title: '功能快速導覽',
    thumbnail: 'https://via.placeholder.com/640x360.png?text=Video+2',
    url: 'https://www.w3schools.com/html/movie.mp4'
  }
];
</script>
