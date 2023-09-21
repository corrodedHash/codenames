import { Ref, onMounted, onUnmounted, watch } from "vue";
import { useRoomStore } from "../store";
import { subscribe } from "../api";

export function useSocket(
  eventHandler: (e: MessageEvent) => void,
  roomID: Ref<string>
) {
  let w = undefined as undefined | WebSocket;
  const roomStore = useRoomStore();

  let lastToken = Symbol("myToken");
  const newSocket = async () => {
    const myToken = Symbol("myToken");
    lastToken = myToken;
    console.log(w);
    w?.close();
    const newSocket = await subscribe(
      roomID.value,
      roomStore.rooms[roomID.value].sessiontoken
    );
    if (myToken !== lastToken) return;
    newSocket.addEventListener("message", eventHandler);
    console.log(w, newSocket);
    w = newSocket;
    console.log(w);
  };

  onMounted(() => {
    newSocket();
  });
  watch(roomID, () => {
    newSocket();
  });
  onUnmounted(() => {
    console.log("unmounting", w);

    w?.close();
  });
}
