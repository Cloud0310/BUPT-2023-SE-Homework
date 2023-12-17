<template>
  <PageHeader page-title="房间" />
  <div class="flex flex-wrap gap-3">
    <DeviceStatusCard
      v-for="(roomId, index) in roomIDs"
      :roomId="roomId"
      :key="index"
      class="h-[370px] shrink-0 grow basis-[max(calc(33%-0.375rem),400px)] bg-[#fffbff] drop-shadow-lg"
    />
    <div
      class="flex h-[370px] flex-1 shrink-0 grow basis-[max(calc(33%-0.375rem),400px)] items-center justify-center rounded-xl bg-[#fffbffb5] p-2 drop-shadow-lg"
    >
      <button type="button" @click="addDeviceDialogVisible = true" class="h-full w-full">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960" class="mx-auto h-24 w-24 text-neutral-300">
          <path fill="currentColor" d="M440-440H200v-80h240v-240h80v240h240v80H520v240h-80v-240Z" />
        </svg>
      </button>
    </div>
  </div>
  <el-dialog v-model="addDeviceDialogVisible" title="添加设备" style="--el-border-radius-small: 0.75rem">
    <div class="flex flex-col gap-4 px-6">
      <el-input v-model="deviceId" placeholder="请输入新设备ID" />
      <el-input v-model="deviceKey" placeholder="请输入新设备公钥" />
    </div>
    <div class="my-4 flex w-full justify-end">
      <el-button type="primary" @click="addDeviceDialogVisible = false" style="--el-color-primary-light-3: #ddd6fe"
        >添加</el-button
      >
    </div>
  </el-dialog>
</template>

<script lang="ts" setup>
import PageHeader from "../components/PageHeader.vue";
import DeviceStatusCard from "../components/DeviceStatusCard.vue";
import { getAvailableDevices, ERROR_CODE_MAP, UNKNOWN_ERROR } from "../utils/requests";

const roomIDs = ref<string[]>([]);
const addDeviceDialogVisible = ref(false);
const deviceId = ref("");
const deviceKey = ref("");

getAvailableDevices(
  null as any,
  data => {
    roomIDs.value = data;
  },
  err => {
    ElMessage({
      type: "error",
      message: `出现错误${ERROR_CODE_MAP[err] ?? UNKNOWN_ERROR}`
    });
  }
);
</script>
