<template>
  <div class="transition-part" ref="container">
    <div class="content">
    </div>

    <!-- TaiwanMap 組件 -->
    <div ref="taiwanMapContainer">
      <TaiwanMap />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'
import TaiwanMap from '@/components/Layout/TaiwanMap.vue'

const container = ref(null)
const taiwanMapContainer = ref(null)

onMounted(() => {
  gsap.set(taiwanMapContainer.value, {
    scale: 0.01,
    opacity: 0
  })

  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      gsap.to(taiwanMapContainer.value, {
        scale: 1.5,
        opacity: 1,
        duration: 2.5,
        ease: 'power3.out'
      })
    } else {
      gsap.to(taiwanMapContainer.value, {
        scale: 0.01,
        opacity: 0,
        duration: 1.2,
        ease: 'power3.in'
      })
    }
  }, { threshold: 0.3 })

  observer.observe(container.value)
})
</script>

<style scoped>
.transition-part {
  position: relative;
  background-color: #12150e;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  position: absolute;
  top: 10%;
  color: white;
  text-align: center;
  z-index: 1;
}
</style>