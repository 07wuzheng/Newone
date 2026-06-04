<template>
  <RouterLink :to="`/category/${category.slug}`"
    class="relative block card-white bg-white rounded-[var(--radius-md)] border border-[var(--border-subtle)] shadow-[var(--shadow-sm)] hover:shadow-[var(--shadow-lg)] hover:-translate-y-1 transition-all duration-300 p-5 sm:p-6 group overflow-hidden">
    <!-- Gradient background -->
    <div class="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300" :class="gradientClass"></div>
    <div class="relative">
      <div class="w-12 h-12 rounded-[var(--radius-sm)] flex items-center justify-center text-xl mb-4 shadow-sm" :class="iconBgClass">
        {{ iconMap[category.icon] || '🧩' }}
      </div>
      <h3 class="font-semibold text-[var(--text-primary)] group-hover:text-[var(--brand)] transition-colors mb-1.5">{{ category.name }}</h3>
      <p class="text-sm text-[var(--text-secondary)] leading-relaxed">{{ category.description }}</p>
    </div>
  </RouterLink>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  category: { type: Object, required: true }
})

const iconMap = {
  chat: '💬', image: '🎨', video: '🎬',
  code: '💻', music: '🎵', grid: '🧩',
}

const gradients = {
  chat: 'bg-gradient-to-br from-indigo-50 to-indigo-100/50',
  image: 'bg-gradient-to-br from-pink-50 to-pink-100/50',
  video: 'bg-gradient-to-br from-purple-50 to-purple-100/50',
  code: 'bg-gradient-to-br from-emerald-50 to-emerald-100/50',
  music: 'bg-gradient-to-br from-amber-50 to-amber-100/50',
  grid: 'bg-gradient-to-br from-sky-50 to-sky-100/50',
}

const iconBgClasses = {
  chat: 'bg-indigo-100 text-indigo-600',
  image: 'bg-pink-100 text-pink-600',
  video: 'bg-purple-100 text-purple-600',
  code: 'bg-emerald-100 text-emerald-600',
  music: 'bg-amber-100 text-amber-600',
  grid: 'bg-sky-100 text-sky-600',
}

const gradientClass = computed(() => gradients[props.category.icon] || gradients.grid)
const iconBgClass = computed(() => iconBgClasses[props.category.icon] || iconBgClasses.grid)
</script>
