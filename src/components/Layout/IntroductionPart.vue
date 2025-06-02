<template>
  <div class="introduction-part" ref="container">
    <div 
      class="line" 
      v-for="(line, index) in lines" 
      :key="index" 
      :ref="el => setLineRef(el, index)"
    >
      <span class="text" :ref="el => setTextRef(el, index)"></span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { gsap } from 'gsap'

const lines = [
  "This is a reserved line.",
  "Another bold statement.",
  "Nothing too fancy yet."
]

const container = ref(null)
const lineRefs = ref([])
const textRefs = ref([])

const setLineRef = (el, index) => {
  if (el) lineRefs.value[index] = el
}
const setTextRef = (el, index) => {
  if (el) textRefs.value[index] = el
}

const typeText = (element, text, speed = 0.05) => {
  const chars = text.split('')
  element.textContent = ''
  chars.forEach((char, i) => {
    gsap.delayedCall(i * speed, () => {
      element.textContent += char
    })
  })
}

onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      const containerTop = entry.boundingClientRect.top
      const viewportHeight = window.innerHeight
      const scrolled = viewportHeight - containerTop
      const perLine = window.innerHeight * 0.2 // 每行約佔 20%

      lineRefs.value.forEach((el, i) => {
        if (scrolled > i * perLine + 20) {
          if (!textRefs.value[i].textContent) {
            typeText(textRefs.value[i], lines[i])
          }
        } else {
          textRefs.value[i].textContent = ''
        }
      })
    })
  }, { threshold: 0 })

  if (container.value) observer.observe(container.value)
})
</script>

<style scoped>
.introduction-part {
  height: 200vh;
  background-color: transparent;
  padding: 20vh 10vw;
  color: #d1ad44;
  font-family: 'Unbounded', sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.line {
  font-size: 6rem;
  font-weight: 700;
  line-height: 1.2;
  min-height: 7rem;
}

.text {
  display: inline-block;
  white-space: pre;
}
</style>