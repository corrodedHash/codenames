<script lang="ts" setup>
import { ref } from "vue";
import { useOfflineRoomStore } from "../store";
import { watch } from "vue";
import { generateOfflineShareURL } from "../url";

const props = defineProps<{ roomID: number }>();

const dialog = ref(false);

const offlineRoomStore = useOfflineRoomStore();

function handleOfflineShare(mode: "complete" | "reduced") {
  const shareString = generateOfflineShareURL(
    offlineRoomStore.offlineRooms[props.roomID],
    mode === "complete"
  );
  shareURL.value = shareString;
}
const shareURL = ref(undefined as undefined | string);

watch(dialog, (d) => {
  console.log("hi");
  if (!d) {
    shareURL.value = undefined;
  }
});
</script>
<template>
  <v-dialog v-model="dialog" width="auto">
    <template v-slot:activator="{ props }">
      <v-btn color="primary" :icon="true" size="small" v-bind="props">
        <i-mdi-share-variant-outline class="hoverEvent" />
      </v-btn>
    </template>

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
</template>
