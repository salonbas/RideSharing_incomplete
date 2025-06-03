<template>
  <div class="transition-part" ref="container">
    <div ref="taiwanMapContainer" class="taiwan-layer">
        <TaiwanMap />
      </div>
      <div class="helix-layer">
        <Helix ref="helixRef" />
      </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'
import TaiwanMap from '@/components/Layout/TaiwanMap.vue'
import Helix from '@/components/Layout/Small/Helix.vue'
import { useRouter } from 'vue-router';  

const router = useRouter();  

const helixRef = ref(null)
const container = ref(null)
const taiwanMapContainer = ref(null)

// 可自定義的縮放倍率
const targetScale = ref(2.2) // 你可以改為任何你想要的倍率，如 2、0.8、3 等
const hasNavigated = ref(false) // 防止重複跳轉

onMounted(async () => {
  gsap.set(taiwanMapContainer.value, {
    scale: 0.01,
    opacity: 0
  })


  const observer = new IntersectionObserver(async (entries) => {
      
    if (entries[0].isIntersecting && !hasNavigated.value) {
      
    alert("start")
    helixRef.value?.$el?.scrollIntoView({
      behavior: 'smooth',
      block: 'center'
    });
    
    // 這邊等待 Helix 動畫流程完整執行
    await helixRef.value.initializeHelix()  // 初始化
    await helixRef.value.startAnimation()   // 全動畫序列執行
      // 放大到指定倍率的動畫
      gsap.to(taiwanMapContainer.value, {
        scale: targetScale.value,
        opacity: 1,
        duration: 2,
        ease: 'power3.out',
        onComplete: () => {
          // 動畫完成後跳轉
          hasNavigated.value = true
          router.push({ name: 'events' });
        }
      })
    } else if (!entries[0].isIntersecting && !hasNavigated.value) {
      // 縮小動畫
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

// 如果需要從外部設定縮放倍率
const setTargetScale = (scale) => {
  targetScale.value = scale
}

// 暴露方法供父組件使用
defineExpose({
  setTargetScale
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

.helix-layer {
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
}

</style>