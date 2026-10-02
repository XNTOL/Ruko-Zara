/* Listen + form loading. Progressive enhancement. Keep under 8 KB. */
(function () {
  "use strict";

  function $(id) {
    return document.getElementById(id);
  }

  /* Form: show loading on submit (UIUX waiting state). */
  var form = document.querySelector('form[action="/check"]');
  if (form) {
    form.addEventListener("submit", function () {
      var btn = form.querySelector('button[type="submit"]');
      if (!btn || btn.disabled) return;
      btn.disabled = true;
      var loading = btn.getAttribute("data-loading");
      if (loading) btn.textContent = loading;
    });
  }

  var btn = $("btn-listen");
  var none = $("voice-none");
  if (!btn) return;

  var text = btn.getAttribute("data-speak") || "";
  var labelListen = btn.getAttribute("data-label-listen") || btn.textContent;
  var labelStop = btn.getAttribute("data-label-stop") || "Stop";
  var pageLang = (document.documentElement.lang || "hi").toLowerCase();
  var locale = pageLang === "en" ? "en-IN" : "hi-IN";
  var prefix = locale.slice(0, 2);
  var speaking = false;
  var utter = null;

  function showFallback() {
    btn.hidden = true;
    if (none) none.hidden = false;
  }

  function hasSpeechApi() {
    return !!(window.speechSynthesis && window.SpeechSynthesisUtterance);
  }

  function matchingVoices() {
    return speechSynthesis.getVoices().filter(function (v) {
      return (v.lang || "").toLowerCase().indexOf(prefix) === 0;
    });
  }

  function evaluateVoices() {
    if (!hasSpeechApi()) {
      showFallback();
      return;
    }
    var voices = speechSynthesis.getVoices();
    if (!voices.length) return; /* still loading */
    if (!matchingVoices().length) showFallback();
  }

  function stop() {
    speaking = false;
    if (window.speechSynthesis) speechSynthesis.cancel();
    btn.textContent = labelListen;
    btn.setAttribute("aria-pressed", "false");
  }

  function start() {
    if (!hasSpeechApi() || !text) {
      showFallback();
      return;
    }
    stop();
    utter = new SpeechSynthesisUtterance(text);
    utter.lang = locale;
    var match = matchingVoices();
    if (match.length) utter.voice = match[0];
    else if (speechSynthesis.getVoices().length) {
      /* Voices loaded but none for this language. */
      showFallback();
      return;
    }
    utter.onend = stop;
    utter.onerror = stop;
    speaking = true;
    btn.textContent = labelStop;
    btn.setAttribute("aria-pressed", "true");
    speechSynthesis.speak(utter);
  }

  btn.addEventListener("click", function () {
    if (speaking) stop();
    else start();
  });

  if (!hasSpeechApi()) {
    showFallback();
    return;
  }

  evaluateVoices();
  if (typeof speechSynthesis.onvoiceschanged !== "undefined") {
    speechSynthesis.onvoiceschanged = evaluateVoices;
  }
  /* Some browsers fill the voice list a moment later. */
  setTimeout(evaluateVoices, 400);
})();
