import { defineStore } from "pinia";

import { ref, watch } from "vue";
import { OfflineRoom } from "./util/offlineRoom";

export const useOptionStore = defineStore("options", {
  state: () => ({
    showVertical: false,
    showMirrored: true,
  }),
});

export type GameRole = "leader" | "revealer" | "spectator";

export const useRoomStore = defineStore("rooms", () => {
  const roomStorageKey = "rooms";

  const rooms: Record<string, string> = ref(
    JSON.parse(localStorage.getItem(roomStorageKey) || "{}")
  );

  watch(
    rooms,
    (v) => {
      console.log(v);
      localStorage.setItem(roomStorageKey, JSON.stringify(v));
    },
    { deep: true }
  );

  return { rooms };
});

export const useOfflineRoomStore = defineStore("offlineRoom", () => {
  const offlineRoomStorageKey = "offlineRooms";
  const offlineIDStorageKey = "offlineID";

  const storedOfflineRooms: Record<number, OfflineRoom> = JSON.parse(
    localStorage.getItem(offlineRoomStorageKey) || "{}"
  );
  const storedOfflineID: number = JSON.parse(
    localStorage.getItem(offlineIDStorageKey) || "0"
  );
  const offlineRooms = ref(storedOfflineRooms);
  const offlineID = ref(storedOfflineID);

  function addOfflineRoom(room: OfflineRoom): number {
    offlineID.value += 1;
    offlineRooms.value[offlineID.value] = room;
    return offlineID.value;
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

  return {
    offlineRooms,
    offlineID,
    addOfflineRoom,
  };
});
