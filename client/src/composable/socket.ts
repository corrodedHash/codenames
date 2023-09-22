import { Ref, onMounted, onUnmounted, ref, watch } from "vue";
import { useRoomStore } from "../store";
import { subscribe } from "../api";

export function useSocket(
  eventHandler: (e: MessageEvent) => void,
  roomID: Ref<string>
) {
  const websocket = ref(undefined as undefined | WebSocket);
  const roomStore = useRoomStore();

  let lastToken = Symbol("myToken");
  const newSocket = async () => {
    const myToken = Symbol("myToken");
    lastToken = myToken;
    console.log(websocket.value);
    websocket.value?.close();
    const newSocket = await subscribe(
      roomID.value,
      roomStore.rooms[roomID.value].sessiontoken
    );
    if (myToken !== lastToken) return;
    newSocket.addEventListener("message", eventHandler);
    console.log(websocket, newSocket);
    websocket.value = newSocket;
    console.log(websocket);
  };

  onMounted(() => {
    newSocket();
  });
  watch(roomID, () => {
    newSocket();
  });
  onUnmounted(() => {
    console.log("unmounting", websocket);

    websocket.value?.close();
  });
  return { websocket };
}
