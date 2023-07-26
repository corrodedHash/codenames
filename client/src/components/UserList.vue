<script setup lang="ts">
import { ref, watch } from "vue";
import { UserSummary, getUsers } from "../api";
import { useRoomStore } from "../store";

const props = defineProps<{ roomID: string }>();
const roomStore = useRoomStore();
const users = ref(undefined as UserSummary[] | undefined);

watch(
  () => props.roomID,
  (id) => {
    getUsers(id, roomStore.rooms[id].sessiontoken).then(
      (v) => (users.value = v)
    );
  },
  { immediate: true }
);
</script>
<template>
  <v-list v-if="users !== undefined">
    <v-list-item
      v-for="u in users"
      :key="u.identifier"
      :title="u.displayname"
      :subtitle="u.role"
    />
  </v-list>
  <v-progress-circular indeterminate v-else />
</template>
