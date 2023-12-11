<template>
  <div class="flex flex-wrap gap-3">
    <DeviceStatusCard
      v-for="device in devices"
      :roomId="device.roomId"
      :isOn="device.isOn"
      :temperature="device.temperature"
      :mode="device.mode"
      :windSpeed="device.windSpeed"
      :isWeeping="device.isWeeping"
      :lastUpdate="device.lastUpdate"
      @update-wind-speed="(n: number) => (device.windSpeed = n)"
      @update-is-on="() => console.log(device.isOn)"
      class="alid min-w-[calc(33%-0.375rem)] shrink-0"
    />
  </div>
</template>

<script lang="ts" setup>
import DeviceStatusCard from "../components/DeviceStatusCard.vue";

enum mode {
  cold = "制冷",
  hot = "制热",
  auto = "自动"
}

const devices = ref([
  {
    roomId: "114",
    isOn: true,
    temperature: 25,
    mode: mode.cold,
    windSpeed: 2,
    isWeeping: false,
    lastUpdate: new Date()
  },
  {
    roomId: "514",
    isOn: false,
    temperature: 25,
    mode: mode.hot,
    windSpeed: 5,
    isWeeping: false,
    lastUpdate: new Date()
  },
  {
    roomId: "191",
    isOn: true,
    temperature: 25,
    mode: mode.auto,
    windSpeed: 8,
    isWeeping: false,
    lastUpdate: new Date()
  },
  {
    roomId: "114",
    isOn: true,
    temperature: 25,
    mode: mode.cold,
    windSpeed: 2,
    isWeeping: false,
    lastUpdate: new Date()
  },
  {
    roomId: "514",
    isOn: false,
    temperature: 25,
    mode: mode.hot,
    windSpeed: 5,
    isWeeping: false,
    lastUpdate: new Date()
  },
  {
    roomId: "191",
    isOn: true,
    temperature: 25,
    mode: mode.auto,
    windSpeed: 8,
    isWeeping: false,
    lastUpdate: new Date()
  },
  {
    roomId: "114",
    isOn: true,
    temperature: 25,
    mode: mode.cold,
    windSpeed: 2,
    isWeeping: false,
    lastUpdate: new Date()
  }
]);
</script>

<style scoped></style>
