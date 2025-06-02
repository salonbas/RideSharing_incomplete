<script setup>
import Navbar from '@/components/Layout/Navbar.vue';
import { RouterView } from 'vue-router';
import { useAuthStore } from '@/stores/authStore'

const auth = useAuthStore()
auth.restoreSession()
</script>

<template>
  <Navbar />
  <RouterView />
</template>

