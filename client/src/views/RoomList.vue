<script setup lang="ts">
import { useRouter } from "vue-router";
import { useAPIStore } from "../store";
import { shareOfflineRoom } from "../offlineRoom";

const API = useAPIStore();
API.pollRooms();
const router = useRouter();

function handleClick(sessionkey: string) {
  console.log(sessionkey);
}
function handleOfflineRoom(offlineRoomID: number) {
  router.push({
    name: "join",
    params: { offline: "x", roomID: offlineRoomID.toString() },
  });
}

function handleOfflineDelete(offlineRoomID: number) {
  delete API.offlineRooms[offlineRoomID];
}

function handleOfflineShare(offlineRoomID: number) {
  alert(shareOfflineRoom(API.offlineRooms[offlineRoomID]));
}
</script>
<template>
  <div class="listBox">
    <RouterLink to="/create">
      <i-mdi-plus-box style="font-size: 200%" />
    </RouterLink>
    <div class="offlineRoomBox">
      <div
        v-for="[offlineRoomID, offlineRoom] in Object.entries(API.offlineRooms)"
        :key="offlineRoomID"
        :class="{ offlineRoom: true, owned: offlineRoom.owned }"
      >
        <span
          class="nameBox"
          @click="handleOfflineRoom(parseInt(offlineRoomID))"
        >
          {{ offlineRoom.words.slice(0, 3).join("").replace(" ", "") }}
        </span>
        <span class="optionBox">
          <i-mdi-delete-outline
            class="hoverEvent"
            @click="handleOfflineDelete(parseInt(offlineRoomID))"
          />
          <i-mdi-share-variant-outline
            class="hoverEvent"
            @click="handleOfflineShare(parseInt(offlineRoomID))"
          />
        </span>
      </div>
    </div>
    <div
      v-for="{ sessionkey, created } in API.rooms"
      :key="sessionkey"
      @click="handleClick(sessionkey)"
    >
      {{ created }}: {{ sessionkey }}
    </div>
  </div>
</template>
<style scoped>
.listBox {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

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
