<template>
  <button
    type="button"
    class="flex w-[200px] items-center justify-evenly rounded-xl bg-primary-100 p-3"
    @click="LoginPanel"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="inline-block h-16 w-16 text-primary-400"
      viewBox="0 -960 960 960"
    >
      <path
        fill="currentColor"
        d="M480-120v-80h280v-560H480v-80h280q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H480Zm-80-160-55-58 102-102H120v-80h327L345-622l55-58 200 200-200 200Z"
      />
    </svg>
    <span v-if="isLogin" class="inline-block align-middle text-5xl font-bold text-neutral-400"> 退出 </span>
    <span v-else class="inline-block align-middle text-5xl font-bold text-neutral-400">登录</span>
  </button>
  <el-dialog v-model="showLoginPanel" append-to-body title="登录" width="30%">
    <div class="flex flex-col gap-4 px-12">
      <el-input v-model="username" placeholder="请输入用户名" clearable />
      <el-input v-model="password" placeholder="请输入密码" clearable type="password" show-password />
      <div class="flex justify-end">
        <el-button type="primary" @click="handleLogin" style="--el-color-primary-light-3: #ddd6fe" small
          >登录</el-button
        >
      </div>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { login } from '../utils/requests.ts';

const isLogin = ref<boolean>(false);
const showLoginPanel = ref(false);
const username = ref("");
const password = ref("");

function LoginPanel(){
  if(!isLogin.value){
    showLoginPanel.value = true;
  } else{
    showLoginPanel.value = false;
    isLogin.value = false;
  }
};

const handleLogin = () => {
  // if (username.value === "admin" && password.value === "admin") {
  //   isLogin.value = true;
  //   showLoginPanel.value = false;
  //   ElMessage({ message: "登录成功！欢迎使用！", type: "success" });
  // } else {
  //   ElMessage({ message: "登录失败！请检查用户名和密码。", type: "error" });
  // };

  login(username.value, password.value, (data) => {
    console.log('登录成功:', data);
    ElMessage({ showClose: true,message: "登录成功！欢迎使用！", type: "success" });
    isLogin.value = true;
    showLoginPanel.value = false;
  }, (errorCode) => {
    console.error('登录错误:', errorCode);
    ElMessage({ showClose: true,message: "登录失败！请检查用户名和密码。", type: "error" });
  });
};
</script>
