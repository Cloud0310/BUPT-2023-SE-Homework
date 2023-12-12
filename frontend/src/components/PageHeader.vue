<template>
  <div class="fixed z-10 h-32 w-full py-3">
    <div class="ml-12 mr-auto">
      <span
        class="decoration-of text-4xl font-bold underline decoration-primary-200 decoration-4 underline-offset-[-2px]"
        >pageTitle</span
      >
    </div>
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
