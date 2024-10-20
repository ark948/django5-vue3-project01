export function prepend_https(url) {
    if (!url.includes("https://")) {
      return "https://" + url;
    } else {
      return url;
    }
  }
  