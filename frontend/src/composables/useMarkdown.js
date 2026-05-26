import { marked, Renderer } from "marked";
import hljs from "highlight.js";
import DOMPurify from "dompurify";

function slugify(text) {
  return text
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^\w\s-]/g, "")
    .trim()
    .replace(/\s+/g, "-");
}

export function parseMarkdown(content) {
  const toc = [];

  const renderer = new Renderer();

  renderer.code = function ({ text, lang }) {
    const language = lang && hljs.getLanguage(lang) ? lang : "plaintext";
    const highlighted = hljs.highlight(text, { language }).value;
    return `<pre class="hljs-pre"><code class="hljs language-${language}">${highlighted}</code></pre>`;
  };

  renderer.heading = function ({ text, depth }) {
    if (depth === 2 || depth === 3) {
      const id = slugify(text);
      toc.push({ depth, text, id });
      return `<h${depth} id="${id}">${text}</h${depth}>\n`;
    }
    return `<h${depth}>${text}</h${depth}>\n`;
  };

  const html = DOMPurify.sanitize(marked.parse(content, { renderer }));
  return { html, toc };
}
