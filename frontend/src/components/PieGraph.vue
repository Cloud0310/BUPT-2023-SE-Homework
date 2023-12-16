<template>
  <div>
    <v-chart class="h-96" :option="option as EChartsOption" />
  </div>
</template>

<script lang="ts" setup>
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart } from "echarts/charts";
import type { EChartsOption } from "echarts";

import { TitleComponent, TooltipComponent, LegendComponent } from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { ref, provide } from "vue";

use([CanvasRenderer, PieChart, TitleComponent, TooltipComponent, LegendComponent]);

provide(THEME_KEY, "light");

const option = ref<EChartsOption>({
  title: {
    text: "月度收支情况",
    left: "center"
  },
  tooltip: {
    trigger: "item",
    formatter: "{a} <br/>{b} : {c} ({d}%)"
  },
  legend: {
    orient: "vertical",
    left: "left",
    data: ["收入", "支出"]
  },
  series: [
    {
      name: "金额",
      type: "pie",
      radius: ["40%", "70%"],
      color: ["#a78bfa", "#8b5cf6"],
      itemStyle: {
        borderRadius: 10,
        borderWidth: 1
      },
      data: [
        { value: 700, name: "收入" },
        { value: 310, name: "支出" }
      ],
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: "rgba(0, 0, 0, 0.5)"
        }
      }
    }
  ]
});
</script>
