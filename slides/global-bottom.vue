<template>
  <div class="slide-meta">
    <span v-if="section" class="section-ref">{{ section }}</span>
    <span class="slide-no">{{ currentPage }} / {{ total }}</span>
  </div>
  <div v-if="!frontmatter.bigQr" class="qr-corner">
    <QrPair />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useNav } from '@slidev/client'
import QrPair from './components/QrPair.vue'

// Крупные QR стоят прямо на титуле и последнем слайде; на остальных — компактно в углу.
// section — раздел методички, к которому относится слайд; рядом — номер слайда.
const { currentSlideRoute, currentPage, total } = useNav()
const frontmatter = computed(() => currentSlideRoute.value?.meta?.slide?.frontmatter ?? {})
const section = computed(() => frontmatter.value.section)
</script>

<style scoped>
.qr-corner {
  position: absolute;
  right: 12px;
  bottom: 8px;
  z-index: 20;
}
.slide-meta {
  position: absolute;
  right: 150px;
  bottom: 14px;
  z-index: 20;
  display: flex;
  align-items: center;
  gap: 10px;
}
.section-ref {
  padding: 2px 10px;
  border-radius: 999px;
  border: 1.5px solid var(--dg-green, #56ff71);
  background: rgba(3, 14, 34, 0.86);
  color: #eaffff;
  font-size: 12px;
  font-weight: 400;
}
.slide-no {
  padding: 3px 12px;
  border-radius: 999px;
  background: rgba(3, 14, 34, 0.86);
  color: #eaffff;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.02em;
}
</style>
