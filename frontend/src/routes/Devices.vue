<template>
  <div class="flex flex-wrap gap-3">
    <DeviceStatusCard
      v-for="(roomId, index) in roomIDs"
      :roomId="roomId"
      :key="index"
      class="alid min-w-[calc(33%-0.375rem)] shrink-0"
    />
  </div>
</template>

<script lang="ts" setup>
import DeviceStatusCard from "../components/DeviceStatusCard.vue";

const roomIDs = ref<string[]>(["114", "514", "191", "115", "513", "192", "119"]);
</script>

<style scoped></style>
