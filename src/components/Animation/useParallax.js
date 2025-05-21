//useParallax.js — 使用 @vueuse/core 的 Hook 版本
import { ref, reactive, onMounted, onBeforeUnmount, computed } from 'vue'
import { useWindowScroll, useMouse, useElementBounding, useElementVisibility } from '@vueuse/core'

export function useParallax(elRef, options = {}) {
  const {
    verticalSpeed = 0.2,
    horizontalSpeed = 0,
    direction = 'vertical',
    relativeTo = 'viewport',
    lazyParallax = true,
    maxOffset = 200
  } = options

  const { x: scrollX, y: scrollY } = useWindowScroll()
  const { x: mouseX, y: mouseY } = useMouse()
  const bounds = useElementBounding(elRef)
  const isInView = useElementVisibility(elRef)

  const centerOffset = computed(() => {
    const viewportCenterY = window.innerHeight / 2
    const viewportCenterX = window.innerWidth / 2
    return {
      x: bounds.left.value + bounds.width.value / 2 - viewportCenterX,
      y: bounds.top.value + bounds.height.value / 2 - viewportCenterY
    }
  })

  const verticalOffset = computed(() => {
    if (lazyParallax && !isInView.value) return 0
    if (direction === 'horizontal') return 0
    const raw = relativeTo === 'element' ? centerOffset.value.y * verticalSpeed : scrollY.value * verticalSpeed
    return Math.max(-maxOffset, Math.min(raw, maxOffset))
  })

  const horizontalOffset = computed(() => {
    if (lazyParallax && !isInView.value) return 0
    if (direction === 'vertical') return 0
    const mouseEffect = direction === 'both' ? (mouseX.value / window.innerWidth) * 20 - 10 : 0
    const raw = relativeTo === 'element'
      ? centerOffset.value.x * horizontalSpeed + mouseEffect
      : scrollX.value * horizontalSpeed + mouseEffect
    return Math.max(-maxOffset, Math.min(raw, maxOffset))
  })

  return {
    verticalOffset,
    horizontalOffset,
    isInView
  }
}