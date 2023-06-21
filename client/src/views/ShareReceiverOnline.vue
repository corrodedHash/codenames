<script setup lang="ts">
import { useRouter } from "vue-router";
import { watch } from "vue";
import { useRoomStore } from "../store";
import { ref } from "vue";
import { RoomRole, getRoomInfo, getRoomRole } from "../api";
const props = defineProps<{ roomID: string; usertoken: string }>();
const roomStore = useRoomStore();

const roomDescription = ref(undefined as undefined | string);
const roomRole = ref(undefined as undefined | RoomRole);
const router = useRouter();
watch(
  () => [props.roomID, props.usertoken] as const,
  async ([roomID, usertoken]) => {
    roomDescription.value = undefined;
    roomRole.value = undefined;

    const room = await getRoomInfo(roomID, usertoken);
    roomDescription.value = room.words.slice(0, 3).join("").replace(" ", "");
    roomRole.value = await getRoomRole(roomID, usertoken);
  },
  { immediate: true }
);

function handleClick() {
  if (roomDescription.value === undefined) return;
  roomStore.rooms[props.roomID] = props.usertoken;
  router.push({ name: "joinOnline", params: { roomID: props.roomID } });
}
</script>
<template>
  <div>
    <span v-if="roomDescription === undefined">Loading</span>
    <span v-else>
      {{ roomDescription }}
      {{ roomRole }}
      <div @click="handleClick">Go</div>
    </span>
  </div>
</template>
