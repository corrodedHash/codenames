import {
  OfflineRoom,
  shareOfflineRoom,
  offlineRoomFromJSON,
} from "./offlineRoom";

import { test, expect } from "vitest";

test("Offline room serialization", async () => {
  const a: OfflineRoom = {
    words: [...new Array(25)].map((_, i) => i.toString()),
    colors: [...new Array(25)],
    owned: false,
    revealed: Array(25).fill(false),
  };

  const sharedRoom = shareOfflineRoom(a);
  console.dir(sharedRoom);
  const rebuiltRoom = await offlineRoomFromJSON(JSON.stringify(sharedRoom));

  expect(rebuiltRoom.words).toStrictEqual(a.words);
  expect(rebuiltRoom.colors).toStrictEqual(a.colors);
});
