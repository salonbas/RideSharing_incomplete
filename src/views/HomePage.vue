<template>
  <MainLayout>
    <FadeIn>
      <h1 class="text-3xl font-bold">垂直淡入動畫</h1>
    </FadeIn>

    <SlideIn>
      <p class="text-lg">側向滑入</p>
    </SlideIn>
    <LogoPart/>


    <!-- 增加上方空間讓你 scroll 看動畫 -->
<div class="h-[100vh] flex items-center justify-center bg-gray-100">
  <p class="text-xl">請向下滑看看動畫效果</p>
</div>
<div class="parallax-demo">
    <Parallax
      :verticalSpeed="0.2"
      :horizontalSpeed="0.1"
      :height="300"
      :maxOffset="150"
      :useInertia="true"
      :inertiaFriction="0.08"
      direction="both"
      @enter-view="handleEnterView"
      @exceed-threshold="handleExceedThreshold"
    >
      <div class="parallax-content bg-red-500">
        <h2>視差效果展示</h2>
        <p>試著滾動頁面和移動滑鼠來體驗效果</p>
      </div>
    </Parallax>
    
    <!-- 多層視差效果 -->
    <Parallax
      :verticalSpeed="0.4"
      :depthLevel="2"
      :height="200"
    >
      <div class="parallax-layer-2">第二層（速度更快）</div>
    </Parallax>
  </div>

<!-- 下方空間避免卡住滾動 -->
<div class="h-[100vh] bg-gray-50"></div>



    <div class="px-4 py-8 max-w-6xl mx-auto bg-orange-500">
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
import FadeIn from '@/components/Animation/FadeIn.vue'
import SlideIn from '@/components/Animation/SlideIn.vue'
import Parallax from '@/components/Animation/Parallax.vue'

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
