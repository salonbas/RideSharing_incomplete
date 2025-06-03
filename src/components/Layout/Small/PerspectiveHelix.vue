<template>
  <div class="helix-container" :style="{ opacity: containerOpacity, transform: `scale(${containerScale})` }">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as THREE from 'three'
import { gsap } from 'gsap'

// Emits
const emit = defineEmits(['animationComplete'])

// Refs
const canvas = ref(null)
const containerOpacity = ref(0)
const containerScale = ref(0)

// 動畫參數 - 使用 ref 讓外部可控制
const k = ref(100)
const totalLength = 3 * 2 * Math.PI  
const constant = ref(10)  // 直線振幅
const isAnimating = ref(false)
const rotateSpeed = ref(-0.08)  // 修正為負值
const cameraZ = ref(500)  // 修正初始相機距離
const targetCameraZ = ref(1)  // function3 的目標距離

// Three.js 變數
let scene, camera, renderer, helixYellow, helixBlue, group
let animationId = null

// 振幅函數 - 保持不變
function getAmplitude(t, progress = 1) {
  if (progress === 0) {
    return constant.value
  } else if (progress === 1) {
    return k.value * Math.sqrt(t / totalLength)
  } else {
    const constantAmp = constant.value
    const sqrtAmp = k.value * Math.sqrt(t / totalLength)
    return constantAmp + (sqrtAmp - constantAmp) * progress
  }
}

// 初始化場景
function initScene() {
  scene = new THREE.Scene()
  
  const width = window.innerWidth 
  const height = window.innerHeight 
  
  // 修正相機設置
  camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
  camera.position.z = cameraZ.value  // 從正前方看
  camera.position.x = 0
  camera.position.y = 0
  camera.lookAt(0, 0, 0)  // 朝向場景中心

  renderer = new THREE.WebGLRenderer({ 
    canvas: canvas.value, 
    antialias: true,
    alpha: true
  })
  renderer.setSize(width, height)
  renderer.setPixelRatio(window.devicePixelRatio)
  renderer.setClearColor(0x000000, 0)

  // 添加環境光
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
  scene.add(ambientLight)
  
  // 添加方向光增加立體感
  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
  directionalLight.position.set(1, 1, 1)
  scene.add(directionalLight)
}

// 建立螺旋線 - 保持震幅函數變換部分完全不變
function createHelix(progress = 0) {
  // 清除舊的線條
  if (helixYellow) {
    group.remove(helixYellow)
    helixYellow.geometry.dispose()
    helixYellow.material.dispose()
  }
  if (helixBlue) {
    group.remove(helixBlue)
    helixBlue.geometry.dispose()
    helixBlue.material.dispose()
  }

  const pointsYellow = []
  const pointsBlue = []

  const steps = 30000  // 增加點密度
  const stepSize = totalLength / steps
  
  for (let i = 0; i <= steps; i+=0.1) {
    const t = i * stepSize
    
    const amplitude = getAmplitude(t, progress)
    
    // 第一條螺旋線（黃色）
    const x1 = amplitude * Math.cos(t)
    const y1 = amplitude * Math.sin(t)
    const z1 = t * 6  

    pointsYellow.push(new THREE.Vector3(x1, y1, z1))

    // 第二條螺旋線（藍色），相位差 π
    const x2 = amplitude * Math.cos(t + Math.PI)
    const y2 = amplitude * Math.sin(t + Math.PI)
    const z2 = z1

    pointsBlue.push(new THREE.Vector3(x2, y2, z2))
  }

  // 改用細線條並加入螢光效果
  const geometryYellow = new THREE.BufferGeometry().setFromPoints(pointsYellow)
  const materialYellow = new THREE.LineBasicMaterial({ 
    color: 0xffd700,
    transparent: true,
    opacity: 0.9,
    linewidth: 2
  })
  helixYellow = new THREE.Line(geometryYellow, materialYellow)

  const geometryBlue = new THREE.BufferGeometry().setFromPoints(pointsBlue)
  const materialBlue = new THREE.LineBasicMaterial({ 
    color: 0x4488ff,
    transparent: true,
    opacity: 0.8,
    linewidth: 2
  })
  helixBlue = new THREE.Line(geometryBlue, materialBlue)

  // 嘗試加入螢光效果
  helixYellow.material.emissive = new THREE.Color(0x332200)
  helixBlue.material.emissive = new THREE.Color(0x001133)

  if (!group) {
    group = new THREE.Group()
    scene.add(group)
    // 移除初始視角設定，讓相機從正前方看
    group.rotation.x = 0
    group.rotation.y = 0
    group.rotation.z = 0
  }
  
  group.add(helixYellow)
  group.add(helixBlue)
}

// 動畫循環
function animate() {
  if (!renderer || !scene || !camera) return
  
  animationId = requestAnimationFrame(animate)
  
  if (group && !isAnimating.value) {
    group.rotation.z += rotateSpeed.value  // Z軸旋轉
  }
  
  renderer.render(scene, camera)
}

