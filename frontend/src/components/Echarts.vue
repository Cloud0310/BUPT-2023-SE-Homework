<template>
  <div class="echart grid grid-cols-5 gap-4">
    <div class="chart col-start-1 col-end-3  w-80 h-80"><v-chart :option="option1"/></div>
    <div class="chart col-end-6 col-span-2 w-80 h-80"><v-chart :option="option2" /></div>
  </div>
</template>
<script lang="ts" setup >
import { use } from 'echarts/core';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';
import { PieChart, LineChart, } from 'echarts/charts';
import {
    TitleComponent,
    TooltipComponent,
    LegendComponent,
    GridComponent,
    VisualMapComponent,
    MarkAreaComponent
} from 'echarts/components';
import VChart, { THEME_KEY } from 'vue-echarts';
import { ref, provide} from 'vue';

use([
    GridComponent,
    CanvasRenderer,
    PieChart,
    LineChart,
    TitleComponent,
    TooltipComponent,
    TooltipComponent,
    LegendComponent,
    VisualMapComponent,
    MarkAreaComponent,
    UniversalTransition
]);

provide(THEME_KEY, 'light');

const option1 = ref({
    xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: [150, 230, 224, 218, 135, 147, 260],
      type: 'line'
    }
  ]
});

const option2 = ref({
    title: {
    text: 'Distribution of Electricity',
    subtext: 'Fake Data'
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'cross'
    }
  },
  toolbox: {
    show: true,
    feature: {
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['00:00', '01:15', '02:30', '03:45', '05:00', '06:15', '07:30', '08:45', '10:00', '11:15', '12:30', '13:45', '15:00', '16:15', '17:30', '18:45', '20:00', '21:15', '22:30', '23:45']
  },
  yAxis: {
    type: 'value',
    axisLabel: {
      formatter: '{value} W'
    },
    axisPointer: {
      snap: true
    }
  },
  visualMap: {
    show: false,
    dimension: 0,
    pieces: [
      {
        lte: 6,
        color: 'green'
      },
      {
        gt: 6,
        lte: 8,
        color: 'red'
      },
      {
        gt: 8,
        lte: 14,
        color: 'green'
      },
      {
        gt: 14,
        lte: 17,
        color: 'red'
      },
      {
        gt: 17,
        color: 'green'
      }
    ]
  },
  series: [
    {
      name: 'Electricity',
      type: 'line',
      smooth: true,
      data: [300, 280, 250, 260, 270, 300, 550, 500, 400, 390, 380, 390, 400, 500, 600, 750, 800, 700, 600, 400],
      markArea: {
        itemStyle: {
          color: 'rgba(255, 173, 177, 0.4)'
        },
        data: [
          [
            {
              name: 'Morning Peak',
              xAxis: '07:30'
            },
            {
              xAxis: '10:00'
            }
          ],
          [
            {
              name: 'Evening Peak',
              xAxis: '17:30'
            },
            {
              xAxis: '21:15'
            }
          ]
        ]
      }
    }
  ]
})
</script>