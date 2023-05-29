import { defineStore } from "pinia";

import { CardStateString } from "./util";

const wordsURL = new URL("/words.txt", import.meta.url).href;
const colorsURL = new URL("/colors.txt", import.meta.url).href;

export const useWordStore = defineStore("words", {
  state: () => ({
    words: [] as string[],
    colors: [] as CardStateString[],
  }),

  actions: {
    async init() {
      const wordFetch = fetch(wordsURL).then((x) => x.text());
      const colorFetch = fetch(colorsURL).then((x) => x.text());
      const [words, colors] = await Promise.all([wordFetch, colorFetch]);
      this.setWords(words);
      this.setColors(colors);
    },
    setWords(wordList: string) {
      this.words = wordList.split("\n");
    },
    setColors(colorList: string) {
      this.colors = colorList.split("\n") as CardStateString[];
    },
  },
});

export const useOptionStore = defineStore("options", {
  state: () => ({
    showVertical: false,
    showMirrored: true,
    leaderMode: false,
    revealer: false,
  }),
});

console.log(import.meta.env.BASE_URL);
