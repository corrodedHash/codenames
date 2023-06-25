export type RoomRole = "admin" | "spymaster" | "revealer" | "spectator";

export function leqRoomRoles(r: RoomRole): RoomRole[] {
  switch (r) {
    case "admin":
      return ["spectator", "revealer", "spymaster", "admin"];
    case "spymaster":
      return ["spectator", "revealer", "spymaster"];
    case "revealer":
      return ["spectator", "revealer"];
    case "spectator":
      return ["spectator"];
  }
}
