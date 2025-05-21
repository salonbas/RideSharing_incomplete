<!-- Parallax.vue -->
<template>
  <div ref="containerRef" 
       class="relative overflow-hidden"
       :style="{ height: `${height}px` }">
    <div ref="contentRef"
         class="absolute inset-0 will-change-transform bg-slate-500"
         :style="{ 
           transform: `translate3d(${finalHorizontalOffset}px, ${finalVerticalOffset}px, 0)`,
           transition: smooth ? `transform ${transitionDuration}ms ${easingFunction}` : 'none'
         }">
      <slot />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, onBeforeUnmount, defineProps, defineEmits, watch } from 'vue';

const props = defineProps({
  // 垂直視差速度，正值向下移動慢，負值向下移動快
  verticalSpeed: { type: Number, default: 0.9 },
  // 水平視差速度，提供水平視差效果
  horizontalSpeed: { type: Number, default: 1.3 },
  // 動畫平滑過渡
  smooth: { type: Boolean, default: true },
  // 過渡動畫持續時間（毫秒）
  transitionDuration: { type: Number, default: 600 },
  // 元素高度
  height: { type: Number, default: 300 },
  // 視差方向：'both', 'horizontal', 'vertical'
  direction: { type: String, default: 'vertical' },
  // 是否僅在視口內可見時執行視差計算
  lazyParallax: { type: Boolean, default: true },
  // 視差效果的相對基準（相對於哪裡產生視差）
  // 'viewport': 相對於視口頂部
  // 'element': 相對於元素在視口中的位置
  relativeTo: { type: String, default: 'viewport' },
  // 新增：最大偏移量限制（避免過度偏移）
  maxOffset: { type: Number, default: 200 },
  // 新增：水平最大偏移量限制
  maxHorizontalOffset: { type: Number, default: 200 },
  // 新增：緩動函數類型
  easingType: { type: String, default: 'easeOutExpo' },
  // 新增：緩動函數表達式（CSS 格式）
  easingFunction: { type: String, default: 'cubic-bezier(0.16, 1, 0.3, 1)' },
  // 新增：視差層級（多層視差結構使用）
  depthLevel: { type: Number, default: 1 },
  // 新增：視差深度係數
  depthFactor: { type: Number, default: 0.5 },
  // 新增：慣性摩擦係數
  inertiaFriction: { type: Number, default: 0.05 },
  // 新增：是否啟用慣性效果
  useInertia: { type: Boolean, default: false },
  // 新增：超過偏移閾值事件的閾值
  offsetThreshold: { type: Number, default: 100 },
  // 新增：是否使用自定義非線性緩動
  useCustomEasing: { type: Boolean, default: false },
  // 新增：捕捉準確度（滾動時多久捕捉一次滾動位置）
  scrollCaptureFps: { type: Number, default: 60 }
});

const emit = defineEmits(['enter-view', 'leave-view', 'exceed-threshold', 'parallax-update']);

// 引用容器和內容元素
const containerRef = ref(null);
const contentRef = ref(null);

// 初始化滾動和交互狀態
const scrollPosition = reactive({
  x: 0,
  y: 0
});

// 慣性相關狀態
const inertiaState = reactive({
  lastY: 0,
  lastX: 0,
  velocityY: 0,
  velocityX: 0,
  offsetY: 0,
  offsetX: 0
});

// 鼠標位置（用於鼠標視差效果）
const mousePosition = reactive({
  x: 0,
  y: 0
});

// 元素是否在視口中
const isInView = ref(false);

// 各種緩動函數集合
const easingFunctions = {
  // 指數緩動
  easeOutExpo: (x) => x === 1 ? 1 : 1 - Math.pow(2, -10 * x),
  // 三次方緩動
  easeOutCubic: (x) => 1 - Math.pow(1 - x, 3),
  // 彈性緩動
  easeOutBack: (x) => {
    const c1 = 1.70158;
    const c3 = c1 + 1;
    return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
  },
  // 線性
  linear: (x) => x
};

// 限制值在指定範圍內
function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

// 應用自定義緩動
function applyEasing(value, maxValue, type = props.easingType) {
  const normalizedValue = Math.min(Math.abs(value) / maxValue, 1);
  const easedValue = easingFunctions[type](normalizedValue);
  return Math.sign(value) * easedValue * maxValue;
}

