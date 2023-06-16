function mulberry32(seed: number): () => number {
  return function () {
    let t = (seed += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

export function permutationFromSeed<T>(
  seed: number,
  elements: T[],
  count: number
): T[] {
  const drawnIndices: number[] = [];
  const result: T[] = [];
  const rng = mulberry32(seed);
  for (let i = 0; i < count; i += 1) {
    const chosenIndex = Math.floor(rng() * (elements.length - result.length));
    let adjustedIndex = chosenIndex;
    for (const di of drawnIndices) {
      if (di <= adjustedIndex) {
        adjustedIndex += 1;
      } else {
        break;
      }
    }
    result.push(elements[adjustedIndex]);
    drawnIndices.push(adjustedIndex);
    drawnIndices.sort((a, b) => a - b);
  }
  return result;
}
