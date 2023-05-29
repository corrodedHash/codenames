<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useOptionStore } from "../store";
import {
  CardStateString,
  CellState,
  nextState,
  stateNameToState,
} from "../util";
const props = defineProps<{
  word: string;
  color: CardStateString;
}>();

const state = ref(CellState.None);
const strikedThrough = ref(false);

const optionStore = useOptionStore();

watch(
  () => optionStore.leaderMode,
  (m) => {
    if (m) {
      state.value = stateNameToState(props.color);
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
function handleClick() {
  if (optionStore.leaderMode) {
    strikedThrough.value = !strikedThrough.value;
  } else {
    if (optionStore.revealer) state.value = stateNameToState(props.color);
    else state.value = nextState(state.value);
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
