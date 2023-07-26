<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useOfflineRoomStore, useRoomStore } from "../store";
import { useRouter } from "vue-router";
import { OfflineRoom } from "../util/offlineRoom";
import {
  buildColorsFromSeed,
  generateWords,
  wordlists,
} from "../wordlistManager";
import { changeRoom, createRoom } from "../api";

const offlineRoomStore = useOfflineRoomStore();
const onlineRoomStore = useRoomStore();
const router = useRouter();

const props = defineProps<{ recreate?: string }>();

const offlineMode = ref(false);
const chosenWords = ref([] as string[]);
const wordSeed = ref(Math.floor(Math.random() * 100000000));
const colorSeed = ref(Math.floor(Math.random() * 1000000));
const manualWordlistToken = "manual";
const chosenWordlist = ref(
  Object.keys(wordlists)[0] as string | typeof manualWordlistToken
);

watch(
  [chosenWordlist, wordSeed],
  async ([w, ws]) => {
    if (w === manualWordlistToken) return;
    chosenWords.value = await generateWords(w, ws);
  },
  { immediate: true }
);

const canStart = computed(
  () => chosenWords.value.length >= 25 && colorSeed.value > 0
);

const formattedWords = computed({
  get() {
    return chosenWords.value.join("\n");
  },
  set(newValue) {
    chosenWords.value = newValue.split("\n");
  },
});

function startOfflineGame() {
  const colors = buildColorsFromSeed(colorSeed.value);
  const x: OfflineRoom = {
    owned: true,
    colorseed: colorSeed.value,
    words: chosenWords.value,
    colors: colors,
    revealed: colors.map(() => false),
    wordseed:
      chosenWordlist.value !== manualWordlistToken
        ? {
            wordlist: chosenWordlist.value,
            wordseed: wordSeed.value,
          }
        : undefined,
  };
  const roomID = offlineRoomStore.addOfflineRoom(x).toString();
  router.push({
    name: "joinOffline",
    params: {
      roomID,
    },
  });
}

async function startOnlineGame() {
  const colors = buildColorsFromSeed(colorSeed.value);
  const words = chosenWords.value;

  let roomID = undefined as undefined | string;
  if (props.recreate === undefined) {
    const info = await createRoom(words, colors);
    onlineRoomStore.rooms[info.id] = { sessiontoken: info.token };
    onlineRoomStore.refreshRooms();
    roomID = info.id;
  } else {
    await changeRoom(
      props.recreate,
      onlineRoomStore.rooms[props.recreate].sessiontoken,
      words,
      colors
    );
    roomID = props.recreate;
  }
  router.push({
    name: "joinOnline",
    params: {
      roomID,
    },
  });
}

function startGame() {
  if (offlineMode.value) {
    startOfflineGame();
  } else {
    startOnlineGame();
  }
}

const wordlistOptions = [
  { value: "manual", title: "Manually" },
  ...Object.keys(wordlists)
    .map((v) => [{ state: v, title: v }])
    .reduce((a, b) => [...a, ...b], []),
];
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
          <v-card width="80%">
            <v-card-text>
              <v-select
                v-model="chosenWordlist"
                :items="wordlistOptions"
                variant="outlined"
                density="compact"
                label="Wordlist"
              />
              <v-text-field
                label="Word seed"
                v-model.number="wordSeed"
                variant="outlined"
                v-if="chosenWordlist !== manualWordlistToken"
              >
                <template v-slot:prepend>
                  <i-mdi-dice-multiple
                    @click="wordSeed = Math.floor(Math.random() * 100000000)"
                  ></i-mdi-dice-multiple> </template
              ></v-text-field>

              <textarea
                v-model="formattedWords"
                :disabled="chosenWordlist !== manualWordlistToken"
              ></textarea>
              <v-switch
                v-model="offlineMode"
                :label="offlineMode ? 'Offline' : 'Online'"
                color="secondary"
                inset
              />

              <v-text-field
                label="Color seed"
                v-model.number="colorSeed"
                variant="outlined"
              >
                <template v-slot:prepend>
                  <i-mdi-dice-multiple
                    @click="colorSeed = Math.floor(Math.random() * 1000000)"
                  ></i-mdi-dice-multiple> </template
              ></v-text-field>
            </v-card-text>
            <v-card-actions>
              <v-btn @click="startGame" :disabled="!canStart">Create</v-btn>
            </v-card-actions>
          </v-card>
        </v-sheet>
      </v-container>
    </v-main>
  </v-app>
</template>
<style scoped>
.startButton {
  margin: 2em;
}
.optionsBox {
  display: grid;
  grid-template-columns: 1fr 1fr;
}
</style>
