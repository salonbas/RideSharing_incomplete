<template>
  <div class="transition-part">
    <div class="content">
      <h2>Transition Section</h2>
      <p>Final section where Image A zooms to center.</p>
    </div>
    
    <!-- Image A that will zoom to center -->
    <div 
      ref="imageA" 
      class="image-a"
      :style="{
        transform: `translate(${imagePosition.x}px, ${imagePosition.y}px) scale(${scale})`,
        opacity: imageOpacity
      }"
    >
      <img src="https://www.google.com/imgres?q=%E7%9A%AE%E5%8D%A1%E4%B8%98&imgurl=https%3A%2F%2Ftw.portal-pokemon.com%2Fplay%2Fresources%2Fpokedex%2Fimg%2Fpm%2F2b3f6ff00db7a1efae21d85cfb8995eaff2da8d8.png&imgrefurl=https%3A%2F%2Ftw.portal-pokemon.com%2Fplay%2Fpokedex%2F0025&docid=ObBsxNzBSb7BCM&tbnid=Qu9uumi9X2QajM&vet=12ahUKEwiz1tDaobSNAxVidfUHHZbcMEYQM3oECBoQAA..i&w=630&h=630&hcb=2&ved=2ahUKEwiz1tDaobSNAxVidfUHHZbcMEYQM3oECBoQAA" alt="Image A" />
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, defineProps, defineExpose } from 'vue';
import { gsap } from 'gsap';

const props = defineProps({
  imagePosition: {
    type: Object,
    default: () => ({ x: 0, y: 0 })
  }
});

// Animation properties
const scale = ref(1);
const imageOpacity = ref(1);
const zoomProgress = ref(0);

// Reference to the image element
const imageA = ref(null);

// Center position calculation
const centerPosition = {
  x: window.innerWidth / 2 - 100, // Subtract half of image width
  y: window.innerHeight / 2 - 100 // Subtract half of image height
};

// Update zoom based on scroll progress
const updateZoomProgress = (progress) => {
  zoomProgress.value = progress;
  
  // Animate zoom effect
  const newScale = 1 + (progress * 2); // Scale from 1x to 3x
  scale.value = newScale;
  
  // Move image to center as we scroll
  gsap.to(imageA.value, {
    x: centerPosition.x - props.imagePosition.x * (1 - progress),
    y: centerPosition.y - props.imagePosition.y * (1 - progress),
    duration: 0.1,
    overwrite: true
  });
  
  // Adjust opacity at the end of the animation
  imageOpacity.value = progress > 0.8 ? 5 * (1 - progress) : 1;
};

onMounted(() => {
  // Set up initial position
  if (imageA.value) {
    gsap.set(imageA.value, {
      x: props.imagePosition.x,
      y: props.imagePosition.y
    });
  }
});

// Watch for updates to image position from parent
watch(() => props.imagePosition, (newPosition) => {
  if (zoomProgress.value === 0 && imageA.value) {
    gsap.set(imageA.value, {
      x: newPosition.x,
      y: newPosition.y
    });
  }
}, { deep: true });

// Expose methods to parent component
defineExpose({
  updateZoomProgress
});
</script>

<style scoped>
.transition-part {
  position: relative;
  background-color: #303030; /* Dark background to focus on image */
  width: 100%;
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  text-align: center;
  color: white;
  z-index: 1;
}

.image-a {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 10;
  will-change: transform, opacity;
  /* Positioning handled by transform in template */
}

.image-a img {
  width: 200px;
  height: 200px;
  object-fit: cover;
}
</style>