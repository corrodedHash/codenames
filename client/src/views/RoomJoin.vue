<script setup lang="ts">
import { useRoute, useRouter } from "vue-router";
import { GameRole, useAPIStore } from "../store";
import { computed, ref } from "vue";
const route = useRoute();
const router = useRouter();
const apiStore = useAPIStore();

const chosenRole = ref("spectator" as GameRole);

const roomInfo = computed(() => {
  if (route.params["offline"] !== undefined) {
    const roomid = route.params["roomID"];
    if (Array.isArray(roomid)) throw Error("Param is array, should be string");
    const room = apiStore.offlineRooms[parseInt(roomid)];
    return {
      words: room.words,
      colors: room.colors,
      readAccess: room.owned,
      writeAccess: room.owned,
      roomID: roomid,
    };
  }
  throw Error("Cant handle online right now");
});
function handleJoin() {
  router.push({
    path: "/play",
    params: { offline: "", roomID: roomInfo.value.roomID },
  });
}
</script>

<template>
  <div>
    {{ roomInfo.words.slice(0, 3).join("") }}
    <br />
    Join as
    <select v-model="chosenRole">
      <option value="leader" v-if="roomInfo.readAccess">Spymaster</option>
      <option value="revealer" v-if="roomInfo.writeAccess">Revealer</option>
      <option value="spectator">Spectator</option>
    </select>
    <div @click="handleJoin">Join</div>
  </div>
</template>
