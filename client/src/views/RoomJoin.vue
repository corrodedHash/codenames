<script setup lang="ts">
import { useRouter } from "vue-router";
import { GameRole, useAPIStore } from "../store";
import { computed, ref } from "vue";
const router = useRouter();
const apiStore = useAPIStore();

const chosenRole = ref("spectator" as GameRole);

const props = defineProps<{ offline: boolean; roomID: string }>();

const roomInfo = computed(() => {
  if (props.offline) {
    const room = apiStore.offlineRooms[parseInt(props.roomID)];
    if (room === undefined) throw Error("Unknown room");
    return {
      words: room.words,
      colors: room.colors,
      readAccess: room.owned,
      writeAccess: room.owned,
      roomID: props.roomID,
    };
  } else {
    throw Error("Cant handle online right now");
  }
});
function handleJoin() {
  router.push({
    name: "play",
    params: {
      offline: null,
      roomID: roomInfo.value.roomID,
      role: chosenRole.value,
    },
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
