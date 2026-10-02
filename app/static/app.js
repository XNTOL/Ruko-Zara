/* Listen, form loading, in-place result language switch. Keep under 8 KB. */
(function () {
  "use strict";

  function $(id) {
    return document.getElementById(id);
  }

  /* Form: show loading on submit (UIUX waiting state). */
  var form = document.querySelector('form[action="/check"]');
  if (form) {
    form.addEventListener("submit", function () {
      var submitBtn = form.querySelector('button[type="submit"]');
      if (!submitBtn || submitBtn.disabled) return;
      submitBtn.disabled = true;
      var loading = submitBtn.getAttribute("data-loading");
      if (loading) submitBtn.textContent = loading;
    });
  }

  var i18nNode = $("result-i18n");
  var i18n = null;
  if (i18nNode) {
    try {
      i18n = JSON.parse(i18nNode.textContent || "{}");
    } catch (e) {
      i18n = null;
    }
  }

  var btn = $("btn-listen");
  var none = $("voice-none");
  var text = btn ? btn.getAttribute("data-speak") || "" : "";
  var labelListen = btn
    ? btn.getAttribute("data-label-listen") || btn.textContent
    : "";
  var labelStop = btn ? btn.getAttribute("data-label-stop") || "Stop" : "";
  var pageLang = (document.documentElement.lang || "hi").toLowerCase();
  var locale = pageLang === "en" ? "en-IN" : "hi-IN";
  var prefix = locale.slice(0, 2);
  var speaking = false;

  function showFallback() {
    if (!btn) return;
    btn.hidden = true;
    if (none) none.hidden = false;
  }

  function showListen() {
    if (!btn) return;
    btn.hidden = false;
    if (none) none.hidden = true;
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
    if (!btn) return;
    if (!hasSpeechApi()) {
      showFallback();
      return;
    }
    var voices = speechSynthesis.getVoices();
    if (!voices.length) return;
    if (!matchingVoices().length) showFallback();
    else showListen();
  }

  function stop() {
    speaking = false;
    if (window.speechSynthesis) speechSynthesis.cancel();
    if (btn) {
      btn.textContent = labelListen;
      btn.setAttribute("aria-pressed", "false");
    }
  }

  function start() {
    if (!btn) return;
    if (!hasSpeechApi() || !text) {
      showFallback();
      return;
    }
    stop();
    var utter = new SpeechSynthesisUtterance(text);
    utter.lang = locale;
    var match = matchingVoices();
    if (match.length) utter.voice = match[0];
    else if (speechSynthesis.getVoices().length) {
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

  if (btn) {
    btn.addEventListener("click", function () {
      if (speaking) stop();
      else start();
    });
    if (!hasSpeechApi()) showFallback();
    else {
      evaluateVoices();
      if (typeof speechSynthesis.onvoiceschanged !== "undefined") {
        speechSynthesis.onvoiceschanged = evaluateVoices;
      }
      setTimeout(evaluateVoices, 400);
    }
  }

  function setText(el, value) {
    if (el && value != null) el.textContent = value;
  }

  function applyResultLang(lang) {
    if (!i18n || !i18n[lang]) return;
    var pack = i18n[lang];
    var t = pack.t || {};
    pageLang = lang;
    locale = lang === "en" ? "en-IN" : "hi-IN";
    prefix = locale.slice(0, 2);
    document.documentElement.lang = lang;
    document.title = pack.level_title || document.title;

    setText(document.querySelector("[data-i18n-brand]"), t.app_title);
    setText(document.querySelector("[data-i18n-footer]"), t.footer);
    var about = document.querySelector("[data-i18n-about-link]");
    if (about) {
      about.textContent = t.about_link;
      about.setAttribute("href", "/about?lang=" + lang);
    }
    setText(document.querySelector('[data-i18n="level_title"]'), pack.level_title);
    setText(
      document.querySelector('[data-i18n="section_reasons"]'),
      t.section_reasons
    );
    setText(document.querySelector('[data-i18n="section_none"]'), pack.section_none);
    setText(document.querySelector('[data-i18n="matched"]'), t.matched);
    setText(document.querySelector('[data-i18n="caveat"]'), pack.caveat);
    setText(document.querySelector('[data-i18n="ai_label"]'), t.ai_label);
    var aiBlock = document.querySelector('[data-ai="1"]');
    if (aiBlock) {
      if (pack.summary) {
        aiBlock.hidden = false;
        setText(document.querySelector("[data-i18n-summary]"), pack.summary);
      } else {
        aiBlock.hidden = true;
      }
    }

    var reasons = pack.reasons || [];
    for (var i = 0; i < reasons.length; i++) {
      var article = document.querySelector(
        '.reason[data-rule="' + reasons[i].rule + '"]'
      );
      if (!article) continue;
      setText(article.querySelector("[data-i18n-reason-title]"), reasons[i].title);
      setText(article.querySelector("[data-i18n-reason-why]"), reasons[i].why);
    }

    var pause = pack.pause || {};
    setText(document.querySelector("[data-i18n-pause-title]"), pause.title);
    var steps = pause.steps || [];
    for (var s = 0; s < steps.length; s++) {
      setText(
        document.querySelector('[data-i18n-pause-step="' + s + '"]'),
        steps[s]
      );
    }
    setText(document.querySelector("[data-i18n-report-title]"), pause.report_title);
    var reports = pause.report || [];
    for (var r = 0; r < reports.length; r++) {
      var li = document.querySelector(
        '[data-report-key="' + reports[r].key + '"]'
      );
      if (!li) continue;
      setText(li.querySelector("[data-i18n-report-text]"), reports[r].text);
    }

    var sebi = pack.sebi || {};
    var sebiNums = sebi.numbers || [];
    for (var n = 0; n < sebiNums.length; n++) {
      var p = document.querySelector(
        '[data-i18n-sebi-text][data-sebi-number="' + sebiNums[n].number + '"]'
      );
      setText(p, sebiNums[n].text);
      setText(document.querySelector("[data-i18n-sebi-btn]"), sebiNums[n].btn);
    }
    setText(document.querySelector("[data-i18n-sebi-claim]"), sebi.claim_text);

    var again = document.querySelector("[data-i18n-again]");
    if (again) {
      again.textContent = t.btn_again;
      again.setAttribute("href", "/?lang=" + lang);
    }

    var brand = document.querySelector("[data-i18n-brand]");
    if (brand) brand.setAttribute("href", "/?lang=" + lang);

    document.querySelectorAll(".lang-opt").forEach(function (el) {
      var on = el.getAttribute("data-set-lang") === lang;
      if (on) el.setAttribute("aria-current", "true");
      else el.removeAttribute("aria-current");
    });

    if (btn) {
      stop();
      text = pack.speak_text || "";
      labelListen = t.btn_listen || labelListen;
      labelStop = t.btn_stop || labelStop;
      btn.setAttribute("data-speak", text);
      btn.setAttribute("data-label-listen", labelListen);
      btn.setAttribute("data-label-stop", labelStop);
      btn.textContent = labelListen;
      if (none) none.textContent = t.voice_none || none.textContent;
      evaluateVoices();
    }
  }

  document.querySelectorAll(".lang-opt[data-set-lang]").forEach(function (el) {
    el.addEventListener("click", function (ev) {
      ev.preventDefault();
      var lang = el.getAttribute("data-set-lang");
      if (lang) applyResultLang(lang);
    });
  });
})();
