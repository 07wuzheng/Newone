<template>
  <div class="min-h-screen flex flex-col" style="background: var(--surface);">
    <NavBar />
    <div class="flex-1 w-full max-w-[1520px] mx-auto">
      <div class="grid grid-cols-1 xl:grid-cols-[1fr_300px] gap-0 xl:gap-8">
        <main class="min-w-0">
          <RouterView v-slot="{ Component }">
            <Transition name="page" mode="out-in">
              <component :is="Component" />
            </Transition>
          </RouterView>
        </main>
        <SideBar class="hidden xl:block pt-8 sticky top-20 max-h-[calc(100vh-6rem)] overflow-y-auto" />
      </div>
    </div>
    <FooterBar />
    <ChatBot />
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
import FooterBar from './components/FooterBar.vue'
import SideBar from './components/SideBar.vue'
import ChatBot from './components/ChatBot.vue'
</script>
