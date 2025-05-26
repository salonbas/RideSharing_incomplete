<template>
  <div class="introduction-part" ref="container">
    <div class="line" v-for="(line, index) in lines" :key="index" :ref="setLineRef">
      {{ line }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'

// 預留句子內容，可隨時更改
const lines = [
  "This is a reserved line.",
  "Another bold statement.",
  "Nothing too fancy yet."
]

const container = ref(null)
const lineRefs = ref([])

// 註冊 ref
const setLineRef = el => {
  if (el) lineRefs.value.push(el)
}

onMounted(() => {
  const revealLine = index => {
    gsap.to(lineRefs.value[index], {
      opacity: 1,
      y: 0,
      duration: 0.6,
      ease: 'power2.out'
    })
  }

  const hideLine = index => {
    gsap.to(lineRefs.value[index], {
      opacity: 0,
      y: 40,
      duration: 0.4,
      ease: 'power2.in'
    })
  }

  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        const containerTop = entry.boundingClientRect.top
        const viewportHeight = window.innerHeight

        const scrolled = viewportHeight - containerTop
        const perLine = 80 // 每行 80px 範圍觸發動畫

        lineRefs.value.forEach((el, i) => {
          if (scrolled > i * perLine + 20) {
            revealLine(i)
          } else {
            hideLine(i)
          }
        })
      })
    },
    {
      threshold: 0,
    }
  )

  if (container.value) observer.observe(container.value)
})
</script>

<style scoped>
.introduction-part {
  width: 100%;
  height: 200vh; /* 給足夠的高度測試滾動 */
  background-color: #12150e;
  color: #d1ad44;
  font-family: 'Unbounded', sans-serif;
  padding: 20vh 10vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.line {
  font-size: 6rem;
  font-weight: 700;
  line-height: 1.2;
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.3s ease, transform 0.3s ease;
}
</style>