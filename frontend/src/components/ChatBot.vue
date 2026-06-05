<template>
  <div class="fixed bottom-5 right-5 z-50">
    <!-- 触发按钮 -->
    <button v-if="!open" @click="open = true"
      class="w-14 h-14 rounded-full bg-[var(--brand)] text-white shadow-[0_4px_20px_rgba(79,70,229,0.35)] hover:shadow-[0_6px_24px_rgba(79,70,229,0.5)] hover:-translate-y-0.5 transition-all flex items-center justify-center">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"/>
      </svg>
    </button>

    <!-- 聊天窗口 -->
    <div v-else
      class="w-[calc(100vw-2.5rem)] max-w-[360px] sm:w-[400px] sm:max-w-none h-[520px] max-h-[calc(100vh-6rem)] bg-white rounded-[var(--radius-lg)] border border-gray-200/80 shadow-[0_8px_32px_rgba(0,0,0,0.12)] flex flex-col overflow-hidden animate-slide-up origin-bottom-right">

      <!-- 头部 -->
      <div class="bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-5 py-4 flex items-center justify-between shrink-0">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
          </div>
          <div>
            <p class="text-sm font-semibold">AI 工具助手</p>
            <p class="text-[11px] text-white/70">推荐你想要的 AI 工具</p>
          </div>
        </div>
        <button @click="open = false" class="text-white/70 hover:text-white transition-colors p-1">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>

      <!-- 消息区 -->
      <div ref="msgContainer" class="flex-1 overflow-y-auto px-4 py-4 space-y-4 scroll-smooth" style="background: #f8f9fb;">
        <!-- 欢迎消息 -->
        <div v-if="messages.length === 0" class="text-center py-8">
          <div class="w-16 h-16 mx-auto mb-3 rounded-2xl bg-gradient-to-br from-indigo-100 to-purple-100 flex items-center justify-center">
            <svg class="w-8 h-8 text-[var(--brand)]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
            </svg>
          </div>
          <p class="text-sm font-medium text-[var(--text-primary)] mb-2">需要什么 AI 工具？</p>
          <p class="text-xs text-[var(--text-tertiary)]">试试问：</p>
          <div class="flex flex-wrap justify-center gap-1.5 mt-2">
            <button v-for="q in suggestions" :key="q"
              @click="send(q)"
              class="text-xs px-3 py-1.5 rounded-full border border-gray-200 text-[var(--text-secondary)] hover:border-[var(--brand-light)] hover:text-[var(--brand)] hover:bg-[var(--brand-subtle)] transition-colors">
              {{ q }}
            </button>
          </div>
        </div>

        <!-- 消息列表 -->
        <div v-for="(msg, i) in messages" :key="i"
          class="flex" :class="msg.role === 'user' ? 'justify-end' : 'justify-start'">
          <!-- 机器人头像 -->
          <div v-if="msg.role === 'assistant'" class="w-7 h-7 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-[10px] font-bold shrink-0 mt-1 mr-2">
            AI
          </div>
          <div :class="msg.role === 'user'
            ? 'bg-[var(--brand)] text-white rounded-[18px] rounded-br-[4px]'
            : 'bg-white border border-gray-200/60 rounded-[18px] rounded-bl-[4px]'" class="max-w-[80%] px-4 py-2.5 text-sm leading-relaxed shadow-sm">
            <div v-if="msg.role === 'assistant'" class="prose prose-sm max-w-none text-[var(--text-primary)]" v-html="renderMarkdown(msg.content)"></div>
            <div v-else>{{ msg.content }}</div>
          </div>
          <div v-if="msg.role === 'user'" class="w-7 h-7 rounded-full bg-gray-100 flex items-center justify-center text-[10px] font-bold shrink-0 mt-1 ml-2 text-[var(--text-secondary)]">
            我
          </div>
        </div>

        <!-- 加载中 -->
        <div v-if="loading" class="flex justify-start">
          <div class="w-7 h-7 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-[10px] font-bold shrink-0 mt-1 mr-2">AI</div>
          <div class="bg-white border border-gray-200/60 rounded-[18px] rounded-bl-[4px] px-4 py-3 shadow-sm">
            <div class="flex gap-1.5">
              <span class="w-2 h-2 rounded-full bg-gray-300 animate-bounce" style="animation-delay:0ms"></span>
              <span class="w-2 h-2 rounded-full bg-gray-300 animate-bounce" style="animation-delay:150ms"></span>
              <span class="w-2 h-2 rounded-full bg-gray-300 animate-bounce" style="animation-delay:300ms"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="shrink-0 border-t border-gray-100 p-3 bg-white">
        <div class="flex items-center gap-2">
          <input v-model="input" @keydown.enter="send(input)"
            placeholder="问一句试试..."
            maxlength="200"
            :disabled="loading"
            class="flex-1 px-4 py-2.5 text-sm bg-gray-50 border border-gray-200/60 rounded-full focus:outline-none focus:ring-2 focus:ring-[var(--brand)]/20 focus:border-[var(--brand-light)] transition-all placeholder:text-gray-400 disabled:opacity-50">
          <button @click="send(input)" :disabled="!input.trim() || loading"
            class="w-10 h-10 rounded-full bg-[var(--brand)] text-white flex items-center justify-center shrink-0 disabled:opacity-40 hover:bg-[var(--brand-dark)] transition-all shadow-sm">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL || '/api' })

const open = ref(false)
const input = ref('')
const messages = ref([])
const loading = ref(false)
const msgContainer = ref(null)

const suggestions = ['推荐免费的 AI 绘画工具', '哪个代码助手好用？', '帮我推荐视频生成工具']

function renderMarkdown(text) {
  // Simple markdown rendering
  let html = text
    .replace(/### (.+)/g, '<strong>$1</strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank" rel="noopener" class="text-[var(--brand)] underline">$1</a>')
    .replace(/\n/g, '<br>')
  return html
}

async function send(text) {
  const msg = (text || input.value).trim()
  if (!msg || loading.value) return

  input.value = ''
  messages.value.push({ role: 'user', content: msg })
  loading.value = true

  try {
    const res = await api.post('/agent/chat', { message: msg })
    messages.value.push({ role: 'assistant', content: res.data.response })
  } catch {
    messages.value.push({ role: 'assistant', content: '网络开小差了，稍后再试试～' })
  } finally {
    loading.value = false
  }

  await nextTick()
  if (msgContainer.value) {
    msgContainer.value.scrollTop = msgContainer.value.scrollHeight
  }
}

watch(open, async () => {
  await nextTick()
  if (msgContainer.value) {
    msgContainer.value.scrollTop = msgContainer.value.scrollHeight
  }
})
</script>

<style scoped>
.animate-slide-up {
  animation: slideUp 0.25s ease-out;
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(16px) scale(0.96); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
</style>
