<script setup lang="ts">
import { useRouter } from "vue-router";
import { useRoomStore } from "../store";
import { onMounted } from "vue";
const roomStore = useRoomStore();
const router = useRouter();

onMounted(() => {
  roomStore.refreshRooms();
});

function handleJoin(sessionkey: string) {
  router.push({
    name: "joinOnline",
    params: { roomID: sessionkey },
  });
}
function handleDelete(roomID: string) {
  delete roomStore.rooms[roomID];
}
</script>
<template>
  <v-list lines="two">
    <v-list-subheader> Online Rooms</v-list-subheader>
    <v-list-item
      v-for="[sessionkey, room] in Object.entries(roomStore.rooms)"
      :key="sessionkey"
      :title="room.shortname"
      :subtitle="room.role"
      @click="handleJoin(sessionkey)"
    >
      <template v-slot:prepend>
        <!-- <v-avatar color="grey-lighten-1">
          <v-icon color="white">mdi-folder</v-icon>
        </v-avatar> -->
      </template>

      <template v-slot:append>
        <div class="pl-2">
          <v-btn @click="handleDelete(sessionkey)">
            <i-mdi-delete-outline class="hoverEvent" />
          </v-btn>
          <share-box :room-i-d="sessionkey" :role="room.role || 'spectator'" />
        </div>
      </template>
    </v-list-item>
  </v-list>
</template>
<style scoped></style>
