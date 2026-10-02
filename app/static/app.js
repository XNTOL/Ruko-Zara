/* Listen, lang switch, copy. Progressive. Keep under 8 KB. */
(function () {
  "use strict";
  function $(id) {
    return document.getElementById(id);
  }
  function q(s) {
    return document.querySelector(s);
  }
  function setText(el, v) {
    if (el && v != null) el.textContent = v;
  }

  var form = q('form[action="/check"]');
  if (form) {
    form.addEventListener("submit", function () {
      var b = form.querySelector('button[type="submit"]');
      if (!b || b.disabled) return;
      b.disabled = true;
      var loading = b.getAttribute("data-loading");
      if (loading) b.textContent = loading;
    });
  }

  var i18n = null;
  var i18nNode = $("result-i18n");
  if (i18nNode) {
    try {
      i18n = JSON.parse(i18nNode.textContent || "{}");
    } catch (e) {}
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
  function hasSpeech() {
    return !!(window.speechSynthesis && window.SpeechSynthesisUtterance);
  }
  function matchingVoices() {
    return speechSynthesis.getVoices().filter(function (v) {
      return (v.lang || "").toLowerCase().indexOf(prefix) === 0;
    });
  }
  function evaluateVoices() {
    if (!btn) return;
    if (!hasSpeech()) return showFallback();
    var voices = speechSynthesis.getVoices();
    if (!voices.length) return;
    if (matchingVoices().length) showListen();
    else showFallback();
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
    if (!hasSpeech() || !text) return showFallback();
    stop();
    var u = new SpeechSynthesisUtterance(text);
    u.lang = locale;
    var m = matchingVoices();
    if (m.length) u.voice = m[0];
    else if (speechSynthesis.getVoices().length) return showFallback();
    u.onend = stop;
    u.onerror = stop;
    speaking = true;
    btn.textContent = labelStop;
    btn.setAttribute("aria-pressed", "true");
    speechSynthesis.speak(u);
  }

  if (btn) {
    btn.addEventListener("click", function () {
      if (speaking) stop();
      else start();
    });
    if (!hasSpeech()) showFallback();
    else {
      evaluateVoices();
      speechSynthesis.onvoiceschanged = evaluateVoices;
      setTimeout(evaluateVoices, 400);
    }
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
    setText(q("[data-i18n-brand]"), t.app_title);
    setText(q("[data-i18n-footer]"), t.footer);
    var about = q("[data-i18n-about-link]");
    if (about) {
      about.textContent = t.about_link;
      about.setAttribute("href", "/about?lang=" + lang);
    }
    setText(q('[data-i18n="level_title"]'), pack.level_title);
    setText(q('[data-i18n="section_reasons"]'), t.section_reasons);
    setText(q('[data-i18n="section_none"]'), pack.section_none);
    setText(q('[data-i18n="matched"]'), t.matched);
    setText(q('[data-i18n="caveat"]'), pack.caveat);
    setText(q('[data-i18n="ai_label"]'), t.ai_label);
    var ai = q('[data-ai="1"]');
    if (ai) {
      if (pack.summary) {
        ai.hidden = false;
        setText(q("[data-i18n-summary]"), pack.summary);
      } else ai.hidden = true;
    }
    (pack.reasons || []).forEach(function (r) {
      var a = q('.reason[data-rule="' + r.rule + '"]');
      if (!a) return;
      setText(a.querySelector("[data-i18n-reason-title]"), r.title);
      setText(a.querySelector("[data-i18n-reason-why]"), r.why);
    });
    var pause = pack.pause || {};
    setText(q("[data-i18n-pause-title]"), pause.title);
    (pause.steps || []).forEach(function (step, s) {
      setText(q('[data-i18n-pause-step="' + s + '"]'), step);
    });
    setText(q("[data-i18n-report-title]"), pause.report_title);
    setText(q("[data-i18n-call-hint]"), pause.report_call_hint);
    setText(q("[data-i18n-bank-hint]"), pause.report_bank_hint);
    (pause.report || []).forEach(function (item) {
      var li = q('[data-report-key="' + item.key + '"]');
      if (li) setText(li.querySelector("[data-i18n-report-text]"), item.text);
    });
    var sebi = pack.sebi || {};
    (sebi.numbers || []).forEach(function (n) {
      setText(
        q('[data-i18n-sebi-text][data-sebi-number="' + n.number + '"]'),
        n.text
      );
      setText(q("[data-i18n-sebi-btn]"), n.btn);
    });
    setText(q("[data-i18n-sebi-claim]"), sebi.claim_text);
    setText(q("[data-i18n-card-title]"), t.card_title);
    setText($("card-text"), pack.card_text);
    var cBtn = $("btn-copy");
    if (cBtn) {
      cBtn.setAttribute("data-label-copy", t.btn_copy || "");
      cBtn.setAttribute("data-label-copied", t.copied || "");
      cBtn.textContent = t.btn_copy || cBtn.textContent;
    }
    var again = q("[data-i18n-again]");
    if (again) {
      again.textContent = t.btn_again;
      again.setAttribute("href", "/?lang=" + lang);
    }
    var brand = q("[data-i18n-brand]");
    if (brand) brand.setAttribute("href", "/?lang=" + lang);
    document.querySelectorAll(".lang-opt").forEach(function (el) {
      if (el.getAttribute("data-set-lang") === lang)
        el.setAttribute("aria-current", "true");
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
      applyResultLang(el.getAttribute("data-set-lang"));
    });
  });

  var copyBtn = $("btn-copy");
  var cardEl = $("card-text");
  if (copyBtn && cardEl) {
    copyBtn.addEventListener("click", function () {
      var val = cardEl.textContent || "";
      var a = copyBtn.getAttribute("data-label-copy") || copyBtn.textContent;
      var b = copyBtn.getAttribute("data-label-copied") || "Copied";
      function done() {
        copyBtn.textContent = b;
        setTimeout(function () {
          copyBtn.textContent = a;
        }, 2000);
      }
      function fallback() {
        var range = document.createRange();
        range.selectNodeContents(cardEl);
        var sel = window.getSelection();
        if (sel) {
          sel.removeAllRanges();
          sel.addRange(range);
        }
        try {
          if (document.execCommand("copy")) done();
        } catch (err) {}
      }
      if (navigator.clipboard && navigator.clipboard.writeText)
        navigator.clipboard.writeText(val).then(done).catch(fallback);
      else fallback();
    });
  }
})();
