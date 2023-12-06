<template>
  <div class="flex flex-col gap-4">
    <!-- card infomation -->
    <div class="flex justify-between gap-4">
      <el-card
        shadow="hover"
        round
        :body-style="{
          height: '150px'
        }"
      >
        <template #header>
          <div class="card-header">
            <!-- savings icon (material symbols)  -->
            <svg xmlns="http://www.w3.org/2000/svg" height="48" viewBox="0 -960 960 960" width="48">
              <path
                fill="currentColor"
                d="M640-520q17 0 28.5-11.5T680-560q0-17-11.5-28.5T640-600q-17 0-28.5 11.5T600-560q0 17 11.5 28.5T640-520ZM320-620h200v-60H320v60ZM180-120q-34-114-67-227.5T80-580q0-92 64-156t156-64h200q29-38 70.5-59t89.5-21q25 0 42.5 17.5T720-820q0 6-1.5 12t-3.5 11q-4 11-7.5 22.5T702-751l91 91h87v279l-113 37-67 224H480v-80h-80v80H180Zm45-60h115v-80h200v80h115l63-210 102-35v-175h-52L640-728q1-25 6.5-48.5T658-824q-38 10-72 29.5T534-740H300q-66.286 0-113.143 46.857T140-580q0 103.158 29 201.579T225-180Zm255-322Z"
              />
            </svg>
            <span class="text-xl font-bold">本月净收入</span>
          </div>
        </template>
        <div class="text-4xl font-bold">{{ netIncome }}</div>
      </el-card>
      <el-card
        shadow="hover"
        :body-style="{
          height: '150px'
        }"
      >
        <template #header>
          <div class="card-header">
            <!-- bolt icon (material symbols)  -->
            <svg xmlns="http://www.w3.org/2000/svg" height="48" viewBox="0 -960 960 960" width="48">
              <path
                fill="currentColor"
                d="m393-165 279-335H492l36-286-253 366h154l-36 255Zm-73 85 40-280H160l360-520h80l-40 320h240L400-80h-80Zm153-395Z"
              />
            </svg>
            <span class="text-xl font-bold">本月电费支出</span>
          </div>
        </template>
        <div class="text-4xl font-bold">{{ expense }}</div>
      </el-card>
      <el-card
        shadow="hover"
        round
        :body-style="{
          height: '150px'
        }"
      >
        <template #header>
          <div class="card-header">
            <!-- attach money icon (material symbols)  -->
            <svg xmlns="http://www.w3.org/2000/svg" height="48" viewBox="0 -960 960 960" width="48">
              <path
                fill="currentColor"
                d="M540-420q-50 0-85-35t-35-85q0-50 35-85t85-35q50 0 85 35t35 85q0 50-35 85t-85 35ZM220-280q-24.75 0-42.375-17.625T160-340v-400q0-24.75 17.625-42.375T220-800h640q24.75 0 42.375 17.625T920-740v400q0 24.75-17.625 42.375T860-280H220Zm100-60h440q0-42 29-71t71-29v-200q-42 0-71-29t-29-71H320q0 42-29 71t-71 29v200q42 0 71 29t29 71Zm480 180H100q-24.75 0-42.375-17.625T40-220v-460h60v460h700v60ZM220-340v-400 400Z"
              />
            </svg>
            <span class="text-xl font-bold">本月毛收入</span>
          </div>
        </template>
        <div class="text-4xl font-bold">{{ income }}</div>
      </el-card>
    </div>
    <el-divider />
    <div class="flex items-center justify-center">
      <echarts />
    </div>
  </div>
</template>

<script lang="ts" setup>
// import Echarts from "../components/Echarts.vue";
const income = ref<Number>(1919810);
const expense = ref<Number>(114514);
const netIncome = ref<Number>((income.value as number) - (expense.value as number));
</script>

<style scoped>
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 10px;
  transition: color 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.el-card {
  flex: 1 0 300px;
  border-radius: 10px;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

:hover.el-card {
  transform: scale(1.01);
  background-color: #f5f3ff;
}
:hover.el-card :has(.card-header) {
  color: #475569;
}
</style>
