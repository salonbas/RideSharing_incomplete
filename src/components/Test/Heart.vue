<template>
  <svg ref="svgRef" class="w-full h-full absolute top-0 left-0 pointer-events-none">
    <g v-for="(line, lineIndex) in circleLines" :key="lineIndex">
      <circle
        v-for="(point, pointIndex) in line"
        :key="pointIndex"
        :cx="point.x"
        :cy="point.y"
        :r="RADIUS"
        fill="none"
        stroke="white"
        stroke-width="1.5"
      />
    </g>
  </svg>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const svgRef = ref(null)
const circleLines = ref([])

const RADIUS = 6               // 半徑
const DIAMETER = RADIUS * 2    // 圓之間距離
const LINES = 5                // 波紋條數
const POINTS_PER_LINE = 60     // 每條線幾個圓
const AMPLITUDE = 15           // 波動幅度
const FREQ = 0.25              // 波動頻率

let mouseX = 0

onMounted(() => {
  for (let i = 0; i < LINES; i++) {
    circleLines.value.push(new Array(POINTS_PER_LINE).fill({ x: 0, y: 0 }))
  }

  window.addEventListener('mousemove', (e) => {
    mouseX = e.clientX
  })

  let t = 0
  function animate() {
    for (let l = 0; l < LINES; l++) {
      const line = []
      for (let i = 0; i < POINTS_PER_LINE; i++) {
        const x = i * DIAMETER
        const y = 200 + Math.sin(i * FREQ + t + l * 0.4 + mouseX * 0.01) * AMPLITUDE
        line.push({ x, y: y + l * 20 }) // y + 間距下移，避免重疊
      }
      circleLines.value[l] = line
    }
    t += 0.05
    requestAnimationFrame(animate)
  }

  animate()
})
</script>

<style scoped>
svg {
  transition: opacity 0.5s;
}
</style>
