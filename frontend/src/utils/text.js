export function cleanDisplayText(value, fallback = "") {
  if (value == null) {
    return fallback;
  }

  const parser = new DOMParser();
  let decoded = parser.parseFromString(String(value), "text/html").documentElement.textContent ?? "";

  decoded = decoded
    .replace(/(\w)[\uFFFD]s\b/g, "$1's")
    .replace(/(\w)[\uFFFD]t\b/g, "$1't")
    .replace(/(\w)[\uFFFD]re\b/g, "$1're")
    .replace(/(\w)[\uFFFD]ve\b/g, "$1've")
    .replace(/(\w)[\uFFFD]ll\b/g, "$1'll")
    .replace(/(\w)[\uFFFD]d\b/g, "$1'd")
    .replace(/(\w)[\uFFFD]m\b/g, "$1'm")
    .replace(/[\uFFFD](.*?)[\uFFFD]/g, '"$1"')
    .replace(/(\w)[\uFFFD](\w)/g, "$1'$2")
    .replace(/[\uFFFD]/g, "");

  return decoded.replace(/\s+/g, " ").replace(/\bContinue reading\.{0,3}\s*$/i, "").trim() || fallback;
}

