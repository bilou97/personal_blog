(function () {
  "use strict";

  function initEditors() {
    var targets = document.querySelectorAll("textarea.toastuieditor-target");
    if (!targets.length) return;

    if (typeof toastui === "undefined" || typeof toastui.Editor === "undefined") {
      console.error("[BlogAdmin] toastui.Editor not available");
      return;
    }

    targets.forEach(function (el) {
      if (el._toastuieditor) return;

      try {
        // Force full width on all ancestor elements up to #content-main
        var parent = el.parentElement;
        while (parent && parent.id !== "content-main") {
          parent.style.width = "100%";
          parent.style.maxWidth = "none";
          parent.style.float = "none";
          parent.style.boxSizing = "border-box";
          parent = parent.parentElement;
        }

        var wrapper = document.createElement("div");
        wrapper.style.marginTop = "8px";
        wrapper.style.width = "100%";
        el.parentNode.insertBefore(wrapper, el);
        el.style.display = "none";

        var editor = new toastui.Editor({
          el: wrapper,
          height: "600px",
          initialEditType: "markdown",
          previewStyle: "vertical",
          initialValue: el.value || "",
          usageStatistics: false,
        });

        el._toastuieditor = editor;

        var form = el.closest("form");
        if (form) {
          form.addEventListener("submit", function () {
            el.value = editor.getMarkdown();
          });
        }
      } catch (err) {
        console.error("[BlogAdmin] Failed to initialize editor:", err);
        el.style.display = "";
        el.style.height = "400px";
      }
    });
  }

  document.addEventListener("DOMContentLoaded", initEditors);
})();
