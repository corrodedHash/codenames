export function toAbsoluteURL(path: string): string {
  return `${location.protocol}//${location.host}/${
    import.meta.env.BASE_URL
  }/${path}`;
}
