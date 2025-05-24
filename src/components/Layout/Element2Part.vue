<template>
  <div class="element2-part">
    <div class="content">
      <h2>Element 2 Section</h2>
      <p>This section features expanding rectangles based on scroll progress.</p>
    </div>
    
    <!-- First expanding rectangle -->
    <div 
      class="expanding-rectangle first-rectangle" 
      :style="{
        width: `${firstRectWidth}px`,
        height: `${firstRectHeight}px`
      }"
    ></div>
    
    <!-- Second expanding rectangle (appears after threshold) -->
    <div 
      class="expanding-rectangle second-rectangle" 
      :style="{
        width: `${secondRectWidth}px`,
        height: `${secondRectHeight}px`,
        opacity: secondRectOpacity
      }"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, defineExpose } from 'vue';

// Constants for rectangle expansion
const k = 1000; // Multiplier for scroll amount
const q = 1.5;  // Width multiplier
const g = 0.8;  // Height multiplier
const threshold = 0.4; // Threshold for second rectangle to appear

// Animation state
const scrollProgress = ref(0);

// Computed properties for first rectangle dimensions
const firstRectWidth = computed(() => {
  return Math.min(q * k * scrollProgress.value, window.innerWidth * 0.8);
});

const firstRectHeight = computed(() => {
  return Math.min(g * k * scrollProgress.value, window.innerHeight * 0.6);
});

// Computed properties for second rectangle
const secondRectOpacity = computed(() => {
  if (scrollProgress.value < threshold) return 0;
  return (scrollProgress.value - threshold) / (1 - threshold);
});

const secondRectWidth = computed(() => {
  if (scrollProgress.value < threshold) return 0;
  const progress = (scrollProgress.value - threshold) / (1 - threshold);
  return Math.min(q * k * progress * 0.7, window.innerWidth * 0.6);
});

const secondRectHeight = computed(() => {
  if (scrollProgress.value < threshold) return 0;
  const progress = (scrollProgress.value - threshold) / (1 - threshold);
  return Math.min(g * k * progress * 0.7, window.innerHeight * 0.5);
});

// Function to update rectangle sizes based on scroll progress
const updateScrollProgress = (progress) => {
  scrollProgress.value = progress;
};

// Expose method to parent component
defineExpose({
  updateScrollProgress
});
</script>

<style scoped>
.element2-part {
  position: relative;
  background-color: #ffffff; /* Default background */
  width: 100%;
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  text-align: center;
  z-index: 10;
  position: relative;
}

.expanding-rectangle {
  position: absolute;
  background-color: #9c27b0; /* Purple color */
  border-radius: 4px;
  transform-origin: left center;
  will-change: width, height;
}

.first-rectangle {
  top: 20%;
  left: 0;
}

.second-rectangle {
  bottom: 20%;
  left: 0;
  opacity: 0; /* Initially hidden, will fade in */
}
</style>