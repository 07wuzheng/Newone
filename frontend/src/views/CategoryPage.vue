<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <!-- 网络错误 -->
    <div v-if="store.error" class="mb-8 bg-red-50/80 backdrop-blur-sm border border-red-200/60 rounded-[var(--radius-md)] px-5 py-3 flex items-center justify-between">
      <p class="text-red-700 text-sm">{{ store.error }}</p>
      <button @click="loadCategory" class="text-sm font-medium text-red-600 hover:text-red-800 underline shrink-0 ml-4">重试</button>
    </div>

    <!-- 加载态 -->
    <div v-else-if="store.loading && !store.currentCategory" class="space-y-6">
      <div class="h-8 skeleton rounded w-1/3"></div>
      <div class="h-4 skeleton rounded w-2/3"></div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-8">
        <div v-for="i in 6" :key="i" class="card-white bg-white rounded-[var(--radius-md)] overflow-hidden">
          <div class="aspect-[4/3] skeleton"></div>
          <div class="p-5 space-y-3">
            <div class="h-5 skeleton rounded w-1/2"></div>
            <div class="h-4 skeleton rounded w-full"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分类不存在 -->
    <div v-else-if="!store.currentCategory && !store.loading" class="text-center py-24">
      <p class="text-[var(--text-tertiary)] text-lg mb-4">分类不存在</p>
      <RouterLink to="/" class="text-[var(--brand)] hover:underline font-medium">返回首页</RouterLink>
    </div>

    <!-- 正常内容 -->
    <template v-else-if="store.currentCategory">
      <!-- 面包屑 -->
      <div class="flex items-center gap-2 text-sm text-[var(--text-tertiary)] mb-8">
        <RouterLink to="/" class="hover:text-[var(--brand)] transition-colors">首页</RouterLink>
        <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        <span class="text-[var(--text-secondary)] font-medium">{{ store.currentCategory.name }}</span>
      </div>

      <!-- 分类头 -->
      <div class="flex items-start gap-4 sm:gap-5 mb-8 sm:mb-10">
        <div class="w-12 h-12 sm:w-16 sm:h-16 rounded-[var(--radius-md)] flex items-center justify-center text-xl sm:text-2xl shadow-sm shrink-0" :class="iconBgClass">
          {{ iconMap[store.currentCategory.icon] || '🧩' }}
        </div>
        <div>
          <h1 class="text-2xl sm:text-4xl font-bold tracking-tight text-[var(--text-primary)]">{{ store.currentCategory.name }}</h1>
          <p class="text-sm sm:text-base text-[var(--text-secondary)] mt-1.5 sm:mt-2 leading-relaxed">{{ store.currentCategory.description }}</p>
          <p class="text-xs text-[var(--text-tertiary)] mt-1.5 sm:mt-2">{{ store.currentCategory.tools.length }} 个工具</p>
        </div>
      </div>

      <!-- 工具列表 -->
      <div v-if="store.currentCategory.tools.length === 0" class="text-center py-16 text-[var(--text-tertiary)]">
        该分类下暂无工具
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <div v-for="(tool, i) in store.currentCategory.tools" :key="tool.id" :class="`stagger-${i + 1}`">
          <ToolCard :tool="tool" />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useCategoryStore } from '../stores/categories'
import ToolCard from '../components/ToolCard.vue'

const route = useRoute()
const store = useCategoryStore()

const iconMap = {
  chat: '💬', image: '🎨', video: '🎬',
  code: '💻', music: '🎵', grid: '🧩',
}

const iconBgMap = {
  chat: 'bg-indigo-100',
  image: 'bg-pink-100',
  video: 'bg-purple-100',
  code: 'bg-emerald-100',
  music: 'bg-amber-100',
  grid: 'bg-sky-100',
}

const iconBgClass = computed(() => iconBgMap[store.currentCategory?.icon] || 'bg-gray-100')

function loadCategory() {
  store.fetchCategoryBySlug(route.params.slug)
}

onMounted(loadCategory)
watch(() => route.params.slug, loadCategory)
</script>
