<template>
  <div class="max-w-6xl mx-auto px-4 py-24 text-center">
    <div class="text-7xl sm:text-8xl font-bold tracking-tight text-[var(--border-subtle)] mb-4 select-none">404</div>
    <p class="text-lg text-[var(--text-secondary)] mb-8">页面不存在</p>
    <RouterLink to="/" class="btn-primary">返回首页</RouterLink>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>
