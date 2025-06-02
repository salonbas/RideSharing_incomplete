<template>
  <div class="bg-black text-white rounded-2xl p-6 shadow-lg backdrop-blur-sm max-w-md w-full">
    <div class="flex items-center gap-4 mb-4">
      <img
        :src="user.avatarUrl || '/default-avatar.png'"
        alt="Avatar"
        class="w-16 h-16 rounded-full object-cover border border-white/30"
      />
      <h2 class="text-xl font-bold">{{ user.nickname }}</h2>
    </div>

    <div class="space-y-2 text-sm">
      <div v-if="user.instagram">
        <span class="font-semibold text-yellow-300">Instagram:</span> {{ user.instagram }}
      </div>
      <div v-if="user.phone">
        <span class="font-semibold text-yellow-300">電話:</span> {{ user.phone }}
      </div>
      <div v-if="user.bio">
        <span class="font-semibold text-yellow-300">簡介:</span>
        <p class="whitespace-pre-line">{{ user.bio }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  user: {
    type: Object,
    required: true
  }
});
</script>
