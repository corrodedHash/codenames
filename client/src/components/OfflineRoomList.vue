<script setup lang="ts">
import { useRouter } from "vue-router";
import { useOfflineRoomStore } from "../store";

const router = useRouter();

const offlineRoomStore = useOfflineRoomStore();
function handleOfflineRoom(offlineRoomID: number) {
  router.push({
    name: "joinOffline",
    params: { roomID: offlineRoomID.toString() },
  });
}

function handleOfflineDelete(offlineRoomID: number) {
  delete offlineRoomStore.offlineRooms[offlineRoomID];
}
function shortName(words: Array<string>): string {
  return words.slice(0, 3).join("").replace(" ", "");
}
</script>
<template>
  <v-list lines="two">
    <v-list-subheader> Offline Rooms</v-list-subheader>

    <v-list-item
      v-for="[offlineRoomID, offlineRoom] in Object.entries(
        offlineRoomStore.offlineRooms
      )"
      :key="offlineRoomID"
      :title="shortName(offlineRoom.words)"
      :subtitle="offlineRoom.owned ? 'Owned' : undefined"
      @click="handleOfflineRoom(parseInt(offlineRoomID))"
    >
      <template v-slot:prepend>
        <!-- <v-avatar color="grey-lighten-1">
          <v-icon color="white">mdi-folder</v-icon>
        </v-avatar> -->
      </template>

      <template v-slot:append>
        <div class="pl-2">
          <v-btn @click="handleOfflineDelete(parseInt(offlineRoomID))">
            <i-mdi-delete-outline class="hoverEvent" />
          </v-btn>
          <share-box-offline :room-i-d="parseInt(offlineRoomID)" />
        </div>
      </template>
    </v-list-item>
  </v-list>
</template>
<style scoped></style>
