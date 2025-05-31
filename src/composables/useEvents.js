// src/composables/useEvents.js

import { ref, computed } from 'vue'
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const API_URL = 'http://localhost:5000'

export const useEventService = () => {
  const auth = useAuthStore()
  const token = computed(() => auth.token)
  const isLoggedIn = computed(() => auth.isLoggedIn)
  const logout = auth.logout

  const joinedEventIds = ref([])
  const loading = ref(false)

  // 初始化已參加的活動
  const initJoinedEvents = async () => {
    if (!isLoggedIn.value) return

    try {
      const res = await axios.get(`${API_URL}/events/joined`, {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      })
      joinedEventIds.value = res.data.joinedEventIds || []
    } catch (err) {
      console.error('載入參加活動列表失敗:', err)
    }
  }

  async function getAllEvents() {
    try {
      const res = await axios.get(`${API_URL}/events`)
      return res.data
    } catch (err) {
      console.error('❌ 無法取得活動資料:', err)
      //handleApiError(err)
      throw err
    }
  }
  // 加入活動
  const joinEvent = async (eventId) => {
    console.log("準備加入活動，Token:", token.value)
    if (!isLoggedIn.value) {
      throw new Error('請先登入再申請加入活動')
    }

    loading.value = true
    try {
      const formattedEventId = parseInt(eventId, 10)

      const res = await axios.post(
        `${API_URL}/events/action`,
        { event_id: formattedEventId, action: 'join' },
        {
          headers: { Authorization: `Bearer ${token.value}`, 'Content-Type': 'application/json' },
        }
      )

      if (res.data.hasJoined) {
        joinedEventIds.value.push(formattedEventId)
      }

      return res.data
    } catch (err) {
      console.error('加入活動錯誤:', err)
      if (err.response?.status === 401) {
        logout()
        alert("請重新登入")
      }
      auth.handleApiError?.(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 退出活動
  const leaveEvent = async (eventId) => {
    console.log("退出活動", eventId)
    if (!isLoggedIn.value) {
      throw new Error('請先登入')
    }

    loading.value = true
    try {
      const formattedEventId = parseInt(eventId, 10)

      const res = await axios.post(
        `${API_URL}/events/action`,
        { event_id: formattedEventId, action: 'cancel' },
        {
          headers: { Authorization: `Bearer ${token.value}`, 'Content-Type': 'application/json' },
        }
      )

      if (!res.data.hasJoined) {
        const index = joinedEventIds.value.indexOf(formattedEventId)
        if (index > -1) joinedEventIds.value.splice(index, 1)
      }

      return res.data
    } catch (err) {
      console.error('退出活動錯誤:', err)
      if (err.response?.status === 401) {
        logout()
        alert("請重新登入")
      }
      auth.handleApiError?.(err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 取消活動
  const cancelEvent = async (eventId) => {
    console.log("取消活動", eventId)
    if (!isLoggedIn.value) {
      throw new Error('請先登入')
    }

    try {
      const formattedEventId = parseInt(eventId, 10)
      const res = await axios.post(
        `${API_URL}/events/action`,
        { event_id: formattedEventId, action: 'delete' },
        {
          headers: { Authorization: `Bearer ${token.value}`, 'Content-Type': 'application/json' },
        }
      )
      return res.data
    } catch (err) {
      console.error('取消活動錯誤:', err)
      if (err.response?.status === 401) {
        logout()
        alert("請重新登入")
      }
      auth.handleApiError?.(err)
      throw err
    }
  }

  // 創建活動
  const createEvent = async (eventData) => {
    if (!token.value) throw new Error('未登入')
    try {
      const res = await axios.post(`${API_URL}/events/create`, eventData, {
        headers: {
          Authorization: `Bearer ${token.value}`,
          'Content-Type': 'application/json',
        },
      })
      return res.data
    } catch (err) {
      console.error('創建活動失敗:', err)
      auth.handleApiError?.(err)
      if (err.response?.status === 401) {
        logout()
        alert("請重新登入")
      }
      throw err
    }
  }

  const hasJoinedEvent = (eventId) => {
    return joinedEventIds.value.includes(parseInt(eventId, 10))
  }

  return {
    joinedEventIds: computed(() => joinedEventIds.value),
    loading: computed(() => loading.value),
    initJoinedEvents,
    getAllEvents,
    joinEvent,
    leaveEvent,
    cancelEvent,
    createEvent,
    hasJoinedEvent
  }
}
