<script lang="ts" setup>
import { computed, ref } from "vue";
import { RoomRole, leqRoomRoles } from "../util/roomInfo";
import { useRoomStore } from "../store";
import { watch } from "vue";
import { generateOnlineShareURL } from "../url";

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
