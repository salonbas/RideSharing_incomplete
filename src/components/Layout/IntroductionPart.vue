//components\Layout\IntroductionPart.vue
<script setup>
import { ref, watch, defineProps, onMounted } from 'vue';
import { gsap } from 'gsap';

const props = defineProps({
  previousImagePosition: Object,
  currentImagePosition: Object
});

const imageA = ref(null);

const animateTransition = () => {
  const targetX = props.currentImagePosition.x;
  const targetY = props.currentImagePosition.y;

  gsap.to(imageA.value, {
    x: targetX,
    y: targetY,
    rotation: 360,
    duration: 2,
    ease: 'power2.inOut'
  });
};

watch(() => props.currentImagePosition, () => {
  animateTransition();
}, { deep: true });

onMounted(() => {
  gsap.set(imageA.value, {
    x: props.previousImagePosition.x,
    y: props.previousImagePosition.y
  });

  // Intersection trigger
  const observer = new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) {
      animateTransition();
    }
  }, { threshold: 0.3 });

  observer.observe(document.querySelector('.introduction-part'));
});
</script>

<template>
  <div class="introduction-part">
    <div class="content">
      <h2>Introduction Section</h2>
    </div>

    <!-- Image A (Only 1 DOM element) -->
    <div ref="imageA" class="image-a">
      <div class="bg-white h-[10vh] w-[10vw]"></div>
    </div>
  </div>
</template>
