//src\components\Event\BottonSvg.vue
<template>
  <div class="taiwan-map">
    <svg 
      ref="mapContainer"
      class="map-svg"
      viewBox="0 0 1000 800"
      xmlns="http://www.w3.org/2000/svg"
    >
      <g fill="none" stroke="#d1ad41" stroke-linecap="round" stroke-linejoin="round" stroke-width="0.5">
        <path id="TWTPE" name="台北市" d="M776.8 321.1l-4.2 0-3.5-0.8-2.6-2.3-2.8-3.2-4.1-3.2-2.9-4.9 1.1-5.3-0.8-4.5-4.2-4-2.7-3.1 1.2-2.1 1.3-1.7 1.5-3.3 2.6-2.9 7.8-4.7 2.1-1.8 2.9-1.4 2.8 0.9 1.5 1.6-0.4 2.6 0.3 2.4 1.1 2.4 1.2 2.6 1.8 7.2 2.8 2.5 1.1 3.2-1.1 4.8 0.1 3.6 3.3 1.9 2.7 2.3-1.4 3-5.5 7-3 1.2z" @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWNWT" name="新北市" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWKEE" name="基隆市" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWILA" name="宜蘭縣" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWTAO" name="桃園市" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWHSQ" name="新竹縣" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWHSZ" name="新竹市" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWMIA" name="苗栗縣" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWCYI" name="嘉義市" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWCYQ" name="嘉義縣" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWNAN" name="南投縣" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWYUN" name="雲林縣" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWCHA" name="彰化縣" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWTXG" name="台中市" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWTNN" name="台南市" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWKHH" name="高雄市" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWPIF" name="屏東縣" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWHUA" name="花蓮縣" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWTTT" name="台東縣" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWKIN" name="金門縣" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWLIE" name="連江縣" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
        <path id="TWPEN" name="澎湖縣" d="...完整d..." @mouseenter="hoveredName = $event.target.getAttribute('name')" @mouseleave="hoveredName = ''" @click="handleClick($event)" />
      </g>
    </svg>

    <div v-if="hoveredName" class="map-label">
      {{ hoveredName }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 暫存 hover 名稱
const hoveredName = ref('')

// 點擊時 emit
const emit = defineEmits(['select'])

const handleClick = (e) => {
  const name = e.target.getAttribute('name')
  emit('select', name)
}
</script>

<style scoped>
.taiwan-map {
  width: 100%;
  max-width: 1000px;
  margin: 0 auto;
  background-color: #12150e;
  padding: 1rem;
  overflow: visible;
  position: relative;
}

.map-svg {
  width: 100%;
  height: auto;
  display: block;
  transform: scale(1.6) translate(-15%, -8%);
  transform-origin: center;
  margin-bottom: 100px;
  overflow: visible;
}

.map-label {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 4px 8px;
  background-color: #333;
  color: white;
  border-radius: 4px;
  font-size: 14px;
}

path {
  stroke: #d1ad41;
  stroke-width: 1;
  fill: transparent;
  cursor: pointer;
  transform-origin: center;
  transform-box: fill-box;
  transition: transform 0.3s ease, fill 0.3s ease;
}

path:hover {
  transform: scale(1.1);
  fill: #d1ad41;
  opacity: 0.5;
}
</style>
