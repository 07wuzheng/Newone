import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL || '/api' })

export const useToolStore = defineStore('tool', () => {
  const featured = ref([])
  const currentTool = ref(null)
  const searchResults = ref([])
  const editorPicks = ref([])
  const stats = ref(null)
  const loading = ref(false)
  const submitting = ref(false)
  const error = ref(null)

  async function fetchFeatured() {
    loading.value = true
    error.value = null
    try {
      const res = await api.get('/tools/featured')
      featured.value = res.data.data
    } catch (err) {
      error.value = err.response?.data?.detail || '加载推荐工具失败，请检查网络连接'
    } finally {
      loading.value = false
    }
  }

  async function fetchTool(id) {
    loading.value = true
    currentTool.value = null
    error.value = null
    try {
      const res = await api.get(`/tools/${id}`)
      currentTool.value = res.data.data
    } catch (err) {
      if (err.response?.status === 404) {
        error.value = null
      } else {
        error.value = err.response?.data?.detail || '加载工具详情失败，请检查网络连接'
      }
    } finally {
      loading.value = false
    }
  }

  async function searchTools(query, extraParams = {}) {
    if (!query.trim()) {
      searchResults.value = []
      return
    }
    loading.value = true
    error.value = null
    try {
      const params = { q: query, ...extraParams }
      const res = await api.get('/tools/search', { params })
      searchResults.value = res.data.data
    } catch (err) {
      error.value = err.response?.data?.detail || '搜索失败，请检查网络连接'
    } finally {
      loading.value = false
    }
  }

  async function fetchTools(params = {}) {
    loading.value = true
    error.value = null
    searchResults.value = []
    try {
      const res = await api.get('/tools', { params })
      searchResults.value = res.data.data
    } catch (err) {
      error.value = err.response?.data?.detail || '加载工具列表失败'
    } finally {
      loading.value = false
    }
  }

  async function fetchStats() {
    try {
      const res = await api.get('/tools/stats')
      stats.value = res.data.data
    } catch (err) {
      // stats 加载失败不影响页面
      console.warn('stats fetch failed', err)
    }
  }

  async function fetchEditorPicks() {
    try {
      const res = await api.get('/tools/editor-picks')
      editorPicks.value = res.data.data
    } catch (err) {
      console.warn('editor-picks fetch failed', err)
    }
  }

  // 一次性加载首页所需全部数据（合并原 categories/featured/editor-picks/stats 4 请求）
  async function fetchHomeInit() {
    loading.value = true
    error.value = null
    try {
      const res = await api.get('/home-init')
      const data = res.data.data
      featured.value = data.featured
      editorPicks.value = data.editor_picks
      stats.value = data.stats
      return data.categories
    } catch (err) {
      error.value = err.response?.data?.detail || '加载失败，请检查网络连接'
      return null
    } finally {
      loading.value = false
    }
  }

  async function submitTool(formData) {
    submitting.value = true
    error.value = null
    try {
      const res = await api.post('/tools/submit', formData)
      return res.data
    } catch (err) {
      const detail = err.response?.data?.detail
      if (Array.isArray(detail)) {
        const fieldErrors = {}
        detail.forEach(d => { fieldErrors[d.field] = d.message })
        throw fieldErrors
      }
      throw new Error(typeof detail === 'string' ? detail : '提交失败，请检查网络连接')
    } finally {
      submitting.value = false
    }
  }

  return { featured, currentTool, searchResults, editorPicks, stats, loading, submitting, error, fetchFeatured, fetchTool, searchTools, fetchTools, fetchStats, fetchEditorPicks, fetchHomeInit, submitTool }
})
