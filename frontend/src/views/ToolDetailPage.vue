<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- 网络错误 -->
    <div v-if="store.error" class="mb-8 bg-red-50/80 backdrop-blur-sm border border-red-200/60 rounded-[var(--radius-md)] px-5 py-3 flex items-center justify-between">
      <p class="text-red-700 text-sm">{{ store.error }}</p>
      <button @click="loadTool" class="text-sm font-medium text-red-600 hover:text-red-800 underline shrink-0 ml-4">重试</button>
    </div>

    <!-- 加载态 -->
    <div v-else-if="store.loading" class="space-y-6">
      <div class="h-4 skeleton rounded w-1/4"></div>
      <div class="aspect-[16/7] skeleton rounded-[var(--radius-md)]"></div>
      <div class="h-8 skeleton rounded w-1/2"></div>
      <div class="h-4 skeleton rounded w-full"></div>
      <div class="h-4 skeleton rounded w-2/3"></div>
    </div>

    <!-- 错误态 -->
    <div v-else-if="!store.currentTool && !store.loading" class="text-center py-24">
      <p class="text-[var(--text-tertiary)] text-lg mb-4">工具不存在</p>
      <RouterLink to="/" class="text-[var(--brand)] hover:underline font-medium">返回首页</RouterLink>
    </div>

    <!-- 正常内容 -->
    <template v-else-if="store.currentTool">
      <!-- 面包屑 -->
      <div class="flex items-center gap-1.5 text-xs sm:text-sm text-[var(--text-tertiary)] mb-6 sm:mb-8">
        <RouterLink to="/" class="hover:text-[var(--brand)] transition-colors shrink-0">首页</RouterLink>
        <svg class="w-3 h-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        <RouterLink :to="`/category/${store.currentTool.category_slug}`" class="hover:text-[var(--brand)] transition-colors truncate max-w-[120px] sm:max-w-none">{{ store.currentTool.category_name }}</RouterLink>
        <svg class="w-3 h-3 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
        <span class="text-[var(--text-secondary)] font-medium truncate max-w-[120px] sm:max-w-none">{{ store.currentTool.name }}</span>
      </div>

      <!-- 主卡片 -->
      <div class="card-white bg-white rounded-[var(--radius-lg)] border border-[var(--border-subtle)] shadow-[var(--shadow-sm)] overflow-hidden">
        <!-- Logo 横幅 -->
        <div class="aspect-[16/6] sm:aspect-[16/5] bg-gradient-to-br from-indigo-100 to-purple-100 relative flex flex-col items-center justify-center gap-3">
          <img v-if="store.currentTool.image_url && !detailImgError" :src="store.currentTool.image_url" :alt="store.currentTool.name" class="w-28 h-28 sm:w-40 sm:h-40 object-contain drop-shadow-md" loading="lazy" @error="detailImgError = true" />
          <span v-else class="text-7xl sm:text-8xl font-bold text-white/80 select-none drop-shadow-sm">{{ store.currentTool.name[0] }}</span>
          <h1 class="text-2xl sm:text-3xl font-bold text-white/90 drop-shadow-md sm:hidden">{{ store.currentTool.name }}</h1>
        </div>
        <div class="p-5 sm:p-8">
          <!-- 标题行（桌面端显示名称，移动端已在横幅中显示） -->
          <div class="hidden sm:flex flex-wrap items-start justify-between gap-4 mb-6">
            <div class="flex-1 min-w-0">
              <h1 class="text-3xl sm:text-4xl font-bold tracking-tight text-[var(--text-primary)]">{{ store.currentTool.name }}</h1>
              <div class="flex flex-wrap items-center gap-3 mt-3">
                <span v-if="store.currentTool.version"
                  class="inline-flex items-center gap-1.5 text-sm font-medium px-3 py-1 rounded-full"
                  :class="isDiscontinued ? 'bg-red-50 text-red-600' : 'bg-emerald-50 text-emerald-700'">
                  <span class="w-1.5 h-1.5 rounded-full" :class="isDiscontinued ? 'bg-red-400' : 'bg-emerald-400'"></span>
                  {{ store.currentTool.version }}
                </span>
                <span v-if="store.currentTool.version_updated_at" class="text-xs text-[var(--text-tertiary)]">
                  更新于 {{ formatDate(store.currentTool.version_updated_at) }}
                </span>
              </div>
            </div>
            <div class="flex items-center gap-1.5 text-amber-500 shrink-0 bg-amber-50 px-3 py-1.5 rounded-full">
              <svg class="w-5 h-5 fill-current" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
              <span class="text-lg font-bold text-[var(--text-secondary)]">{{ store.currentTool.rating }}</span>
            </div>
          </div>
          <!-- 移动端：版本和评分独立一行 -->
          <div class="flex sm:hidden flex-wrap items-center gap-3 mb-3">
            <span v-if="store.currentTool.version"
              class="inline-flex items-center gap-1.5 text-sm font-medium px-3 py-1 rounded-full"
              :class="isDiscontinued ? 'bg-red-50 text-red-600' : 'bg-emerald-50 text-emerald-700'">
              <span class="w-1.5 h-1.5 rounded-full" :class="isDiscontinued ? 'bg-red-400' : 'bg-emerald-400'"></span>
              {{ store.currentTool.version }}
            </span>
            <div class="flex items-center gap-1 text-amber-500">
              <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
              <span class="text-sm font-semibold text-[var(--text-secondary)]">{{ store.currentTool.rating }}</span>
            </div>
          </div>

          <!-- 描述 -->
          <div class="mb-6 sm:mb-8">
            <p class="text-[var(--text-secondary)] leading-relaxed text-[15px] sm:text-base">{{ store.currentTool.description }}</p>
          </div>

          <!-- 标签 & 定价（分类已在面包屑显示，标签中与分类同名的已过滤） -->
          <div class="flex flex-wrap items-center gap-2 mb-5 sm:mb-6">
            <!-- 定价 -->
            <span v-if="store.currentTool.pricing"
              class="inline-flex items-center gap-1 text-xs font-semibold px-3 py-1.5 rounded-full"
              :class="pricingClass">
              <span class="w-1.5 h-1.5 rounded-full" :class="pricingDotClass"></span>
              {{ pricingLabel }}
            </span>
            <!-- 标签 -->
            <RouterLink v-for="tag in dedupedTags" :key="tag" :to="`/search?tag=${tag}`"
              class="inline-block text-xs px-3 py-1.5 rounded-full bg-[var(--brand-subtle)] text-[var(--brand)] font-medium hover:bg-[var(--brand)] hover:text-white transition-colors">
              {{ tag }}
            </RouterLink>
          </div>

          <!-- 优缺点 -->
          <div v-if="store.currentTool.pros || store.currentTool.cons" class="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6 mb-6 sm:mb-8">
            <div v-if="store.currentTool.pros">
              <h3 class="text-sm font-semibold text-emerald-600 mb-3 flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                优点
              </h3>
              <ul class="space-y-1.5">
                <li v-for="(item, i) in prosList" :key="i"
                  class="text-sm text-[var(--text-secondary)] pl-4 relative before:content-[''] before:absolute before:left-0 before:top-2 before:w-1.5 before:h-1.5 before:rounded-full before:bg-emerald-400">
                  {{ item }}
                </li>
              </ul>
            </div>
            <div v-if="store.currentTool.cons">
              <h3 class="text-sm font-semibold text-red-500 mb-3 flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
                缺点
              </h3>
              <ul class="space-y-1.5">
                <li v-for="(item, i) in consList" :key="i"
                  class="text-sm text-[var(--text-secondary)] pl-4 relative before:content-[''] before:absolute before:left-0 before:top-2 before:w-1.5 before:h-1.5 before:rounded-full before:bg-red-400">
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>

          <!-- 操作区 -->
          <div class="flex flex-wrap items-center gap-3 mb-8">
            <a :href="store.currentTool.url" target="_blank" rel="noopener noreferrer"
               class="btn-primary w-full sm:w-auto justify-center">
              访问官网
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
            </a>
          </div>

          <!-- 相关工具 -->
          <div v-if="store.currentTool.related_tools && store.currentTool.related_tools.length > 0" class="border-t border-[var(--border-subtle)] pt-6 sm:pt-8">
            <h2 class="text-base sm:text-lg font-semibold text-[var(--text-primary)] mb-4 sm:mb-5">相关工具</h2>
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
              <RouterLink v-for="r in store.currentTool.related_tools" :key="r.id" :to="`/tool/${r.id}`"
                class="group block bg-[var(--surface)] rounded-[var(--radius-sm)] border border-[var(--border-subtle)] p-3 hover:border-[var(--brand-light)] hover:shadow-[var(--shadow-md)] transition-all">
                <div class="aspect-[4/3] bg-gradient-to-br from-indigo-50 to-purple-50 rounded mb-2 overflow-hidden flex items-center justify-center">
                  <img v-if="!relatedImgErrors.has(r.id)" :src="r.image_url" :alt="r.name" class="w-10 h-10 sm:w-12 sm:h-12 object-contain group-hover:scale-110 transition-transform duration-300" loading="lazy" @error="onRelatedImgError(r.id)" />
                  <span v-else class="text-lg font-bold text-white/70 select-none">{{ r.name[0] }}</span>
                </div>
                <p class="text-sm font-medium text-[var(--text-primary)] group-hover:text-[var(--brand)] transition-colors truncate">{{ r.name }}</p>
                <div class="flex items-center gap-1 text-amber-500 text-xs mt-1">
                  <svg class="w-3 h-3 fill-current" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
                  {{ r.rating }}
                </div>
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>

