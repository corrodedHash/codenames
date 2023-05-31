<script setup lang="ts">
import { computed } from "vue";
import { useOptionStore } from "../store";
import { CardStateString } from "../util";
const props = defineProps<{
  word: string;
  color?: CardStateString;
  strikedThrough?: boolean;
}>();

const emit = defineEmits<{
  (e: "click"): void;
}>();

const optionStore = useOptionStore();

const stateClassName = computed(() => {
  const cssMap = {
    none: "stateNone",
    red: "stateRed",
    blue: "stateBlue",
    neutral: "stateNeutral",
    black: "stateBlack",
  } as const;
  return cssMap[props.color || "none"];
});
</script>
<template>
  <div
    :class="{
      wordBoxInternal: true,
      [stateClassName]: true,
      strikedThrough: strikedThrough || false,
    }"
    @click="emit('click')"
    tabindex="0"
  >
    <span class="wordEntry noselect topWord" v-if="optionStore.showMirrored">
      {{ props.word }}
    </span>
    <span class="wordEntry noselect leftWord" v-if="optionStore.showVertical">
      {{ props.word }}
    </span>
    <span class="wordEntry noselect rightWord" v-if="optionStore.showVertical">
      {{ props.word }}
    </span>
    <span
      :class="{
        wordEntry: true,
        noselect: true,
        mainWord: true,
        singleMode: !optionStore.showMirrored && !optionStore.showVertical,
      }"
    >
      {{ props.word }}
    </span>
  </div>
</template>

<style scoped>
.wordBoxInternal {
  position: relative;
}
.wordEntry {
  position: absolute;
  text-align: center;

  font-size: 3vw;
}

.strikedThrough .wordEntry {
  text-decoration: line-through solid black 0.1em;
  border: 2px solid black;
}

.wordBoxInternal.stateRed {
  background-color: hsl(0, 100%, 70%);
}
.wordBoxInternal.stateBlue {
  background-color: hsl(240, 100%, 70%);
}
.wordBoxInternal.stateNeutral {
  background-color: rgb(190, 190, 159);
}
.wordBoxInternal.stateNone {
  background-color: transparent;
}
.wordBoxInternal.stateBlack {
  background-color: black;
  color: white;
}
.leftWord {
  transform: rotate(90deg);
  left: 10%;
  top: 40%;
}
.rightWord {
  transform: rotate(-90deg);
  right: 10%;
  top: 40%;
}
.topWord {
  transform: rotate(180deg);
  left: 0;
  right: 0;
  top: 10%;
}
.mainWord {
  font-size: 3vw;
  font-weight: bold;
  left: 0;
  right: 0;
  bottom: 10%;
}
.mainWord.singleMode {
  bottom: 30%;
}
</style>
