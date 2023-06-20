import { CardStateString } from "./util/util";

const API_ENDPOINT = "/api/";

export async function getRoomInfo(
  roomID: string,
  token: string
): Promise<{
  words: string[];
  colors: (CardStateString | undefined)[];
  revealed: boolean[];
}> {
  const response = await fetch(API_ENDPOINT + `room/${roomID}`, {
    headers: { Authorization: token },
  });
  return await response.json();
}

export async function createRoom(
  words: string[],
  colors: CardStateString[]
): Promise<{ id: string; token: string }> {
  const response = await fetch(API_ENDPOINT + "room", {
    method: "POST",
    body: JSON.stringify({ words, colors }),
    headers: { "Content-Type": "application/json" },
  });
  return await response.json();
}

export async function clickCell(roomID: string, cellID: number, token: string) {
  await fetch(API_ENDPOINT + `room/${roomID}/${cellID}`, {
    method: "PUT",
    headers: { Authorization: token },
  });
}

interface RoomUpdateResponse {
  clickState: number;
  roomState: number;
}
export async function heartBeat(
  roomID: string,
  token: string
): Promise<RoomUpdateResponse> {
  const response = await fetch(API_ENDPOINT + `roomUpdates/${roomID}`, {
    method: "GET",
    headers: { Authorization: token },
  });
  return await response.json();
}

export type RoomRole = "admin" | "spymaster" | "revealer" | "spectator";

export async function getRoomRole(
  roomID: string,
  token: string
): Promise<RoomRole> {
  const response = await fetch(API_ENDPOINT + `role/${roomID}`, {
    method: "GET",
    headers: { Authorization: token },
  });
  return await response.json();
}

export async function makeShare(
  roomID: string,
  token: string,
  role: RoomRole
): Promise<string> {
  const response = await fetch(API_ENDPOINT + `roomShare/${roomID}/${role}`, {
    method: "POST",
    headers: { Authorization: token },
  });
  return await response.json();
}
