<template>
  <footer class="border-t border-[var(--border-subtle)] bg-white/50 backdrop-blur-sm mt-12">
    <div class="max-w-6xl mx-auto px-4 py-8 sm:py-10">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-8">
        <div class="sm:col-span-1">
          <div class="text-lg font-bold tracking-tight mb-2">
            <span class="text-[var(--brand)]">AI</span>
            <span class="text-[var(--text-primary)]"> 导航</span>
          </div>
          <p class="text-sm text-[var(--text-tertiary)] leading-relaxed max-w-xs">
            发现、探索、对比各类 AI 工具 —— 面试作品集项目
          </p>
        </div>
        <div>
          <h4 class="text-xs font-semibold text-[var(--text-tertiary)] uppercase tracking-wider mb-3">浏览</h4>
          <div class="space-y-2">
            <RouterLink to="/" class="block text-sm text-[var(--text-secondary)] hover:text-[var(--brand)] transition-colors">首页</RouterLink>
            <RouterLink to="/search" class="block text-sm text-[var(--text-secondary)] hover:text-[var(--brand)] transition-colors">搜索</RouterLink>
            <RouterLink to="/about" class="block text-sm text-[var(--text-secondary)] hover:text-[var(--brand)] transition-colors">关于</RouterLink>
          </div>
        </div>
        <div>
          <h4 class="text-xs font-semibold text-[var(--text-tertiary)] uppercase tracking-wider mb-3">贡献</h4>
          <div class="space-y-2">
            <RouterLink to="/submit" class="block text-sm text-[var(--text-secondary)] hover:text-[var(--brand)] transition-colors">提交工具</RouterLink>
          </div>
        </div>
      </div>
      <div class="border-t border-[var(--border-subtle)] mt-8 pt-6 text-center text-xs text-[var(--text-tertiary)]">
        &copy; 2026 AI 工具导航平台 &mdash; 面试作品集项目
      </div>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
