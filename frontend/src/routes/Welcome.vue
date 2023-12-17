<template>
  <PageHeader page-title="主页" />
  <div class="flex h-[calc(100%-9rem)] flex-col justify-between py-10">
    <div class="flex flex-col gap-1">
      <span class="text-6xl font-bold text-neutral-400"> 欢迎使用 </span>
      <br />
      <span class="text-7xl font-bold text-primary-400">巴普特空调管理系统</span>
    </div>
    <div class="flex h-24 w-full justify-end">
      <Login />
    </div>
  </div>
</template>

<script lang="ts" setup>
import Login from '../components/Login.vue';

</script>
