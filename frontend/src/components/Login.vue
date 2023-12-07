<template>
  <Teleport to="body">
    <div
      v-if="isLoginPannelEnabled"
      class="fixed left-0 top-0 z-20 flex h-full w-full items-center justify-center bg-black bg-opacity-50"
    >
      <div class="relative w-96 rounded-lg bg-white p-8">
        <p class="top-0 my-10 ml-3 text-3xl font-bold">登录</p>
        <button
          class="absolute right-0 top-0 m-3 cursor-pointer border-none bg-transparent text-xl text-neutral-500 outline-none"
          @click="closePanel"
        >
          <!-- close button -->
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
            <path
              fill="currentColor"
              d="m256-200-56-56 224-224-224-224 56-56 224 224 224-224 56 56-224 224 224 224-56 56-224-224-224 224Z"
            />
          </svg>
        </button>
        <div>
          <form action="" class="top-0 my-2 flex flex-col items-start justify-center gap-3">
            <label for="username" class="ml-3">用户名</label>
            <input
              type="text"
              v-model="username"
              id="username"
              class="focus:border-1 h-9 w-full rounded-lg bg-neutral-50 px-3 py-3 caret-neutral-300 shadow-md transition-colors focus-within:border-primary-200 focus:bg-neutral-100 focus:outline-none"
            />
            <label for="password" class="ml-3">密码</label>
            <input
              type="password"
              id="password"
              v-model="password"
              class="focus:border-1 h-9 w-full rounded-lg bg-neutral-50 px-3 py-3 caret-neutral-300 shadow-md transition-colors focus-within:border-primary-200 focus:bg-neutral-100 focus:outline-none"
            />
          </form>
        </div>
        <div class="mt-7 flex items-center justify-start gap-4">
          <button
            type="button"
            class="rounded-lg bg-primary-300 px-5 py-2 text-sm text-neutral-50 transition-all hover:bg-primary-400 hover:text-neutral-100"
            @click="confirmlogin"
          >
            登录
          </button>
          <div>
            <el-radio-group v-model="options">
              <el-radio label="前台" />
              <el-radio label="空调管理员" />
            </el-radio-group>
          </div>

        </div>
        <div class="text-right">
          <button type="button" @click="handleRegisterClick" class="underline">注册
          </button>
          <Register 
          :is-register-pannel-enabled="isRegisterPannelEnabled"
          @close="isRegisterPannelEnabled = false"
          @register="handleRegister"
          ></Register>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from "vue";
// import { ElMessage } from "element-plus";
import Register from "./Register.vue";

defineProps({
  isLoginPannelEnabled: { type: Boolean, required: true }
});

const emits = defineEmits(["close", "login"]);
const closePanel = () => {
  emits("close");
};

const username = ref("");
const password = ref("");
const options = ref("前台");

// const emitsLogin = defineEmits(['login']);
const isRegister = ref<boolean>(false);

function confirmlogin() {
  if (username.value === "admin" && password.value === "admin") {
    console.log("确认登录");
    console.log(options.value)
    isLogin.value = true;
    emits("login", isLogin.value);
    ElMessage({ message: "登录成功！欢迎使用！", type: "success" });
    emits("close");
  } else {
    ElMessage({ message: "登录失败！请检查用户名和密码。", type: "error" });
  }
}
const isRegisterPannelEnabled = ref<boolean>(false);
const isLogin = ref<boolean>(false);
function handleRegister(isregistered: boolean) {
  isLogin.value = isregistered;
}
function handleRegisterClick() {
  if (!isLogin.value) {
    isRegisterPannelEnabled.value = true;
    // router.push('/login');
  } else {
    isRegister.value = false;
  }
}
</script>
