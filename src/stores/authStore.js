// src/stores/authStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const API_URL = 'http://localhost:5000'

export const useAuthStore = defineStore('auth', () => {
  const isLoggedIn = ref(false)
  const user = ref(null)
  const token = ref('')

  function login(userData, tokenData) {
    isLoggedIn.value = true
    user.value = userData
    token.value = tokenData
    localStorage.setItem('user', JSON.stringify(userData))
    localStorage.setItem('token', tokenData)
    console.log("✅ 成功登入，Token:", tokenData)
  }

  function logout() {
    isLoggedIn.value = false
    user.value = null
    token.value = ''
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  }

  function restoreSession() {
    const storedUser = localStorage.getItem('user')
    const storedToken = localStorage.getItem('token')
    if (storedUser && storedToken) {
      user.value = JSON.parse(storedUser)
      token.value = storedToken
      isLoggedIn.value = true
    }
  }

  async function getProfile() {
    if (!token.value) return null
    try {
      const res = await axios.get(`${API_URL}/profile`, {
        headers: {
          Authorization: `Bearer ${token.value}`,
        },
      })
      return res.data
    } catch (err) {
      console.error('取得使用者資料失敗:', err)
      throw err
    }
  }

  async function joinEvent(eventId) {
    console.log("✅ 成功登入，Token:", token.value)
    try {
      const res = await axios.post(
        `${API_URL}/events/join`,
        {
          event_id: String(eventId),
          action: 'join',
        },
        {
          headers: {
            Authorization: `Bearer ${token.value}`,
            'Content-Type': 'application/json',
          },
        }
      )
      return res.data
    } catch (err) {
      console.error('加入活動錯誤:', err)
      if (err.response) {
        console.error("🔥 錯誤狀態碼:", err.response.status)
        console.error("🔥 錯誤內容:", err.response.data)
      }
      throw err
    }
  }

  return {
    isLoggedIn,
    user,
    token,
    login,
    logout,
    restoreSession,
    getProfile,
    joinEvent,
  }
})
