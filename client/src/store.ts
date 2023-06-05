import { defineStore } from "pinia";

import { CardStateString } from "./util";

const APIRoot = "/api/";

export const useWordStore = defineStore("words", {
  state: () => ({
    words: [] as string[],
    colors: [] as (CardStateString | undefined)[],
    revealed: [] as boolean[],
  }),
});

export const useOptionStore = defineStore("options", {
  state: () => ({
    showVertical: false,
    showMirrored: true,
  }),
});

export const useRoomStore = defineStore("room", {
  state: () => ({
    gamemode: "spectator" as GameRole,
    roomID: undefined as undefined | string,
  }),
});

export type GameRole = "leader" | "revealer" | "spectator";

export interface WordlistSeed {
  wordlist: string;
  wordseed: number;
}

export interface OfflineRoom {
  words: string[];
  colors: (CardStateString | undefined)[];
  revealed: boolean[];
  wordseed?: WordlistSeed;
  colorseed?: number;
  owned: boolean;
}

export const useAPIStore = defineStore("api", {
  state: () => ({
    offlineRooms: [] as OfflineRoom[],
    rooms: [] as { sessionkey: string; created: number }[],
    adminkeys: {} as Record<string, string>,
  }),
  actions: {
    async pollRooms() {
      const rooms = await fetch(APIRoot + "list").then((x) => x.json());
      this.rooms = rooms;
    },
  },
});
