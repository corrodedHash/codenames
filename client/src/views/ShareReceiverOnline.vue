<script setup lang="ts">
import { useRouter } from "vue-router";
import { watch } from "vue";
import { useRoomStore } from "../store";
import { ref } from "vue";
import { getRoomInfo, getRoomRole } from "../api";
import { RoomRole } from "../util/roomInfo";
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
  roomStore.rooms[props.roomID] = { sessiontoken: props.usertoken };
  router.push({ name: "joinOnline", params: { roomID: props.roomID } });
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
          <v-card width="80%" v-if="roomDescription === undefined">
            <v-card-text>Loading</v-card-text>
          </v-card>
          <v-card v-else>
            <v-card-title>
              {{ roomDescription }}
            </v-card-title>
            <v-card-text>
              {{ roomRole }}
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
