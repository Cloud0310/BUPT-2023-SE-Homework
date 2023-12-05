# Wait a minute, refactor please

1. why import the whole Echart lib?

- so huge and slow
- please use [vue-echarts](https://github.com/ecomfe/vue-echarts) lib for more human readable code, and dynamically import the echarts lib

2. why use the `onMounted` hook?

- please, do review the [vue3 lifecycle](https://v3.vuejs.org/guide/composition-api-lifecycle-hooks.html#lifecycle-hooks) and [vue3 lifecycle diagram](https://v3.vuejs.org/guide/instance.html#lifecycle-diagram)
  thick about when the `onMounted` hook will be called, and how data is passed through the component.
- if you use the `onMounted` hook, data will only be passed once, when the component is mounted, which is not what you want.

3. refactor your layout code

- if you don't know how to use the `el-row` and `el-col` layout, please read the [element-ui layout docs](https://element-plus.org/en-US/component/layout.html)
- currently, your layout is looks pretty weird, and the `el-row` and `el-col` is not used properly
- I personally recommend you just use flex or grid layout, which is much more easier to use and robust.

tip: there's vite plugins to auto import element-ui components and vue builtin functions, no need to import them manually.

<!-- <template>
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
  </script> -->
