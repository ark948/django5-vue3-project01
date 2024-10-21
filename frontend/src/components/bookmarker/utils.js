export function prepend_https(url) {
    if (!url.includes("https://")) {
      return "https://" + url;
    } else {
      return url;
    }
  }

export function append_some_domain(url) {
  if (!url.includes(".com") || !url.includes(".net") || !url.includes(".org")) {
    return url + '.com';
  } else {
    return url;
  }
}