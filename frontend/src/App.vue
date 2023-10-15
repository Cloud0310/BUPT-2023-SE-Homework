<script setup lang="ts">
import { Avatar } from "@element-plus/icons-vue";
import { ref } from "vue";
import Button from "./components/Button.vue";

const dateInfo = ref<Date>(new Date(Date.now()));

const isLoginPannelEnabled = ref<boolean>(false);
const isLogin = ref<boolean>(false);

function handleLoginClick() {
  if (!isLogin) {
    isLoginPannelEnabled.value = true;
  } else {
    isLogin.value = false;
  }
}
</script>

<template>
  <div class="h-[100vh] w-[100vw] flex">
    <div class="w-1/6 px-12 h-full sticky flex justify-between flex-col py-5">
      <!-- user avatar and title -->
      <div>
        <div class="my-5 flex justify-center items-center gap-3 h-20">
          <el-avatar :icon="Avatar" :size="40" />
          <div class="text-l font-bold w-fit">空调管理系统</div>
        </div>
        <!-- menu -->
        <div class="flex flex-col gap-3">
          <div>
            <router-link to="/">
              <Button class="hover:gap-3 w-full">
                <el-icon><MessageBox /></el-icon>
                <span>主页</span>
              </Button>
            </router-link>
          </div>
          <div>
            <router-link to="/devices">
              <Button class="hover:gap-3 w-full">
                <el-icon><DataBoard /></el-icon>
                <span>设备</span>
              </Button>
            </router-link>
          </div>
          <!-- help page (may not implement) -->
          <!-- <div class=""></div> -->
          <!-- login and logout -->
        </div>
      </div>
      <div class="w-full flex justify-center my-5">
        <Button @click="handleLoginClick">
          <el-icon><User /></el-icon>
          <span v-if="isLogin">退出</span>
          <span v-else>登录</span>
        </Button>
      </div>
    </div>
    <div class="w-5/6 bg-neutral-200 px-16" id="content">
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
.router-link-active > button {
  background-color: #c4b5fd;
  color: #f5f3ff;
  transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
  gap: 0.75rem;
}
</style>
