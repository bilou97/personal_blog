(function () {
  "use strict";

  function initEditors() {
    document.querySelectorAll("textarea.easymde-target").forEach(function (el) {
      if (el._easymde) return;
      el._easymde = new EasyMDE({
        element: el,
        spellChecker: false,
        autosave: { enabled: false },
        sideBySideFullscreen: false,
        minHeight: "500px",
        toolbar: [
          "bold", "italic", "strikethrough", "|",
          "heading-2", "heading-3", "|",
          "quote", "code", "unordered-list", "ordered-list", "|",
          "link", "image", "table", "horizontal-rule", "|",
          "preview", "side-by-side", "fullscreen", "|",
          "guide",
        ],
      });
    });
  }

  document.addEventListener("DOMContentLoaded", initEditors);
})();
