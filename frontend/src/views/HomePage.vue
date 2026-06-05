<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <!-- Error Banner -->
    <div v-if="catStore.error || toolStore.error"
      class="mb-8 bg-red-50/80 backdrop-blur-sm border border-red-200/60 rounded-[var(--radius-md)] px-5 py-3 flex items-center justify-between">
      <p class="text-red-700 text-sm">{{ catStore.error || toolStore.error }}</p>
      <button @click="retry"
        class="text-sm font-medium text-red-600 hover:text-red-800 underline shrink-0 ml-4">重试</button>
    </div>

    <!-- Hero -->
    <section class="relative text-center py-10 sm:py-20 overflow-hidden rounded-[var(--radius-xl)] mb-8 sm:mb-14">
      <div class="absolute inset-0 bg-gradient-to-br from-indigo-50/80 via-white to-purple-50/80"></div>
      <div class="absolute top-1/4 -left-10 w-[500px] h-[500px] bg-indigo-300/15 rounded-full blur-[120px]"></div>
      <div class="absolute bottom-1/4 -right-10 w-[400px] h-[400px] bg-purple-300/15 rounded-full blur-[120px]"></div>
      <div class="relative">
        <div class="inline-flex items-center gap-2 bg-white/70 backdrop-blur-sm border border-gray-200/60 rounded-full px-4 py-1.5 text-xs font-medium text-[var(--text-tertiary)] mb-6 tracking-wide">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          收录 {{ catStore.categories.length }} 个分类
        </div>
        <h1 class="text-3xl sm:text-6xl font-bold tracking-tight text-[var(--text-primary)] mb-3 sm:mb-5 leading-[1.1]">
          发现 AI 工具
        </h1>
        <p class="text-sm sm:text-lg text-[var(--text-secondary)] mb-6 sm:mb-10 max-w-md mx-auto leading-relaxed px-4">
          在 ChatGPT 之外，还有 60+ 款值得知道的 AI 工具
        </p>
        <div class="max-w-lg mx-auto">
          <RouterLink to="/search"
            class="flex items-center gap-3 bg-white/90 backdrop-blur-md border border-gray-200/80 rounded-[var(--radius-md)] px-5 py-4 text-[var(--text-tertiary)] hover:border-[var(--brand-light)] hover:text-[var(--brand)] transition-all shadow-[var(--shadow-sm)] hover:shadow-[var(--shadow-md)] group">
            <svg class="w-5 h-5 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
            <span class="flex-1 text-left">搜索 AI 工具...</span>
            <kbd class="hidden sm:inline-flex text-[11px] text-[var(--text-tertiary)] bg-gray-100 border border-gray-200 rounded px-1.5 py-0.5">⌘K</kbd>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- 统计条 -->
    <section class="mb-10 sm:mb-16">
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="card-white bg-white rounded-[var(--radius-md)] border border-[var(--border-subtle)] p-4 sm:p-5 text-center">
          <div class="text-2xl sm:text-3xl font-bold text-[var(--brand)]">{{ toolStore.stats?.total_tools ?? '—' }}</div>
          <div class="text-xs sm:text-sm text-[var(--text-secondary)] mt-1">收录工具</div>
        </div>
        <div class="card-white bg-white rounded-[var(--radius-md)] border border-[var(--border-subtle)] p-4 sm:p-5 text-center">
          <div class="text-2xl sm:text-3xl font-bold text-emerald-500">{{ toolStore.stats?.total_categories ?? '—' }}</div>
          <div class="text-xs sm:text-sm text-[var(--text-secondary)] mt-1">分类</div>
        </div>
        <div class="card-white bg-white rounded-[var(--radius-md)] border border-[var(--border-subtle)] p-4 sm:p-5 text-center">
          <div class="text-2xl sm:text-3xl font-bold text-amber-500">{{ toolStore.stats?.featured_tools ?? '—' }}</div>
          <div class="text-xs sm:text-sm text-[var(--text-secondary)] mt-1">推荐工具</div>
        </div>
        <div class="card-white bg-white rounded-[var(--radius-md)] border border-[var(--border-subtle)] p-4 sm:p-5 text-center">
          <div class="text-2xl sm:text-3xl font-bold text-purple-500">{{ toolStore.stats?.editor_picks ?? '—' }}</div>
          <div class="text-xs sm:text-sm text-[var(--text-secondary)] mt-1">编辑精选</div>
        </div>
      </div>
    </section>

    <!-- 筛选 -->
    <section class="mb-10">
      <div class="flex flex-wrap items-center gap-2">
        <span class="text-sm font-medium text-[var(--text-secondary)] mr-1">定价：</span>
        <RouterLink to="/search"
          class="text-sm px-5 py-2 sm:px-4 sm:py-1.5 rounded-full border border-gray-200 text-[var(--text-secondary)] hover:border-[var(--brand-light)] transition-colors">
          全部
        </RouterLink>
        <RouterLink to="/search?pricing=free"
          class="text-sm px-5 py-2 sm:px-4 sm:py-1.5 rounded-full border border-gray-200 text-[var(--text-secondary)] hover:border-emerald-300 hover:text-emerald-600 transition-colors">
          免费
        </RouterLink>
        <RouterLink to="/search?pricing=freemium"
          class="text-sm px-5 py-2 sm:px-4 sm:py-1.5 rounded-full border border-gray-200 text-[var(--text-secondary)] hover:border-amber-300 hover:text-amber-600 transition-colors">
          免费增值
        </RouterLink>
        <RouterLink to="/search?pricing=paid"
          class="text-sm px-5 py-2 sm:px-4 sm:py-1.5 rounded-full border border-gray-200 text-[var(--text-secondary)] hover:border-blue-300 hover:text-blue-600 transition-colors">
          付费
        </RouterLink>
      </div>
    </section>

    <!-- 编辑精选 -->
    <section v-if="toolStore.editorPicks.length > 0" class="mb-10 sm:mb-16">
      <div class="flex items-end justify-between mb-5 sm:mb-8">
        <div>
          <h2 class="section-title">编辑精选</h2>
          <p class="section-subtitle">编辑团队精心挑选的顶尖 AI 工具</p>
        </div>
        <RouterLink to="/search?editor_pick=true"
          class="text-sm text-[var(--brand)] hover:underline font-medium shrink-0">查看全部</RouterLink>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <div v-for="(tool, i) in toolStore.editorPicks" :key="tool.id" :class="`stagger-${i + 1}`">
          <div class="relative">
            <div class="absolute -top-2 -right-2 z-10 bg-amber-400 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-sm">精选</div>
            <ToolCard :tool="tool" />
          </div>
        </div>
      </div>
    </section>

    <!-- 分类入口 -->
    <section class="mb-10 sm:mb-16">
      <div class="flex items-end justify-between mb-5 sm:mb-8">
        <div>
          <h2 class="section-title">分类浏览</h2>
          <p class="section-subtitle">按领域探索 AI 工具</p>
        </div>
      </div>
      <div v-if="catStore.loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <div v-for="i in 6" :key="i" class="card-white bg-white rounded-[var(--radius-md)] p-6">
          <div class="w-12 h-12 skeleton rounded-[var(--radius-sm)] mb-4"></div>
          <div class="h-5 skeleton rounded w-2/3 mb-2"></div>
          <div class="h-4 skeleton rounded w-full"></div>
        </div>
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-5">
        <div v-for="(cat, i) in catStore.categories" :key="cat.id" :class="`stagger-${i + 1}`">
          <CategoryCard :category="cat" />
        </div>
      </div>
    </section>

    <!-- 热门推荐 -->
    <section>
      <div class="flex items-end justify-between mb-5 sm:mb-8">
        <div>
          <h2 class="section-title">热门推荐</h2>
          <p class="section-subtitle">精选最受欢迎的 AI 工具</p>
        </div>
        <RouterLink to="/search"
          class="text-sm text-[var(--brand)] hover:underline font-medium shrink-0">查看全部</RouterLink>
      </div>
      <div v-if="toolStore.loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <div v-for="i in 6" :key="i" class="card-white bg-white rounded-[var(--radius-md)] overflow-hidden">
          <div class="aspect-[4/3] skeleton"></div>
          <div class="p-5 space-y-3">
            <div class="h-5 skeleton rounded w-1/2"></div>
            <div class="h-4 skeleton rounded w-full"></div>
            <div class="h-4 skeleton rounded w-2/3"></div>
          </div>
        </div>
      </div>
      <div v-else-if="!toolStore.error && toolStore.featured.length === 0"
        class="text-center py-16 text-[var(--text-tertiary)]">
        <div class="text-5xl mb-4 opacity-30">✨</div>
        <p>暂无推荐工具</p>
      </div>
      <div v-else-if="!toolStore.error" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <div v-for="(tool, i) in featuredNoDup.slice(0, 6)" :key="tool.id" :class="`stagger-${i + 1}`">
          <ToolCard :tool="tool" />
        </div>
      </div>
      <div v-if="!toolStore.loading && !toolStore.error && featuredNoDup.length > 6"
        class="mt-6 sm:mt-8 text-center">
        <RouterLink to="/search"
          class="inline-flex items-center gap-1.5 text-sm font-medium text-[var(--brand)] hover:text-[var(--brand-dark)] transition-colors">
          浏览全部工具
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useCategoryStore } from '../stores/categories'
import { useToolStore } from '../stores/tools'
import CategoryCard from '../components/CategoryCard.vue'
import ToolCard from '../components/ToolCard.vue'

const catStore = useCategoryStore()
const toolStore = useToolStore()

// 热门推荐去掉已经在"编辑精选"展示过的，避免视觉重复
const featuredNoDup = computed(() => {
  const picked = new Set(toolStore.editorPicks.map(t => t.id))
  return toolStore.featured.filter(t => !picked.has(t.id))
})

function retry() {
  catStore.fetchCategories()
  toolStore.fetchFeatured()
  toolStore.fetchStats()
  toolStore.fetchEditorPicks()
}

onMounted(retry)
</script>
