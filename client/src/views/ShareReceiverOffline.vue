<script setup lang="ts">
import { useRouter } from "vue-router";
import { watch } from "vue";
import { OfflineRoom, offlineRoomFromJSON } from "../util/offlineRoom";
import { useOfflineRoomStore } from "../store";
import { ref } from "vue";
const props = defineProps<{ shareinfo: string }>();
const offlineRoomStore = useOfflineRoomStore();
const sharedRoom = ref(undefined as undefined | OfflineRoom);
const roomDescription = ref(undefined as undefined | string);
const router = useRouter();
watch(
  () => props.shareinfo,
  async (shareinfo) => {
    sharedRoom.value = undefined;
    roomDescription.value = undefined;
    const room = await offlineRoomFromJSON(atob(shareinfo));
    sharedRoom.value = room;
    roomDescription.value = sharedRoom.value.words
      .slice(0, 3)
      .join("")
      .replace(" ", "");
  },
  { immediate: true }
);

function handleClick() {
  if (sharedRoom.value === undefined) return;
  const roomID = offlineRoomStore.addOfflineRoom(sharedRoom.value).toString();
  router.push({
    name: "joinOffline",
    params: {
      roomID,
    },
  });
}
</script>
<template>
  <div>
    <span v-if="roomDescription === undefined">Loading</span>
    <span v-else>
      {{ roomDescription }}
      <div @click="handleClick">Go</div>
    </span>
  </div>
</template>
