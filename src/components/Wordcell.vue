<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useOptionStore } from "../store";
const props = defineProps<{
  word: string;
  color?: "red" | "blue" | "neutral" | "black";
}>();
enum CellState {
  None,
  Red,
  Blue,
  Neutral,
  Black,
}

const optionStore = useOptionStore();

function stateNameToState(stateName: string): CellState {
  switch (stateName) {
    case "red":
      return CellState.Red;
    case "blue":
      return CellState.Blue;
    case "black":
      return CellState.Black;
    case "neutral":
      return CellState.Neutral;
  }
  throw Error("Unknown state name" + stateName);
}
const state = ref(CellState.None);
const strikedThrough = ref(false);

watch(
  () => props.color,
  (c) => {
    if (c) {
      state.value = stateNameToState(c);
    } else {
      state.value = CellState.None;
    }
  },
  { immediate: true }
);

const stateClassName = computed(() => {
  switch (state.value) {
    case CellState.None:
      return "stateNone";
    case CellState.Red:
      return "stateRed";
    case CellState.Blue:
      return "stateBlue";
    case CellState.Neutral:
      return "stateNeutral";
    case CellState.Black:
      return "stateBlack";
  }
});

function nextState(state: CellState): CellState {
  switch (state) {
    case CellState.None:
      return CellState.Red;
    case CellState.Red:
      return CellState.Blue;
    case CellState.Blue:
      return CellState.Neutral;
    case CellState.Neutral:
      return CellState.Black;
    case CellState.Black:
      return CellState.None;
  }
}

function handleClick() {
  if (optionStore.leaderMode) {
    strikedThrough.value = !strikedThrough.value;
  } else {
    state.value = nextState(state.value);
  }
}
</script>
<template>
  <div
    :class="{
      wordBoxInternal: true,
      [stateClassName]: true,
      strikedThrough: strikedThrough,
    }"
    @click="handleClick"
  >
    <span class="wordEntry noselect mainWord">
      {{ props.word }}
    </span>
    <span class="wordEntry noselect leftWord" v-if="optionStore.showVertical">
      {{ props.word }}
    </span>
    <span class="wordEntry noselect rightWord" v-if="optionStore.showVertical">
      {{ props.word }}
    </span>
    <span class="wordEntry noselect topWord">
      {{ props.word }}
    </span>
  </div>
</template>

<style scoped>
.noselect {
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome, Edge, Opera and Firefox */
}
.wordBoxInternal {
  position: relative;
}
.wordEntry {
  position: absolute;
  text-align: center;
}

.strikedThrough .wordEntry {
  text-decoration: line-through solid black 0.1em;
  border: 2px solid black;
}

.wordBoxInternal.stateRed {
  background-color: red;
}
.wordBoxInternal.stateBlue {
  background-color: blue;
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
  font-size: 150%;
  font-weight: bold;
  left: 0;
  right: 0;
  bottom: 20%;
}
</style>
