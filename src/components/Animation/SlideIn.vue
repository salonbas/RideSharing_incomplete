<!-- SlideIn.vue -->
<template>
  <div
    ref="el"
    class="transition-all duration-700 ease-out"
    :class="inView ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-12'"
  >
    <slot />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const el = ref(null)
const inView = ref(false)
let observer = null

onMounted(() => {
  observer = new IntersectionObserver(([entry]) => {
    inView.value = entry.isIntersecting
  }, { threshold: 0.3 })

  if (el.value) observer.observe(el.value)
})

onBeforeUnmount(() => {
  if (observer && el.value) observer.unobserve(el.value)
})
</script>
