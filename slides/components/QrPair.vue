<template>
  <div class="qr-pair" :class="{ big }">
    <a v-for="item in items" :key="item.key" class="qr-item" :href="item.url" target="_blank">
      <svg :viewBox="`-3 -3 ${item.size + 6} ${item.size + 6}`" :width="px" :height="px" shape-rendering="crispEdges">
        <rect x="-3" y="-3" :width="item.size + 6" :height="item.size + 6" fill="#fff" />
        <path :d="item.d" fill="#071318" />
      </svg>
      <span class="qr-label">{{ item.label }}</span>
    </a>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import paths from './qr_paths.json'

const props = defineProps<{ big?: boolean }>()
const px = computed(() => (props.big ? 132 : 50))
const items = [
  { key: 'repo', label: 'Материалы', ...paths.repo },
  { key: 'channel', label: 'Telegram-канал', ...paths.channel },
]
</script>

<style scoped>
.qr-pair {
  display: flex;
  gap: 10px;
  align-items: flex-start;
}
.qr-pair.big {
  gap: 36px;
  justify-content: center;
}
.qr-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none !important;
  border: 0 !important;
}
.qr-item svg {
  display: block;
  border-radius: 4px;
}
.qr-label {
  margin-top: 3px;
  font-size: 9px;
  line-height: 1;
  color: rgba(255, 255, 255, 0.86);
}
.big .qr-label {
  margin-top: 8px;
  font-size: 15px;
  font-weight: 600;
  color: inherit;
}
</style>
