<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <h1 class="text-3xl sm:text-4xl font-bold tracking-tight text-[var(--text-primary)] mb-8">关于本项目</h1>

    <div class="card-white bg-white rounded-[var(--radius-lg)] border border-[var(--border-subtle)] shadow-[var(--shadow-sm)] p-5 sm:p-8 space-y-6 sm:space-y-8">
      <section>
        <h2 class="text-xl font-semibold text-[var(--text-primary)] mb-2">AI 工具导航平台</h2>
        <p class="text-[var(--text-secondary)] leading-relaxed">
          一个帮助用户发现和探索 AI 工具的导航目录网站。在这里，你可以浏览各类 AI 工具的分类，搜索感兴趣的工具，并了解它们的详细信息。
        </p>
      </section>

      <section class="border-t border-[var(--border-subtle)] pt-8">
        <h2 class="text-xl font-semibold text-[var(--text-primary)] mb-4">技术栈</h2>
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
          <div v-for="tech in techStack" :key="tech.name"
            class="bg-[var(--surface)] rounded-[var(--radius-sm)] border border-[var(--border-subtle)] p-4 hover:border-[var(--brand-light)] transition-colors">
            <p class="font-semibold text-sm text-[var(--text-primary)]">{{ tech.name }}</p>
            <p class="text-xs text-[var(--text-tertiary)] mt-0.5">{{ tech.desc }}</p>
          </div>
        </div>
      </section>

      <section class="border-t border-[var(--border-subtle)] pt-8">
        <h2 class="text-xl font-semibold text-[var(--text-primary)] mb-3">项目说明</h2>
        <ul class="space-y-3 text-sm text-[var(--text-secondary)]">
          <li class="flex gap-3">
            <span class="text-[var(--brand)] shrink-0 mt-0.5">◆</span>
            <span>该项目为 AI PM 面试作品集项目，展示从需求分析到项目交付的全流程能力</span>
          </li>
          <li class="flex gap-3">
            <span class="text-[var(--brand)] shrink-0 mt-0.5">◆</span>
            <span>MVP 阶段覆盖首页推荐、分类浏览、实时搜索、工具详情、提交工具等核心功能</span>
          </li>
          <li class="flex gap-3">
            <span class="text-[var(--brand)] shrink-0 mt-0.5">◆</span>
            <span>采用 Vue 3 + FastAPI 技术栈，前后端分离架构</span>
          </li>
        </ul>
      </section>

      <section class="border-t border-[var(--border-subtle)] pt-8">
        <h2 class="text-xl font-semibold text-[var(--text-primary)] mb-3">数据来源</h2>
        <p class="text-sm text-[var(--text-secondary)] leading-relaxed">
          平台中的工具数据为示例数据，仅用于功能演示。工具评分、描述等信息仅供参考。
        </p>
      </section>
    </div>
  </div>
</template>

<script setup>
const techStack = [
  { name: 'Vue 3', desc: '前端框架（Composition API）' },
  { name: 'Tailwind CSS', desc: '样式框架' },
  { name: 'FastAPI', desc: 'Python 后端框架' },
  { name: 'SQLite', desc: '数据库' },
  { name: 'Pinia', desc: '状态管理' },
  { name: 'Vue Router', desc: '前端路由' },
]
</script>
