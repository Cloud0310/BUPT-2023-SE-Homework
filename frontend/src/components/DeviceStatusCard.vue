<template>
  <div class="flex flex-col justify-center rounded-xl bg-neutral-200 p-5 shadow-sm">
    <div>
      <span class="text-lg font-bold">
        {{ roomId }}
      </span>
      <div>
        <el-switch
          v-model="isOn"
          @change="$emit('updateIsOn')"
          style="--el-switch-on-color: #13ce66; --el-switch-off-color: #ff4949"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ElSwitch } from "element-plus";
import P5 from "p5";

const props = defineProps({
  roomId: {
    type: String,
    required: true
  },
  _isOn: {
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

const emit = defineEmits(["updateWindSpeed", "updateIsOn"]);
// const speedOptions = [
//   { value: 2, label: "慢速" },
//   { value: 5, label: "适中" },
//   { value: 8, label: "快速" }
// ];

const speed = ref(props.windSpeed);
const isOn = ref(props._isOn);

let angle = 0;
onMounted(() => {
  new P5(
    (p: P5) => {
      p.setup = () => {
        p.createCanvas(200, 200, p.WEBGL);
      };

      p.draw = () => {
        p.background(0, 0, 0, 0);
        p.stroke(221, 214, 254);
        p.strokeWeight(3);
        p.fill(237, 233, 254);
        p.push();
        p.rotate(angle);

        for (let i = 0; i < 3; i++) {
          // fan blades
          p.beginShape();
          p.curveVertex(0, 0);
          p.curveVertex(-25, -75);
          p.curveVertex(35, -52);
          p.curveVertex(0, 0);
          p.curveVertex(0, 0);
          p.endShape(p.CLOSE);

          p.rotate(p.TWO_PI / 3);
        }
        p.pop();

        p.fill(167, 139, 250); // center circle
        p.strokeWeight(5);
        p.ellipse(0, 0, 30, 30);

        angle += p.radians(speed.value);
      };
    },
    document.getElementById(props.roomId) as HTMLElement
  );
});
</script>
