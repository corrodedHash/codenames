<script setup lang="ts">
import { useRouter } from "vue-router";
import { watch } from "vue";
import { OfflineRoom, offlineRoomFromJSON } from "../offlineRoom";
import { useAPIStore } from "../store";
import { ref } from "vue";
const props = defineProps<{ shareinfo: string }>();
const apiStore = useAPIStore();
const sharedRoom = ref(undefined as undefined | OfflineRoom);
const router = useRouter();
watch(
  () => props.shareinfo,
  async (r) => {
    const room = await offlineRoomFromJSON(atob(r));
    sharedRoom.value = room;
  },
  { immediate: true }
);

function handleClick() {
  if (sharedRoom.value === undefined) return;
  const roomID = apiStore.addOfflineRoom(sharedRoom.value).toString();
  router.push({
    name: "join",
    params: {
      offline: "x",
      roomID,
    },
  });
}
</script>
<template>
  <div>
    <span v-if="sharedRoom === undefined">Loading</span>
    <span v-else>
      {{ sharedRoom.words }}
      <div @click="handleClick">Go</div>
    </span>
  </div>
</template>
