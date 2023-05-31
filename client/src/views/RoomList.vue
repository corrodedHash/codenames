<script setup lang="ts">
import { useAPIStore } from "../store";

const API = useAPIStore();
API.pollRooms();

function handleClick(sessionkey: string) {
  console.log(sessionkey);
}
</script>
<template>
  <div>
    <div
      v-for="{ sessionkey, created } in API.rooms"
      :key="sessionkey"
      @click="handleClick(sessionkey)"
    >
      {{ created }}: {{ sessionkey }}
    </div>
  </div>
</template>
