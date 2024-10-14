export function append_http(url) {
    if (!url.includes("http://")) {
      return "http://" + url;
    } else {
      return url;
    }
  }
  