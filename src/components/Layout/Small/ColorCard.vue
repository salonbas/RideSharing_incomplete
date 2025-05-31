<template>
  <div class="parent">
    <div
      class="card"
      :style="cardStyle"
      ref="cardRef"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

/**
 * 父層要有 position: relative，才能讓子層 absolute 根據它定位
 */
const props = defineProps({
  widthPercent: { type: Number, default: 40 },     // 卡片寬度 %（例如 40% 表示父元素的 40%）
  heightPercent: { type: Number, default: 30 },    // 卡片高度 %
  topPercent: { type: Number, default: 30 },       // 從上方偏移 %（位置）
  leftPercent: { type: Number, default: 20 },      // 從左方偏移 %
  fixedCorner: { type: Number, default: 1 },       // 1~4：固定角落（決定 transform-origin）
  rotateDeg: { type: Number, default: 0 },         // 旋轉角度
  z: { type: Number, default: 1 }                  // z-index（堆疊順序）
})

const cardRef = ref(null)

/**
 * 計算卡片的樣式
 * transform-origin 是關鍵，根據選定的角來控制「縮放中心點」
 */
const cardStyle = computed(() => {
  const originMap = {
    1: 'top left',
    2: 'top right',
    3: 'bottom right',
    4: 'bottom left'
  }

  return {
    width: `${props.widthPercent}%`,
    height: `${props.heightPercent}%`,
    top: `${props.topPercent}%`,
    left: `${props.leftPercent}%`,
    transformOrigin: originMap[props.fixedCorner], // 控制從哪個角落縮放
    transform: `rotate(${props.rotateDeg}deg)`,
    zIndex: props.z
  }
})

/**
 * 提供對外控制用的函數（可用 emit / expose）
 * 這邊用 expose，外層父元件可以調用這些動作
 */
defineExpose({
  resizeCard,
  rotateCard,
  moveCard
})

/**
 * 縮放函數：控制卡片寬高
 * 可帶動畫時間，改變 style 的 transition 屬性達成動畫
 */
function resizeCard(width, height, duration = 500) {
  const el = cardRef.value
  el.style.transition = `all ${duration}ms ease`
  el.style.width = `${width}%`
  el.style.height = `${height}%`
}

/**
 * 旋轉函數
 */
function rotateCard(deg, duration = 500) {
  const el = cardRef.value
  el.style.transition = `all ${duration}ms ease`
  el.style.transform = `rotate(${deg}deg)`
}

/**
 * 移動函數：更改 top、left
 */
function moveCard(top, left, duration = 500) {
  const el = cardRef.value
  el.style.transition = `all ${duration}ms ease`
  el.style.top = `${top}%`
  el.style.left = `${left}%`
}
</script>

<style scoped>
.parent {
  position: relative;
  width: 100%;
  height: 100vh;
  background-color: #222;
}

/* 卡片外觀樣式，可修改顏色或邊框 */
.card {
  position: absolute;
  background-color: yellow;
  transition: all 0.3s ease; /* 預設 transition，可被 JS 動態覆蓋 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}
</style>
