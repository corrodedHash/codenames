import { CardStateString } from "./util";

export interface WordlistSeed {
  wordlist: string;
  wordseed: number;
}

export interface OfflineRoom {
  words: string[];
  colors: (CardStateString | undefined)[];
  revealed: boolean[];
  wordseed?: WordlistSeed;
  colorseed?: number;
  owned: boolean;
  id: number;
}

interface SharedOfflineRoomManual {
  words: string[];
  wordseed?: never;
}
interface SharedOfflineRoomSeeded {
  words?: never;
  wordseed: WordlistSeed;
}

type SharedOfflineRoomWords = SharedOfflineRoomManual | SharedOfflineRoomSeeded;

type SharedOfflineRoom = SharedOfflineRoomWords & {
  colors?: CardStateString[];
  colorseed?: number;
};

function isSharedOfflineRoom(o: object): o is SharedOfflineRoom {
  const hasWords = "words" in o;
  const hasWordseed = "wordseed" in o;
  if (hasWords === hasWordseed) return false;

  return true;
}

export function offlineRoomFromJSON(json: string): OfflineRoom {
  const parsed = JSON.parse(json);
  if (typeof parsed !== "object") throw Error("Not an object");
  if (!isSharedOfflineRoom(parsed)) throw Error("Not an offline room");

  if (parsed.wordseed !== undefined) {
  } else {
    parsed.wordseed;
  }
}
