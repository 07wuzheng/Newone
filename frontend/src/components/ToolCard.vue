<template>
  <RouterLink :to="`/tool/${tool.id}`"
    class="relative block card-white bg-white rounded-[var(--radius-md)] border border-[var(--border-subtle)] shadow-[var(--shadow-sm)] hover:shadow-[var(--shadow-lg)] hover:-translate-y-1 transition-all duration-300 overflow-hidden group">
    <!-- Logo / Fallback initial -->
    <div class="relative aspect-[4/3] overflow-hidden flex items-center justify-center" :class="gradientClass">
      <img v-if="tool.image_url && !imgError" :src="tool.image_url" :alt="tool.name"
        class="w-16 h-16 sm:w-20 sm:h-20 object-contain group-hover:scale-110 transition-transform duration-500"
        loading="lazy" @error="imgError = true" />
      <span v-else class="text-4xl sm:text-5xl font-bold text-white/80 select-none drop-shadow-sm">{{ tool.name[0] }}</span>
    </div>
    <!-- Body -->
    <div class="p-4 sm:p-5">
      <div class="flex items-start justify-between gap-3 mb-2">
        <div class="min-w-0 flex-1">
          <h3 class="font-semibold text-[var(--text-primary)] group-hover:text-[var(--brand)] transition-colors leading-snug truncate">{{ tool.name }}</h3>
          <p v-if="tool.version && !isDiscontinued" class="text-xs text-[var(--text-tertiary)] mt-1 font-medium tracking-wide">
            {{ tool.version }}
          </p>
          <span v-if="isDiscontinued"
            class="inline-block mt-1 text-xs font-medium text-red-500 bg-red-50 px-2 py-0.5 rounded-full">已关停</span>
        </div>
        <div class="flex items-center gap-1 text-amber-500 shrink-0 mt-0.5">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20"><path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/></svg>
          <span class="text-sm font-semibold text-[var(--text-secondary)]">{{ tool.rating }}</span>
        </div>
      </div>
      <p class="text-sm text-[var(--text-secondary)] leading-relaxed line-clamp-2 mb-3">{{ tool.description }}</p>
      <div class="flex flex-wrap items-center gap-1.5">
        <span v-if="tool.pricing"
          class="inline-block text-[11px] sm:text-[10px] font-semibold px-2.5 py-1 sm:px-2 sm:py-0.5 rounded-full"
          :class="pricingBadgeClass">{{ pricingLabel }}</span>
        <span v-if="tool.category_name"
          class="inline-block text-xs sm:text-[11px] font-medium px-2.5 py-1 sm:px-2.5 sm:py-1 rounded-full tracking-wide"
          :class="badgeClass">{{ tool.category_name }}</span>
        <span v-if="tool.tags && tool.tags.length" class="text-[11px] sm:text-[10px] text-[var(--text-tertiary)] ml-0.5">
          {{ tool.tags.slice(0, 2).join('、') }}{{ tool.tags.length > 2 ? '…' : '' }}
        </span>
      </div>
    </div>
  </RouterLink>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  tool: { type: Object, required: true }
})

const imgError = ref(false)
const isDiscontinued = computed(() => props.tool.version === '已关停')

const gradients = {
  llm: 'bg-gradient-to-br from-indigo-100 to-indigo-200/50',
  'ai-image': 'bg-gradient-to-br from-pink-100 to-pink-200/50',
  'ai-video': 'bg-gradient-to-br from-purple-100 to-purple-200/50',
  coding: 'bg-gradient-to-br from-emerald-100 to-emerald-200/50',
  'ai-audio': 'bg-gradient-to-br from-amber-100 to-amber-200/50',
  others: 'bg-gradient-to-br from-sky-100 to-sky-200/50',
}

const badges = {
  llm: 'text-indigo-700 bg-indigo-50',
  'ai-image': 'text-pink-700 bg-pink-50',
  'ai-video': 'text-purple-700 bg-purple-50',
  coding: 'text-emerald-700 bg-emerald-50',
  'ai-audio': 'text-amber-700 bg-amber-50',
  others: 'text-sky-700 bg-sky-50',
}

const gradientClass = computed(() => {
  const slug = props.tool.category_slug || ''
  return gradients[slug] || gradients.others
})

const badgeClass = computed(() => {
  const slug = props.tool.category_slug || ''
  return badges[slug] || badges.others
})

const pricingBadgeClass = computed(() => {
  const p = props.tool.pricing
  if (p === 'free') return 'bg-emerald-50 text-emerald-700'
  if (p === 'freemium') return 'bg-amber-50 text-amber-700'
  if (p === 'paid') return 'bg-blue-50 text-blue-700'
  return 'bg-gray-50 text-gray-600'
})

const pricingLabel = computed(() => {
  const p = props.tool.pricing
  if (p === 'free') return '免费'
  if (p === 'freemium') return '免费增值'
  if (p === 'paid') return '付费'
  return p || ''
})
</script>
