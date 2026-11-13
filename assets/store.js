// Shared storage for the practice site. Everything lives in this browser's localStorage,
// one key per exam, holding every attempt at that exam. Backups are plain JSON files.
(function () {
  const PREFIX = "cs226-practice:v1:";
  const BACKUP_FORMAT = "cs226-practice-backup";

  function keyFor(examId) { return PREFIX + examId; }

  function available() {
    try {
      const k = PREFIX + "__test";
      localStorage.setItem(k, "1");
      localStorage.removeItem(k);
      return true;
    } catch (e) { return false; }
  }

  function newId() {
    return "a_" + Date.now().toString(36) + "_" + Math.random().toString(36).slice(2, 8);
  }

  function blankAttempt() {
    const now = Date.now();
    return { id: newId(), createdAt: now, updatedAt: now, answers: {}, scores: {},
             elapsed: 0, submitted: false, submittedAt: null };
  }

  function emptyExam(examId) {
    const a = blankAttempt();
    return { v: 1, exam: examId, currentId: a.id, attempts: [a] };
  }

  function isValidExam(data) {
    return data && typeof data === "object" && Array.isArray(data.attempts) &&
           data.attempts.every(a => a && typeof a.id === "string" && typeof a.answers === "object");
  }

  function isPristine(a) {
    return !a.submitted && !(a.elapsed > 0) && !Object.keys(a.answers || {}).length && !Object.keys(a.scores || {}).length;
  }

  // Returns the stored record, or null if there is none (or it is unreadable).
  function read(examId) {
    try {
      const raw = localStorage.getItem(keyFor(examId));
      if (!raw) return null;
      const data = JSON.parse(raw);
      return isValidExam(data) ? data : null;
    } catch (e) { return null; }
  }

  // Throws if the browser refuses the write (private mode, storage full), so callers can warn.
  function write(examId, data) {
    localStorage.setItem(keyFor(examId), JSON.stringify(data));
  }

  function remove(examId) {
    try { localStorage.removeItem(keyFor(examId)); } catch (e) {}
  }

  // Merges attempts from a backup into what is stored: unknown attempts are added,
  // and for an attempt that exists in both, the more recently edited copy wins.
  function merge(examId, incoming) {
    const current = read(examId);
    if (!current) { write(examId, incoming); return { added: incoming.attempts.length, updated: 0 }; }
    let added = 0, updated = 0;
    // An untouched blank attempt (made just by opening the page) shouldn't linger next to imported ones.
    if (incoming.attempts.length) current.attempts = current.attempts.filter(a => !isPristine(a) || incoming.attempts.some(b => b.id === a.id));
    const byId = new Map(current.attempts.map(a => [a.id, a]));
    incoming.attempts.forEach(a => {
      const mine = byId.get(a.id);
      if (!mine) { current.attempts.push(a); added++; }
      else if ((a.updatedAt || 0) > (mine.updatedAt || 0)) {
        current.attempts[current.attempts.indexOf(mine)] = a; updated++;
      }
    });
    current.attempts.sort((x, y) => (x.createdAt || 0) - (y.createdAt || 0));
    if (!current.attempts.length) current.attempts.push(blankAttempt());
    if (!current.attempts.some(a => a.id === current.currentId)) current.currentId = current.attempts[current.attempts.length - 1].id;
    write(examId, current);
    return { added, updated };
  }

  function makeBackup(examIds) {
    const exams = {};
    examIds.forEach(id => { const d = read(id); if (d) exams[id] = d; });
    return { format: BACKUP_FORMAT, v: 1, exportedAt: new Date().toISOString(), exams };
  }

  // Parses a backup file's text and merges every exam in it. Returns per-exam counts.
  function importBackup(text, knownIds) {
    let data;
    try { data = JSON.parse(text); } catch (e) { throw new Error("That file isn't valid JSON."); }
    if (!data || data.format !== BACKUP_FORMAT || typeof data.exams !== "object") {
      throw new Error("That file isn't a backup from this site.");
    }
    const result = {};
    Object.keys(data.exams).forEach(id => {
      if (knownIds && !knownIds.includes(id)) return;
      if (!isValidExam(data.exams[id])) return;
      result[id] = merge(id, data.exams[id]);
    });
    if (!Object.keys(result).length) throw new Error("The backup has no attempts for these exams.");
    return result;
  }

  function download(filename, text, type) {
    const blob = new Blob([text], { type: type || "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  function today() { return new Date().toISOString().slice(0, 10); }

  function fmtDuration(sec) {
    sec = Math.max(0, Math.round(sec || 0));
    const h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60);
    return h ? h + "h " + m + "m" : m + "m " + (sec % 60) + "s";
  }

  function fmtDate(ms) {
    if (!ms) return "";
    return new Date(ms).toLocaleString(undefined, { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
  }

  function scoreOf(attempt, examQuestionIds) {
    let total = 0, n = 0;
    examQuestionIds.forEach(id => {
      const v = attempt.scores && attempt.scores[id];
      if (typeof v === "number" && !isNaN(v)) { total += v; n++; }
    });
    return { total: Math.round(total * 1000) / 1000, scored: n };
  }

  async function askPersistent() {
    try { if (navigator.storage && navigator.storage.persist) await navigator.storage.persist(); } catch (e) {}
  }

  window.PracticeStore = { PREFIX, keyFor, available, blankAttempt, emptyExam, read, write, remove,
    merge, isPristine, makeBackup, importBackup, download, today, fmtDuration, fmtDate, scoreOf, askPersistent };
})();
