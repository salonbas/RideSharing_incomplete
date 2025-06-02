<template>
  <div class="main-page min-h-screen bg-[#12150e] text-[#FFD700] relative">
    <!-- 星空背景 -->
    <div class="sky" ref="skyRef"></div>

    <!-- 原本你的內容 -->
    <LogoMovingPart 
      @update-image-position="updateImagePosition" 
      :initial-image-position="imagePosition"
    />
    
    <IntroductionPart 
      :previous-image-position="previousImagePosition"
      :current-image-position="imagePosition"
    />
    
    <TransitionPart :image-position="imagePosition" ref="transitionRef" />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import LogoMovingPart from '@/components/Layout/LogoMovingPart.vue';
import IntroductionPart from '@/components/Layout/IntroductionPart.vue';
import TransitionPart from '@/components/Layout/TransitionPart.vue';

// 星空部分
const skyRef = ref(null);
onMounted(async () => {
  await nextTick();
  const sky = skyRef.value;
  if (!sky) return;

  // 產生星星
  for (let i = 0; i < 200; i++) {
    const star = document.createElement('div');
    star.classList.add('star');
    star.style.top = `${Math.random() * 100}%`;
    star.style.left = `${Math.random() * 100}%`;
    const size = Math.random() * 2 + 1;
    star.style.width = `${size}px`;
    star.style.height = `${size}px`;

    const duration = 1.5 + Math.random() * 2;
    const delay = Math.random() * 2;
    star.style.animationDuration = `${duration}s`;
    star.style.animationDelay = `${delay}s`;

    sky.appendChild(star);
  }

  // 產生流星
  setInterval(() => {
    if (Math.random() < 0.6) {
      const meteor = document.createElement('div');
      meteor.classList.add('shooting-star');
      meteor.style.top = `${Math.random() * 80}%`;
      meteor.style.left = `-${Math.random() * 200 + 50}px`;
      meteor.style.width = `${100 + Math.random() * 60}px`;
      sky.appendChild(meteor);
      setTimeout(() => meteor.remove(), 3500);
    }
  }, 2000);
});

// 你原本的動畫邏輯繼續照常
gsap.registerPlugin(ScrollTrigger);
const imagePosition = ref({ x: 300, y: 400 });
const previousImagePosition = ref({ x: 300, y: 400 });
const transitionRef = ref(null);

const updateImagePosition = (newPosition) => {
  previousImagePosition.value = { ...imagePosition.value };
  imagePosition.value = newPosition;
};

onMounted(async () => {
  await nextTick();
  setupScrollAnimations();
});

const setupScrollAnimations = () => {
  setupScrollTriggers();
};

const setupScrollTriggers = () => {
  if (transitionRef.value) {
    ScrollTrigger.create({
      trigger: '.transition-part',
      start: 'top center',
      end: 'center center',
      onUpdate: (self) => {
        transitionRef.value.updateZoomProgress(self.progress);
      }
    });
  }
};
</script>

<style scoped>
.main-page {
  position: relative;
  width: 100%;
  overflow-x: hidden;
}

.main-page > * {
  min-height: 100vh;
  width: 100%;
}
</style>

<!-- 星空專用 css 不要 scoped -->
<style>
.sky {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}

.star {
  position: absolute;
  background: white;
  border-radius: 50%;
  opacity: 0;
  animation: twinkle 2s infinite ease-in-out alternate;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.1; }
  50% { opacity: 1; }
}

.shooting-star {
  position: absolute;
  width: 140px;
  height: 2px;
  background: linear-gradient(to left, white, rgba(255, 255, 255, 0));
  opacity: 0;
  animation: shoot 3s ease-out forwards;
  z-index: 20;
  pointer-events: none;
  transform: rotate(35deg);
}

@keyframes shoot {
  0% { transform: translate(0, 0) rotate(35deg); opacity: 0; }
  10% { opacity: 1; }
  100% { transform: translate(800px, 400px) rotate(35deg); opacity: 0; }
}
</style>