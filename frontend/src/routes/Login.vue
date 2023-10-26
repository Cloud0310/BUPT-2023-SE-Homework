<template>
  <Teleport to="body">
    <div v-if="isLoginPannelEnabled" class="fixed top-0 left-0 w-full h-full flex justify-center items-center bg-black bg-opacity-50 z-20">
      <div class="w-96 h-80 bg-white rounded-lg p-8 relative">
        <p class="top-0 text-lg font-bold text-center">登录</p>
        <button class="absolute top-0 right-0 m-3 bg-transparent border-none outline-none cursor-pointer text-gray-500 text-xl " @click="closePanel">
            <el-icon><Close /></el-icon>
        </button>
        <div>
          <form action="" class="top-0 mt-2">
            <div class="my-1 flex justify-star items-center">
              <div>
                <svg height="24" width="24" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" data-v-ea893728="">
                  <path fill="currentColor" d="M512 512a192 192 0 1 0 0-384 192 192 0 0 0 0 384zm0 64a256 256 0 1 1 0-512 256 256 0 0 1 0 512zm320 320v-96a96 96 0 0 0-96-96H288a96 96 0 0 0-96 96v96a32 32 0 1 1-64 0v-96a160 160 0 0 1 160-160h448a160 160 0 0 1 160 160v96a32 32 0 1 1-64 0z"></path>
                </svg>
              </div>
              <div class="block text-gray-700">用户名</div>
            </div>
            <input type="text" v-model="username" class="w-full h-10 px-4 py-3 mt-2 bg-gray-200 border rounded-lg focus:border-blue-500 focus:bg-white focus:outline-none"/>
            
            <div class="mt-5 my-1 flex justify-star items-center">
              <div>
                <svg height="24" width="24" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" data-v-ea893728="">
                  <path fill="currentColor" d="M224 448a32 32 0 0 0-32 32v384a32 32 0 0 0 32 32h576a32 32 0 0 0 32-32V480a32 32 0 0 0-32-32H224zm0-64h576a96 96 0 0 1 96 96v384a96 96 0 0 1-96 96H224a96 96 0 0 1-96-96V480a96 96 0 0 1 96-96z"></path><path fill="currentColor" d="M512 544a32 32 0 0 1 32 32v192a32 32 0 1 1-64 0V576a32 32 0 0 1 32-32zm192-160v-64a192 192 0 1 0-384 0v64h384zM512 64a256 256 0 0 1 256 256v128H256V320A256 256 0 0 1 512 64z"></path>
                </svg>
              </div>  
              <div class="block text-gray-700">密码</div>
            </div>            
            <input type="password" v-model="password" class="w-full h-10 px-4 py-3 mt-2 bg-gray-200 border rounded-lg focus:border-blue-500 focus:bg-white focus:outline-none"/>
            <i class="fa fa-eye-slash" aria-hidden="true"></i>
          </form>
        </div>
        <div class="flex justify-center items-center mt-5 ">
          <button type="button" class="flex justify-center gap-2 items-center h-10 rounded-xl px-10 bg-primary-200" @click="confirmlogin">
              登录
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">

defineProps ({
    isLoginPannelEnabled: { type: Boolean, required: true }
});

const emits = defineEmits(['close','login']); 
const closePanel = () => {
  emits('close');
};

const username = ref("");
const password = ref("");

// const emitsLogin = defineEmits(['login']);
const isLogin = ref<boolean>(false);

function confirmlogin() {
  if (username.value === "admin" && password.value === "admin"){
    console.log("确认登录");
    isLogin.value = true;
    emits('login',isLogin.value);
    showDialog("登录成功!欢迎使用！");
    emits('close');
    
  }else{
    showDialog("登录失败!请检查用户名和密码。");
  }
}

function showDialog(message: string) {
  const elDialog = document.createElement("div");
  elDialog.className = "fixed top-0 left-0 w-full h-full flex justify-center items-center bg-black bg-opacity-50 z-50";

  const dialogContent = document.createElement("div");
  dialogContent.className = "w-86 h-24 bg-white rounded-lg p-8 text-center flex justify-center items-center";
  dialogContent.textContent = message;

  elDialog.appendChild(dialogContent);
  document.body.appendChild(elDialog);

  setTimeout(() => {
    dialogContent.remove();
    elDialog.remove();
  }, 1000);
}
</script>
