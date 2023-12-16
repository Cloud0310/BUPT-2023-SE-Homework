<template>
  <PageHeader page-title="主页" />
  <div class="flex h-[calc(100%-9rem)] flex-col justify-between py-10">
    <div class="flex flex-col gap-1">
      <span class="text-6xl font-bold text-neutral-400"> 欢迎使用 </span>
      <br />
      <span class="text-7xl font-bold text-primary-400">巴普特空调管理系统</span>
    </div>
    <div class="flex h-24 w-full justify-end">
      <button
        type="button"
        class="flex w-[200px] items-center justify-evenly rounded-xl bg-primary-100 p-3"
        @click="showLoginPanel = true"
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
        <span class="inline-block align-middle text-5xl font-bold text-neutral-400"> 登录 </span>
      </button>
      <el-dialog v-model="showLoginPanel" append-to-body title="登录" width="30%">
        <div class="flex flex-col gap-4 px-12">
          <el-input v-model="username" placeholder="请输入用户名" clearable />
          <el-input v-model="password" placeholder="请输入密码" clearable type="password" show-password />
          <div class="flex justify-end">
            <el-button type="primary" @click="showLoginPanel = false" style="--el-color-primary-light-3: #ddd6fe" small
              >登录</el-button
            >
          </div>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script lang="ts" setup>
const showLoginPanel = ref(false);
const username = ref("");
const password = ref("");
</script>
