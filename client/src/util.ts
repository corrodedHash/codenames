export type CardStateString = "red" | "blue" | "neutral" | "black";

export function nextState(
  state: CardStateString | undefined
): CardStateString | undefined {
  const sequence = ["red", "blue", "neutral", "black", "none"] as const;
  const currentIndex = sequence.findIndex((v) => v === (state || "none"));
  const nextIndex = (currentIndex + 1) % sequence.length;
  const nextState = sequence[nextIndex];
  if (nextState === "none") return undefined;
  else return nextState;
}
