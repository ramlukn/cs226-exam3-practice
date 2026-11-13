// Exam page: editor behaviour, timer, autosave, attempts, submit, rubrics, grading export.
(function () {
  const S = window.PracticeStore;
  const spec = JSON.parse(document.getElementById("exam-spec").textContent);
  const EXAM = spec.id;
  const LIMIT = spec.minutes * 60;
  const $ = id => document.getElementById(id);

  const fields = Array.from(document.querySelectorAll(".field"));
  const examFields = fields.filter(f => f.classList.contains("ex"));
  const codes = fields.filter(f => f.classList.contains("code"));
  const scoreInputs = Array.from(document.querySelectorAll(".sc"));
  const examIds = spec.questions.filter(q => q.exam).map(q => q.id);
  const defaults = {};
  fields.forEach(f => { defaults[f.id] = f.defaultValue; });

  const storageOk = S.available();
  let data = null;          // the whole stored record for this exam
  let att = null;           // the attempt being shown
  let paused = false;
  let dirty = false;        // edits not yet written
  let saveTimer = null;
  let lastWrite = 0;

  // ---------- status and toast ----------
  function setStatus(text, cls) { $("status").textContent = text; $("status").className = "status" + (cls ? " " + cls : ""); }
  let toastTimer = null;
  function toast(text) {
    const t = $("toast"); t.textContent = text; t.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(() => { t.hidden = true; }, 3200);
  }
  function clock(ms) { return new Date(ms).toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit", second: "2-digit" }); }

  // ---------- reading and writing ----------
  function collectInto(a) {
    fields.forEach(f => {
      if (f.value === defaults[f.id]) delete a.answers[f.id];   // untouched stubs aren't stored
      else a.answers[f.id] = f.value;
    });
    a.scores = {};
    scoreInputs.forEach(s => { if (s.value !== "") a.scores[s.dataset.for] = clampScore(s); });
  }

  function clampScore(s) {
    const v = Number(s.value);
    if (isNaN(v)) return 0;
    return Math.min(Number(s.max), Math.max(0, v));
  }

  function persist(quiet) {
    if (!att) return;
    collectInto(att);
    att.updatedAt = Date.now();
    if (!storageOk) { dirty = false; setStatus("Not saved: storage is blocked", "err"); return; }
    try {
      S.write(EXAM, data);
      dirty = false; lastWrite = att.updatedAt;
      if (!quiet) setStatus("Saved " + clock(att.updatedAt), "ok");
    } catch (e) {
      setStatus("Couldn't save. Download a backup now.", "err");
      showBanner("storageBanner", "This browser refused to save (storage may be full or blocked). Download a backup so you don't lose your answers.");
    }
  }

  function scheduleSave() {
    dirty = true;
    setStatus("Saving…");
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => persist(false), 400);
  }

  function saveNow() { clearTimeout(saveTimer); if (dirty) persist(false); }

  // ---------- showing an attempt ----------
  function showAttempt(a) {
    att = a;
    fields.forEach(f => { f.value = (typeof a.answers[f.id] === "string") ? a.answers[f.id] : defaults[f.id]; });
    scoreInputs.forEach(s => { const v = a.scores && a.scores[s.dataset.for]; s.value = (typeof v === "number") ? v : ""; });
    paused = false; $("pauseBtn").textContent = "Pause";
    refreshAll(); renderTimer(); renderSubmit(); renderAttempts();
  }

  function renderAttempts() {
    const sel = $("attemptSelect");
    sel.innerHTML = "";
    data.attempts.forEach((a, i) => {
      const o = document.createElement("option");
      const sc = S.scoreOf(a, examIds);
      let label = "Attempt " + (i + 1) + " · " + S.fmtDate(a.createdAt);
      label += a.submitted ? (sc.scored ? " · " + sc.total + " / " + spec.total : " · submitted") : " · in progress";
      o.value = a.id; o.textContent = label;
      if (a.id === att.id) o.selected = true;
      sel.appendChild(o);
    });
    $("deleteAttemptBtn").textContent = data.attempts.length > 1 ? "Delete this attempt" : "Clear this attempt";
    $("attemptInfo").textContent = "Time used " + S.fmtDuration(att.elapsed) + (att.submitted ? " · submitted " + S.fmtDate(new Date(att.submittedAt).getTime()) : "");
  }

  // ---------- editor helpers ----------
  function refreshCode(ta) {
    const n = ta.value.split("\n").length;
    let s = ""; for (let i = 1; i <= n; i++) s += i + (i < n ? "\n" : "");
    ta.parentElement.querySelector(".ln").textContent = s;
    ta.style.height = (n * 20 + 16) + "px";
  }
  function refreshAns(ta) { ta.style.height = "auto"; ta.style.height = Math.max(64, ta.scrollHeight + 2) + "px"; }
  function refreshTodos() {
    let n = 0;
    codes.filter(c => c.classList.contains("ex")).forEach(c => { n += (c.value.match(/\/\/ TODO/g) || []).length; });
    $("todoCount").textContent = n;
  }
  function refreshTally() {
    let t = 0, n = 0;
    scoreInputs.forEach(s => { if (s.value !== "") { t += clampScore(s); n++; } });
    $("tally").textContent = String(Math.round(t * 1000) / 1000);
    $("tallyNote").textContent = n < scoreInputs.length ? "(" + n + " of " + scoreInputs.length + " questions scored)" : "";
  }
  function refreshAll() { codes.forEach(refreshCode); fields.filter(f => f.classList.contains("ans")).forEach(refreshAns); refreshTodos(); refreshTally(); }

  fields.forEach(f => f.addEventListener("input", () => {
    if (f.classList.contains("code")) refreshCode(f); else refreshAns(f);
    refreshTodos(); scheduleSave();
  }));
  fields.forEach(f => f.addEventListener("blur", saveNow));
  scoreInputs.forEach(s => s.addEventListener("input", () => { refreshTally(); scheduleSave(); }));

  codes.forEach(ta => ta.addEventListener("keydown", e => {
    if (e.key === "Tab" && !e.shiftKey) {
      e.preventDefault();
      ta.setRangeText("  ", ta.selectionStart, ta.selectionEnd, "end");
      ta.dispatchEvent(new Event("input"));
    } else if (e.key === "Enter") {
      e.preventDefault();
      const s = ta.selectionStart;
      const line = ta.value.slice(0, s).split("\n").pop();
      let ind = line.match(/^\s*/)[0];
      if (/\{\s*$/.test(line)) ind += "  ";
      ta.setRangeText("\n" + ind, s, ta.selectionEnd, "end");
      ta.dispatchEvent(new Event("input"));
    }
  }));

  // A button that needs a second click within 3 s to act.
  function twoClick(btn, armedText, action) {
    let armed = false, t = null, label = null;
    btn.addEventListener("click", () => {
      if (!armed) {
        armed = true; label = btn.textContent; btn.textContent = armedText;
        t = setTimeout(() => { armed = false; btn.textContent = label; }, 3000);
        return;
      }
      clearTimeout(t); armed = false; btn.textContent = label;
      action();
    });
  }

  document.querySelectorAll(".resetBtn").forEach(b => twoClick(b, "Click again to reset", () => {
    const ta = $(b.dataset.for); ta.value = defaults[ta.id]; ta.dispatchEvent(new Event("input"));
  }));

  // ---------- timer ----------
  function fmt(t) { const a = Math.abs(t); return (t < 0 ? "-" : "") + Math.floor(a / 60) + ":" + String(a % 60).padStart(2, "0"); }
  function renderTimer() {
    const left = LIMIT - (att ? att.elapsed : 0);
    $("timer").textContent = fmt(left);
    $("timer").className = "timer" + (left < 0 ? " over" : left <= 600 ? " warn" : "");
  }
  let ticks = 0;
  setInterval(() => {
    if (!att || paused || att.submitted || document.visibilityState !== "visible") return;
    att.elapsed++; renderTimer();
    if (++ticks % 10 === 0 && !dirty) persist(true);   // keep the clock saved without flashing the status
  }, 1000);
  $("pauseBtn").addEventListener("click", () => {
    paused = !paused;
    $("pauseBtn").textContent = paused ? "Resume" : "Pause";
    persist(false);
  });

  // ---------- submit ----------
  function renderSubmit() {
    const sub = !!att.submitted;
    $("submitBox").classList.toggle("done", sub);
    $("doneRow").hidden = !sub;
    document.querySelectorAll(".rub.exam").forEach(d => { d.hidden = !sub; });
    document.querySelectorAll(".lock").forEach(p => { p.hidden = sub; });
    document.querySelectorAll(".score").forEach(l => { l.hidden = !sub; });
    $("submitNote").textContent = sub
      ? "Submitted. Rubrics are open under each question. You can still edit; changes keep saving."
      : "When you're done, submit. Your answers stay saved and editable afterward.";
    $("submitRow").hidden = sub;
    $("confirmRow").hidden = true;
  }
  $("submitBtn").addEventListener("click", () => {
    let blank = 0;
    examFields.forEach(f => { if (!f.value.trim() || f.value === defaults[f.id]) blank++; });
    $("confirmText").textContent = blank ? "Submit now? " + blank + " of " + examFields.length + " answers are still blank or unchanged." : "Submit now?";
    $("submitRow").hidden = true; $("confirmRow").hidden = false;
  });
  $("cancelBtn").addEventListener("click", () => { $("confirmRow").hidden = true; $("submitRow").hidden = false; });
  $("confirmBtn").addEventListener("click", () => {
    att.submitted = true; att.submittedAt = new Date().toISOString();
    persist(false); renderSubmit(); renderAttempts();
    $("submitBox").scrollIntoView({ block: "nearest" });
  });

  // ---------- attempts ----------
  $("attemptSelect").addEventListener("change", e => {
    saveNow();
    const a = data.attempts.find(x => x.id === e.target.value);
    if (!a) return;
    data.currentId = a.id; persist(true); showAttempt(a);
    toast("Showing " + e.target.selectedOptions[0].textContent.split(" · ")[0]);
  });
  twoClick($("newAttemptBtn"), "Click again: start blank", () => {
    saveNow();
    const a = S.blankAttempt();
    data.attempts.push(a); data.currentId = a.id;
    showAttempt(a); persist(false);
    window.scrollTo({ top: 0 });
    toast("New attempt started. Earlier attempts are kept in the menu.");
  });
  twoClick($("deleteAttemptBtn"), "Click again to confirm", () => {
    if (data.attempts.length > 1) {
      data.attempts = data.attempts.filter(a => a.id !== att.id);
      const next = data.attempts[data.attempts.length - 1];
      data.currentId = next.id; showAttempt(next); persist(false);
      toast("Attempt deleted.");
    } else {
      const a = S.blankAttempt();
      data.attempts = [a]; data.currentId = a.id; showAttempt(a); persist(false);
      toast("Attempt cleared.");
    }
  });

  // ---------- backups ----------
  $("exportBtn").addEventListener("click", () => {
    saveNow();
    S.download("cs226-" + EXAM + "-backup-" + S.today() + ".json", JSON.stringify(S.makeBackup([EXAM]), null, 2));
    toast("Backup downloaded.");
  });
  $("importInput").addEventListener("change", e => {
    const file = e.target.files[0]; e.target.value = "";
    if (!file) return;
    saveNow();
    file.text().then(text => {
      try {
        const res = S.importBackup(text);
        const mine = res[EXAM];
        load();
        const others = Object.keys(res).filter(k => k !== EXAM).length;
        toast(mine ? "Imported: " + mine.added + " new, " + mine.updated + " updated attempts" + (others ? " (plus " + others + " other exam" + (others > 1 ? "s" : "") + ")" : "") + "."
                   : "Imported attempts for other exams; none for this one.");
      } catch (err) { toast(err.message); }
    });
  });

  // ---------- grading export ----------
  function answerFor(q) {
    const v = att.answers[q.id];
    if (typeof v !== "string" || !v.trim()) return null;
    return v;
  }
  function gradingText(forAI) {
    collectInto(att);
    const qs = spec.questions.filter(q => q.exam || answerFor(q) !== null);
    let out = "";
    if (forAI) {
      out += "You are grading a CS226 (Data Structures in Java) practice exam: " + spec.title + ", " + spec.total + " points, " + spec.minutes + " minutes.\n\n";
      out += "Grade it the way the course's graders do:\n";
      out += "- For each question, start at 0 and add every rubric item the answer earns. Give part of an item only when the item has separate parts, and say which part.\n";
      out += "- Then subtract the penalties that apply. A question never goes below 0 or above its points.\n";
      out += "- Syntax is graded lightly: at most -0.125 per question for major syntax errors that show a lack of understanding. Never withhold a rubric item only because of syntax.\n";
      out += "- Judge the logic as written. If the answer would crash, loop forever or return the wrong thing, say on what input.\n\n";
      out += "For each question give: the score out of its points; each rubric item marked earned, partly earned or missed, with its points; the penalties applied; and a one-line fix. ";
      out += "Finish with a table of scores, the total out of " + spec.total + ", and the 3 habits that cost the most points.\n";
      out += "Questions marked [extra drill] are not part of the total: grade them separately.\n\n";
    } else {
      out += "# " + spec.title + " — answers for grading\n\n";
    }
    out += "Time used: " + S.fmtDuration(att.elapsed) + (att.submitted ? "" : " (not submitted yet)") + "\n\n";
    qs.forEach(q => {
      const ans = answerFor(q);
      out += "---\n\n## " + q.id + (q.exam ? "" : " [extra drill]") + " (" + q.pts + " pts)\n\n";
      out += "### Question\n\n" + q.prompt + "\n\n";
      if (q.stub) out += "Starter code:\n\n```java\n" + q.stub + "\n```\n\n";
      out += "### Rubric\n\n" + q.rubric.map(r => (r[0] === "alt" ? "" + r[1] : "+" + r[0] + "  " + r[1])).join("\n") + "\n";
      if (q.pen.length) out += "\nPenalties:\n" + q.pen.map(p => "-" + Math.abs(p[0]) + "  " + p[1]).join("\n") + "\n";
      if (q.reference) out += "\n### Reference solution\n\n" + (q.kind === "code" ? "```java\n" + q.reference + "\n```" : q.reference) + "\n";
      out += "\n### Student answer\n\n" + (ans === null ? "(blank)" : q.kind === "code" ? "```java\n" + ans + "\n```" : ans) + "\n\n";
      if (!forAI && q.exam) {
        const sc = att.scores[q.id];
        out += "Self-score: " + (typeof sc === "number" ? sc + " / " + q.pts : "not scored") + "\n\n";
      }
    });
    return out;
  }
  $("copyPromptBtn").addEventListener("click", () => {
    const text = gradingText(true);
    navigator.clipboard.writeText(text).then(() => { $("copyMsg").textContent = "Copied. Paste it into Claude or another AI chat."; })
      .catch(() => { const box = $("copyBox"); box.hidden = false; box.value = text; box.focus(); box.select(); $("copyMsg").textContent = "Copy the selected text (Cmd+C or Ctrl+C)."; });
  });
  $("downloadMdBtn").addEventListener("click", () => {
    S.download("cs226-" + EXAM + "-answers-" + S.today() + ".md", gradingText(false), "text/markdown");
  });

  // ---------- banners and other tabs ----------
  function showBanner(id, text) { const b = $(id); if (text) b.querySelector(".msg").textContent = text; b.hidden = false; }
  window.addEventListener("storage", e => {
    if (e.key !== S.keyFor(EXAM) || !e.newValue) return;
    let other; try { other = JSON.parse(e.newValue); } catch (err) { return; }
    const theirs = other.attempts && other.attempts.find(a => a.id === att.id);
    if (theirs && (theirs.updatedAt || 0) <= lastWrite) return;   // nothing newer for what we're showing
    if (!dirty) { load(); toast("Updated with changes from another tab."); }
    else showBanner("tabBanner");
  });
  $("loadTheirsBtn").addEventListener("click", () => { $("tabBanner").hidden = true; dirty = false; load(); toast("Loaded the other tab's version."); });
  $("keepMineBtn").addEventListener("click", () => {
    $("tabBanner").hidden = true;
    const fresh = S.read(EXAM);
    if (fresh) {                                   // keep their other attempts, overwrite only this one
      const mine = att;
      data = fresh;
      const i = data.attempts.findIndex(a => a.id === mine.id);
      if (i >= 0) data.attempts[i] = mine; else data.attempts.push(mine);
      att = mine;
    }
    persist(false); renderAttempts();
  });

  window.addEventListener("pagehide", saveNow);
  document.addEventListener("visibilitychange", () => { if (document.visibilityState === "hidden") { saveNow(); if (att && !att.submitted) persist(true); } });
  window.addEventListener("beforeunload", e => { if (dirty) { saveNow(); } });

  // ---------- start ----------
  function load() {
    data = storageOk ? S.read(EXAM) : null;
    let fresh = false;
    if (!data) { data = S.emptyExam(EXAM); fresh = true; }
    const a = data.attempts.find(x => x.id === data.currentId) || data.attempts[data.attempts.length - 1];
    data.currentId = a.id;
    showAttempt(a);
    lastWrite = a.updatedAt || 0;
    if (!storageOk) {
      setStatus("Not saving: storage blocked", "err");
      showBanner("storageBanner", "This browser is blocking storage (for example a private window), so answers will be lost when you close the tab. Use “Download backup” before leaving, or open the site in a normal window.");
    } else if (fresh) {
      try { S.write(EXAM, data); } catch (e) {}
      setStatus("Ready. Answers save as you type");
    } else {
      setStatus("Restored " + (a.updatedAt ? "from " + S.fmtDate(a.updatedAt) : ""), "ok");
    }
  }
  load();
  if (storageOk) S.askPersistent();
})();
