<script setup lang="ts">
import { useRouter } from "vue-router";
import { OfflineRoom, useAPIStore } from "../store";

const API = useAPIStore();
API.pollRooms();
const router = useRouter();

function handleClick(sessionkey: string) {
  console.log(sessionkey);
}
function handleOfflineRoom(offlineRoom: OfflineRoom) {
  router.push({
    name: "join",
    params: { offline: "x", roomID: offlineRoom.id },
  });
}
</script>
<template>
  <div>
    <RouterLink to="/create">Create Room</RouterLink>
    <div
      v-for="(offlineRoom, index) in API.offlineRooms"
      :key="index"
      @click="handleOfflineRoom(offlineRoom)"
    >
      Offline Room: {{ offlineRoom.owned }}
      {{ offlineRoom.words.slice(0, 3).join("") }}
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
