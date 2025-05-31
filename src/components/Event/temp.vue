// components/Event/EventCard.vue
<template>
  <div class="card-wrapper" @click="$emit('show-detail', eventData.id)">
    <div class="card-inner group">
      <!-- 正面 -->
      <div class="card-face card-front">
        <div class="flex-1 flex mb-2">
          <!-- 上半部：頭像 + 主辦人與路線 -->
          <div class="w-1/2 h-full flex items-center justify-center p-6">
            <!-- 🧑 頭像 -->
            <div
              class="h-full aspect-square rounded-full overflow-hidden cursor-pointer"
              @click.stop="$emit('show-profile', eventData.organizer.id)"
            >
            <img
            :src="eventData.organizer.avatarUrl || '/default-avatar.png'"
            :alt="eventData.organizer.nickname"
            class="h-full w-full object-cover"
            />
            </div>
          </div>
          <!-- 👤 名字 + 路線 -->
          <div class="w-1/2 flex flex-col justify-center items-center pl-2 ">
            <div class="text-xl font-semibold truncate group-hover:text-[#1a1a1a]">
              {{ eventData.organizer.nickname }}
            </div>
            <div class="text-sm text-gray-300 w-full break-words whitespace-normal group-hover:text-[#1a1a1a]">
              {{ eventData.location.from.city }} {{ eventData.location.from.detail }}
              →
              {{ eventData.location.destination.city }} {{ eventData.location.destination.detail }}
            </div>
          </div>
        </div>

        <div class="flex-1 flex">
        <!-- 下半部：資訊 3:1 -->
        <div class="w-3/4 space-y-1 text-sm text-gray-300 flex flex-col justify-center items-start pl-4 group-hover:text-[#1a1a1a]">
          <div>時間： {{ formattedDate }}</div>
          <div>金額： {{ eventData.price === 0 ? '免費' : `$${eventData.price}` }}</div>
          <div>地點： {{ eventData.location.from.city }} {{ eventData.location.from.detail }}
                    →
                  {{ eventData.location.destination.city }} {{ eventData.location.destination.detail }}
          </div>
        </div>
        <!-- 右側 1 欄 -->
        <div class="w-1/4 flex flex-col justify-end">
          <div
            class="text-xs mb-0 font-semibold"
            :class="spotsColorClass"
            >
              剩 {{ eventData.spotsRemaining }} 人
          </div>
          <button
            :class="btnClass"
            @click.stop="handleButtonClick"
            :disabled="eventData.spotsRemaining <= 0 && !isOrganizer && !isJoined"
          >
            <span class="btn-text group-hover:text-[#1a1a1a]">
              {{ btnText }}
            </span>
            <svg viewBox="0 0 100 40" preserveAspectRatio="none">
              <rect x="3" y="3" width="94" height="34" rx="17" ry="17" />
            </svg>
          </button>
          </div>
        </div>
      </div>

      <!-- 背面 -->
      <div class="card-face card-back">
        <div class="h-full flex flex-col justify-center items-center p-6 space-y-4">
          <div class="text-center">
            <h3 class="text-2xl font-bold mb-4 group-hover:text-[#1a1a1a]">活動詳情</h3>
            <div class="space-y-3 text-left group-hover:text-[#1a1a1a]">
              <div class="flex items-center">
                <span class="font-medium w-16">類型：</span>
                <span class="bg-[#d1ad41] text-black px-2 py-1 rounded text-sm">{{ typeLabel }}</span>
              </div>
              <div class="flex">
                <span class="font-medium w-16">時間：</span>
                <span>{{ formattedDate }}</span>
              </div>
              <div class="flex">
                <span class="font-medium w-16">人數：</span>
                <span>{{ eventData.joinedSeats }}/{{ eventData.requiredSeats }}</span>
              </div>
              <div class="flex">
                <span class="font-medium w-16">費用：</span>
                <span>{{ eventData.price === 0 ? '免費' : `$${eventData.price}` }}</span>
              </div>
              <div class="flex">
                <span class="font-medium w-16">備註：</span>
                <span class="text-sm">{{ eventData.description || '無' }}</span>
              </div>
            </div>
          </div>
          
          <div class="flex flex-col items-center">
            <div
              class="text-sm mb-2 font-semibold"
              :class="spotsColorClass"
            >
              剩 {{ eventData.spotsRemaining }} 人
            </div>
            <button
              :class="btnClass"
              @click.stop="handleButtonClick"
              :disabled="eventData.spotsRemaining <= 0 && !isOrganizer && !isJoined"
            >
              <span class="btn-text group-hover:text-[#1a1a1a]">
                {{ btnText }}
              </span>
              <svg viewBox="0 0 100 40" preserveAspectRatio="none">
                <rect x="3" y="3" width="94" height="34" rx="17" ry="17" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



.card-wrapper {
  perspective: 1000px;
  width: 100%;
  height: 100%;
}

.card-inner {
  transition: transform 0.6s ease;
  transform-style: preserve-3d;
  will-change: transform;
}

.card-wrapper:hover .card-inner {
  transform: rotateY(20deg) scale(1.02);
}

/* 卡片主體 */
.card-face {
  backface-visibility: hidden;
  background-color: #12150e;
  border: 2px solid #d1ad44;
  color: white;
  padding: 1rem;
  border-radius: 28px;
  transition:
    background-color 0.6s ease,
    color 0.6s ease,
    transform 0.3s ease,
    box-shadow 0.3s ease;
  height: 40vh;
  display: flex;
  flex-direction: column;
}

/*  hover 時變亮 + 放大 */
.card-wrapper:hover .card-face {
  background-color: #faf6e9;
  color: #1a1a1a;
  transform: scale(1.02);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.25);
}


.card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.6s ease;
  transform-style: preserve-3d;
}

.card-wrapper:hover .card-inner {
  transform: rotateY(180deg);
}

.card-front, .card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 28px;
}
.card-back {
  
  backface-visibility: hidden;
  transform: rotateY(180deg);
  background-color: #faf6e9; /* 🟡 淺底色 */
  color: #1a1a1a;            /* ⚫ 黑字 */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}



