<template>
  <div class="z-10 flex h-24 w-full items-center">
    <span class="text-4xl font-bold underline decoration-primary-300 decoration-[10px] underline-offset-[-4px]">{{
      pageTitle
    }}</span>
  </div>
</template>
<script lang="ts" setup>
const props = defineProps({
  pageTitle: {
    type: String,
    required: true
  }
});
props;
</script>
