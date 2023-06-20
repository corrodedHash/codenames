<script setup lang="ts">
import { useRouter } from "vue-router";
import { useRoomStore } from "../store";
import { ref } from "vue";
import { watch } from "vue";
import { RoomRole, getRoomRole, makeShare } from "../api";
const roomStore = useRoomStore();
const router = useRouter();

function handleJoin(sessionkey: string) {
  router.push({
    name: "joinOnline",
    params: { roomID: sessionkey },
  });
}
function handleDelete(roomID: string) {
  delete roomStore.rooms[roomID];
}
function handleShare(roomID: string, role: RoomRole) {
  makeShare(roomID, roomStore.rooms[roomID], role).then((v) => {
    alert(v);
  });
}

const shareToggle = ref(undefined as undefined | string);
const shareOptions = ref(undefined as undefined | RoomRole[]);
watch(shareToggle, (s) => {
  if (s === undefined) {
    shareOptions.value = undefined;
    return;
  }
  getRoomRole(s, roomStore.rooms[s]).then((v: RoomRole) => {
    switch (v) {
      case "admin":
        shareOptions.value = ["spectator", "revealer", "spymaster", "admin"];
        break;
      case "spymaster":
        shareOptions.value = ["spectator", "revealer", "spymaster"];
        break;
      case "revealer":
        shareOptions.value = ["spectator", "revealer"];
        break;
      case "spectator":
        shareOptions.value = ["spectator"];
        break;
    }
  });
});
</script>
<template>
  <div
    v-for="[sessionkey, usertoken] in Object.entries(roomStore.rooms)"
    :key="sessionkey"
  >
    <span @click="handleJoin(sessionkey)">
      {{ sessionkey }}
    </span>
    <span class="optionBox">
      <i-mdi-delete-outline
        class="hoverEvent"
        @click="handleDelete(sessionkey)"
      />
      <i-mdi-share-variant-outline
        class="hoverEvent"
        v-if="shareToggle !== sessionkey"
        @click="shareToggle = sessionkey"
      />
      <div v-if="shareToggle === sessionkey && shareOptions !== undefined">
        <div @click="shareToggle = undefined">X</div>
        <div
          v-for="s in shareOptions"
          :key="s"
          @click="handleShare(sessionkey, s)"
        >
          {{ s }}
        </div>
      </div>
    </span>
  </div>
</template>
<style scoped></style>
