<script setup lang="ts">
import { onMounted } from "vue";
import { useAPIStore, useWordStore } from "../store";
import { CardStateString } from "../util";

const API = useAPIStore();
API.pollRooms();

const wordStore = useWordStore();

function handleClick(sessionkey: string) {
  console.log(sessionkey);
}

const wordsURL = new URL("/words.txt", import.meta.url).href;
const colorsURL = new URL("/colors.txt", import.meta.url).href;

let initWords: string[] = [];
let initColors: (CardStateString | undefined)[] = [];

async function init() {
  const wordFetch = fetch(wordsURL).then((x) => x.text());
  const colorFetch = fetch(colorsURL).then((x) => x.text());
  const [words, colors] = await Promise.all([wordFetch, colorFetch]);
  initWords = words.split("\n");
  initColors = colors.split("\n") as (CardStateString | undefined)[];
}
onMounted(async () => {
  await init();
  handleOffline();
});

function handleOffline() {
  wordStore.words = initWords;
  wordStore.colors = initColors;
  wordStore.revealed = [...wordStore.words.keys()].map(() => false);
}
</script>
<template>
  <div>
    <RouterLink to="/create">Create Room</RouterLink>
    <div @click="handleOffline">Offline</div>
    <div
      v-for="{ sessionkey, created } in API.rooms"
      :key="sessionkey"
      @click="handleClick(sessionkey)"
    >
      {{ created }}: {{ sessionkey }}
    </div>
  </div>
</template>
