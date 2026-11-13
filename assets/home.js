// Home page: one card per exam with its saved progress, attempt history, and site-wide backups.
(function () {
  const S = window.PracticeStore;
  const exams = JSON.parse(document.getElementById("site-spec").textContent);
  const ids = exams.map(e => e.id);
  const $ = id => document.getElementById(id);

  let toastTimer = null;
  function toast(text) {
    const t = $("toast"); t.textContent = text; t.hidden = false;
    clearTimeout(toastTimer); toastTimer = setTimeout(() => { t.hidden = true; }, 3200);
  }

  function el(tag, attrs, text) {
    const n = document.createElement(tag);
    Object.entries(attrs || {}).forEach(([k, v]) => n.setAttribute(k, v));
    if (text !== undefined) n.textContent = text;
    return n;
  }

  function render() {
    const cards = $("cards"); cards.innerHTML = "";
    const hist = $("history"); hist.innerHTML = "";
    let anyAttempts = false;

    exams.forEach(ex => {
      const data = S.read(ex.id);
      const card = el("article", { class: "card" });
      card.appendChild(el("h2", {}, ex.title));
      card.appendChild(el("p", { class: "topics" }, ex.topics));
      card.appendChild(el("p", { class: "small" }, ex.total + " pts · " + ex.minutes + " min · " + ex.count + " questions" + (ex.drills ? " + " + ex.drills + " extra drills" : "")));

      const state = el("p", { class: "state" });
      let label = "Open";
      if (!data || !data.attempts.length) {
        state.textContent = "Not started";
        label = "Start";
      } else {
        const cur = data.attempts.find(a => a.id === data.currentId) || data.attempts[data.attempts.length - 1];
        const started = Object.keys(cur.answers || {}).length > 0 || cur.elapsed > 0;
        if (cur.submitted) {
          const sc = S.scoreOf(cur, ex.questionIds);
          state.innerHTML = "";
          state.append("Submitted · ");
          state.appendChild(el("b", {}, sc.scored ? sc.total + " / " + ex.total : "not self-scored yet"));
          label = "Review";
        } else if (started) {
          state.textContent = "In progress · " + S.fmtDuration(cur.elapsed) + " used";
          label = "Continue";
        } else {
          state.textContent = "Not started";
          label = "Start";
        }
        const real = data.attempts.filter(a => !S.isPristine(a)).length;
        if (real > 1) state.append(" · " + real + " attempts");
      }
      card.appendChild(state);
      card.appendChild(el("a", { class: "open", href: "exams/" + ex.id + ".html" }, label));
      cards.appendChild(card);

      if (data) data.attempts.forEach((a, i) => {
        const started = Object.keys(a.answers || {}).length > 0 || a.elapsed > 0 || a.submitted;
        if (!started) return;
        anyAttempts = true;
        const sc = S.scoreOf(a, ex.questionIds);
        const tr = el("tr");
        tr.appendChild(el("td", {}, ex.title));
        tr.appendChild(el("td", { class: "num" }, String(i + 1)));
        tr.appendChild(el("td", {}, S.fmtDate(a.createdAt)));
        tr.appendChild(el("td", { class: "num" }, S.fmtDuration(a.elapsed)));
        tr.appendChild(el("td", {}, a.submitted ? "Submitted" : "In progress"));
        tr.appendChild(el("td", { class: "num" }, sc.scored ? sc.total + " / " + ex.total + (sc.scored < ex.questionIds.length ? " (" + sc.scored + " scored)" : "") : "—"));
        hist.appendChild(tr);
      });
    });
    $("historyEmpty").hidden = anyAttempts;
    $("historyTable").hidden = !anyAttempts;
  }

  if (!S.available()) {
    $("storageBanner").hidden = false;
  } else {
    S.askPersistent();
  }

  $("exportAllBtn").addEventListener("click", () => {
    const backup = S.makeBackup(ids);
    if (!Object.keys(backup.exams).length) { toast("Nothing saved yet."); return; }
    S.download("cs226-practice-backup-" + S.today() + ".json", JSON.stringify(backup, null, 2));
    toast("Backup downloaded.");
  });

  $("importAllInput").addEventListener("change", e => {
    const file = e.target.files[0]; e.target.value = "";
    if (!file) return;
    file.text().then(text => {
      try {
        const res = S.importBackup(text, ids);
        let added = 0, updated = 0;
        Object.values(res).forEach(r => { added += r.added; updated += r.updated; });
        render();
        toast("Imported " + added + " new and " + updated + " updated attempts.");
      } catch (err) { toast(err.message); }
    });
  });

  let armed = false, t = null;
  $("resetAllBtn").addEventListener("click", () => {
    const b = $("resetAllBtn");
    if (!armed) { armed = true; b.textContent = "Click again to erase everything"; t = setTimeout(() => { armed = false; b.textContent = "Erase all saved answers"; }, 3000); return; }
    clearTimeout(t); armed = false; b.textContent = "Erase all saved answers";
    ids.forEach(S.remove); render(); toast("All saved answers on this browser were erased.");
  });

  window.addEventListener("storage", e => { if (e.key && e.key.startsWith(S.PREFIX)) render(); });
  window.addEventListener("pageshow", render);
  render();
})();
