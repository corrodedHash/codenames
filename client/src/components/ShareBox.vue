<script lang="ts" setup>
import { computed, ref } from "vue";
import { RoomRole, leqRoomRoles } from "../util/roomInfo";
import { useRoomStore } from "../store";
import { watch } from "vue";
import { generateOnlineShareURL } from "../url";

import * as qrcode from "qrcode";
import CopyTextBox from "./CopyTextBox.vue";

const props = defineProps<{ role: RoomRole; roomID: string }>();

const dialog = ref(false);

const roomStore = useRoomStore();
const shareURL = ref(undefined as undefined | string);
async function handleShare(role: RoomRole) {
  shareURL.value = await generateOnlineShareURL(
    props.roomID,
    roomStore.rooms[props.roomID].sessiontoken,
    role
  );
}

watch(dialog, (d) => {
  if (!d) {
    shareURL.value = undefined;
  }
});

const allowedRoles = computed(() => leqRoomRoles(props.role));

const qrcodecanvas = ref(undefined as undefined | HTMLCanvasElement);

const canShare = computed(() => {
  return !!navigator.share;
});

function maybeShare() {
  if (canShare.value) {
    navigator.share({
      title: "Invitation to Codenames room",
      url: shareURL.value,
    });
  } else {
    console.warn("Device cannot share");
  }
}

watch(
  [shareURL, qrcodecanvas],
  ([url, canvas]) => {
    console.log("heya");
    if (url === undefined) return;
    console.log("heyaya");
    if (canvas === undefined) return;
    qrcode.toCanvas(canvas, url, {});
  },
  { immediate: true }
);
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
        <canvas ref="qrcodecanvas" @click="maybeShare"></canvas>
        <copy-text-box :text="shareURL" />
      </v-card-text>
      <v-card-text v-else>
        <v-list lines="one" v-if="shareURL === undefined">
          <v-list-item
            v-for="item in allowedRoles"
            :key="item"
            :title="item"
            @click="handleShare(item)"
          ></v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
