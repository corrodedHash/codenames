<script lang="ts" setup>
import { computed, ref } from "vue";
import { RoomRole, leqRoomRoles } from "../util/roomInfo";
import { useOfflineRoomStore, useRoomStore } from "../store";
import { watch } from "vue";
import { generateOfflineShareURL, generateOnlineShareURL } from "../url";

const props = defineProps<{ roomID: number }>();

const dialog = ref(false);

const offlineRoomStore = useOfflineRoomStore();

function handleOfflineShare(mode: "complete" | "reduced") {
  const shareString = generateOfflineShareURL(
    offlineRoomStore.offlineRooms[props.roomID]
  );
  shareURL.value = shareString;
}
const shareURL = ref(undefined as undefined | string);

watch(dialog, (d) => {
  if (!d) {
    shareURL.value = undefined;
  }
});
</script>
<template>
  <v-btn color="primary">
    <i-mdi-share-variant-outline class="hoverEvent" @click="dialog = true" />
    <v-dialog v-model="dialog" activator="parent" width="auto">
      <v-card>
        <v-card-text v-if="shareURL !== undefined">
          {{ shareURL }}
        </v-card-text>
        <v-card-text v-else>
          <v-btn @click="handleOfflineShare('reduced')">Reduced</v-btn>
          <v-btn @click="handleOfflineShare('complete')">Complete</v-btn>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-btn>
</template>
