<template>
  <div class="flex flex-col justify-center gap-1 rounded-xl p-5">
    <div class="flex items-center">
      <!-- room information -->
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
          <el-select v-model="currentMode" size="small" style="width: 60px" :disabled="!on">
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
          <el-switch v-model="sweeping" :disabled="!on" inlinePrompt :activeIcon="Check" :inactiveIcon="Close" />
        </div>
      </div>
      <div class="mx-3 h-10 w-[1px] bg-neutral-300" />
      <!-- toggle on/off -->
      <div>
        <button
          type="button"
          @click="() => (fanSpeed = (on = !on) ? fanSpeed : 0)"
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
    <div class="flex h-full justify-between">
      <!-- temperature display -->
      <div class="inline-block">
        <div
          class="inline-block w-24 align-bottom transition-colors"
          :style="{
            color: temperatureToHSL(temperature)
          }"
        >
          <span class="text-6xl font-bold">{{ temperature }}</span>
          <span class="text-2xl">℃</span>
        </div>
        <div class="mr-10 inline-block h-[150px]">
          <el-slider
            v-model="temperature"
            vertical
            :max="35"
            :min="0"
            :marks="marks"
            placement="right"
            :disabled="!on"
          />
        </div>
      </div>
      <!-- wind speed display-->
      <div class="inline-block">
        <div :id="roomId" class="flex justify-end" />
        <div>
          <div class="mr-3 inline-block h-6 w-6 align-middle">
            <!-- fan icon -->
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -960 960 960">
              <path
                fill="currentColor"
                d="M400-40q0-33 23.5-56.5T480-120v-208q-12-5-22.5-11.5T438-354l-88 56q-14 8-30.5 10.5T286-290l-180-51q-29-8-47.5-32.5T40-429q0-38 26.5-64.5T131-520h301q10-11 22-19t26-13v-137q0-17 6.5-32t18.5-26l137-128q23-22 53.5-25t56.5 13q32 20 41.5 56.5T783-762L624-499q7 12 10.5 26t4.5 29l108 26q16 4 29 14t21 24l91 164q15 27 11 57t-26 52q-27 27-64.5 27T744-107L560-291v171q33 0 56.5 23.5T640-40H400ZM160-760v-80h240v80H160Zm400 71v137q1 0 1.5.5t1.5.5l152-253q2-4 1-8.5t-5-6.5q-3-2-7.5-1t-6.5 3L560-689ZM40-600v-80h200v80H40Zm480 200q17 0 28.5-11.5T560-440q0-17-11.5-28.5T520-480q-17 0-28.5 11.5T480-440q0 17 11.5 28.5T520-400Zm-211 34 93-56q-1-5-1-9v-9H131q-5 0-8 3t-3 8q0 4 2 7t6 4l181 52Zm419 25-114-26q-2 2-4 5t-4 5l195 194q3 3 8 3t8-3q3-3 3.5-6.5T819-177l-91-164ZM120-120v-80h200v80H120Zm400-320Zm43-111ZM401-440Zm205 83Z"
              />
            </svg>
          </div>
          <div class="inline-block align-middle text-lg">
            <el-input-number v-model="fanSpeed" :disabled="!on" :min="0" :max="5"></el-input-number>
          </div>
        </div>
      </div>
    </div>
    <!-- last update time -->
    <div class="flex justify-between">
      <div>
        <el-button v-if="!isCheckedIn" @click="isCheckedIn = true"> 入住 </el-button>
        <el-button v-else @click="(showBillDialog = true), (isCheckedIn = false), (on = false), (fanSpeed = 0)">
          退房
        </el-button>
        <el-dialog v-model="showBillDialog" center title="账单" append-to-body>
          <el-table :data="billData" stripe>
            <el-table-column prop="startTime" label="开始时间" width="120" />
            <el-table-column prop="endTime" label="结束时间" width="120" />
            <el-table-column prop="temperature" label="温度" />
            <el-table-column prop="wind_speed" label="风速" />
            <el-table-column prop="mode" label="模式" />
            <el-table-column prop="sweep" label="扫风" />
            <el-table-column prop="duration" label="时长" />
            <el-table-column prop="cost" label="费用" fixed="right" />
          </el-table>
        </el-dialog>
      </div>
      <span class="text-xs text-neutral-500"
        >最后更新于
        {{
          lastUpdate.toLocaleDateString("zh-cn", {
            month: "short",
            day: "numeric",
            hour: "numeric",
            minute: "numeric"
          })
        }}</span
      >
    </div>
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

