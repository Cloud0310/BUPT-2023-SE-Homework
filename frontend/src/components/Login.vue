<!-- <template>
  <div></div>
</template>

<script lang="ts" setup></script>

<style scoped></style> -->

<template>
  <div class="fixed top-0 left-0 w-full h-full flex justify-center items-center bg-black bg-opacity-50 z-20">
    <div class="w-96 h-80 bg-white rounded-lg p-8 relative">
      <button class="absolute top-0 right-0 m-3 bg-transparent border-none outline-none cursor-pointer text-gray-500 text-xl " @click="closePanel">
          <el-icon><Close /></el-icon>
      </button>
      登录面板内容
    </div>
  </div>
</template>
<script lang="ts">
export default {
  methods: {
    closePanel() {
      this.$emit('close');
    },
  },
};
</script>
