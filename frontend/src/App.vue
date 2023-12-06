<script setup lang="ts">
import { ref } from "vue";
import Button from "./components/Button.vue";
import Login from "./components/Login.vue";
const dateInfo = ref<Date>(new Date(Date.now()));

const isLoginPannelEnabled = ref<boolean>(false);
const isLogin = ref<boolean>(false);
function handleLogin(isLoggedIn: boolean) {
  isLogin.value = isLoggedIn;
}

function handleLoginClick() {
  if (!isLogin.value) {
    isLoginPannelEnabled.value = true;
    // router.push('/login');
  } else {
    isLogin.value = false;
  }
}
</script>

<template>
  <div class="flex h-[100vh] w-[100vw]">
    <div class="sticky flex h-full w-1/6 flex-col justify-between px-12 py-5">
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
              <Button class="w-full hover:gap-3">
                <!-- home icon from material symbols -->
                <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
                  <path
                    fill="currentColor"
                    d="M240-200h120v-240h240v240h120v-360L480-740 240-560v360Zm-80 80v-480l320-240 320 240v480H520v-240h-80v240H160Zm320-350Z"
                  />
                </svg>
                <span>主页</span>
              </Button>
            </router-link>
          </div>
          <div>
            <router-link to="/devices">
              <Button class="w-full hover:gap-3">
                <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
                  <path
                    fill="currentColor"
                    d="M450.001-90v-179.848L310-131.847 267.847-174l182.154-182.154v-93.847h-93.847L174-267.847 131.847-310l138.001-140.001H90.001v-59.998h179.847L131.847-650 174-692.153l182.154 182.154h93.847v-93.847L267.847-786 310-828.153l140.001 138.001v-179.847h59.998v179.847L650-828.153 692.153-786 509.999-603.846v93.847h93.847L786-692.153 828.153-650 690.152-509.999h179.847v59.998H690.152L828.153-310 786-267.847 603.846-450.001h-93.847v93.847L692.153-174 650-131.847 509.999-269.848v179.847h-59.998Z"
                  />
                </svg>
                <span>设备</span>
              </Button>
            </router-link>
          </div>
          <!-- help page (may not implement) -->
          <!-- <div class=""></div> -->
          <!-- login and logout -->
        </div>
      </div>
      <div class="my-5 flex w-full justify-center">
        <Button @click="handleLoginClick">
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
            <path
              fill="currentColor"
              d="M480.026-140.001v-50.255h277.409q4.616 0 8.462-3.847 3.847-3.846 3.847-8.462v-554.87q0-4.616-3.847-8.462-3.846-3.847-8.462-3.847H480.026v-50.255h277.409q25.788 0 44.176 18.388t18.388 44.176v554.87q0 25.788-18.388 44.176t-44.176 18.388H480.026Zm-41.922-181.54-35.845-35.947 97.385-97.385H140.001v-50.254h358.822l-97.384-97.385 35.589-36.204 159.126 159.254-158.05 157.921Z"
            />
          </svg>
          <span v-if="isLogin">退出</span>
          <span v-else>登录</span>
        </Button>
        <Login
          :is-login-pannel-enabled="isLoginPannelEnabled"
          @close="isLoginPannelEnabled = false"
          @login="handleLogin"
        ></Login>
      </div>
    </div>
    <div class="w-5/6 bg-neutral-100 px-16" id="content">
      <div class="my-5 flex h-20 items-center justify-between px-5">
        <div class="flex h-full flex-col justify-center gap-[0.2rem] font-bold">
          <div class="text-2xl">仪表板</div>
          <div class="text-sm text-neutral-400">
            {{
              dateInfo.toLocaleTimeString("zh-CN", {
                hour: "2-digit",
                minute: "2-digit"
              })
            }}
          </div>
        </div>
        <div class="flex items-center justify-evenly gap-3">
          <div>
            <!-- avatar icon -->
            <svg xmlns="http://www.w3.org/2000/svg" height="40" viewBox="0 -960 960 960" width="40">
              <path
                fill="currentColor"
                d="M243.924-277.307q54-36.846 112.615-54.769Q415.154-349.999 480-349.999t123.461 17.923q58.615 17.923 112.615 54.769 37.308-41 56.616-92.923Q792-422.154 792-480q0-129.675-91.23-220.838Q609.541-792 479.77-792 350-792 259-700.838 168-609.675 168-480q0 57.846 19.308 109.77 19.308 51.923 56.616 92.923Zm236.088-140.694q-55.781 0-94.896-39.103-39.115-39.104-39.115-94.884 0-55.781 39.103-94.896 39.104-39.115 94.884-39.115 55.781 0 94.896 39.103 39.115 39.104 39.115 94.884 0 55.781-39.103 94.896-39.104 39.115-94.884 39.115Zm.264 302q-75.43 0-141.775-28.27-66.346-28.269-116.154-78.076-49.807-49.808-78.076-116.112-28.27-66.304-28.27-141.999 0-75.696 28.27-141.541 28.269-65.846 78.076-115.654 49.808-49.807 116.112-78.076 66.304-28.27 141.999-28.27 75.696 0 141.541 28.27 65.846 28.269 115.654 78.076 49.807 49.808 78.076 115.878 28.27 66.07 28.27 141.499 0 75.43-28.27 141.775-28.269 66.346-78.076 116.154-49.808 49.807-115.878 78.076-66.07 28.27-141.499 28.27ZM480-168q53.154 0 104.423-18.423 51.27-18.423 93.27-52.731-43-28.154-93.116-43.5Q534.462-298.001 480-298.001q-54.462 0-105.27 14.654-50.808 14.654-92.423 44.193 42 34.308 93.27 52.731Q426.846-168 480-168Zm0-301.999q33.846 0 57.924-24.077 24.077-24.078 24.077-57.924 0-33.846-24.077-57.924-24.078-24.077-57.924-24.077-33.846 0-57.924 24.077-24.077 24.078-24.077 57.924 0 33.846 24.077 57.924 24.078 24.077 57.924 24.077ZM480-552Zm0 314Z"
              />
            </svg>
          </div>
          <div class="text-xl font-bold">Cloud Liu</div>
        </div>
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
