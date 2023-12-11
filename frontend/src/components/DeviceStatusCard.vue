<template>
  <div class="flex flex-col justify-center gap-1 rounded-xl bg-[#fffbff] p-5 shadow-sm">
    <div class="flex items-center">
      <!-- TODO: room information -->
      <div class="self-start">
        <!-- ROOM icon -->
        <svg
          class="mr-2 inline-block align-middle text-[#625b70]"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 -960 960 960"
          height="40"
          width="40"
        >
          <path
            fill="currentColor"
            d="M80-200v-240q0-27 11-49t29-39v-112q0-50 35-85t85-35h160q23 0 43 8.5t37 23.5q17-15 37-23.5t43-8.5h160q50 0 85 35t35 85v112q18 17 29 39t11 49v240h-80v-80H160v80H80Zm440-360h240v-80q0-17-11.5-28.5T720-680H560q-17 0-28.5 11.5T520-640v80Zm-320 0h240v-80q0-17-11.5-28.5T400-680H240q-17 0-28.5 11.5T200-640v80Zm-40 200h640v-80q0-17-11.5-28.5T760-480H200q-17 0-28.5 11.5T160-440v80Zm640 0H160h640Z"
          />
        </svg>
        <span class="inline-block align-top text-3xl font-bold text-[#625b70]">{{ roomId }}</span>
      </div>
      <div class="grow" />
      <div class="text-sm">
        <div class="my-1">
          <img src="/images/icons/mode_heat_cool.svg" alt="模式" class="mr-2 inline-block h-6 w-6" />
          <!-- <span class="mr-2 inline-block align-middle text-xs">模式</span> -->
          <el-select v-model="currentMode" size="small" style="width: 60px">
            <el-option v-for="mode in modeOptions" :key="mode.value" :label="mode.label" :value="mode.value">
              <div class="flex items-center justify-between">
                <img :src="`images/icons/${mode.value}.svg`" :alt="mode.label" class="h-6 w-6 text-primary-100" />
                <span> {{ mode.label }}</span>
              </div>
            </el-option>
          </el-select>
        </div>
        <div class="my-1">
          <img src="/images/icons/sweep.svg" alt="扫风" class="mr-2 inline-block h-6 w-6" />
          <el-switch v-model="sweeping" inlinePrompt :activeIcon="Check" :inactiveIcon="Close" />
        </div>
      </div>
      <div class="mx-3 h-10 w-[1px] bg-neutral-300" />
      <!-- TODO: toggle on/off -->
      <div>
        <button
          type="button"
          @click="() => (on = !on)"
          class="h-11 w-11 rounded-full border border-transparent bg-neutral-100 p-2 transition-colors"
          :class="{
            'text-primary-500': on,
            'text-neutral-500': !on,
            'hover:text-primary-300': !on
          }"
        >
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960">
            <path
              fill="currentColor"
              d="M440-440v-400h80v400h-80Zm40 320q-74 0-139.5-28.5T226-226q-49-49-77.5-114.5T120-480q0-80 33-151t93-123l56 56q-48 40-75 97t-27 121q0 116 82 198t198 82q117 0 198.5-82T760-480q0-64-26.5-121T658-698l56-56q60 52 93 123t33 151q0 74-28.5 139.5t-77 114.5q-48.5 49-114 77.5T480-120Z"
            />
          </svg>
        </button>
      </div>
    </div>
    <div class="my-3 h-[1px] w-full bg-neutral-300" />
    <div>
      <!-- TODO: temperature display -->
      <div class="flex justify-start">
        <div>
          <span class="text-6xl font-bold text-[#49454e]">{{ temperature }}</span>
          <span class="text-2xl text-[#1c1b1e]">℃</span>
        </div>
        <div>
          <button type="button">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960" class="h-6 w-6">
              <path
                d="M680-520v-120H560v-80h120v-120h80v120h120v80H760v120h-80ZM320-120q-83 0-141.5-58.5T120-320q0-48 21-89.5t59-70.5v-240q0-50 35-85t85-35q50 0 85 35t35 85v240q38 29 59 70.5t21 89.5q0 83-58.5 141.5T320-120Zm-40-440h80v-160q0-17-11.5-28.5T320-760q-17 0-28.5 11.5T280-720v160Z"
              />
            </svg>
          </button>
          <button type="button">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960" class="h-6 w-6">
              <path
                fill="currentColor"
                d="M880-640H560v-80h320v80ZM320-120q-83 0-141.5-58.5T120-320q0-48 21-89.5t59-70.5v-240q0-50 35-85t85-35q50 0 85 35t35 85v240q38 29 59 70.5t21 89.5q0 83-58.5 141.5T320-120Zm0-80q50 0 85-35t35-85q0-29-12.5-54T392-416l-32-24v-280q0-17-11.5-28.5T320-760q-17 0-28.5 11.5T280-720v280l-32 24q-23 17-35.5 42T200-320q0 50 35 85t85 35Zm0-120Z"
              />
            </svg>
          </button>
        </div>
      </div>
      <!-- TODO: wind speed display-->
      <div></div>
    </div>
    <!-- TODO: last update time -->
    <div></div>
  </div>
</template>

<script lang="ts" setup>
import { Check, Close } from "@element-plus/icons-vue";

// import P5 from "p5";

const props = defineProps({
  roomId: {
    type: String,
    required: true
  },
  isOn: {
    type: Boolean
  },
  temperature: {
    type: Number
  },
  mode: {
    type: String
  },
  windSpeed: {
    type: Number,
    required: true
  },
  isWeeping: {
    type: Boolean
  },
  lastUpdate: {
    type: Date
  }
});

const modeOptions = [
  {
    value: "cool",
    label: "制冷"
  },
  {
    value: "heat",
    label: "制热"
  },
  {
    value: "auto",
    label: "自动"
  }
];

const sweeping = ref(props.isWeeping);
const currentMode = ref(props.mode);
const on = ref(props.isOn);
// console.log(props);
// const isOn = ref(props._isOn);

// const speed = ref(props.windSpeed);
// let angle = 0;
// onMounted(() => {
//   new P5(
//     (p: P5) => {
//       p.setup = () => {
//         p.createCanvas(200, 200, p.WEBGL);
//       };

//       p.draw = () => {
//         p.background(0, 0, 0, 0);
//         p.stroke(221, 214, 254);
//         p.strokeWeight(3);
//         p.fill(237, 233, 254);
//         p.push();
//         p.rotate(angle);

//         for (let i = 0; i < 3; i++) {
//           // fan blades
//           p.beginShape();
//           p.curveVertex(0, 0);
//           p.curveVertex(-25, -75);
//           p.curveVertex(35, -52);
//           p.curveVertex(0, 0);
//           p.curveVertex(0, 0);
//           p.endShape(p.CLOSE);

//           p.rotate(p.TWO_PI / 3);
//         }
//         p.pop();

//         p.fill(167, 139, 250); // center circle
//         p.strokeWeight(5);
//         p.ellipse(0, 0, 30, 30);

//         angle += p.radians(speed.value);
//       };
//     },
//     document.getElementById(props.roomId) as HTMLElement
//   );
// });
</script>
