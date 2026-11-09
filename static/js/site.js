// Small progressive enhancements. Every page works without this file.
(function () {
  "use strict";
  var lang = document.documentElement.lang || "en";

  // Mobile menu
  var toggle = document.querySelector("[data-menu]");
  if (toggle) {
    var links = document.getElementById(toggle.getAttribute("aria-controls"));
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    links.addEventListener("click", function (e) {
      if (e.target.closest("a")) { links.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); }
    });
  }

  // Show/hide panels, e.g. the "Ask a question" notice on the homepage
  document.querySelectorAll("[data-toggle]").forEach(function (btn) {
    var target = document.getElementById(btn.getAttribute("data-toggle"));
    if (!target) return;
    btn.addEventListener("click", function () {
      target.hidden = !target.hidden;
      btn.setAttribute("aria-expanded", target.hidden ? "false" : "true");
    });
  });

  // Course "Book" buttons preselect the level in the booking form
  document.querySelectorAll("[data-level]").forEach(function (a) {
    a.addEventListener("click", function () {
      var select = document.querySelector("#contact select[name=level]");
      if (select) select.value = a.getAttribute("data-level");
    });
  });

  // Show / hide password
  document.querySelectorAll("[data-show-pass]").forEach(function (btn) {
    var input = btn.parentElement.querySelector("input");
    btn.addEventListener("click", function () {
      var show = input.type === "password";
      input.type = show ? "text" : "password";
      btn.textContent = show ? btn.dataset.hide : btn.dataset.show;
      btn.setAttribute("aria-pressed", show ? "true" : "false");
    });
  });

  // Sign-up: child fields appear when "My child" is chosen
  var signup = document.querySelector("[data-signup]");
  if (signup) {
    var update = function () {
      var child = signup.querySelector("input[name=learner]:checked").value === "child";
      signup.querySelector("[data-child-fields]").hidden = !child;
      signup.querySelector("[data-name-self]").hidden = child;
      signup.querySelector("[data-name-child]").hidden = !child;
    };
    signup.querySelectorAll("input[name=learner]").forEach(function (r) { r.addEventListener("change", update); });
  }

  // Lesson times in the student's own time zone
  document.querySelectorAll("time[data-local]").forEach(function (t) {
    var d = new Date(t.getAttribute("datetime"));
    if (isNaN(d)) return;
    var opts = { weekday: "short", day: "numeric", month: "short", hour: "numeric", minute: "2-digit" };
    try { t.textContent = new Intl.DateTimeFormat(lang === "ar" ? "ar-SY" : undefined, opts).format(d); } catch (e) {}
  });

  // Confirm before destructive actions
  document.querySelectorAll("form[data-confirm]").forEach(function (f) {
    f.addEventListener("submit", function (e) { if (!window.confirm(f.dataset.confirm)) e.preventDefault(); });
  });

  // Copy invite link
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy");
      var done = function () { var old = btn.textContent; btn.textContent = "Copied"; setTimeout(function () { btn.textContent = old; }, 1500); };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () { window.prompt("Copy this link:", text); });
      else window.prompt("Copy this link:", text);
    });
  });

  // Quick-insert Arabic words in the answer box
  document.querySelectorAll("[data-insert]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var box = document.getElementById(btn.dataset.target);
      if (!box) return;
      var start = box.selectionStart || box.value.length;
      box.value = box.value.slice(0, start) + " " + btn.dataset.insert + " " + box.value.slice(box.selectionEnd || start);
      box.focus();
    });
  });
})();
