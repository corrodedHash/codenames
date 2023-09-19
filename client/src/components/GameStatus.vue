<template>
  <div>
    <!-- <span>Turn: {{ turn }}</span> -->
    <div>{{ event }}</div>
  </div>
</template>
<script lang="ts" setup>
import { ref } from "vue";

const props = defineProps<{
  turn: "red" | "blue";
  participants: string[];
}>();

const event = ref("");

const cellRevealed = (actor: string, cellWord: string) => {
  event.value = `${actor} clicked "${cellWord}"`;
};

defineExpose({ cellRevealed });
</script>
