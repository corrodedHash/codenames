import { permutationFromSeed } from "./permutation";
import { CardStateString } from "./util";

function pathToWordlistName(path: string) {
  const basename = path.replace(/.*\//, "");
  const noextension = basename.replace(".json", "");
  return noextension;
}

export const wordlists = Object.entries(
  import.meta.glob("../assets/wordlists/*.json")
)
  .map(([n, p]) => {
    return { [pathToWordlistName(n)]: p };
  })
  .reduce((x, v) => ({ ...x, ...v }), {});

export async function generateWords(
  wordlist: string,
  seed: number
): Promise<string[]> {
  const wl = ((await wordlists[wordlist]()) as { default: string[] }).default;
  return permutationFromSeed(seed, wl, 25);
}

export function buildColorsFromSeed(seed: number): CardStateString[] {
  const result: CardStateString[] = [
    ...Array(9).fill("red"),
    ...Array(8).fill("blue"),
    ...Array(7).fill("neutral"),
    "black",
  ];
  return permutationFromSeed(seed, result, result.length);
}
