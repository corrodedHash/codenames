import { CardStateString } from "./util";
import { buildColorsFromSeed, generateWords } from "../wordlistManager";

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

function isSharedOfflineRoom(o: unknown): o is SharedOfflineRoom {
  if (typeof o !== "object") return false;
  if (o === null) return false;
  const hasWords = "words" in o;
  const hasWordseed = "wordseed" in o;
  if (hasWords === hasWordseed) return false;

  return true;
}

function createSharedOfflineRoom(
  room: OfflineRoom,
  complete: boolean
): SharedOfflineRoom {
  const colorseed = room.colorseed;
  const colors =
    room.colorseed === undefined
      ? room.colors.every((v): v is CardStateString => v !== undefined)
        ? room.colors
        : undefined
      : undefined;
  const colorinfo = complete ? { colorseed, colors } : {};
  const words =
    room.wordseed === undefined
      ? { words: room.words }
      : { wordseed: room.wordseed };
  return { ...colorinfo, ...words };
}

export function shareOfflineRoom(room: OfflineRoom, complete: boolean): string {
  const r = createSharedOfflineRoom(room, complete);
  return btoa(JSON.stringify(r, undefined, 0));
}

export async function offlineRoomFromJSON(json: string): Promise<OfflineRoom> {
  const parsed = JSON.parse(json);
  if (!isSharedOfflineRoom(parsed)) throw Error("Not an offline room");
  let words = [];
  if (parsed.wordseed !== undefined) {
    words = await generateWords(
      parsed.wordseed.wordlist,
      parsed.wordseed.wordseed
    );
  } else {
    words = parsed.words;
  }
  const colors =
    parsed.colors !== undefined
      ? parsed.colors
      : parsed.colorseed !== undefined
      ? buildColorsFromSeed(parsed.colorseed)
      : words.map(() => undefined);
  const revealed = words.map(() => false);
  const owned = parsed.colors !== undefined || parsed.colorseed !== undefined;
  return {
    colors,
    colorseed: parsed.colorseed,
    wordseed: parsed.wordseed,
    revealed,
    words,
    owned,
  };
}
