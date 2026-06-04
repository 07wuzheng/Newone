<template>
  <div class="max-w-2xl mx-auto px-4 py-8">
    <h1 class="text-2xl sm:text-4xl font-bold tracking-tight text-[var(--text-primary)] mb-2">提交工具</h1>
    <p class="text-[var(--text-secondary)] mb-8">推荐你发现的 AI 工具，审核后将会展示在平台上</p>

    <!-- 成功提示 -->
    <div v-if="submitted" class="bg-emerald-50/80 backdrop-blur-sm border border-emerald-200/60 rounded-[var(--radius-md)] p-8 text-center mb-8">
      <div class="text-5xl mb-4">🎉</div>
      <h2 class="text-xl font-semibold text-emerald-800 mb-2">提交成功！</h2>
      <p class="text-emerald-600 mb-5">感谢推荐，审核通过后将会展示在平台上</p>
      <button @click="resetForm" class="text-sm font-medium text-[var(--brand)] hover:underline">再提交一个</button>
    </div>

    <!-- 网络错误 -->
    <div v-else-if="networkError" class="bg-red-50/80 backdrop-blur-sm border border-red-200/60 rounded-[var(--radius-md)] px-5 py-3 mb-6">
      <p class="text-red-700 text-sm">{{ networkError }}</p>
    </div>

    <!-- 表单 -->
    <form v-else @submit.prevent="handleSubmit" class="card-white bg-white rounded-[var(--radius-lg)] border border-[var(--border-subtle)] shadow-[var(--shadow-sm)] p-6 sm:p-8 space-y-6" :class="{ shake: shaking }">
      <!-- 工具名称 -->
      <div>
        <label class="block text-sm font-medium text-[var(--text-primary)] mb-1.5">工具名称 <span class="text-red-400">*</span></label>
        <input v-model="form.name" type="text" maxlength="100" placeholder="例如：ChatGPT"
          class="w-full px-4 py-2.5 bg-white border rounded-[var(--radius-sm)] text-[var(--text-primary)] placeholder-[var(--text-tertiary)] focus:outline-none focus:ring-2 focus:ring-[var(--brand)]/20 focus:border-[var(--brand-light)] transition-all"
          :class="errors.name ? 'border-red-300' : 'border-gray-200/80'" />
        <p v-if="errors.name" class="text-red-500 text-xs mt-1.5">{{ errors.name }}</p>
      </div>

      <!-- 工具描述 -->
      <div>
        <label class="block text-sm font-medium text-[var(--text-primary)] mb-1.5">工具描述 <span class="text-red-400">*</span></label>
        <textarea v-model="form.description" rows="4" maxlength="500" placeholder="简单介绍这个工具的功能和特点"
          class="w-full px-4 py-2.5 bg-white border rounded-[var(--radius-sm)] text-[var(--text-primary)] placeholder-[var(--text-tertiary)] focus:outline-none focus:ring-2 focus:ring-[var(--brand)]/20 focus:border-[var(--brand-light)] transition-all resize-none"
          :class="errors.description ? 'border-red-300' : 'border-gray-200/80'"></textarea>
        <div class="flex justify-between mt-1.5">
          <p v-if="errors.description" class="text-red-500 text-xs">{{ errors.description }}</p>
          <p v-else></p>
          <p class="text-xs text-[var(--text-tertiary)]">{{ form.description.length }}/500</p>
        </div>
      </div>

      <!-- 官网链接 -->
      <div>
        <label class="block text-sm font-medium text-[var(--text-primary)] mb-1.5">官网链接 <span class="text-red-400">*</span></label>
        <input v-model="form.url" type="url" placeholder="https://example.com"
          class="w-full px-4 py-2.5 bg-white border rounded-[var(--radius-sm)] text-[var(--text-primary)] placeholder-[var(--text-tertiary)] focus:outline-none focus:ring-2 focus:ring-[var(--brand)]/20 focus:border-[var(--brand-light)] transition-all"
          :class="errors.url ? 'border-red-300' : 'border-gray-200/80'" />
        <p v-if="errors.url" class="text-red-500 text-xs mt-1.5">{{ errors.url }}</p>
      </div>

      <!-- 分类 -->
      <div>
        <label class="block text-sm font-medium text-[var(--text-primary)] mb-1.5">所属分类 <span class="text-red-400">*</span></label>
        <select v-model="form.category_id"
          class="w-full px-4 py-2.5 bg-white border rounded-[var(--radius-sm)] text-[var(--text-primary)] focus:outline-none focus:ring-2 focus:ring-[var(--brand)]/20 focus:border-[var(--brand-light)] transition-all appearance-none"
          :class="errors.category_id ? 'border-red-300' : 'border-gray-200/80'">
          <option value="" disabled>{{ catStore.loading ? '加载中...' : '请选择分类' }}</option>
          <option v-for="cat in catStore.categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
        </select>
        <p v-if="errors.category_id" class="text-red-500 text-xs mt-1.5">{{ errors.category_id }}</p>
      </div>

      <button type="submit" :disabled="toolStore.submitting"
        class="w-full font-semibold text-white bg-[var(--brand)] hover:bg-[var(--brand-dark)] py-3 rounded-[var(--radius-sm)] transition-all disabled:opacity-60 disabled:cursor-not-allowed shadow-[var(--shadow-sm)] hover:shadow-[0_4px_12px_rgba(79,70,229,0.35)] hover:-translate-y-0.5 flex items-center justify-center gap-2">
        <span v-if="toolStore.submitting" class="spinner"></span>
        <span>{{ toolStore.submitting ? '提交中...' : '提交工具' }}</span>
      </button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { useCategoryStore } from '../stores/categories'
import { useToolStore } from '../stores/tools'

const catStore = useCategoryStore()
const toolStore = useToolStore()

const form = reactive({ name: '', description: '', url: '', category_id: '' })
const errors = reactive({ name: '', description: '', url: '', category_id: '' })
const submitted = ref(false)
const networkError = ref(null)
const shaking = ref(false)

function triggerShake() {
  shaking.value = true
  setTimeout(() => shaking.value = false, 400)
}

onMounted(() => {
  catStore.fetchCategories()
})

function validate() {
  let valid = true
  Object.keys(errors).forEach(k => errors[k] = '')

  if (!form.name || form.name.length < 2) {
    errors.name = '名称至少 2 个字符'
    valid = false
  }
  if (!form.description || form.description.length < 10) {
    errors.description = '描述至少 10 个字符'
    valid = false
  }
  if (!form.url) {
    errors.url = '请输入官网链接'
    valid = false
  } else if (!form.url.startsWith('http://') && !form.url.startsWith('https://')) {
    errors.url = '请输入以 http:// 或 https:// 开头的网址'
    valid = false
  }
  if (!form.category_id) {
    errors.category_id = '请选择分类'
    valid = false
  }

  if (!valid) triggerShake()
  return valid
}

async function handleSubmit() {
  if (!validate()) return
  networkError.value = null

  try {
    await toolStore.submitTool({
      name: form.name,
      description: form.description,
      url: form.url,
      category_id: Number(form.category_id),
    })
    submitted.value = true
  } catch (e) {
    if (e && typeof e === 'object' && !(e instanceof Error)) {
      Object.assign(errors, e)
    } else if (e instanceof Error) {
      networkError.value = e.message
    }
  }
}

function resetForm() {
  form.name = ''
  form.description = ''
  form.url = ''
  form.category_id = ''
  submitted.value = false
  networkError.value = null
}
</script>
