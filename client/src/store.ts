import { defineStore } from "pinia";

import { CardStateString } from "./util";
import { ref, watch } from "vue";

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

export const useAPIStore = defineStore("api", () => {
  const offlineRoomStorageKey = "offlineRooms";
  const offlineIDStorageKey = "offlineID";

  const storedOfflineRoomsJSON = localStorage.getItem(offlineRoomStorageKey);
  let storedOfflineRooms: OfflineRoom[];
  if (storedOfflineRoomsJSON !== null) {
    storedOfflineRooms = JSON.parse(storedOfflineRoomsJSON);
  } else {
    storedOfflineRooms = [];
  }
  const storedOfflineIDJSON = localStorage.getItem(offlineIDStorageKey);
  let storedOfflineID: number;
  if (storedOfflineIDJSON !== null) {
    storedOfflineID = JSON.parse(storedOfflineIDJSON);
  } else {
    storedOfflineID = 0;
  }
  const offlineRooms = ref(storedOfflineRooms);
  const offlineID = ref(storedOfflineID);
  const rooms = ref([] as { sessionkey: string; created: number }[]);
  const adminkeys = ref({} as Record<string, string>);

  async function pollRooms() {
    const fetchedRooms = await fetch(APIRoot + "list").then((x) => x.json());
    rooms.value = fetchedRooms;
  }
  watch(offlineID, (v) => {
    localStorage.setItem(offlineIDStorageKey, JSON.stringify(v));
  });

  watch(
    offlineRooms,
    (r) => {
      localStorage.setItem(offlineRoomStorageKey, JSON.stringify(r));
    },
    { deep: true }
  );

  return { offlineRooms, offlineID, rooms, adminkeys, pollRooms };
});
