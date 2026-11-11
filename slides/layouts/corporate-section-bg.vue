<template>
  <div class="slidev-layout corporate-section-bg">
    <img
      v-if="showLogo"
      :src="logoSrc"
      class="corporate-logo"
      alt=""
    />
    <div class="section-content">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
const logoSrc = '/image32.png'
const showLogo = ref(false)
onMounted(() => {
  const img = new Image()
  img.onerror = () => { showLogo.value = false }
  img.onload = () => { showLogo.value = true }
  img.src = logoSrc
})
</script>

<style scoped>
/* image20.jpeg — яркий бирюзово-голубой (оригинальный разделительный фон Сбера).
   Тёмный оверлей обеспечивает читаемость белого текста. */
.corporate-section-bg {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 2rem;
  background: url('/image20.jpeg') center / cover no-repeat !important;
  position: relative;
}

.corporate-section-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.40);
  z-index: 0;
}

.corporate-logo {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  height: 2.5rem;
  width: auto;
  object-fit: contain;
  z-index: 2;
}

.section-content {
  position: relative;
  z-index: 1;
}

.section-content :deep(h1),
.section-content :deep(h2) {
  font-size: 2.5rem;
  font-weight: 600;
  color: #ffffff !important;
}
</style>
