import { defineStore } from "pinia";

import { CardStateString } from "./util";
import { ref, watch } from "vue";
import { OfflineRoom } from "./offlineRoom";

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

export const useAPIStore = defineStore("api", () => {
  const offlineRoomStorageKey = "offlineRooms";
  const offlineIDStorageKey = "offlineID";

  const storedOfflineRooms: OfflineRoom[] = JSON.parse(
    localStorage.getItem(offlineRoomStorageKey) || "[]"
  );
  const storedOfflineID: number = JSON.parse(
    localStorage.getItem(offlineIDStorageKey) || "0"
  );
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