</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { useToolStore } from '../stores/tools'

const route = useRoute()
const store = useToolStore()
const detailImgError = ref(false)
const relatedImgErrors = ref(new Set())


function onRelatedImgError(id) {
  relatedImgErrors.value = new Set([...relatedImgErrors.value, id])
}

const isDiscontinued = computed(() => store.currentTool?.version === '已关停')

const pricingClass = computed(() => {
  const p = store.currentTool?.pricing
  if (p === 'free') return 'bg-emerald-50 text-emerald-700'
  if (p === 'freemium') return 'bg-amber-50 text-amber-700'
  if (p === 'paid') return 'bg-blue-50 text-blue-700'
  return 'bg-gray-50 text-gray-600'
})

const pricingDotClass = computed(() => {
  const p = store.currentTool?.pricing
  if (p === 'free') return 'bg-emerald-400'
  if (p === 'freemium') return 'bg-amber-400'
  if (p === 'paid') return 'bg-blue-400'
  return 'bg-gray-400'
})

const pricingLabel = computed(() => {
  const p = store.currentTool?.pricing
  if (p === 'free') return '免费'
  if (p === 'freemium') return '免费增值'
  if (p === 'paid') return '付费'
  return p || ''
})

// 过滤掉跟分类同名的标签，避免与面包屑重复
const dedupedTags = computed(() => {
  const tags = store.currentTool?.tags || []
  const cat = store.currentTool?.category_name || ''
  return tags.filter(t => t !== cat && t !== cat.replace(/\s/g, ''))
})

const prosList = computed(() => {
  const raw = store.currentTool?.pros
  if (!raw) return []
  return raw.split('\n').filter(Boolean)
})

const consList = computed(() => {
  const raw = store.currentTool?.cons
  if (!raw) return []
  return raw.split('\n').filter(Boolean)
})

function formatDate(iso) {
  if (!iso) return ''
  const d = new Date(iso)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

function loadTool() {
  detailImgError.value = false
  relatedImgErrors.value = new Set()
  store.fetchTool(route.params.id)
}

onMounted(loadTool)
watch(() => route.params.id, loadTool)
</script>
