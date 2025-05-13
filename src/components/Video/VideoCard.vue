<template>
  <div class="rounded-xl overflow-hidden shadow-md bg-white p-4">
    <h3 class="text-lg font-semibold mb-2">{{ videoData.title }}</h3>
    <video
      class="w-full rounded-md"
      controls
      :poster="videoData.thumbnail"
    >
      <source :src="videoData.url" type="video/mp4" />
      您的瀏覽器不支援影片播放。
    </video>
  </div>
</template>

<script setup>
defineProps({
  videoData: {
    type: Object,
    required: true
  }
});
</script>
