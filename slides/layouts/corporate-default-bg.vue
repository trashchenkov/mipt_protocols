<template>
  <div class="slidev-layout corporate-default-bg">
    <img
      v-if="showLogo"
      :src="logoSrc"
      class="corporate-logo"
      alt=""
    />
    <div class="slide-content">
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
/* image8.jpg — тёмный слева, яркий бирюзовый справа (контентный фон).
   Псевдоэлемент ::before затемняет светлую правую часть для читаемости белого текста. */
.corporate-default-bg {
  padding: 2rem 3rem 2rem 2rem;
  background: url('/image8.jpg') center / cover no-repeat !important;
  position: relative;
}

.corporate-default-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to right,
    rgba(0, 0, 0, 0.10) 0%,
    rgba(0, 0, 0, 0.35) 50%,
    rgba(0, 0, 0, 0.55) 80%,
    rgba(0, 0, 0, 0.50) 100%
  );
  z-index: 0;
  pointer-events: none;
}

.corporate-logo {
  position: absolute;
  top: 1rem;
  right: 1.5rem;
  height: 2rem;
  width: auto;
  object-fit: contain;
  z-index: 2;
}

.slide-content {
  position: relative;
  z-index: 1;
  padding-right: 1rem;
}

.slide-content :deep(h1),
.slide-content :deep(h2) {
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 0.75em;
}

.slide-content :deep(p),
.slide-content :deep(li) {
}

.slide-content :deep(ul),
.slide-content :deep(ol) {
  padding-left: 1.5em;
}

.slide-content :deep(li) {
  margin-bottom: 0.35em;
}
</style>
