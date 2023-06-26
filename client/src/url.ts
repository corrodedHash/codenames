import { makeShare } from "./api";
import router from "./router";
import { RoomRole } from "./util/roomInfo";

export function toAbsoluteURL(path: string): string {
  return `${location.protocol}//${location.host}/${
    import.meta.env.BASE_URL
  }/${path}`;
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