// 淡入效果 - 新增
function fadeIn(duration = 4) {
  return new Promise((resolve) => {
    const timeline = gsap.timeline()
    
    timeline
      .to(containerOpacity, {
        value: 1,
        duration: duration * 0.6,
        ease: "power2.out"
      })
      .to(containerScale, {
        value: 1,
        duration: duration * 0.8,
        ease: "back.out(1.7)"
      }, 0.2)
      .call(() => {
        resolve()
      })
  })
}

// Function 1: 振幅轉換動畫 - 保持完全不變
function function1(durationInSeconds = 2) {
  if (isAnimating.value) return Promise.resolve()
  
  return new Promise((resolve) => {
    isAnimating.value = true
    
    const animationObject = { progress: 0 }
    
    gsap.to(animationObject, {
      progress: 1,
      duration: durationInSeconds,
      ease: "power2.inOut",
      onUpdate: () => {
        createHelix(animationObject.progress)
      },
      onComplete: () => {
        isAnimating.value = false
        emit('animationComplete', 'function1')
        resolve()
      }
    })
  })
}

// Function 2: 直線+X軸旋轉180度
function function2(durationInSeconds = 4) {
  if (isAnimating.value) return Promise.resolve()
  
  return new Promise((resolve) => {
    isAnimating.value = true
    
    // 先將振幅變為直線效果
    const timeline = gsap.timeline()
    
    // 第一階段：變成直線
    const animationObject = { progress: 1 }
    timeline.to(animationObject, {
      progress: 0,
      duration: durationInSeconds * 0.3,
      ease: "power2.inOut",
      onUpdate: () => {
        createHelix(animationObject.progress)
      }
    })
    
    // 第二階段：X軸旋轉180度
    timeline.to(group.rotation, {
      x: group.rotation.x + Math.PI,
      duration: durationInSeconds * 0.7,
      ease: "power2.inOut",
      onComplete: () => {
        isAnimating.value = false
        emit('animationComplete', 'function2')
        resolve()
      }
    })
  })
}

// Function 3: Zoom In 動畫 + 增加自轉速度
function function3(durationInSeconds = 3) {
  if (isAnimating.value) return Promise.resolve()
  
  return new Promise((resolve) => {
    isAnimating.value = true
    
    const startCameraZ = 300  // 更遠的起始距離
    const originalRotateSpeed = rotateSpeed.value
    
    // 設定起始位置
    camera.position.z = startCameraZ
    cameraZ.value = startCameraZ
    
    const animationObject = { 
      cameraZ: startCameraZ,
      rotateSpeedMultiplier: 1
    }
    
    gsap.to(animationObject, {
      cameraZ: targetCameraZ.value,
      rotateSpeedMultiplier: 3, // 增加自轉速度
      duration: durationInSeconds,
      ease: "power3.inOut",
      onUpdate: () => {
        camera.position.z = animationObject.cameraZ
        cameraZ.value = animationObject.cameraZ
        rotateSpeed.value = originalRotateSpeed * animationObject.rotateSpeedMultiplier
      },
      onComplete: () => {
        isAnimating.value = false
        emit('animationComplete', 'function3')
        resolve()
      }
    })
  })
}

// 重置到初始狀態
function resetToInitial() {
  if (isAnimating.value) return
  
  return new Promise((resolve) => {
    // 重置所有參數
    constant.value = 10
    k.value = 20
    cameraZ.value = 100
    rotateSpeed.value = -0.08
    
    // 平滑重置相機位置
    gsap.to(camera.position, {
      z: 100,
      duration: 1,
      ease: "power2.out"
    })
    
    // 重置群組旋轉
    if (group) {
      gsap.to(group.rotation, {
        x: 0,
        y: 0,
        z: 0,
        duration: 1,
        ease: "power2.out",
        onComplete: () => {
          createHelix(0)
          resolve()
        }
      })
    } else {
      createHelix(0)
      resolve()
    }
  })
}

// 視窗大小調整
function handleResize() {
  if (!camera || !renderer) return
  
  const width = window.innerWidth
  const height = window.innerHeight
  
  camera.aspect = width / height
  camera.updateProjectionMatrix()
  renderer.setSize(width, height)
}

// 組件掛載
onMounted(async () => {
  await nextTick()
  initScene()
  createHelix(0)
  animate()
  window.addEventListener('resize', handleResize)
})

// 組件卸載
onUnmounted(() => {
  if (animationId) {
    cancelAnimationFrame(animationId)
  }
  
  window.removeEventListener('resize', handleResize)
  
  if (renderer) {
    renderer.dispose()
  }
  
  if (helixYellow) {
    helixYellow.geometry.dispose()
    helixYellow.material.dispose()
  }
  
  if (helixBlue) {
    helixBlue.geometry.dispose()
    helixBlue.material.dispose()
  }
})

// 暴露方法給父組件
defineExpose({
  fadeIn,
  function1,
  function2,
  function3,
  resetToInitial,
  k,
  constant,
  rotateSpeed,
  cameraZ,
  targetCameraZ
})
</script>

<style scoped>
.helix-container {
  width: 100%;
  height: 100vh;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease;
}

canvas {
  display: block;
  background: transparent !important;
}
</style>