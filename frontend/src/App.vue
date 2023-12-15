<script setup lang="ts">
import { ref } from "vue";
import PanelSwitchButton from "./components/PanelSwitchButton.vue";
import Login from "./components/Login.vue";
// const dateInfo = ref<Date>(new Date(Date.now()));

const isLoginPannelEnabled = ref<boolean>(false);
const isLogin = ref<boolean>(false);
function handleLogin(isLoggedIn: boolean) {
  isLogin.value = isLoggedIn;
}

function handleLoginClick() {
  if (!isLogin.value) {
    isLoginPannelEnabled.value = true;
  } else {
    isLogin.value = false;
  }
}
</script>

<template>
  <div class="flex h-[100vh] w-[100vw]">
    <div class="sticky flex h-full w-1/6 min-w-fit shrink-0 flex-col justify-between px-12 py-5">
      <!-- logo and title -->
      <div>
        <div class="my-5 flex h-20 items-center justify-center gap-3">
          <div>
            <!-- air icon from material symbols -->
            <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
              <path
                fill="currentColor"
                d="M750-614q-27 27-62 41t-70 14q-35 0-69-13.5T488-614l-75-75q-15-15-34-22.5t-39-7.5q-20 0-39 7.5T267-689l-75 75-57-57 75-75q27-27 61-40.5t69-13.5q35 0 68.5 13.5T469-746l75 75q16 16 35 23.5t39 7.5q20 0 39.5-7.5T693-671l75-75 57 57-75 75Zm0 200q-27 27-61.5 40.5T619-360q-35 0-69.5-13.5T488-414l-75-75q-15-15-34-22.5t-39-7.5q-20 0-39 7.5T267-489l-75 75-57-56 75-76q27-27 61-40.5t69-13.5q35 0 68.5 13.5T469-546l75 75q16 16 35 23.5t39 7.5q20 0 39.5-7.5T693-471l75-75 57 57-75 75Zm-1 200q-27 27-61 40.5T619-160q-35 0-69.5-13.5T488-214l-76-75q-15-15-34-22.5t-39-7.5q-20 0-39 7.5T266-289l-75 75-56-56 75-76q27-27 61-40.5t69-13.5q35 0 68.5 13.5T469-346l75 75q16 16 35.5 23.5T619-240q20 0 39-7.5t35-23.5l75-75 56 57-75 75Z"
              />
            </svg>
          </div>
          <div class="w-fit text-xl font-bold">空调管理系统</div>
        </div>
        <!-- menu -->
        <div class="flex flex-col gap-3">
          <div>
            <router-link to="/">
              <PanelSwitchButton class="w-full hover:gap-3">
                <!-- home icon from material symbols -->
                <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
                  <path
                    fill="currentColor"
                    d="M240-200h120v-240h240v240h120v-360L480-740 240-560v360Zm-80 80v-480l320-240 320 240v480H520v-240h-80v240H160Zm320-350Z"
                  />
                </svg>
                <span>主页</span>
              </PanelSwitchButton>
            </router-link>
          </div>
          <div>
            <router-link to="/devices">
              <PanelSwitchButton class="w-full hover:gap-3">
                <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
                  <path
                    fill="currentColor"
                    d="M120-120v-80h80v-640h400v40h160v240h-80v-160h-80v240h-80v-280H280v560h200v80H120Zm560 40-12-60q-12-5-22.5-11T625-165l-58 20-40-69 45-40q-2-15-2-25.5t2-25.5l-45-40 40-69 58 20q10-8 20.5-14.5T668-420l12-60h80l12 60q12 5 22.5 11t20.5 14l58-20 40 69-45 40q2 15 2 25.5t-2 25.5l45 40-40 69-58-19q-10 8-20.5 14T772-140l-12 60h-80Zm40-120q33 0 56.5-23.5T800-280q0-33-23.5-56.5T720-360q-33 0-56.5 23.5T640-280q0 33 23.5 56.5T720-200ZM440-440q-17 0-28.5-11.5T400-480q0-17 11.5-28.5T440-520q17 0 28.5 11.5T480-480q0 17-11.5 28.5T440-440ZM280-200v-560 560Z"
                  />
                  /> />
                </svg>
                <span>房间</span>
              </PanelSwitchButton>
            </router-link>
          </div>
          <div>
            <router-link to="/admin">
              <PanelSwitchButton class="w-full hover:gap-3">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960" class="h-6 w-6">
                  <path
                    fill="currentColor"
                    d="M120-120v-80h80v-560q0-33 23.5-56.5T280-840h400q33 0 56.5 23.5T760-760v560h80v80H120Zm560-80v-560H280v560h400ZM560-440q17 0 28.5-11.5T600-480q0-17-11.5-28.5T560-520q-17 0-28.5 11.5T520-480q0 17 11.5 28.5T560-440ZM280-760v560-560Z"
                  />
                </svg>
                <span>管理</span>
              </PanelSwitchButton>
            </router-link>
          </div>
          <!-- help page (may not implement) -->
        </div>
      </div>
      <div class="my-5 flex w-full justify-center">
        <PanelSwitchButton @click="handleLoginClick">
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
            <path
              fill="currentColor"
              d="M480.026-140.001v-50.255h277.409q4.616 0 8.462-3.847 3.847-3.846 3.847-8.462v-554.87q0-4.616-3.847-8.462-3.846-3.847-8.462-3.847H480.026v-50.255h277.409q25.788 0 44.176 18.388t18.388 44.176v554.87q0 25.788-18.388 44.176t-44.176 18.388H480.026Zm-41.922-181.54-35.845-35.947 97.385-97.385H140.001v-50.254h358.822l-97.384-97.385 35.589-36.204 159.126 159.254-158.05 157.921Z"
            />
          </svg>
          <span v-if="isLogin">退出</span>
          <span v-else>登录</span>
        </PanelSwitchButton>
        <Login
          :is-login-pannel-enabled="isLoginPannelEnabled"
          @close="isLoginPannelEnabled = false"
          @login="handleLogin"
        ></Login>
      </div>
    </div>
    <div class="h-full w-5/6 overflow-y-scroll bg-neutral-100 px-16" id="content">
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
