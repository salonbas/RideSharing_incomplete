// src/stores/authStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const API_URL = 'https://ridesharingbackend-production.up.railway.app'
//const API_URL = 'http://localhost:5000'

export function handleApiError(err, { toast = null, autoLogout = true, redirect = '/' } = {}) {
  const status = err.response?.status

  switch (status) {
    case 400:
      if (toast) toast.error(err.response.data?.msg || '請求格式錯誤')
      break
    case 401:
      console.warn('登入已過期，請重新登入')
      if (toast) toast.error('登入已過期，請重新登入')
      const auth = useAuthStore()
      if (autoLogout) {
        auth.logout()
        if (redirect) window.location.href = redirect
      }
      break
    case 403:
      if (toast) toast.error('權限不足，無法執行此操作')
      break
    case 404:
      if (toast) toast.error('資源不存在')
      break
    case 500:
      if (toast) toast.error('伺服器錯誤，請稍後再試')
      break
    default:
      if (toast) toast.error('發生未知錯誤')
  }

  console.error('❌ 錯誤細節:', err)
}

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
    console.log("成功登入，Token:", tokenData)
  }

  function logout() {
    console.log("logout has been trigger")
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

  // 註冊新使用者
  async function register(userData) {
    try {
      const res = await axios.post(`${API_URL}/register`, userData)
      return res.data
    } catch (err) {
      console.error('註冊失敗:', err)
      handleApiError(err)
      throw err
    }
  }

  // 登入使用者
  async function loginUser(credentials) {
    try {
      const res = await axios.post(`${API_URL}/login`, credentials)
      const { token: tokenData, user: userData } = res.data
      login(userData, tokenData)
      return res.data
    } catch (err) {
      console.error('登入失敗:', err)
      handleApiError(err)
      throw err
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
      handleApiError(err)
      if (err.response?.status === 401) {
        logout()
      }
      throw err
    }
  }

  // 更新個人資料
  async function updateProfile(profileData) {
    if (!token.value) throw new Error('未登入')
    try {
      const res = await axios.post(`${API_URL}/profile/update`, profileData, {
        headers: {
          Authorization: `Bearer ${token.value}`,
          'Content-Type': 'application/json',
        },
      })
      if (res.data.user) {
        user.value = res.data.user
        localStorage.setItem('user', JSON.stringify(res.data.user))
      }
      return res.data
    } catch (err) {
      console.error('更新個人資料失敗:', err)
      handleApiError(err)
      if (err.response?.status === 401) {
        logout()
      }
      throw err
    }
  }

  // 更新頭像
  async function updateAvatar(avatarFile) {
    if (!token.value) throw new Error('未登入')
    try {
      const formData = new FormData()
      formData.append('avatar', avatarFile)
      
      const res = await axios.post(`${API_URL}/profile/avatar`, formData, {
        headers: {
          Authorization: `Bearer ${token.value}`,
          'Content-Type': 'multipart/form-data',
        },
      })
      
      if (res.data.avatarUrl && user.value) {
        user.value.avatarUrl = res.data.avatarUrl
        localStorage.setItem('user', JSON.stringify(user.value))
      }
      
      return res.data
    } catch (err) {
      console.error('更新頭像失敗:', err)
      handleApiError(err)
      if (err.response?.status === 401) {
        logout()
      }
      throw err
    }
  }

  // 取得其他使用者的公開資料
  async function getPublicUser(userId) {
    try {
      const res = await axios.get(`${API_URL}/users/${userId}`)
      return res.data
    } catch (err) {
      console.error('取得使用者資料失敗:', err)
      handleApiError(err)
      throw err
    }
  }

  // 取得所有活動
  async function getAllEvents() {
    try {
      const res = await axios.get(`${API_URL}/events`)
      return res.data
    } catch (err) {
      console.error('❌ 無法取得活動資料:', err)
      handleApiError(err)
      throw err
    }
  }

  // 取得自己參加或主辦的活動
  async function getMyEvents() {
    if (!token.value) throw new Error('未登入')
    try {
      const res = await axios.get(`${API_URL}/events/myevents`, {
        headers: {
          Authorization: `Bearer ${token.value}`,
          'Content-Type': 'application/json'
        }
      })
      return res.data
    } catch (err) {
      console.error('取得自己活動失敗:', err)
      handleApiError(err)
      if (err.response?.status === 401) {
        logout()
      }
      throw err
    }
  }

  // 加入活動
  async function joinEvent(eventId) {
    console.log("準備加入活動，Token:", token.value)
    if (!isLoggedIn.value) {
      throw new Error('請先登入再申請加入活動')
    }

    try {
      const formattedEventId = typeof eventId === 'string' ? parseInt(eventId, 10) : eventId
      
      const res = await axios.post(
        `${API_URL}/events/action`,
        {
          event_id: formattedEventId,
          action: 'join',
        },
        {
          headers: {
            Authorization: `Bearer ${token.value}`,
            'Content-Type': 'application/json',
          },
        }
      )
      console.log('加入成功:', res.data)
      return res.data
    } catch (err) {
      console.error('加入活動錯誤:', err)
      if (err.response?.status === 401) {
        logout()
      }
      handleApiError(err)
      throw err
    }
  }

  // 取消參加活動
  async function leaveEvent(eventId) {
    console.log("退出活動", eventId)
    if (!isLoggedIn.value) {
      throw new Error('請先登入')
    }

    try {
      const formattedEventId = typeof eventId === 'string' ? parseInt(eventId, 10) : eventId

      const res = await axios.post(
        `${API_URL}/events/action`,
        {
          event_id: formattedEventId,
          action: 'cancel',
        },
        {
          headers: {
            Authorization: `Bearer ${token.value}`,
            'Content-Type': 'application/json',
          },
        }
      )
      console.log('退出成功:', res.data)
      return res.data
    } catch (err) {
      console.error('退出活動錯誤:', err)
      if (err.response?.status === 401) {
        logout()
      }
      handleApiError(err)
      throw err
    }
  }

  async function cancelEvent(eventId) {
    console.log("取消活動", eventId)
    if (!isLoggedIn.value) {
      throw new Error('請先登入')
    }

    try {
      const formattedEventId = typeof eventId === 'string' ? parseInt(eventId, 10) : eventId

      const res = await axios.post(
        `${API_URL}/events/action`,
        {
          event_id: formattedEventId,
          action: 'delete',
        },
        {
          headers: {
            Authorization: `Bearer ${token.value}`,
            'Content-Type': 'application/json',
          },
        }
      )
      console.log('取消活動成功:', res.data)
      return res.data
    } catch (err) {
      console.error('取消活動錯誤:', err)
      if (err.response?.status === 401) {
        logout()
      }
      handleApiError(err)
      throw err
    }
  }

  // 創建新活動
  async function createEvent(eventData) {
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
      handleApiError(err)
      if (err.response?.status === 401) {
        logout()
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
    register,
    loginUser,
    getProfile,
    updateProfile,
    updateAvatar,
    getPublicUser,
    getAllEvents,
    getMyEvents,
    joinEvent,
    leaveEvent,
    cancelEvent,
    createEvent,
  }
})