<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { OfflineRoom, useAPIStore, useWordStore } from "../store";
import { useRouter } from "vue-router";
import { permutationFromSeed } from "../permutation";
import { CardStateString } from "../util";

const wordlists = Object.entries(import.meta.glob("../assets/wordlists/*.json"))
  .map(([n, p]) => {
    return { [pathToWordlistName(n)]: p };
  })
  .reduce((x, v) => ({ ...x, ...v }), {});

const wordStore = useWordStore();
const apiStore = useAPIStore();
const router = useRouter();

const offlineMode = ref(false);
const chosenWords = ref([] as string[]);
const wordSeed = ref(Math.floor(Math.random() * 100000000));
const colorSeed = ref(Math.floor(Math.random() * 1000000));
const chosenWordlist = ref(Object.keys(wordlists)[0]);

watch(
  [chosenWordlist, wordSeed],
  async ([w, ws]) => {
    if (w !== undefined) {
      const wl = ((await wordlists[w]()) as { default: string[] }).default;
      chosenWords.value = permutationFromSeed(ws, wl, 25);
    }
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

function pathToWordlistName(path: string) {
  const basename = path.replace(/.*\//, "");
  const noextension = basename.replace(".json", "");
  return noextension;
}

function buildColorsFromSeed(seed: number): CardStateString[] {
  const result: CardStateString[] = [
    ...Array(9).fill("red"),
    ...Array(8).fill("blue"),
    ...Array(7).fill("neutral"),
    "black",
  ];
  return permutationFromSeed(seed, result, result.length);
}

function startGame() {
  if (offlineMode.value) {
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
    apiStore.offlineRooms.push(x);
    const roomID = apiStore.offlineID.toString();
    apiStore.offlineID += 1;
    wordStore.words = chosenWords.value;
    wordStore.colors = colors;
    router.push({
      path: "/join",
      query: {
        offline: null,
        roomID,
      },
    });
  } else {
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
