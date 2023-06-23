<script setup lang="ts">
import { useOptionStore } from "../store";
const optionStore = useOptionStore();
</script>
<template>
  <div>
    <div>
      <input type="checkbox" v-model="optionStore.showVertical" />
      <span> Vertical </span>
    </div>
    <div>
      <input type="checkbox" v-model="optionStore.showMirrored" />
      <span> Horizontal </span>
    </div>
  </div>
</template>
