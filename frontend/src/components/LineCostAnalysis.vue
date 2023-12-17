<template>
  <div class="flex flex-col gap-2">
    <el-select v-model="currentOption" class="w-[10rem] self-end" placeholder="本月净收入" size="small">
      <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
    </el-select>
    <v-chart class="h-96" :option="option as any" />
  </div>
</template>

<script lang="ts" setup>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { LineChart } from "echarts/charts";
import { UniversalTransition } from "echarts/features";

import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  VisualMapComponent,
  MarkAreaComponent
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { ref, provide } from "vue";

const income = Array.from({ length: 30 }, () => Math.floor(Math.random() * (1000 - 500 + 1)) + 500);
const cost = Array.from({ length: 30 }, () => Math.floor(Math.random() * (500 - 300 + 1)) + 300);
const netIncome = Array.from({ length: cost.length }, (_, index) => income[index] - cost[index]);

const currentOption = ref("净收入");

const options = [
  {
    value: "收入",
    label: "本月收入情况"
  },
  {
    value: "净收入",
    label: "本月净收入情况"
  },
  {
    value: "支出",
    label: "本月支出情况"
  }
];

const currentData = computed(() => {
  switch (currentOption.value) {
    case "收入":
      console.log(income);
      return income;
    case "净收入":
      return netIncome;
    case "支出":
      return cost;
  }
});

use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  VisualMapComponent,
  MarkAreaComponent,
  LineChart,
  CanvasRenderer,
  UniversalTransition
]);

provide(THEME_KEY, "light");

const option = ref<any>({
  title: {
    text: "本月收支情况"
  },
  color: "#a78bfa",
  tooltip: {
    trigger: "axis"
  },
  xAxis: {
    type: "category",
    data: Array.from({ length: 30 }, (_, index) => index + 1).map(String)
  },
  yAxis: {
    type: "value"
  },
  series: [
    {
      data: currentData,
      type: "line",
      smooth: true
    }
  ]
});
</script>
