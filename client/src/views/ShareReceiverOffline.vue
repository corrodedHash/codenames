<script setup lang="ts">
import { useRouter } from "vue-router";
import { watch } from "vue";
import { OfflineRoom, offlineRoomFromJSON } from "../util/offlineRoom";
import { useOfflineRoomStore } from "../store";
import { ref } from "vue";
import { computed } from "vue";
const props = defineProps<{ shareinfo: string }>();
const offlineRoomStore = useOfflineRoomStore();
const sharedRoom = ref(undefined as undefined | OfflineRoom);
const roomDescription = computed(() => {
  if (sharedRoom.value === undefined) {
    return undefined;
  }
  return sharedRoom.value.words.slice(0, 3).join("").replace(" ", "");
});
const router = useRouter();
watch(
  () => props.shareinfo,
  async (shareinfo) => {
    sharedRoom.value = undefined;
    const room = await offlineRoomFromJSON(atob(shareinfo));
    sharedRoom.value = room;
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
  <v-app id="inspire">
    <v-main class="bg-grey-lighten-3">
      <v-container>
        <v-sheet
          min-height="70vh"
          rounded="lg"
          class="align-center d-flex flex-column justify-center"
        >
          <v-card width="80%" v-if="sharedRoom === undefined">
            <v-card-text>Loading</v-card-text>
          </v-card>
          <v-card v-else>
            <v-card-title>
              {{ roomDescription }}
            </v-card-title>
            <v-card-text>
              {{ sharedRoom.owned ? "Owned" : "Unonwned" }}
            </v-card-text>
            <v-card-actions>
              <v-btn @click="handleClick">Go</v-btn>
            </v-card-actions>
          </v-card>
        </v-sheet>
      </v-container>
    </v-main>
  </v-app>
</template>
