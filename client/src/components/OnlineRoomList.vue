<script setup lang="ts">
import { useRouter } from "vue-router";
import { useRoomStore } from "../store";
import { onMounted } from "vue";
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
