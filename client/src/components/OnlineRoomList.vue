<script setup lang="ts">
import { useRouter } from "vue-router";
import { useRoomStore } from "../store";
const roomStore = useRoomStore();
const router = useRouter();

function handleOnlineRoom(sessionkey: string) {
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
    v-for="[sessionkey, usertoken] in Object.entries(roomStore.rooms)"
    :key="sessionkey"
    @click="handleOnlineRoom(sessionkey)"
  >
    {{ sessionkey }}
    <span class="optionBox">
      <i-mdi-delete-outline
        class="hoverEvent"
        @click.stop="handleDelete(sessionkey)"
      />
      <!-- <i-mdi-share-variant-outline
        class="hoverEvent"
        @click="handleShare(offlineRoomID)"
      /> -->
    </span>
  </div>
</template>
<style scoped></style>
