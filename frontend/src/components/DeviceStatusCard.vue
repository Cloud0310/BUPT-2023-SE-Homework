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
        <div class="mb-1">
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
        <div class="mt-1">
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
            'text-primary-400': on,
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
      <div class="inline-block">
        <div class="inline-block w-24 align-bottom">
          <span class="text-6xl font-bold text-[#49454e]">{{ temperature }}</span>
          <span class="text-2xl text-[#1c1b1e]">℃</span>
        </div>
        <div class="mr-10 inline-block h-[150px]">
          <el-slider v-model="temperature" vertical :max="35" :min="0" :marks="marks" placement="right"></el-slider>
        </div>
      </div>
      <!-- TODO: wind speed display-->
      <div :id="roomId" class="inline-block" />
    </div>
    <!-- TODO: last update time -->
    <div></div>
  </div>
</template>

<script lang="ts" setup>
import { Check, Close } from "@element-plus/icons-vue";
import P5 from "p5";

const props = defineProps({
  roomId: {
    type: String,
    required: true
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

const marks = {
  10: "10℃",
  20: "20℃"
};

interface roomStatus {
  roomId: number;
  isOn: boolean;
  temperature: number;
  mode: string;
  windSpeed: number;
  isWeeping: boolean;
  lastUpdate: Date;
}

function getRoomStatus(
  csrfToken: string,
  roomId: string,
  onSuccess: (s: roomStatus) => void,
  onError: (e: string) => void
) {
  csrfToken;
  roomId;
  const s = {
    roomId: 114,
    isOn: true,
    temperature: 25,
    mode: "cool",
    windSpeed: 2,
    isWeeping: false,
    lastUpdate: new Date()
  };
  onSuccess(s);
  onError("failed");
}

const currentMode = ref("cool");
const sweeping = ref(false);
const temperature = ref(25);
const on = ref(true);
const fansSpeed = ref(1);

function updateRoomStatus() {
  getRoomStatus(
    "csrfToken",
    props.roomId,
    s => {
      currentMode.value = s.mode;
      sweeping.value = s.isWeeping;
      temperature.value = s.temperature;
      on.value = s.isOn;
    },
    () => {}
  );
}

let intervalId = 0;
intervalId;

let angle = 0;
let buffer: P5.Graphics;
onMounted(() => {
  updateRoomStatus();
  // intervalId = setInterval(updateRoomStatus, 5000);
  new P5(
    (p: P5) => {
      p.setup = () => {
        p.createCanvas(150, 150, p.WEBGL);
        buffer = p.createGraphics(150, 150, p.WEBGL);
        buffer.background(0, 0, 0, 0);
        buffer.fill(167, 139, 250);
        buffer.stroke(221, 214, 254);
        buffer.strokeWeight(3);
        buffer.ellipse(0, 0, 18, 18);
      };

      p.draw = () => {
        // p.background(0, 0, 0, 0);
        p.clear(0, 0, 0, 0);
        p.stroke(221, 214, 254);
        p.strokeWeight(2);
        p.fill(237, 233, 254);
        p.push();
        p.rotate(angle);

        for (let i = 0; i < 3; i++) {
          // fan blades
          p.beginShape();
          p.vertex(0, 0);
          p.bezierVertex(-40, -80, 40, -80, 0, 0);
          p.endShape(p.CLOSE);
          p.rotate(p.TWO_PI / 3);
        }
        p.pop();
        angle += p.radians(fansSpeed.value);
        p.image(buffer, -75, -75);
      };
    },
    document.getElementById(props.roomId) as HTMLElement
  );
});

onUnmounted(() => {
  // clearInterval(intervalId);
});
</script>
