<script setup lang="ts">
import { useOptionStore } from "../store";
const optionStore = useOptionStore();
</script>
<template>
  <div>
    <v-switch
      inset
      color="secondary"
      hide-details
      v-model="optionStore.showVertical"
      label="Vertical"
    />
    <v-switch
      inset
      color="secondary"
      hide-details
      v-model="optionStore.showMirrored"
      label="Horizontal"
    />
  </div>
</template>
