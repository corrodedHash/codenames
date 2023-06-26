<script setup lang="ts">
import { useRouter } from "vue-router";
import { useRoomStore } from "../store";
import { ref } from "vue";
import { watch } from "vue";
import { getRoomRole } from "../api";
import { onMounted } from "vue";
import { RoomRole, leqRoomRoles } from "../util/roomInfo";
const roomStore = useRoomStore();
const router = useRouter();

onMounted(() => {
  roomStore.refreshRooms();
});

function handleJoin(sessionkey: string) {
  router.push({
    name: "joinOnline",
    params: { roomID: sessionkey },
  });
}
function handleDelete(roomID: string) {
  delete roomStore.rooms[roomID];
}

const shareToggle = ref(undefined as undefined | string);
const shareOptions = ref(undefined as undefined | RoomRole[]);
watch(shareToggle, (s) => {
  if (s === undefined) {
    shareOptions.value = undefined;
    return;
  }
  getRoomRole(s, roomStore.rooms[s].sessiontoken).then((v: RoomRole) => {
    shareOptions.value = leqRoomRoles(v);
  });
});
</script>
<template>
  <div
    v-for="[sessionkey, room] in Object.entries(roomStore.rooms)"
    :key="sessionkey"
  >
    <span @click="handleJoin(sessionkey)">
      {{ room.shortname ?? sessionkey }}
    </span>
    <span class="optionBox">
      <i-mdi-delete-outline
        class="hoverEvent"
        @click="handleDelete(sessionkey)"
      />

      <share-box :room-i-d="sessionkey" :role="room.role || 'spectator'" />
    </span>
  </div>
</template>
<style scoped></style>
