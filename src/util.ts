export type CardStateString = "red" | "blue" | "neutral" | "black";

export enum CellState {
  None,
  Red,
  Blue,
  Neutral,
  Black,
}


export function stateNameToState(stateName: string): CellState {
  switch (stateName) {
    case "red":
      return CellState.Red;
    case "blue":
      return CellState.Blue;
    case "black":
      return CellState.Black;
    case "neutral":
      return CellState.Neutral;
  }
  throw Error("Unknown state name" + stateName);
}

export function nextState(state: CellState): CellState {
  switch (state) {
    case CellState.None:
      return CellState.Red;
    case CellState.Red:
      return CellState.Blue;
    case CellState.Blue:
      return CellState.Neutral;
    case CellState.Neutral:
      return CellState.Black;
    case CellState.Black:
      return CellState.None;
  }
}
