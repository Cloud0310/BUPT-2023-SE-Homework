<script setup lang="ts">
import { User } from "@element-plus/icons-vue"
</script>

<template>
  <div class="flex justify-center h-[100vh]">
    <div class="basis-1/5 px-10 py-5">
      <div class="h-10 w-full">
        <el-avatar :icon="User" />
      </div>
      <div class="flex flex-col">
        <div class=""></div>
        <el-divider />
        <div class=""></div>
        <div class="before:grow "></div>
      </div>
    </div>
    <div class="basis-4/5 bg-background-100"></div>
  </div>
</template>

<style scoped></style>