// 計算垂直偏移量
const verticalOffset = computed(() => {
  if (props.lazyParallax && !isInView.value) return 0;
  if (props.direction === 'horizontal') return 0;
  
  let offset;
  if (props.relativeTo === 'element') {
    // 相對於元素在視口中的位置計算
    offset = elementRelativeOffset.value.y * props.verticalSpeed;
  } else {
    // 預設相對於視口
    offset = scrollPosition.y * props.verticalSpeed;
  }
  
  // 根據深度層級調整偏移量
  const depthAdjustedOffset = offset * (props.depthLevel * props.depthFactor);

  // 應用慣性效果（如果啟用）
  if (props.useInertia) {
    offset = depthAdjustedOffset + inertiaState.offsetY;
  } else {
    offset = depthAdjustedOffset;
  }
  
  return clamp(offset, -props.maxOffset, props.maxOffset);
});

// 計算水平偏移量
const horizontalOffset = computed(() => {
  if (props.lazyParallax && !isInView.value) return 0;
  if (props.direction === 'vertical') return 0;
  
  let offset;
  if (props.relativeTo === 'element') {
    // 相對於元素在視口中的位置 + 鼠標效果
    const mouseEffect = mousePosition.x / window.innerWidth * 20 - 10;
    offset = elementRelativeOffset.value.x * props.horizontalSpeed + mouseEffect;
  } else {
    // 預設相對於視口 + 鼠標效果
    const mouseEffect = props.direction === 'both' ? 
      (mousePosition.x / window.innerWidth * 20 - 10) : 0;
    offset = scrollPosition.x * props.horizontalSpeed + mouseEffect;
  }
  
  // 根據深度層級調整偏移量
  const depthAdjustedOffset = offset * (props.depthLevel * props.depthFactor);

  // 應用慣性效果（如果啟用）
  if (props.useInertia) {
    offset = depthAdjustedOffset + inertiaState.offsetX;
  } else {
    offset = depthAdjustedOffset;
  }
  
  return clamp(offset, -props.maxHorizontalOffset, props.maxHorizontalOffset);
});

// 應用自定義非線性緩動後的最終垂直偏移量
const finalVerticalOffset = computed(() => {
  if (props.useCustomEasing) {
    return applyEasing(verticalOffset.value, props.maxOffset);
  }
  return verticalOffset.value;
});

// 應用自定義非線性緩動後的最終水平偏移量
const finalHorizontalOffset = computed(() => {
  if (props.useCustomEasing) {
    return applyEasing(horizontalOffset.value, props.maxHorizontalOffset);
  }
  return horizontalOffset.value;
});

// 元素相對於視口中心的偏移量
const elementRelativeOffset = computed(() => {
  if (!containerRef.value || !isInView.value) return { x: 0, y: 0 };
  
  const rect = containerRef.value.getBoundingClientRect();
  const viewportHeight = window.innerHeight;
  const viewportWidth = window.innerWidth;
  
  // 計算元素中心到視口中心的距離
  const centerOffsetY = (rect.top + rect.height / 2) - (viewportHeight / 2);
  const centerOffsetX = (rect.left + rect.width / 2) - (viewportWidth / 2);
  
  return {
    x: centerOffsetX,
    y: centerOffsetY
  };
});

// 使用 Intersection Observer 監測元素是否在視口中
function setupIntersectionObserver() {
  const observer = new IntersectionObserver(
    (entries) => {
      const [entry] = entries;
      isInView.value = entry.isIntersecting;
    },
    { threshold: 0.1 } // 當 10% 的元素可見時觸發
  );
  
  if (containerRef.value) {
    observer.observe(containerRef.value);
  }
  
  // 在組件卸載時移除觀察者
  onBeforeUnmount(() => {
    if (containerRef.value) {
      observer.unobserve(containerRef.value);
    }
    observer.disconnect();
  });
}

// 更高效的滾動處理
let scrollTicking = false;
let scrollCaptureInterval = 1000 / props.scrollCaptureFps; // 捕捉率控制
let lastScrollCaptureTime = 0;

