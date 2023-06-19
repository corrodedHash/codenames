<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useOfflineRoomStore } from "../store";
import { useRouter } from "vue-router";
import { OfflineRoom } from "../util/offlineRoom";
import {
  buildColorsFromSeed,
  generateWords,
  wordlists,
} from "../wordlistManager";

const apiStore = useOfflineRoomStore();
const router = useRouter();

const offlineMode = ref(false);
const chosenWords = ref([] as string[]);
const wordSeed = ref(Math.floor(Math.random() * 100000000));
const colorSeed = ref(Math.floor(Math.random() * 1000000));
const chosenWordlist = ref(Object.keys(wordlists)[0]);

watch(
  [chosenWordlist, wordSeed],
  async ([w, ws]) => {
    if (w === undefined) return;
    chosenWords.value = await generateWords(w, ws);
  },
  { immediate: true }
);

const canStart = computed(
  () => chosenWords.value.length >= 25 && colorSeed.value > 0
);

const formattedWords = computed({
  get() {
    return chosenWords.value.join("\n");
  },
  set(newValue) {
    chosenWords.value = newValue.split("\n");
  },
});

function startOfflineGame() {
  const colors = buildColorsFromSeed(colorSeed.value);
  const x: OfflineRoom = {
    owned: true,
    colorseed: colorSeed.value,
    words: chosenWords.value,
    colors: colors,
    revealed: colors.map(() => false),
    wordseed:
      chosenWordlist.value !== undefined
        ? {
            wordlist: chosenWordlist.value,
            wordseed: wordSeed.value,
          }
        : undefined,
  };
  const roomID = apiStore.addOfflineRoom(x).toString();
  router.push({
    name: "joinOffline",
    params: {
      roomID,
    },
  });
}

function startOnlineGame() {}

function startGame() {
  if (offlineMode.value) {
    startOfflineGame();
  } else {
    startOnlineGame();
  }
}
</script>
<template>
  <div class="contentBox">
    <select v-model="chosenWordlist">
      <option :value="undefined">Manually</option>
      <option v-for="w in Object.keys(wordlists)" :key="w" :value="w">
        {{ w }}
      </option>
    </select>
    <input
      type="text"
      v-model.number="wordSeed"
      v-if="chosenWordlist !== undefined"
    />

    <textarea
      v-model="formattedWords"
      :disabled="chosenWordlist !== undefined"
    ></textarea>
    <div><input type="checkbox" v-model="offlineMode" /> Offline</div>
    <input type="text" v-model.number="colorSeed" />
    <!-- <router-link to="/play" class="startButton">Start</router-link> -->
    <input
      type="button"
      value="Create"
      @click="startGame"
      :disabled="!canStart"
    />
  </div>
</template>
<style scoped>
.startButton {
  margin: 2em;
}
.optionsBox {
  display: grid;
  grid-template-columns: 1fr 1fr;
}
.contentBox {
  margin: 1em;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
