import { defineStore } from "pinia";

import { ref, watch } from "vue";
import { OfflineRoom } from "./util/offlineRoom";
import { RoomRole, getRoomInfo } from "./api";
import { notUndefined } from "./util/util";

export const useOptionStore = defineStore("options", {
  state: () => ({
    showVertical: false,
    showMirrored: true,
  }),
});

export type GameRole = "leader" | "revealer" | "spectator";

export interface RoomSummary {
  sessiontoken: string;
  shortname?: string;
  role?: RoomRole;
}

export const useRoomStore = defineStore("rooms", () => {
  const roomStorageKey = "rooms";

  const rooms = ref(
    JSON.parse(localStorage.getItem(roomStorageKey) || "{}") as Record<
      string,
      RoomSummary
    >
  );

  watch(
    rooms,
    (v) => {
      localStorage.setItem(roomStorageKey, JSON.stringify(v));
    },
    { deep: true }
  );

  async function refreshRooms() {
    const refreshPromises = Object.entries(rooms.value).map(
      ([roomID, summary]) =>
        getRoomInfo(roomID, summary.sessiontoken)
          .then(
            (v) =>
              [
                roomID,
                {
                  sessiontoken: summary.sessiontoken,
                  shortname: v.words.slice(0, 3).join("").replace(" ", ""),
                },
              ] as const
          )
          .catch(() => undefined)
    );
    const refreshedRooms = await Promise.all(refreshPromises);
    const refreshedRoomObject = refreshedRooms
      .filter(notUndefined)
      .map(([key, value]) => ({ [key]: value }))
      .reduce((p, v) => ({ ...p, ...v }), {});
    rooms.value = refreshedRoomObject;
  }

  return { rooms, refreshRooms };
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