function handleScroll() {
  const now = performance.now();
  
  // 控制捕捉率
  if (now - lastScrollCaptureTime < scrollCaptureInterval) {
    return;
  }
  
  lastScrollCaptureTime = now;
  
  if (!scrollTicking) {
    window.requestAnimationFrame(() => {
      // 更新滾動位置
      const currentX = window.scrollX;
      const currentY = window.scrollY;
      
      // 計算滾動速度（用於慣性效果）
      if (props.useInertia) {
        inertiaState.velocityY = currentY - inertiaState.lastY;
        inertiaState.velocityX = currentX - inertiaState.lastX;
        inertiaState.lastY = currentY;
        inertiaState.lastX = currentX;
      }
      
      scrollPosition.x = currentX;
      scrollPosition.y = currentY;
      scrollTicking = false;
    });
    scrollTicking = true;
  }
}

// 慣性效果動畫
let inertiaAnimationId = null;

function updateInertia() {
  // 慢慢減少速度（模擬摩擦）
  inertiaState.velocityY *= (1 - props.inertiaFriction);
  inertiaState.velocityX *= (1 - props.inertiaFriction);
  
  // 更新偏移量
  inertiaState.offsetY += inertiaState.velocityY * props.inertiaFriction;
  inertiaState.offsetX += inertiaState.velocityX * props.inertiaFriction;
  
  // 當速度接近零時停止動畫
  if (Math.abs(inertiaState.velocityY) < 0.01 && Math.abs(inertiaState.velocityX) < 0.01) {
    inertiaState.velocityY = 0;
    inertiaState.velocityX = 0;
    cancelAnimationFrame(inertiaAnimationId);
    inertiaAnimationId = null;
    return;
  }
  
  inertiaAnimationId = requestAnimationFrame(updateInertia);
}

// 鼠標移動處理（用於鼠標視差效果）
let mouseTicking = false;

function handleMouseMove(e) {
  if (!mouseTicking) {
    window.requestAnimationFrame(() => {
      mousePosition.x = e.clientX;
      mousePosition.y = e.clientY;
      mouseTicking = false;
    });
    mouseTicking = true;
  }
}

// 監聽視口變化
watch(isInView, (val) => {
  emit('enter-view', val);
  if (val) {
    emit('enter-view');
  } else {
    emit('leave-view');
  }
});

// 監聽垂直偏移量是否超過閾值
watch(() => finalVerticalOffset.value, (val) => {
  emit('parallax-update', { vertical: val, horizontal: finalHorizontalOffset.value });
  
  if (Math.abs(val) > props.offsetThreshold) {
    emit('exceed-threshold', { 
      value: val, 
      direction: val > 0 ? 'down' : 'up',
      axis: 'vertical'
    });
  }
});

// 監聽水平偏移量是否超過閾值
watch(() => finalHorizontalOffset.value, (val) => {
  if (Math.abs(val) > props.offsetThreshold) {
    emit('exceed-threshold', { 
      value: val, 
      direction: val > 0 ? 'right' : 'left',
      axis: 'horizontal'
    });
  }
});

// 啟動慣性動畫
function startInertiaAnimation() {
  if (props.useInertia && !inertiaAnimationId) {
    inertiaAnimationId = requestAnimationFrame(updateInertia);
  }
}

onMounted(() => {
  // 設置滾動偵測
  window.addEventListener('scroll', handleScroll, { passive: true });
  
  // 設置鼠標移動偵測
  if (props.direction === 'both' || props.horizontalSpeed !== 0) {
    window.addEventListener('mousemove', handleMouseMove, { passive: true });
  }
  
  // 設置 Intersection Observer
  if (props.lazyParallax) {
    setupIntersectionObserver();
  } else {
    isInView.value = true;
  }
  
  // 初始化滾動位置
  scrollPosition.x = window.scrollX;
  scrollPosition.y = window.scrollY;
  
  // 初始化慣性值
  inertiaState.lastX = window.scrollX;
  inertiaState.lastY = window.scrollY;
  
  // 啟動慣性動畫
  if (props.useInertia) {
    startInertiaAnimation();
  }
});

onBeforeUnmount(() => {
  window.removeEventListener('scroll', handleScroll);
  
  if (props.direction === 'both' || props.horizontalSpeed !== 0) {
    window.removeEventListener('mousemove', handleMouseMove);
  }
  
  // 取消慣性動畫
  if (inertiaAnimationId) {
    cancelAnimationFrame(inertiaAnimationId);
  }
});
</script>