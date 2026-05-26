export function readingTime(content) {
  const text = content.replace(/[#*`[\]()>_~\-]/g, " ").replace(/\s+/g, " ").trim();
  const words = text.split(" ").filter(Boolean).length;
  return Math.max(1, Math.ceil(words / 200));
}