const dateOptions = {
  month: "short",
  day: "numeric",
  hour: "numeric",
  minute: "numeric"
};

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
  },
  {
    value: "off",
    label: "关闭"
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

const billData = [
  {
    startTime: new Date("01-01 00:12:00").toLocaleString("zh-cn", dateOptions as any),
    endTime: new Date("01-01 01:12:00").toLocaleString("zh-cn", dateOptions as any),
    temperature: "25℃",
    wind_speed: "2",
    mode: "制冷",
    sweep: "是",
    duration: "1 小时",
    cost: "10 元"
  },
  {
    startTime: new Date("01-01 02:12:00").toLocaleString("zh-cn", dateOptions as any),
    endTime: new Date("01-01 03:12:00").toLocaleString("zh-cn", dateOptions as any),
    temperature: "18℃",
    wind_speed: "3",
    mode: "制冷",
    sweep: "是",
    duration: "30 分钟",
    cost: "5 元"
  },
  {
    startTime: new Date("01-01 04:12:00").toLocaleString("zh-cn", dateOptions as any),
    endTime: new Date("01-01 05:12:00").toLocaleString("zh-cn", dateOptions as any),
    temperature: "25℃",
    wind_speed: "2",
    mode: "制冷",
    sweep: "是",
    duration: "1 小时",
    cost: "10 元"
  },
  {
    startTime: new Date("01-01 06:12:00").toLocaleString("zh-cn", dateOptions as any),
    endTime: new Date("01-01 07:12:00").toLocaleString("zh-cn", dateOptions as any),
    temperature: "18℃",
    wind_speed: "3",
    mode: "制冷",
    sweep: "是",
    duration: "30 分钟",
    cost: "5 元"
  },
  {
    startTime: new Date("01-01 08:12:00").toLocaleString("zh-cn", dateOptions as any),
    endTime: new Date("01-01 09:12:00").toLocaleString("zh-cn", dateOptions as any),
    temperature: "25℃",
    wind_speed: "2",
    mode: "制冷",
    sweep: "是",
    duration: "1 小时",
    cost: "10 元"
  },
  {
    startTime: new Date("01-01 10:12:00").toLocaleString("zh-cn", dateOptions as any),
    endTime: new Date("01-01 11:12:00").toLocaleString("zh-cn", dateOptions as any),
    temperature: "18℃",
    wind_speed: "3",
    mode: "制冷",
    sweep: "是",
    duration: "30 分钟",
    cost: "5 元"
  },
  {
    startTime: new Date("01-01 12:12:00").toLocaleString("zh-cn", dateOptions as any),
    endTime: new Date("01-01 13:12:00").toLocaleString("zh-cn", dateOptions as any),
    temperature: "25℃",
    wind_speed: "2",
    mode: "制冷",
    sweep: "是",
    duration: "1 小时",
    cost: "10 元"
  }
];

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
const isCheckedIn = ref<boolean>(true);
const showBillDialog = ref<boolean>(false);

const on = ref(true);
const currentMode = ref(on ? "cool" : "off");
const sweeping = ref(on ? true : false);
const temperature = ref(Math.floor(Math.random() * 30));
const minTemperature = 0;
const maxTemperature = 35;
const fanSpeed = ref(on.value ? 1 : 0);
const lastUpdate = ref<Date>(new Date());

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

function temperatureToHSL(temp: number) {
  if (on.value) {
    const hue = 240 + ((temp - minTemperature) / (maxTemperature - minTemperature)) * 120;
    return `hsl(${hue}, 80%, 65%)`;
  } else {
    return "hsl(0, 0%, 70%)";
  }
}

let intervalId = 0;

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
        angle += p.radians(fanSpeed.value * 2);
        p.image(buffer, -75, -75);
      };
    },
    document.getElementById(props.roomId) as HTMLElement
  );
});

onUnmounted(() => {
  clearInterval(intervalId);
});
</script>
