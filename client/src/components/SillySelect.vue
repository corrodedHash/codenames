<script setup lang="ts">
const props = defineProps<{
  options: string[] | { title: string; value: string }[];
}>();

const emits = defineEmits<{
  (e: "selected", option: string): undefined;
}>();
</script>
<template>
  <div class="selectionOptionBox">
    <div
      class="selectionBoxOption"
      v-for="x in props.options"
      :key="typeof x === 'string' ? x : x.value"
      @click="emits('selected', typeof x === 'string' ? x : x.value)"
    >
      {{ typeof x === "string" ? x : x.title }}
    </div>
  </div>
</template>

<style scoped>
.selectionOptionBox {
  display: flex;
  flex-direction: row;
}
.selectionBoxOption {
  border: 1px solid black;
  margin: 0.2em;
  padding: 0.2em;
  transition: font-size ease 0.5s;
}
.selectionBoxOption:hover {
  /* transform: scale(1.5); */
  font-size: 200%;
  background-color: white;
}
</style>
