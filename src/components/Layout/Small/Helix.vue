<template>
  <div class="helix-container">
    <canvas
      ref="canvasRef"
      :width="canvasWidth"
      :height="canvasHeight"
      class="helix-canvas"
      @mousemove="onMouseMove"
    />
    
    <!-- Debug Info (可選，開發時使用) -->
    <div v-if="showDebug" class="debug-info">
      <p>Animation: {{ currentAnimation }}</p>
      <p>Amplitude: {{ amplitude.toFixed(2) }}</p>
      <p>HelixFactor: {{ helixFactor.toFixed(2) }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { gsap } from 'gsap'

// ============ Props & Emits ============
const props = defineProps({
  showDebug: { type: Boolean, default: false }
})

// ============ Canvas Setup ============
const canvasRef = ref(null)
const canvasWidth = 1920
const canvasHeight = 1080
let ctx = null
let animationId = null

// ============ 3D Parameters ============
const helixFactor = ref(0.5)
const scale = ref(80)
const speed = ref(3)
const amplitude = ref(2)
const opacity = ref(0)  // For fade in/out
const constant = ref(0) // 振幅修正參數，控制一端的振幅是否為0

// ============ Rotation Angles ============
const rotationX = ref(0)
const rotationY = ref(0)
const rotationZ = ref(0)

// ============ Animation State ============
const time = ref(0)
const currentAnimation = ref('')
const isAnimating = ref(false)
const isInitialized = ref(false)

// ============ Matrix Operations ============
const rotateXMatrix = (angle) => [
  [1, 0, 0],
  [0, Math.cos(angle), -Math.sin(angle)],
  [0, Math.sin(angle), Math.cos(angle)]
]

const rotateYMatrix = (angle) => [
  [Math.cos(angle), 0, Math.sin(angle)],
  [0, 1, 0],
  [-Math.sin(angle), 0, Math.cos(angle)]
]

const rotateZMatrix = (angle) => [
  [Math.cos(angle), -Math.sin(angle), 0],
  [Math.sin(angle), Math.cos(angle), 0],
  [0, 0, 1]
]

const multiplyMatrices = (a, b) => {
  const result = []
  for (let i = 0; i < 3; i++) {
    result[i] = []
    for (let j = 0; j < 3; j++) {
      result[i][j] = 0
      for (let k = 0; k < 3; k++) {
        result[i][j] += a[i][k] * b[k][j]
      }
    }
  }
  return result
}

const rotatePoint = (point, matrix) => {
  const [x, y, z] = point
  return [
    matrix[0][0] * x + matrix[0][1] * y + matrix[0][2] * z,
    matrix[1][0] * x + matrix[1][1] * y + matrix[1][2] * z,
    matrix[2][0] * x + matrix[2][1] * y + matrix[2][2] * z
  ]
}

// ============ Projection ============
const project3DTo2D = (point) => {
  const [x, y, z] = point
  return [
    canvasWidth / 2 + x * scale.value,
    canvasHeight / 2 - y * scale.value
  ]
}

// ============ Helix Generation ============
const generateHelixPoints = () => {
  const points = []
  const tMin = -16
  const tMax = 12
  const step = 0.08
  
  for (let t = tMin; t <= tMax; t += step) {
    // 中文解釋：當 constant=1，會造成一端振幅被固定為0，另一端正常振盪
    let amplitudeValue = amplitude.value - (constant.value * amplitude.value * (t - 12))
    const x = amplitudeValue * Math.cos(t + time.value * 0.01 * speed.value)
    const y = amplitudeValue * Math.sin(t + time.value * 0.01 * speed.value)
    const z = t * helixFactor.value / 2
    points.push([x, y, z])
  }
  return points
}

// ============ Rendering ============
const drawAxes = (rotationMatrix) => {
  const axisLength = 3
  const axes = [
    [[0, 0, 0], [axisLength, 0, 0], 'rgba(255,255,255,0.3)'],
    [[0, 0, 0], [0, axisLength, 0], 'rgba(255,255,255,0.3)'],
    [[0, 0, 0], [0, 0, axisLength], 'rgba(255,255,255,0.3)']
  ]
  
  ctx.lineWidth = 2
  axes.forEach(([start, end, color]) => {
    const rotatedStart = rotatePoint(start, rotationMatrix)
    const rotatedEnd = rotatePoint(end, rotationMatrix)
    const [x1, y1] = project3DTo2D(rotatedStart)
    const [x2, y2] = project3DTo2D(rotatedEnd)
    ctx.strokeStyle = color
    ctx.globalAlpha = opacity.value * 0.7
    ctx.beginPath()
    ctx.moveTo(x1, y1)
    ctx.lineTo(x2, y2)
    ctx.stroke()
  })
}

const drawHelix = () => {
  if (!ctx) return
  ctx.clearRect(0, 0, canvasWidth, canvasHeight)
  const points3D = generateHelixPoints()

  // 3D 旋轉矩陣合併
  let combinedMatrix = multiplyMatrices(
    multiplyMatrices(rotateZMatrix(rotationZ.value), rotateYMatrix(rotationY.value)),
    rotateXMatrix(rotationX.value)
  )

  const points2D = points3D.map(point => {
    const rotatedPoint = rotatePoint(point, combinedMatrix)
    return project3DTo2D(rotatedPoint)
  })

  //drawAxes(combinedMatrix)

  if (points2D.length > 1) {
    ctx.strokeStyle = '#F7C71F'
    ctx.lineWidth = 2.5
    ctx.globalAlpha = opacity.value
    ctx.shadowColor = '#F7C71F'
    ctx.shadowBlur = 4
    ctx.beginPath()
    points2D.forEach(([x, y], i) => {
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    })
    ctx.stroke()
    ctx.shadowBlur = 0
    ctx.globalAlpha = 1
  }
}

// ============ Animation Functions ============

// 初始化動畫
const initializeHelix = async () => {
  if (isInitialized.value) return
  currentAnimation.value = 'Initializing...'
  scale.value = 0
  opacity.value = 0
  await new Promise(resolve => gsap.to(opacity, { duration: 1.5, value: 1, ease: "power2.out", onComplete: resolve }))
  await new Promise(resolve => gsap.to(scale, { duration: 2, value: 120, ease: "elastic.out(1, 0.4)", onComplete: resolve }))
  isInitialized.value = true
  currentAnimation.value = ''
}

// 動畫一：彈簧旋轉
const animation1_SpringRotation = async () => {
  currentAnimation.value = 'Spring Rotation with Bounce'
  await new Promise(resolve => {
    const tl = gsap.timeline({ onComplete: resolve })
    tl.to(rotationX, { duration: 3, value: Math.PI * 2, ease: "bounce.out" }, 0)
    tl.to(rotationZ, { duration: 3, value: Math.PI * 2, ease: "elastic.out(1, 0.3)" }, 0)
    tl.to(scale, { duration: 1, value: 150, ease: "power2.out", repeat: 2, yoyo: true }, 2)
    tl.to(scale, { duration: 1, value: 100, ease: "power2.out", repeat: 2, yoyo: true }, 2)
  })
}

// 動畫二：轉側面並切換振幅函數
const animation4_SideViewAmplitudeFunctions = async () => {
  currentAnimation.value = 'Side View with Amplitude change'
  await new Promise(resolve => {
    const tl = gsap.timeline({ onComplete: resolve })
    tl.to(rotationY, { duration: 1, value: Math.PI / 6, ease: "power2.inOut" }, 0)
  })

  await new Promise(resolve => {
    const tl = gsap.timeline({ onComplete: resolve })
    tl.to(constant, { duration: 3, value: 1, ease: "power3.out" }, 0)
    tl.to(scale, { duration: 3, value: 10, ease: "power3.out" }, 0)
    tl.to(helixFactor, { duration: 3, value: 5, ease: "power3.out" }, 0)
    tl.to(speed, { duration: 3, value: 6, ease: "power3.out" }, 0)

  })
}
// 動畫三：消失至無限放大
const animation5_SwirlExpansion = async () => {
  currentAnimation.value = 'Swirl Expansion to Infinity'
  await new Promise(resolve => {
    const tl = gsap.timeline({ onComplete: resolve })
    // 回到軸心視角
    tl.to(rotationX, { duration: 2, value: 0, ease: "none" }, 0)
      .to(rotationY, { duration: 2, value: 0, ease: "none" }, 1)
      .to(rotationZ, { duration: 1.5, value: 0, ease: "none" }, 2)
      
      // 創造戲劇性的漩渦效果
      .to(rotationZ, { duration: 4, value: Math.PI*4.5, ease: "power2.out" }, 3)
      
      // 多層次的縮放效果 - 先收縮再爆炸式放大
      .to(scale, { duration: 1, value: 50, ease: "power2.in" }, 3)
      .to(scale, { duration: 2, value: 200, ease: "expo.out" }, 4)
      
      // 螺旋密度變化 - 創造更密集的漩渦
      .to(helixFactor, { duration: 3, value: 0.1, ease: "power3.out" }, 3.5)
      
      // 速度變化 - 創造加速旋轉效果
      //.to(speed, { duration: 2, value: 12, ease: "expo.out" }, 3)
      //.to(speed, { duration: 2, value: 2, ease: "power2.out" }, 4)
      
      // 振幅的波動效果 - 創造呼吸感
      .to(amplitude, { duration: 1.5, value: 2.5, ease: "power2.out" }, 3)
      .to(amplitude, { duration: 1.5, value: 1, ease: "power2.in" }, 4.5)
      
      // 漸隱效果延後開始，創造更戲劇性的消失
      .to(opacity, { duration: 2, value: 0, ease: "power2.in" }, 4)
  })
}

// 總動畫流程
const startAnimation = async () => {
  if (isAnimating.value) return
  isAnimating.value = true
  try {
    await initializeHelix()
    await animation1_SpringRotation()
    await animation4_SideViewAmplitudeFunctions()
    await animation5_SwirlExpansion()
  } catch (error) {
    console.error('Animation sequence error:', error)
  } finally {
    isAnimating.value = false
    currentAnimation.value = 'Animation Complete'
  }
}

// ============ Utility ============
const resetHelix = () => {
  gsap.killTweensOf([rotationX, rotationY, rotationZ, scale, helixFactor, speed, amplitude, opacity])
  rotationX.value = 0
  rotationY.value = 0
  rotationZ.value = 0
  scale.value = 120
  helixFactor.value = 0.5
  speed.value = 1
  amplitude.value = 1
  opacity.value = 1
  currentAnimation.value = ''
  isAnimating.value = false
  isInitialized.value = true
}

const onMouseMove = (event) => {
  const rect = canvasRef.value.getBoundingClientRect()
  mouseX.value = event.clientX - rect.left
  mouseY.value = event.clientY - rect.top
}

// ============ Animation Loop ============
const animate = () => {
  time.value += 1
  drawHelix()
  animationId = requestAnimationFrame(animate)
}

// ============ Lifecycle ============
onMounted(async () => {
  await nextTick()
  ctx = canvasRef.value.getContext('2d')
  animate()
})

onUnmounted(() => {
  if (animationId) cancelAnimationFrame(animationId)
  gsap.killTweensOf([rotationX, rotationY, rotationZ, scale, helixFactor, speed, amplitude, opacity])
})

// ============ Expose Methods ============
defineExpose({
  startAnimation,
  resetHelix,
  initializeHelix
})
</script>


<style scoped>
.helix-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.helix-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: transparent;
  pointer-events: all;
  z-index: 10;
}

.debug-info {
  position: absolute;
  top: 20px;
  left: 20px;
  background: rgba(0, 0, 0, 0.7);
  color: #F7C71F;
  padding: 10px;
  border-radius: 5px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  line-height: 1.4;
  z-index: 20;
  pointer-events: none;
}

.debug-info p {
  margin: 0;
}
</style>