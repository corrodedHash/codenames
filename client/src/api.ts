import { RoomRole } from "./util/roomInfo";
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
  if (!response.ok)
    throw new Error(`Response status not okay\n${await response.text()}`);
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
export async function changeRoom(
  roomID: string,
  token: string,
  words: string[],
  colors: CardStateString[]
) {
  await fetch(API_ENDPOINT + "room/" + roomID, {
    method: "PATCH",
    body: JSON.stringify({ words, colors }),
    headers: { "Content-Type": "application/json", Authorization: token },
  });
}

export async function clickCell(roomID: string, cellID: number, token: string) {
  await fetch(API_ENDPOINT + `room/${roomID}/${cellID}`, {
    method: "PUT",
    headers: { Authorization: token },
  });
}

export async function getUser(
  roomID: string,
  token: string
): Promise<UserSummary> {
  const response = await fetch(API_ENDPOINT + `user/${roomID}/me`, {
    method: "GET",
    headers: { Authorization: token },
  });
  return await response.json();
}

export interface UserSummary {
  displayname: string;
  user_id: string;
  role: RoomRole;
}

export async function getUsers(
  roomID: string,
  token: string
): Promise<UserSummary[]> {
  const response = await fetch(API_ENDPOINT + `user/${roomID}`, {
    method: "GET",
    headers: { Authorization: token },
  });
  return await response.json();
}

export async function deleteUser(
  roomID: string,
  userID: string,
  token: string
) {
  await fetch(API_ENDPOINT + `user/${roomID}/${userID}`, {
    method: "DELETE",
    headers: { Authorization: token },
  });
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

export async function subscribe(
  roomID: string,
  token: string
): Promise<WebSocket> {
  const ws_protocol = location.protocol === "http:" ? "ws" : "wss";
  // const ws_protocol = "wss";
  const ws = new WebSocket(
    ws_protocol +
      "://" +
      location.host +
      API_ENDPOINT +
      `roomSubscription/${roomID}`
  );
  const open_promise = new Promise((resolve) => {
    ws.onopen = () => resolve(ws);
  });
  await open_promise;
  ws.send(token);
  return ws;
}
