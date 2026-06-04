<template>
  <nav class="sticky top-0 z-50 nav-blur bg-white/80 backdrop-blur-lg border-b border-gray-200/50">
    <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
      <RouterLink to="/" class="text-xl font-bold tracking-tight">
        <span class="text-[var(--brand)]">AI</span>
        <span class="text-[var(--text-primary)]"> 导航</span>
      </RouterLink>

      <!-- 桌面端导航 -->
      <div class="hidden sm:flex items-center gap-1">
        <RouterLink to="/"
          class="text-sm text-[var(--text-secondary)] hover:text-[var(--brand)] px-3 py-2 rounded-[var(--radius-sm)] hover:bg-[var(--brand-subtle)] transition-colors"
          :class="{ 'text-[var(--brand)] bg-[var(--brand-subtle)] font-medium': $route.path === '/' }">
          首页
        </RouterLink>
        <!-- 分类下拉 -->
        <div class="relative" @mouseenter="open = true" @mouseleave="open = false">
          <button
            class="text-sm text-[var(--text-secondary)] hover:text-[var(--brand)] px-3 py-2 rounded-[var(--radius-sm)] hover:bg-[var(--brand-subtle)] transition-colors flex items-center gap-1"
            :class="{ 'text-[var(--brand)] bg-[var(--brand-subtle)] font-medium': $route.path.startsWith('/category/') }">
            分类
            <svg class="w-3 h-3 mt-0.5 transition-transform duration-200" :class="{ 'rotate-180': open }" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
          </button>
          <transition name="dropdown">
            <div v-if="open"
              class="absolute right-0 top-full mt-2 bg-white/95 backdrop-blur-lg border border-gray-200/80 rounded-[var(--radius-md)] shadow-[var(--shadow-lg)] py-1.5 w-48 z-50 origin-top-right">
              <RouterLink v-for="cat in catStore.categories" :key="cat.slug" :to="`/category/${cat.slug}`"
                class="block px-4 py-2.5 text-sm text-[var(--text-secondary)] hover:text-[var(--brand)] hover:bg-[var(--brand-subtle)] transition-colors"
                :class="{ 'text-[var(--brand)] bg-[var(--brand-subtle)] font-medium': $route.params.slug === cat.slug }"
                @click="open = false">
                {{ cat.name }}
              </RouterLink>
            </div>
          </transition>
        </div>
        <RouterLink to="/about"
          class="text-sm text-[var(--text-secondary)] hover:text-[var(--brand)] px-3 py-2 rounded-[var(--radius-sm)] hover:bg-[var(--brand-subtle)] transition-colors"
          :class="{ 'text-[var(--brand)] bg-[var(--brand-subtle)] font-medium': $route.path === '/about' }">
          关于
        </RouterLink>
        <RouterLink to="/submit"
          class="text-sm font-semibold text-white bg-[var(--brand)] hover:bg-[var(--brand-dark)] px-5 py-2 rounded-[var(--radius-sm)] transition-all ml-3 shadow-[var(--shadow-sm)] hover:shadow-[0_4px_12px_rgba(79,70,229,0.35)] hover:-translate-y-0.5">
          提交工具
        </RouterLink>

        <!-- 深色模式切换 -->
        <button @click="toggleDark"
          class="ml-2 p-2 rounded-[var(--radius-sm)] text-[var(--text-tertiary)] hover:text-[var(--brand)] hover:bg-[var(--brand-subtle)] transition-colors"
          :title="isDark ? '切换亮色模式' : '切换深色模式'">
          <svg v-if="isDark" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
          </svg>
          <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
          </svg>
        </button>
      </div>

      <!-- 移动端汉堡菜单 -->
      <button class="sm:hidden p-2 text-[var(--text-secondary)] hover:text-[var(--brand)] transition-colors rounded-lg" @click="mobileOpen = !mobileOpen">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path v-if="!mobileOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16"/>
          <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>

    <!-- 移动端菜单面板 -->
    <transition name="mobile-menu">
      <div v-if="mobileOpen" class="sm:hidden border-t border-gray-200/50 bg-white/95 backdrop-blur-lg px-4 py-4 pb-6 space-y-1 max-h-[80vh] overflow-y-auto">
        <RouterLink to="/"
          class="block px-3 py-2.5 text-sm text-[var(--text-secondary)] rounded-[var(--radius-sm)] hover:bg-[var(--brand-subtle)] hover:text-[var(--brand)] transition-colors"
          :class="{ 'text-[var(--brand)] bg-[var(--brand-subtle)] font-medium': $route.path === '/' }"
          @click="mobileOpen = false">首页</RouterLink>
        <div class="text-xs font-medium text-[var(--text-tertiary)] px-3 py-2 tracking-wide uppercase">分类</div>
        <RouterLink v-for="cat in catStore.categories" :key="cat.slug" :to="`/category/${cat.slug}`"
          class="block px-6 py-2.5 text-sm text-[var(--text-secondary)] rounded-[var(--radius-sm)] hover:bg-[var(--brand-subtle)] hover:text-[var(--brand)] transition-colors"
          :class="{ 'text-[var(--brand)] bg-[var(--brand-subtle)] font-medium': $route.params.slug === cat.slug }"
          @click="mobileOpen = false">
          {{ cat.name }}
        </RouterLink>
        <RouterLink to="/about"
          class="block px-3 py-2.5 text-sm text-[var(--text-secondary)] rounded-[var(--radius-sm)] hover:bg-[var(--brand-subtle)] hover:text-[var(--brand)] transition-colors"
          :class="{ 'text-[var(--brand)] bg-[var(--brand-subtle)] font-medium': $route.path === '/about' }"
          @click="mobileOpen = false">关于</RouterLink>
        <RouterLink to="/submit"
          class="block px-3 py-2.5 text-sm font-semibold text-white bg-[var(--brand)] rounded-[var(--radius-sm)] text-center mt-2"
          @click="mobileOpen = false">提交工具</RouterLink>
        <button @click="toggleDark"
          class="w-full mt-2 px-3 py-2.5 text-sm text-[var(--text-secondary)] rounded-[var(--radius-sm)] hover:bg-[var(--brand-subtle)] hover:text-[var(--brand)] transition-colors flex items-center justify-center gap-2">
          <svg v-if="isDark" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
          </svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
          </svg>
          <span>{{ isDark ? '亮色模式' : '深色模式' }}</span>
        </button>
      </div>
    </transition>
  </nav>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useCategoryStore } from '../stores/categories'

const route = useRoute()
const open = ref(false)
const mobileOpen = ref(false)
const catStore = useCategoryStore()

// 移动端菜单打开时锁定 body 滚动
watch(mobileOpen, (v) => {
  document.body.style.overflow = v ? 'hidden' : ''
})

// ── 深色模式 ──
const isDark = ref(false)

function applyTheme(dark) {
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
  isDark.value = dark
  localStorage.setItem('theme', dark ? 'dark' : 'light')
}

function toggleDark() {
  applyTheme(!isDark.value)
}

onMounted(() => {
  if (catStore.categories.length === 0 && !catStore.loading) {
    catStore.fetchCategories()
  }
  // 恢复主题偏好
  const saved = localStorage.getItem('theme')
  if (saved) {
    applyTheme(saved === 'dark')
  } else {
    // 跟随系统
    applyTheme(window.matchMedia('(prefers-color-scheme: dark)').matches)
  }
})
</script>
