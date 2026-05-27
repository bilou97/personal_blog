import { Marked } from "marked";
import DOMPurify from "dompurify";
import hljs from "highlight.js";

function slugify(text) {
  return text
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^\w\s-]/g, "")
    .trim()
    .replace(/\s+/g, "-");
}

function parseTocFromMarkdown(content) {
  const toc = [];
  for (const line of content.split("\n")) {
    const match = line.match(/^(#{2,3})\s+(.+)/);
    if (match) {
      const depth = match[1].length;
      const text = match[2].trim()
        .replace(/\*\*(.+?)\*\*/g, "$1")
        .replace(/`(.+?)`/g, "$1");
      toc.push({ depth, text, id: slugify(text) });
    }
  }
  return toc;
}

function addHeadingIds(html) {
  return html.replace(/<h([23])>([\s\S]*?)<\/h\1>/g, (_, depth, content) => {
    const text = content.replace(/<[^>]+>/g, "").trim();
    return `<h${depth} id="${slugify(text)}">${content}</h${depth}>`;
  });
}

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

const marked = new Marked({
  renderer: {
    code(text, lang) {
      if (typeof text !== "string") return "<pre><code></code></pre>";
      let highlighted;
      try {
        if (lang && hljs.getLanguage(lang)) {
          highlighted = hljs.highlight(text, { language: lang, ignoreIllegals: true }).value;
        } else {
          highlighted = escapeHtml(text);
        }
      } catch {
        highlighted = escapeHtml(text);
      }
      const langClass = lang ? ` language-${lang}` : "";
      return `<pre class="hljs-pre not-prose"><code class="hljs${langClass}">${highlighted}</code></pre>`;
    },
  },
});

export function parseMarkdown(content) {
  const toc = parseTocFromMarkdown(content);

  const rawHtml = marked.parse(content);
  const htmlWithIds = addHeadingIds(rawHtml);
  const html = DOMPurify.sanitize(htmlWithIds);
  return { html, toc };
}
