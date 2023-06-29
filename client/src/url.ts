import { makeShare } from "./api";
import router from "./router";
import { OfflineRoom, shareOfflineRoom } from "./util/offlineRoom";
import { RoomRole } from "./util/roomInfo";

export function toAbsoluteURL(path: string): string {
  return `${location.protocol}//${location.host}/${
    import.meta.env.BASE_URL
  }/${path}`;
}

export function generateOfflineShareURL(room: OfflineRoom): string {
  const shareinfo = shareOfflineRoom(room);
  const path = router.resolve({
    name: "shareReceiveOffline",
    params: { shareinfo },
  });
  return toAbsoluteURL(path.href);
}

export async function generateOnlineShareURL(
  roomID: string,
  sessiontoken: string,
  role: RoomRole
): Promise<string> {
  const usertoken = await makeShare(roomID, sessiontoken, role);

  const shareRoute = router.resolve({
    name: "shareReceiveOnline",
    params: { roomID, usertoken },
  });
  return toAbsoluteURL(shareRoute.href);
}
