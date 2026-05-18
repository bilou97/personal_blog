import { isRef, watchEffect } from "vue";

export function useHead({ title, meta } = {}) {
  watchEffect(() => {
    const t = isRef(title) ? title.value : title;
    if (t) document.title = t;

    const metas = isRef(meta) ? meta.value : meta;
    if (!metas) return;
    metas.forEach(({ name, property, content }) => {
      const selector = name ? `meta[name="${name}"]` : `meta[property="${property}"]`;
      let el = document.querySelector(selector);
      if (!el) {
        el = document.createElement("meta");
        if (name) el.setAttribute("name", name);
        if (property) el.setAttribute("property", property);
        document.head.appendChild(el);
      }
      el.setAttribute("content", content ?? "");
    });
  });
}
