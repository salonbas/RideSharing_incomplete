<template>
  <div class="wave-animation-container">
    <canvas 
      ref="canvas" 
      :width="canvasWidth" 
      :height="canvasHeight"
      @mousemove="handleMouseMove"
      @mouseleave="handleMouseLeave"
    ></canvas>
    <div class="left-mask"></div>
    <div class="right-mask"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'

const baseAmplitude = ref(20)
const mouseAmplitudeMultiplier = ref(2)
const animationSpeed = ref(1)
const frequency = ref(0.015)

const canvas = ref(null)
const canvasWidth = ref(0)
const canvasHeight = ref(0)
const currentWaveCount = ref(1)
const animationId = ref(null)
const time = ref(0)
const mouseX = ref(0)
const mouseY = ref(0)
const isMouseOver = ref(false)

const waveConfigs = [
  { color: '#FFD700', thickness: 1.2, amplitudeFunction: 'smooth', always: true },
  { color: '#4A90E2', thickness: 0.9, amplitudeFunction: 'quadratic', always: false },
  { color: '#FFFFFF', thickness: 0.9, amplitudeFunction: 'cubic', always: false }
]

const amplitudeFunctions = {
  smooth: (normX) => normX * normX * (3 - 2 * normX),
  quadratic: (normX) => normX * normX,
  cubic: (normX) => normX * normX * normX
}

let waveTimer = null
const startWaveTimer = () => {
  const updateWaveCount = () => {
    const count = currentWaveCount.value
    if (count === 1) {
      currentWaveCount.value++
      waveTimer = setTimeout(updateWaveCount, 1000)
    } else if (count === 2) {
      const delta = Math.random() > 0.5 ? 1 : -1
      currentWaveCount.value = Math.min(3, Math.max(1, count + delta))
      waveTimer = setTimeout(updateWaveCount, 3000)
    } else if (count === 3) {
      currentWaveCount.value--
      waveTimer = setTimeout(updateWaveCount, 2000)
    }
  }
  updateWaveCount()
}

const handleMouseMove = (event) => {
  const rect = canvas.value.getBoundingClientRect()
  mouseX.value = event.clientX - rect.left
  mouseY.value = event.clientY - rect.top
  isMouseOver.value = true
}
const handleMouseLeave = () => {
  isMouseOver.value = false
}

const updateCanvasSize = () => {
  if (!canvas.value) return
  const viewportWidth = window.innerWidth
  const viewportHeight = window.innerHeight
  canvasWidth.value = Math.floor(viewportWidth * 0.2)
  canvasHeight.value = Math.floor(viewportHeight * 0.12)
  canvasWidth.value = Math.max(canvasWidth.value, 100)
  canvasHeight.value = Math.max(canvasHeight.value, 60)
}

const drawWaves = () => {
  if (!canvas.value) return
  const ctx = canvas.value.getContext('2d')
  const width = canvasWidth.value
  const height = canvasHeight.value
  const centerY = height / 2

  ctx.clearRect(0, 0, width, height)
  ctx.globalAlpha = 0.9  // 整體透明度再高一點

  for (let i = 0; i < currentWaveCount.value; i++) {
    const config = waveConfigs[i]
    const theta = (i * Math.PI * 2) / currentWaveCount.value
    const freq = 0.01 + i * 0.001
    const amplitudeFunction = amplitudeFunctions[config.amplitudeFunction]

    let mouseInfluence = 1
    if (isMouseOver.value) {
      const dist = Math.sqrt(Math.pow(mouseX.value - width/2, 2) + Math.pow(mouseY.value - centerY, 2))
      mouseInfluence = 1 + Math.exp(-dist / (width * 0.3)) * mouseAmplitudeMultiplier.value
    }

    ctx.strokeStyle = config.color
    ctx.lineCap = 'round'
    ctx.lineJoin = 'round'
    ctx.beginPath()

    for (let x = 0; x <= width; x += 1) {
      const normX = x / width

      // 改良版振幅函數：左邊拉升快、右邊 soft cap
      let ampNorm = Math.pow(normX, 0.8)
      ampNorm = amplitudeFunction(ampNorm)
      ampNorm *= 0.3 + 0.7 * normX

      let ampScale = ampNorm * baseAmplitude.value * mouseInfluence

      // 右半邊 soft limit，避免太高
      if (normX > 0.5) {
        const softFactor = 1 - (normX - 0.5) * 0.3
        ampScale *= Math.max(softFactor, 0.7)
      }

      // 最終防止超出畫布
      ampScale = Math.min(ampScale, height * 0.45)

      const y = ampScale * Math.sin(freq * x + theta - time.value * 0.005 * animationSpeed.value) + centerY

      const edgeFactor = 1 - Math.abs((x - width / 2) / (width / 2))
      const dynamicThickness = config.thickness * (0.7 + 0.3 * edgeFactor)
      ctx.lineWidth = dynamicThickness

      if (x === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }

    ctx.stroke()
  }
}

const animate = () => {
  time.value += 16
  drawWaves()
  animationId.value = requestAnimationFrame(animate)
}

onMounted(async () => {
  await nextTick()
  updateCanvasSize()
  window.addEventListener('resize', updateCanvasSize)
  startWaveTimer()
  animate()
})

onUnmounted(() => {
  if (animationId.value) cancelAnimationFrame(animationId.value)
  if (waveTimer) clearTimeout(waveTimer)
  window.removeEventListener('resize', updateCanvasSize)
})

defineExpose({
  baseAmplitude, mouseAmplitudeMultiplier, animationSpeed, frequency
})
</script>

<style scoped>
.wave-animation-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 9999;
  pointer-events: none;
}

canvas {
  pointer-events: auto;
  background: transparent;
  display: block;
  position: relative;
  z-index: 1;
}

.left-mask {
  position: absolute;
  top: 0;
  left: 0;
  width: 8%;
  height: 100%;
  background: linear-gradient(to left, transparent, rgba(0,0,0,0.2));
  pointer-events: none;
  z-index: 2;
}

.right-mask {
  position: absolute;
  top: 0;
  right: 0;
  width: 25%;
  height: 100%;
  background: linear-gradient(to right, transparent, rgba(0,0,0,0.5));
  pointer-events: none;
  z-index: 2;
}
</style>
