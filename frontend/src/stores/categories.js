import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api' })

export const useCategoryStore = defineStore('category', () => {
  const categories = ref([])
  const currentCategory = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function fetchCategories() {
    if (loading.value) return
    loading.value = true
    error.value = null
    try {
      const res = await api.get('/categories')
      categories.value = res.data.data
    } catch (err) {
      error.value = err.response?.data?.detail || '加载分类失败，请检查网络连接'
    } finally {
      loading.value = false
    }
  }

  async function fetchCategoryBySlug(slug) {
    loading.value = true
    currentCategory.value = null
    error.value = null
    try {
      const res = await api.get(`/categories/${slug}`)
      currentCategory.value = res.data.data
    } catch (err) {
      if (err.response?.status === 404) {
        error.value = null // 404 由页面展示"分类不存在"来处理
      } else {
        error.value = err.response?.data?.detail || '加载分类失败，请检查网络连接'
      }
    } finally {
      loading.value = false
    }
  }

  return { categories, currentCategory, loading, error, fetchCategories, fetchCategoryBySlug }
})
