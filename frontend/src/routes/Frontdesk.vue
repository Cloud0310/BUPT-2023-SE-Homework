<template>
  <div class="bg-primary-100 h-full ">
    <div class="flex flex-col gap-3 ">
        <div class="flex justify-center">欢迎登录波普特酒店温控管理系统！</div>
        <div class="flex justify-center">
            <button 
                type="button"
                class="rounded-lg bg-primary-300 px-5 py-2 text-sm text-neutral-50 transition-all hover:bg-primary-400 hover:text-neutral-100"
                @click="dialogPrintbill=true"
                >
                打印账单
            </button>
        </div>
        <div class="flex justify-center">
            <button 
                type="button"
                class="rounded-lg bg-primary-300 px-5 py-2 text-sm text-neutral-50 transition-all hover:bg-primary-400 hover:text-neutral-100"
                @click="dialogPrintdetail=true"
                >
                打印详单
            </button>
        </div>
    </div>
    <el-dialog v-model="dialogPrintbill" title="账单" center>
        <el-table :data="billData" class="flex justify-center">
            <el-table-column property="roomID" label="房间号" width="85" />
            <el-table-column property="timeIN" label="入住时间" width="150" />
            <el-table-column property="timeOUT" label="退房时间" width="150" />
            <el-table-column property="cost" label="费用" width="75" />
            <el-table-column property="note" label="备注" width="100"/>
        </el-table>
    </el-dialog>

    <el-dialog v-model="dialogPrintdetail" title="详单" center>
        <el-table :data="detailData" class="flex justify-center">
            <el-table-column property="roomID" label="房间号" width="85" />
            <el-table-column property="timeIN" label="入住时间" width="100" />
            <el-table-column property="timeOUT" label="退房时间" width="100" />
            <el-table-column property="temperature" label="温度" width="75" />
            <el-table-column property="mode" label="模式" width="75" />
            <el-table-column property="windSpeed" label="风速" width="75" />
            <el-table-column property="cost" label="费用" width="75" />
            <el-table-column property="note" label="备注" width="100"/>
        </el-table>
    </el-dialog>
  </div>

</template>


<script lang="ts" setup>
const dialogPrintbill = ref<boolean>(false);
const dialogPrintdetail = ref<boolean>(false);
const billData =[
    {
        roomID: '1-114',
        timeIN: '2023-12-14',
        timeOUT: '2023-12-16',
        cost: 500.00,
        note: '',
    },
    {
        roomID: '1-113',
        timeIN: '2023-12-14',
        timeOUT: '2023-12-16',
        cost: 500.00,
        note: '',
    },
    {
        roomID: '1-112',
        timeIN: '2023-12-14',
        timeOUT: '2023-12-16',
        cost: 500.00,
        note: '',
    },
];
const detailData = [
    {
        roomID: '1-114',
        timeIN: '2023-12-14',
        timeOUT: '2023-12-16',
        temperature: 28,
        mode: '制冷',
        windSpeed: 3,
        cost: 500.00,
        note: '',
    },
    {
        roomID: '1-113',
        timeIN: '2023-12-14',
        timeOUT: '2023-12-16',
        temperature: 28,
        mode: '制冷',
        windSpeed: 3,
        cost: 500.00,
        note: '',
    },
    {
        roomID: '1-112',
        timeIN: '2023-12-14',
        timeOUT: '2023-12-16',
        temperature: 28,
        mode: '制冷',
        windSpeed: 3,
        cost: 500.00,
        note: '',
    },
]
</script>
