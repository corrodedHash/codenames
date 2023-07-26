<script setup lang="ts">
import { ref, watch } from "vue";
import { UserSummary, getUsers, deleteUser as apiDeleteUser } from "../api";
import { useRoomStore } from "../store";
import { computed } from "vue";

const props = defineProps<{ roomID: string }>();
const roomStore = useRoomStore();
const users = ref(undefined as UserSummary[] | undefined);

const isAdmin = computed(() => roomStore.rooms[props.roomID].role === "admin");

watch(
  () => props.roomID,
  (id) => {
    getUsers(id, roomStore.rooms[id].sessiontoken).then(
      (v) => (users.value = v)
    );
  },
  { immediate: true }
);

function deleteUser(userID: string) {
  apiDeleteUser(
    props.roomID,
    userID,
    roomStore.rooms[props.roomID].sessiontoken
  ).then(() => roomStore.refreshRooms());
}
</script>
<template>
  <v-list v-if="users !== undefined" lines="two">
    <v-list-item
      v-for="u in users"
      :key="u.user_id"
      :title="u.displayname"
      :subtitle="u.role"
    >
      <template v-slot:append>
        <v-btn
          color="primary"
          icon
          size="small"
          v-bind="props"
          v-if="isAdmin"
          @click="deleteUser(u.user_id)"
        >
          <i-mdi-trash-can-outline />
        </v-btn>
      </template>
    </v-list-item>
  </v-list>
  <v-progress-circular indeterminate v-else />
</template>
