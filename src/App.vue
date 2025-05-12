<script setup>
import Navbar from '@/components/Layout/Navbar.vue';
import { RouterView } from 'vue-router';
</script>

<template>
  <div class="p-10">
    <div class="bg-red-600 text-white text-2xl rounded shadow p-6">
      Tailwind 有成功載入！
    </div>
    <div class="bg-gray-500 text-white shadow rounded p-4">
      如果這是灰白字＋陰影＋圓角=>Tailwind 有成功載入！
    </div>

  </div>  
  <Navbar />
  <RouterView />
</template>

