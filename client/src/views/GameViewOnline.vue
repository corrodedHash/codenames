<script setup lang="ts">
import GameBoard from "../components/GameBoard.vue";
import GameStatus from "../components/GameStatus.vue";
import { GameRole, useRoomStore } from "../store";
import { CardStateString } from "../util/util";
import { ref, watch } from "vue";
import { clickCell, getRoomInfo } from "../api";
import { useSocket } from "../composable/socket";
import { computed } from "vue";

const props = defineProps<{
  roomID: string;
  role: GameRole;
}>();

const roomStore = useRoomStore();
const gameinfo = ref(
  undefined as
    | undefined
    | {
        words: string[];
        colors: (CardStateString | undefined)[];
        revealed: boolean[];
      }
);

function updateOnlineRoom() {
  getRoomInfo(props.roomID, roomStore.rooms[props.roomID].sessiontoken).then(
    (v) => {
      gameinfo.value = {
        colors: v.colors,
        words: v.words,
        revealed: v.revealed,
      };
    }
  );
}

const participants = ref([] as string[]);
const statusbar = ref(undefined as undefined | typeof GameStatus);

function handleTick(event: MessageEvent) {
  const message = JSON.parse(event.data);
  switch (message["event"]) {
    case "click":
      const clicked_word =
        gameinfo.value?.words[message["cell"]] || message["cell"];
      updateOnlineRoom();
      statusbar.value?.cellRevealed(message["displayname"], clicked_word);
      break;
    case "roomchange":
      updateOnlineRoom();
      break;
    case "useronline":
      participants.value.push(message["displayname"]);
      break;
    case "useroffline":
      const participantIndex = participants.value.findIndex(
        (v) => v === message["displayname"]
      );
      if (participantIndex !== -1) {
        participants.value.splice(participantIndex, 1);
      }

      break;
    default:
      console.warn("Unknown message: ", event.data);
      break;
  }
}
const { websocket } = useSocket(
  handleTick,
  computed(() => props.roomID)
);

watch(websocket, updateOnlineRoom, { immediate: true });

function handleCellClick(index: number) {
  switch (props.role) {
    case "revealer":
      clickCell(
        props.roomID,
        index,
        roomStore.rooms[props.roomID].sessiontoken
      ).then(() => {
        updateOnlineRoom();
      });
      break;
    case "leader":
    case "spectator":
      break;
  }
}
const turn = computed(() => "red" as const);
</script>
<template>
  <div class="game-box">
    <GameStatus
      ref="statusbar"
      class="gameStatus"
      :participants="participants"
      :turn="turn"
    />

    <GameBoard
      class="gameBoard"
      v-if="gameinfo !== undefined"
      :words="gameinfo.words"
      :colors="gameinfo.colors"
      :revealed="gameinfo.revealed"
      :leader-mode="role === 'leader'"
      @cell-clicked="handleCellClick"
    />
  </div>
</template>

<style scoped>
.gameStatus {
  height: 10%;
}
.gameBoard {
  height: 90%;
}
.nobreak {
  white-space: pre;
}
.settings-modal {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 2em;
  z-index: 1;
  border: 0.2em solid black;
}
.game-box {
  display: flex;
  flex-direction: column;
  height: 100vh;
  width: 100vw;
}
</style>
