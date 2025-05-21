// components\Layout\LogoMovingPart.vue
<template>
  <div class="logo-moving-part">
    <div class="content">
      <h2>Logo Section</h2>
      <p>This is the first section with a yellow background.</p>
    </div>
    
    <!-- Image A element that will be moved across different sections -->
    <div 
      ref="imageA"
      class="image-a"
      :style="{
        transform: `translate(${currentPosition.x}px, ${currentPosition.y}px)`
      }"
    >
      <div class="bg-white h-[10vh] w-[10vw]"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps, defineEmits } from 'vue';
import { gsap } from 'gsap';

const props = defineProps({
  initialImagePosition: {
    type: Object,
    default: () => ({ x: 300, y: 400 })
  }
});

const emit = defineEmits(['update-image-position']);

// Reference to the image element for animation
const imageA = ref(null);

// Track current position
const currentPosition = ref(props.initialImagePosition);

// Watch for changes in scroll position to update animation
onMounted(() => {
  // Initialize the image at the specified position
  gsap.set(imageA.value, {
    x: currentPosition.value.x,
    y: currentPosition.value.y
  });
  
  // Set up scroll animation for this section
  const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      // When this section is visible, animate the image to its designated position
      animateImage();
    }
  }, { threshold: 0.5 });
  
  observer.observe(document.querySelector('.logo-moving-part'));

  // Clean up
  return () => {
    observer.disconnect();
  };
});

// Animate the image and emit position updates
const animateImage = () => {
  // Target position for this section
  const targetPosition = { x: 300, y: 400 };
  
  gsap.to(currentPosition.value, {
    x: targetPosition.x,
    y: targetPosition.y,
    duration: 1,
    ease: "power2.out",
    onUpdate: () => {
      // Emit                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               updates as animation progresses
      emit('update-image-position', { ...currentPosition.value });
    }
  });
};
</script>

<style scoped>
.logo-moving-part {
  position: relative;
  background-color: #ffeb3b; /* Yellow background */
  width: 100%;
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  text-align: center;
  z-index: 1;
}

.image-a {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 10;
  /* Initial positioning handled by transform in template */
}

.image-a img {
  width: 200px;
  height: 200px;
  object-fit: cover;
}
</style>