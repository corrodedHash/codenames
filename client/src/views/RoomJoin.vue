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
function handleJoin(role: GameRole) {
  router.push({
    name: "play",
    params: {
      offline: null,
      roomID: roomInfo.value.roomID,
      role,
    },
  });
}
</script>

<template>
  <div class="box">
    <span class="titleBox">{{ roomInfo.words.slice(0, 3).join("") }}</span>
    <div class="selectionBox">
      <div class="selectionBoxTitle">Join as</div>
      <div class="selectionOptionBox">
        <div
          class="selectionBoxOption"
          @click="handleJoin('leader')"
          v-if="roomInfo.readAccess"
        >
          Spymaster
        </div>
        <div
          class="selectionBoxOption"
          @click="handleJoin('revealer')"
          v-if="roomInfo.writeAccess"
        >
          Revealer
        </div>
        <div class="selectionBoxOption" @click="handleJoin('spectator')">
          Spectator
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.selectionOptionBox {
  display: flex;
  flex-direction: row;
}
.selectionBoxOption {
  border: 1px solid black;
  margin: 0.2em;
  padding: 0.2em;
  transition: font-size ease 0.5s;
}
.selectionBoxOption:hover {
  /* transform: scale(1.5); */
  font-size: 200%;
  background-color: white;
}
.selectionBoxTitle {
  text-align: center;
  font-weight: bold;
}
.titleBox {
  border-bottom: 0.1em double black;
  padding-left: 1em;
  padding-right: 1em;
  font-size: 200%;
  margin-bottom: 0.3em;
}
.box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
