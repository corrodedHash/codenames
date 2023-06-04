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
    gamemode: "spectator" as "leader" | "revealer" | "spectator",
    roomID: undefined as undefined | string,
  }),
});

export const useAPIStore = defineStore("api", {
  state: () => ({
    offlineRooms: [] as {
      words: string[];
      colors: (CardStateString | undefined)[];
      owned: boolean;
    }[],
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
