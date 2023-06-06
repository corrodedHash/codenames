<script setup lang="ts">
import { useRoute } from "vue-router";
import { watch } from "vue";
const route = useRoute();
watch(route.query, (r) => {
  if (r["offline"] !== undefined) {
    const colorseed = r["colorseed"];
    const wordseed = r["wordseed"];
    const words = r["words"];
  } else {
    throw Error("Could not load shared non-offline room");
  }
});
</script>
<template><div></div></template>
