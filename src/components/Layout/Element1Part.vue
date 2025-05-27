<template>
  <div class="element1-part">
    <div class="content">
      <h2>Element 1 Section</h2>
      <p>Green section with fast parallax scroll-in effect.</p>
    </div>
    
    <!-- Image grid that will animate in with fast parallax -->
    <div class="image-grid" ref="imageGrid">
      <div class="grid-item" v-for="index in 6" :key="index">
        <img :src="`/api/placeholder/${200 + index * 10}/${150 + index * 5}`" :alt="`Grid Image ${index}`" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineExpose } from 'vue';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// References for animation targets
const imageGrid = ref(null);

// Animation state
const isAnimated = ref(false);

onMounted(() => {
  setupScrollTrigger();
});

// Set up the scroll trigger for fast parallax effect
const setupScrollTrigger = () => {
  ScrollTrigger.create({
    trigger: '.element1-part',
    start: 'top bottom',
    end: 'top 30%',
    onEnter: () => triggerFastScroll()
  });
};

// Function to trigger the fast parallax animation
const triggerFastScroll = () => {
  if (isAnimated.value) return;
  isAnimated.value = true;
  
  // Animate the entire section as if it's being pulled in faster than normal scrolling
  gsap.fromTo(
    '.element1-part',
    { 
      y: 200,
      opacity: 0 
    },
    {
      y: 0,
      opacity: 1,
      duration: 1.2,
      ease: 'power2.out'
    }
  );
  
  // Staggered animation for grid items
  gsap.fromTo(
    '.grid-item',
    { 
      y: 300, 
      opacity: 0,
      scale: 0.8
    },
    {
      y: 0,
      opacity: 1,
      scale: 1,
      duration: 1.5,
      stagger: 0.1,
      ease: 'back.out(1.7)'
    }
  );
};

// Expose methods to parent component
defineExpose({
  triggerFastScroll
});
</script>

<style scoped>
.element1-part {
  position: relative;
  background-color: #4caf50; /* Green background */
  width: 100%;
  min-height: 100vh;
  padding: 50px 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.content {
  text-align: center;
  color: white;
  margin-bottom: 50px;
  z-index: 1;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-gap: 20px;
  max-width: 1000px;
  padding: 20px;
}

.grid-item {
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.grid-item img {
  width: 100%;
  height: auto;
  display: block;
  transition: transform 0.3s ease;
}

.grid-item:hover img {
  transform: scale(1.05);
}
</style>