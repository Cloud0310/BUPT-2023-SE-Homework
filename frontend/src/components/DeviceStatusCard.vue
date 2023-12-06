<template>
  <div class="h-14 w-20 rounded shadow-sm">
    <div>
      <div id="fans"></div>
      <el-select v-model="speed" placeholder="风速">
        <el-option v-for="option in speedOptions" :key="option.value" :label="option.label" :value="option.value" />
      </el-select>
    </div>
  </div>
</template>

<script lang="ts" setup>
import P5 from "p5";

let angle = 0;
const speedOptions = [
  { value: 1, label: "快速" },
  { value: 2, label: "适中" },
  { value: 3, label: "慢速" }
];
const speed = ref();
new P5(
  (p: P5) => {
    p.setup = () => {
      // @ts-ignore
      p.createCanvas(200, 200, WEBGL);
    };

    p.draw = () => {
      p.background(220);
      p.push();
      p.rotate(angle);
      for (let i = 0; i < 3; i++) {
        p.fill(255, 255, 255);
        p.beginShape();
        p.curveVertex(0, 0);
        p.curveVertex(0, 0);
        p.curveVertex(-25, -75);
        p.curveVertex(35, -52);
        p.curveVertex(0, 0);
        p.curveVertex(0, 0);
        p.endShape();
        p.rotate((p.PI / 3) * 2);
      }
      p.pop();
      angle += p.radians(speed.value);
    };
  },
  document.getElementById("fans") as HTMLElement
);

enum mode {
  cold = "制冷",
  hot = "制热",
  auto = "自动"
}

interface device {
  roomId: String;
  isOn: Boolean;
  temperature: Number;
  mode: mode;
  windSpeed: Number;
  isWeeping: Boolean;
  lastUpdateTime: Date;
}

const devices = ref<device[]>([]);
</script>
