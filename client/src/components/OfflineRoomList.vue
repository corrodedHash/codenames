<script setup lang="ts">
import { useRouter } from "vue-router";
import { useOfflineRoomStore } from "../store";
import { shareOfflineRoom } from "../util/offlineRoom";
import { toAbsoluteURL } from "../url";

const router = useRouter();

const offlineRoomStore = useOfflineRoomStore();
function handleOfflineRoom(offlineRoomID: number) {
  router.push({
    name: "joinOffline",
    params: { roomID: offlineRoomID.toString() },
  });
}

function handleOfflineDelete(offlineRoomID: number) {
  delete offlineRoomStore.offlineRooms[offlineRoomID];
}

function handleOfflineShare(offlineRoomID: number) {
  const shareinfo = shareOfflineRoom(
    offlineRoomStore.offlineRooms[offlineRoomID]
  );
  const path = router.resolve({
    name: "shareReceiveOffline",
    params: { shareinfo },
  });
  alert(toAbsoluteURL(path.href));
}
</script>
<template>
  <div class="offlineRoomBox">
    <div
      v-for="[offlineRoomID, offlineRoom] in Object.entries(
        offlineRoomStore.offlineRooms
      )"
      :key="offlineRoomID"
      :class="{ offlineRoom: true, owned: offlineRoom.owned }"
    >
      <span class="nameBox" @click="handleOfflineRoom(parseInt(offlineRoomID))">
        {{ offlineRoom.words.slice(0, 3).join("").replace(" ", "") }}
      </span>
      <span class="optionBox">
        <i-mdi-delete-outline
          class="hoverEvent"
          @click="handleOfflineDelete(parseInt(offlineRoomID))"
        />
        <share-box-offline :room-i-d="parseInt(offlineRoomID)" />
      </span>
    </div>
  </div>
</template>
<style scoped>
.offlineRoom {
  display: flex;
  padding: 0.2em;
  margin: 0.1em;
  border: 0.1em solid black;
  border-style: outset;
}
.offlineRoom {
  transition: all ease 0.2s;
  background-color: rgba(0, 255, 0, 0.2);
}
.offlineRoom .nameBox {
  text-align: center;
  flex-grow: 1;
  margin-right: 1em;
  margin-left: 1em;
}
.offlineRoom .optionBox {
  margin-left: auto;
  font-size: 130%;
}

.offlineRoom .optionBox .hoverEvent:hover {
  transform: rotate(10deg);
}

.offlineRoom.owned {
  background-color: rgba(0, 0, 255, 0.2);
}
.offlineRoom .nameBox:hover {
  transform: scale(0.9);
}
</style>
