<template>
  <aside class="w-[300px]">
    <!-- 推荐工具 -->
    <div v-if="toolStore.editorPicks.length > 0" class="mb-8">
      <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-4 flex items-center gap-2">
        <svg class="w-4 h-4 text-amber-400" viewBox="0 0 20 20" fill="currentColor">
          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
        </svg>
        编辑推荐
      </h3>
      <div class="space-y-1">
        <RouterLink v-for="tool in toolStore.editorPicks.slice(0, 5)" :key="tool.id"
          :to="`/tool/${tool.id}`"
          class="flex items-center gap-3 p-2.5 rounded-[var(--radius-sm)] hover:bg-[var(--brand-subtle)] transition-colors group">
          <div class="w-10 h-10 rounded-[var(--radius-sm)] bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center shrink-0 overflow-hidden">
            <img v-if="tool.image_url" :src="tool.image_url" :alt="tool.name" class="w-6 h-6 object-contain" loading="lazy" />
            <span v-else class="text-sm font-bold text-white/70">{{ tool.name[0] }}</span>
          </div>
          <div class="min-w-0 flex-1">
            <p class="text-sm font-medium text-[var(--text-primary)] group-hover:text-[var(--brand)] truncate transition-colors">{{ tool.name }}</p>
            <div class="flex items-center gap-2 text-xs text-[var(--text-tertiary)] mt-0.5">
              <span class="flex items-center gap-0.5 text-amber-500">
                <svg class="w-3 h-3 fill-current" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                {{ tool.rating }}
              </span>
              <span class="truncate">{{ tool.category_name }}</span>
            </div>
          </div>
        </RouterLink>
      </div>
    </div>

    <!-- 推荐工具骨架 -->
    <div v-else class="mb-8">
      <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-4">编辑推荐</h3>
      <div class="space-y-3">
        <div v-for="i in 4" :key="i" class="flex items-center gap-3 p-2.5">
          <div class="w-10 h-10 skeleton rounded-[var(--radius-sm)] shrink-0"></div>
          <div class="flex-1 space-y-2">
            <div class="h-3 skeleton rounded w-3/4"></div>
            <div class="h-2.5 skeleton rounded w-1/2"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 分类导航 -->
    <div>
      <h3 class="text-sm font-semibold text-[var(--text-primary)] mb-4 flex items-center gap-2">
        <svg class="w-4 h-4 text-[var(--text-tertiary)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16"/>
        </svg>
        分类
      </h3>
      <div class="space-y-0.5">
        <RouterLink v-for="cat in catStore.categories" :key="cat.slug"
          :to="`/category/${cat.slug}`"
          class="flex items-center gap-2.5 px-3 py-2 text-sm text-[var(--text-secondary)] hover:text-[var(--brand)] hover:bg-[var(--brand-subtle)] rounded-[var(--radius-sm)] transition-colors"
          :class="{ 'text-[var(--brand)] bg-[var(--brand-subtle)] font-medium': $route.params.slug === cat.slug }">
          <span class="text-base shrink-0">{{ iconMap[cat.icon] || '🧩' }}</span>
          <span class="truncate">{{ cat.name }}</span>
        </RouterLink>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useToolStore } from '../stores/tools'
import { useCategoryStore } from '../stores/categories'

const toolStore = useToolStore()
const catStore = useCategoryStore()

const iconMap = {
  chat: '💬', image: '🎨', video: '🎬',
  code: '💻', music: '🎵', grid: '🧩',
}

onMounted(() => {
  if (toolStore.editorPicks.length === 0) toolStore.fetchEditorPicks()
  if (catStore.categories.length === 0) catStore.fetchCategories()
})
</script>
