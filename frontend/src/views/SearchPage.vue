<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <!-- 搜索框 -->
    <div class="max-w-2xl mx-auto mb-6">
      <h1 class="text-2xl sm:text-4xl font-bold tracking-tight text-[var(--text-primary)] text-center mb-6 sm:mb-8">搜索 AI 工具</h1>
      <div class="relative">
        <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-[var(--text-tertiary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        <input
          v-model="query"
          type="text"
          placeholder="输入关键词搜索 AI 工具..."
          class="w-full pl-12 pr-4 py-4 bg-white/90 backdrop-blur-sm border border-gray-200/80 rounded-[var(--radius-md)] text-[var(--text-primary)] placeholder-[var(--text-tertiary)] focus:outline-none focus:ring-2 focus:ring-[var(--brand)]/20 focus:border-[var(--brand-light)] shadow-[var(--shadow-sm)] transition-all text-[15px]"
        />
      </div>
    </div>

    <!-- 筛选标签 -->
    <div class="flex flex-wrap items-center gap-2 mb-6 sm:mb-8 justify-center">
      <span class="text-sm font-medium text-[var(--text-secondary)]">筛选：</span>
      <button @click="setPricing(null)"
        class="text-sm px-5 py-2 sm:px-4 sm:py-1.5 rounded-full border transition-colors"
        :class="!activePricing ? 'border-[var(--brand)] bg-[var(--brand)] text-white' : 'border-gray-200 text-[var(--text-secondary)] hover:border-[var(--brand-light)]'">
        全部
      </button>
      <button @click="setPricing('free')"
        class="text-sm px-5 py-2 sm:px-4 sm:py-1.5 rounded-full border transition-colors"
        :class="activePricing === 'free' ? 'border-emerald-500 bg-emerald-50 text-emerald-700 font-medium' : 'border-gray-200 text-[var(--text-secondary)] hover:border-[var(--brand-light)]'">
        免费
      </button>
      <button @click="setPricing('freemium')"
        class="text-sm px-5 py-2 sm:px-4 sm:py-1.5 rounded-full border transition-colors"
        :class="activePricing === 'freemium' ? 'border-amber-500 bg-amber-50 text-amber-700 font-medium' : 'border-gray-200 text-[var(--text-secondary)] hover:border-[var(--brand-light)]'">
        免费增值
      </button>
      <button @click="setPricing('paid')"
        class="text-sm px-5 py-2 sm:px-4 sm:py-1.5 rounded-full border transition-colors"
        :class="activePricing === 'paid' ? 'border-blue-500 bg-blue-50 text-blue-700 font-medium' : 'border-gray-200 text-[var(--text-secondary)] hover:border-[var(--brand-light)]'">
        付费
      </button>
      <button @click="toggleEditorPick"
        class="text-sm px-5 py-2 sm:px-4 sm:py-1.5 rounded-full border transition-colors"
        :class="activeEditorPick ? 'border-amber-500 bg-amber-50 text-amber-700 font-medium' : 'border-gray-200 text-[var(--text-secondary)] hover:border-[var(--brand-light)]'">
        编辑精选
      </button>
    </div>

    <!-- 网络错误 -->
    <div v-if="store.error" class="max-w-2xl mx-auto mb-8 bg-red-50/80 backdrop-blur-sm border border-red-200/60 rounded-[var(--radius-md)] px-5 py-3 flex items-center justify-between">
      <p class="text-red-700 text-sm">{{ store.error }}</p>
    </div>

    <!-- 空状态：无搜索词且无筛选 -->
    <div v-else-if="!query && !activePricing && !activeEditorPick && !activeTag" class="text-center py-16">
      <div class="text-5xl mb-4 opacity-30">&#x1F50D;</div>
      <p class="text-[var(--text-tertiary)]">输入关键词开始搜索</p>
      <div class="flex flex-wrap justify-center gap-2 mt-5">
        <span v-for="tag in suggestions" :key="tag"
          class="text-xs sm:text-xs font-medium card-white bg-white border border-gray-200/60 text-[var(--text-tertiary)] hover:border-[var(--brand-light)] hover:text-[var(--brand)] hover:bg-[var(--brand-subtle)] px-4 py-2 sm:px-3 sm:py-1.5 rounded-full cursor-pointer transition-colors"
          @click="query = tag">
          {{ tag }}
        </span>
      </div>
    </div>

    <!-- 加载态 -->
    <div v-else-if="store.loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
      <div v-for="i in 6" :key="i" class="card-white bg-white rounded-[var(--radius-md)] overflow-hidden">
        <div class="aspect-[4/3] skeleton"></div>
        <div class="p-5 space-y-3">
          <div class="h-5 skeleton rounded w-1/2"></div>
          <div class="h-4 skeleton rounded w-full"></div>
        </div>
      </div>
    </div>

    <!-- 无结果 -->
    <div v-else-if="store.searchResults.length === 0" class="text-center py-16">
      <div class="text-5xl mb-4 opacity-30">&#x1F615;</div>
      <p v-if="query" class="text-[var(--text-secondary)] mb-2">没有找到与 "<span class="font-medium text-[var(--text-primary)]">{{ query }}</span>" 相关的工具</p>
      <p v-else class="text-[var(--text-secondary)] mb-2">没有符合条件的工具</p>
      <p class="text-[var(--text-tertiary)] text-sm">试试其他关键词或筛选条件</p>
    </div>

    <!-- 搜索结果 -->
    <div v-else>
      <p class="text-sm text-[var(--text-tertiary)] mb-4 sm:mb-5">找到 {{ store.searchResults.length }} 个结果</p>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <div v-for="(tool, i) in store.searchResults" :key="tool.id" :class="`stagger-${i + 1}`">
          <ToolCard :tool="tool" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToolStore } from '../stores/tools'
import { useDebounceFn } from '@vueuse/core'
import ToolCard from '../components/ToolCard.vue'

const store = useToolStore()
const route = useRoute()
const router = useRouter()
const query = ref('')
const mounted = ref(false)

const suggestions = ['ChatGPT', 'Midjourney', 'GitHub Copilot', 'Suno', 'Runway', 'Perplexity']

const activePricing = computed(() => route.query.pricing || null)
const activeEditorPick = computed(() => route.query.editor_pick === 'true')
const activeTag = computed(() => route.query.tag || null)

function setPricing(val) {
  const q = { ...route.query }
  if (val) q.pricing = val
  else delete q.pricing
  router.replace({ query: q })
}

function toggleEditorPick() {
  const q = { ...route.query }
  if (activeEditorPick.value) delete q.editor_pick
  else q.editor_pick = 'true'
  router.replace({ query: q })
}

async function loadResults() {
  const params = {}
  if (activePricing.value) params.pricing = activePricing.value
  if (activeTag.value) params.tag = activeTag.value
  if (activeEditorPick.value) params.editor_pick = true

  if (query.value.trim()) {
    params.q = query.value.trim()
    await store.searchTools(query.value.trim(), params)
  } else {
    // 有筛选参数则按筛选查询，否则显示全部工具
    await store.fetchTools(Object.keys(params).length ? params : {})
  }
}

const debouncedLoad = useDebounceFn(loadResults, 300)

watch([query, () => route.query.pricing, () => route.query.editor_pick, () => route.query.tag], () => {
  if (mounted.value) debouncedLoad()
})

onMounted(() => {
  mounted.value = true
  if (activePricing.value || activeEditorPick.value || activeTag.value) {
    store.loading = true  // 防止初始渲染闪烁空状态
    loadResults()
  }
})
</script>
