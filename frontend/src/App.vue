<script setup lang="ts">
import { Avatar } from "@element-plus/icons-vue";

const dateInfo = ref<Date>(new Date(Date.now()));
</script>

<template>
  <div class="h-[100vh] w-[100vw] flex">
    <div class="w-1/6 px-12 h-full sticky flex justify-between flex-col">
      <!-- user avatar and title -->
      <div>
        <div class="my-5 flex justify-center items-center gap-3 h-20">
          <el-avatar :icon="Avatar" :size="40" />
          <div class="text-l font-bold w-fit">空调管理系统</div>
        </div>
        <!-- menu -->
        <div class="flex flex-col gap-3">
          <div>
            <button type="button" class="w-full">
              <router-link to="/">
                <div
                  class="flex justify-start gap-2 items-center h-10 rounded-xl px-3 hover:bg-primary-100 transition-colors hover:text-neutral-500"
                >
                  <el-icon><MessageBox /></el-icon>
                  <span>主页</span>
                </div>
              </router-link>
            </button>
          </div>
          <div>
            <button type="button" class="w-full">
              <router-link to="/devices">
                <div
                  class="flex justify-start gap-2 items-center h-10 rounded-xl px-3 hover:bg-primary-100 transition-colors hover:text-neutral-500"
                >
                  <el-icon><DataBoard /></el-icon>
                  <span>设备</span>
                </div>
              </router-link>
            </button>
          </div>
          <!-- help page (may not implement) -->
          <!-- <div class=""></div> -->
          <!-- login and logout -->
        </div>
      </div>
      <div class="w-full flex justify-center py-5">
        <button type="button">
          <div
            class="flex justify-center gap-2 items-center h-10 px-3 hover:bg-primary-100 transition-colors rounded-xl hover:text-neutral-500"
          >
            <el-icon><User /></el-icon>
            <span>登录</span>
          </div>
        </button>
      </div>
    </div>
    <div class="w-5/6 bg-neutral-200">
      <div class="h-20 my-5 px-10 flex justify-between items-center">
        <div class="font-bold flex flex-col justify-center gap-[0.2rem] h-full">
          <div class="text-2xl">仪表板</div>
          <div class="text-neutral-400 text-sm">
            {{
              dateInfo.toLocaleTimeString("zh-CN", {
                hour: "2-digit",
                minute: "2-digit"
              })
            }}
          </div>
        </div>
        <div></div>
      </div>
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.router-link-active > div {
  background-color: #c4b5fd;
  color: #f5f3ff;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  gap: 0.65rem;
}
</style>
