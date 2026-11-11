<template>
  <div class="slidev-layout corporate-title-bg">
    <img
      v-if="showLogo"
      :src="logoSrc"
      class="corporate-logo"
      alt=""
    />
    <div class="title-content">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
const logoSrc = ref('/image32.png')
const showLogo = ref(false)
onMounted(() => {
  const img = new Image()
  img.onerror = () => { showLogo.value = false }
  img.onload = () => { showLogo.value = true }
  img.src = logoSrc.value
})
</script>

<style scoped>
/* image39.jpg — светлый зелёно-бирюзовый градиент (оригинальный титульный фон Сбера).
   Текст тёмный, как в оригинальном шаблоне. */
.corporate-title-bg {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 2rem;
  background: url('/image39.jpg') center / cover no-repeat !important;
  color: #0a0a0a !important;
}

.corporate-logo {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  height: 2.5rem;
  width: auto;
  object-fit: contain;
}

.title-content {
  width: 100%;
}

.title-content :deep(h1) {
  font-size: 3rem;
  font-weight: 600;
  margin-bottom: 0.5em;
  color: #0a0a0a !important;
  text-shadow: none;
}

.title-content :deep(h2) {
  color: #1a1a1a !important;
  text-shadow: none;
}

.title-content :deep(p),
.title-content :deep(strong) {
  color: #1a1a1a !important;
  text-shadow: none;
}
</style>
