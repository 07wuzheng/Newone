import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Home', component: () => import('./views/HomePage.vue') },
  { path: '/category/:slug', name: 'Category', component: () => import('./views/CategoryPage.vue') },
  { path: '/tool/:id', name: 'ToolDetail', component: () => import('./views/ToolDetailPage.vue') },
  { path: '/search', name: 'Search', component: () => import('./views/SearchPage.vue') },
  { path: '/submit', name: 'Submit', component: () => import('./views/SubmitPage.vue') },
  { path: '/about', name: 'About', component: () => import('./views/AboutPage.vue') },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('./views/NotFound.vue') },
]

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})
