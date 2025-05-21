<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <h1 class="text-2xl font-bold mb-4">我參加的活動</h1>

    <div v-if="loading" class="text-center text-gray-500">載入中...</div>

    <div v-else-if="joinedEvents.length === 0" class="text-center text-gray-400">
      你尚未參加任何活動
    </div>

    <div v-else class="space-y-4">
      <EventCard
        v-for="event in joinedEvents"
        :key="event.id"
        :event-data="event"
        @show-profile="handleShowProfile"
        @join-event="() => {}"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import axios from 'axios'
import EventCard from '@/components/Event/EventCard.vue'

const auth = useAuthStore()
const joinedEvents = ref([])
const loading = ref(true)

const fetchJoinedEvents = async () => {
  try {
    const res = await axios.get('http://localhost:5000/events')
    joinedEvents.value = res.data.filter(e => auth.joinedEventIds.includes(e.id))
  } catch (err) {
    console.error('❌ 載入活動失敗', err)
  } finally {
    loading.value = false
  }
}

const handleShowProfile = (userId) => {
  console.log('顯示主辦人資料：', userId)
}

onMounted(() => {
  fetchJoinedEvents()
})
</script>
