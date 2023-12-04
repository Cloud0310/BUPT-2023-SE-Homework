<template>
    <el-row>
      <el-col :span="8">
        <div ref="info1" class="w-80 h-80"></div>
      </el-col>
      <el-col :span="8" :offset="8">
        <div ref="info2" class="w-80 h-80"></div>
      </el-col>
    </el-row>
  </template>
  
  <script lang="ts" setup>
  import { onMounted, ref } from "vue";
  import * as echarts from 'echarts';
  
  const info1 = ref<HTMLElement | null>(null);
  const info2 = ref<HTMLElement | null>(null);
  
  onMounted(() => {
    const infoEl1 = info1.value;
    const infoEl2 = info2.value;
  
    if (infoEl1 && infoEl2) {
      const userEc1 = echarts.init(infoEl1, "light");
      const userEc2 = echarts.init(infoEl2, "light");
  
      const option1 = {
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
      };
  
      const option2 = {
        xAxis: {
          type: 'category',
          data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [100, 200, 300, 400, 500, 600, 700],
            type: 'bar'
          }
        ]
      };
  
      userEc1.setOption(option1);
      userEc2.setOption(option2);
    }
  });
  </script>