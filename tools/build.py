"""Builds the site from source/: index.html plus one page per exam in exams/.

Each source/<exam>/ folder has questions.py (prompts, stubs, rubrics) and java/*.java,
whose // <REF id> ... // </REF id> blocks are the reference solutions shown after submit.

    python3 tools/build.py
"""
import html, json, re, runpy, textwrap, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = "https://github.com/ramlukn/cs226-exam3-practice/blob/main/docs/"

EXAMS = [
    dict(id="test3", title="Test 3 Practice Exam", minutes=90,
         subtitle="heaps, priority queues and hashing",
         topics="Heap insert and remove traces, heapify and heapsort trace, chaining and rehash trace, open-addressing tombstone trace, equals and hashCode, open-addressing get and remove, chained remove, heap remove and sink, indexed PQ remove(item), top k with a PriorityQueue"),
]

FONTS = ('<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 16 16%27%3E%3Crect width=%2716%27 height=%2716%27 rx=%273%27 fill=%27%231f4f8f%27/%3E%3C/svg%3E">\n'
         '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">')


def load_refs(folder):
    refs = {}
    for f in (folder / "java").glob("*.java"):
        for m in re.finditer(r"[ \t]*// <REF (\w+)>\n(.*?)\n[ \t]*// </REF \1>", f.read_text(), re.S):
            body = "\n".join(l for l in m.group(2).split("\n") if "comparisons++" not in l)
            refs[m.group(1)] = textwrap.dedent(body).rstrip()
    return refs


def plain(s):
    """HTML fragment -> readable plain text for the grading export."""
    s = re.sub(r"<li>", "\n- ", s)
    s = re.sub(r"</p>\s*<p>", "\n\n", s)
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).strip()


def fmt(p):
    return "%g" % abs(p)


def check_points(q):
    total, alt = 0, False
    for p, _ in q["rubric"]:
        if p == "alt":
            alt = True
            continue
        if not alt:
            total += p
    assert abs(total - q["pts"]) < 1e-9, (q["id"], total, q["pts"])


def rubric_html(q, exam, refs):
    items = []
    for p, text in q["rubric"]:
        items.append('<li class="alt">%s</li>' % text if p == "alt" else '<li><b>+%s</b><span>%s</span></li>' % (fmt(p), text))
    for p, text in q.get("pen", []):
        items.append('<li class="pen"><b>−%s</b><span>%s</span></li>' % (fmt(p), text))
    ref = ""
    if q.get("ref"):
        ref = '<pre class="show">%s</pre>' % html.escape("\n\n".join(refs[r] for r in q["ref"]))
    ref += q.get("ref_html", "") + q.get("note", "")
    score = ""
    if exam:
        score = ('<label class="score" hidden>Your score <input type="number" class="sc" data-for="%s" min="0" max="%s" step="0.125" inputmode="decimal"> / %s</label>'
                 % (q["id"], q["pts"], fmt(q["pts"])))
    return ('<details class="rub%s"%s><summary>Rubric and reference solution</summary>'
            '<p class="rub-h">%s pts. Start from 0 and add each item the answer earns; penalties come off at the end.</p>'
            '<ul class="items">%s</ul><div class="refsol">%s</div></details>%s'
            % (" exam" if exam else "", " hidden" if exam else "", fmt(q["pts"]), "".join(items), ref, score))


def q_html(q, exam, refs):
    pts = fmt(q["pts"]) + (" pt" if q["pts"] == 1 else " pts")
    if q["kind"] == "code":
        field = ('<div class="ed"><div class="ln" aria-hidden="true"></div><textarea class="code field%s" id="%s" spellcheck="false" autocomplete="off" autocapitalize="off" aria-label="Code for %s">%s</textarea></div>'
                 '<div class="ed-foot"><span>Tab inserts 2 spaces</span><span class="spacer"></span><button type="button" class="resetBtn" data-for="%s">Reset to stub</button></div>'
                 % (" ex" if exam else "", q["id"], q["id"], html.escape(q["stub"]), q["id"]))
    else:
        field = '<textarea class="ans field%s" id="%s" aria-label="Answer %s"></textarea>' % (" ex" if exam else "", q["id"], q["id"])
    lock = '<p class="lock">The rubric unlocks when you submit.</p>' if exam else ""
    return ('<div class="q"><div class="q-h"><span class="q-id">%s</span><span class="q-pts">%s</span></div>%s%s%s%s</div>'
            % (q["id"], pts, q["prompt"], field, lock, rubric_html(q, exam, refs)))


def spec_entry(q, exam, refs):
    reference = "\n\n".join(refs[r] for r in q.get("ref", [])) if q.get("ref") else plain(q.get("ref_html", ""))
    note = plain(q.get("note", ""))
    if note:
        reference = (reference + "\n\n" + note).strip()
    return dict(id=q["id"], pts=q["pts"], kind=q["kind"], exam=exam, prompt=plain(q["prompt"]),
                stub=q.get("stub", ""), rubric=[[p, plain(t)] for p, t in q["rubric"]],
                pen=[[p, plain(t)] for p, t in q.get("pen", [])], reference=reference)


def json_script(id_, obj):
    text = json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")
    return '<script type="application/json" id="%s">%s</script>' % (id_, text)


def exam_page(meta, exam_qs, drills, refs):
    total = sum(q["pts"] for q in exam_qs)
    short = [q for q in exam_qs if q["kind"] == "text"]
    coding = [q for q in exam_qs if q["kind"] == "code"]
    chips = '<span class="chip">%d short answer and trace · %s pts</span><span class="chip">%d coding · %s pts</span>' % (
        len(short), fmt(sum(q["pts"] for q in short)), len(coding), fmt(sum(q["pts"] for q in coding)))
    spec = dict(id=meta["id"], title=meta["title"], minutes=meta["minutes"], total=total,
                questions=[spec_entry(q, True, refs) for q in exam_qs] + [spec_entry(q, False, refs) for q in drills])
    drill_section = ""
    if drills:
        drill_section = ('<section class="part" aria-labelledby="pd"><div class="part-h"><h2 id="pd">Extra coding drills</h2><span>untimed · not part of the %s</span></div>'
                         '<p class="drill-intro">More questions in the same format, for after the exam or a second round. Their rubrics are open from the start, so write your answer before you expand one. They save with the current attempt.</p>%s</section>'
                         % (fmt(total), "\n".join(q_html(q, False, refs) for q in drills)))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>CS226 {meta["title"]}</title>
{FONTS}
<link rel="stylesheet" href="../assets/site.css">
</head>
<body>
<div class="bar">
  <div class="bar-in">
    <div>
      <div class="bar-title"><a href="../index.html">CS226 practice</a> · {meta["title"]}</div>
      <div class="bar-sub">Closed book · {meta["minutes"]} min · {fmt(total)} pts · <span id="todoCount">0</span> TODO stubs left</div>
    </div>
    <span class="spacer"></span>
    <span class="status" id="status" aria-live="polite">Loading…</span>
    <span class="timer" id="timer" aria-label="Time remaining">{meta["minutes"]}:00</span>
    <button id="pauseBtn" type="button">Pause</button>
  </div>
</div>

<main class="wrap">
  <div class="banner err" id="storageBanner" hidden><span class="msg"></span><button type="button" onclick="document.getElementById('exportBtn').click()">Download backup</button></div>
  <div class="banner" id="tabBanner" hidden><span class="msg">This exam was changed in another tab while you were typing here.</span><button type="button" id="loadTheirsBtn">Load the other tab's version</button><button type="button" id="keepMineBtn">Keep mine</button></div>

  <div class="cover">
    <h1>{meta["title"]}: {meta.get("subtitle", "heaps, hashing, sorting and graphs")}</h1>
    <ul>
      <li>{len(exam_qs)} questions, {fmt(total)} points, in the shape of the real exam: short answers and a trace, then coding questions.</li>
      <li>{meta["minutes"]} minutes. The timer runs only while this tab is visible and not paused. Trace one tiny input through every coding answer before moving on.</li>
      <li>Helpers marked GIVEN already exist: call them, don't rewrite them. Use the course's exceptions: <code>IllegalArgumentException</code>, <code>NoSuchElementException</code>.</li>
      <li>Everything saves in this browser as you type. Use <b>Download backup</b> below to move to another device or keep a copy.</li>
      <li>After you submit, each question shows its rubric and a reference solution, and you can score yourself. See <a href="{DOCS}grading.md">how to grade</a>.</li>
    </ul>
    <div class="rubric">{chips}</div>
  </div>

  <div class="panel" aria-labelledby="attH">
    <h2 id="attH">Attempt</h2>
    <div class="attempt-row">
      <select id="attemptSelect" aria-label="Choose an attempt"></select>
      <button type="button" id="newAttemptBtn">New attempt</button>
      <button type="button" id="deleteAttemptBtn" class="danger">Delete this attempt</button>
    </div>
    <p class="small" id="attemptInfo"></p>
  </div>

  <section class="part" aria-labelledby="pa">
    <div class="part-h"><h2 id="pa">{meta["title"]}</h2><span>{fmt(total)} pts · about {meta["minutes"]} min</span></div>
{chr(10).join(q_html(q, True, refs) for q in exam_qs)}
  </section>

  <div class="submit" id="submitBox">
    <p class="note" id="submitNote">When you're done, submit. Your answers stay saved and editable afterward.</p>
    <div class="row" id="submitRow"><button type="button" class="primary" id="submitBtn">Submit exam</button></div>
    <div class="row" id="confirmRow" hidden>
      <span class="note" id="confirmText">Submit now?</span>
      <button type="button" class="primary" id="confirmBtn">Submit</button>
      <button type="button" id="cancelBtn">Keep working</button>
    </div>
    <div id="doneRow" hidden>
      <p class="tally">Self-graded: <b id="tally">0</b> / {fmt(total)} <span class="note" id="tallyNote"></span></p>
      <p class="note">Score each question in the box under its rubric. For a second opinion, copy the grading prompt into Claude (or another AI) or send the answers file to a friend.</p>
      <div class="row" style="margin-top:8px">
        <button type="button" id="copyPromptBtn">Copy grading prompt</button>
        <button type="button" id="downloadMdBtn">Download answers (.md)</button>
        <span class="note" id="copyMsg"></span>
      </div>
      <textarea id="copyBox" hidden readonly aria-label="Grading prompt"></textarea>
    </div>
  </div>

  <div class="panel" aria-labelledby="bkH">
    <h2 id="bkH">Backup</h2>
    <p class="small">Answers live only in this browser. A backup file holds every attempt at this exam; importing one merges it in (the newer copy of an attempt wins), so it is safe to import twice.</p>
    <div class="row">
      <button type="button" id="exportBtn">Download backup</button>
      <label class="file-btn"><button type="button" onclick="this.nextElementSibling.click()">Import backup</button><input type="file" id="importInput" accept="application/json,.json"></label>
    </div>
  </div>

  {drill_section}
</main>
<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>
{json_script("exam-spec", spec)}
<script src="../assets/store.js"></script>
<script src="../assets/exam.js"></script>
</body>
</html>
"""


def index_page(cards):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>CS226 Exam 3 Practice</title>
{FONTS}
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<div class="bar">
  <div class="bar-in">
    <div>
      <div class="bar-title">CS226 Exam 3 practice</div>
      <div class="bar-sub">Priority queues · heaps · hashing</div>
    </div>
  </div>
</div>
<main class="wrap">
  <div class="banner err" id="storageBanner" hidden><span class="msg">This browser is blocking storage (for example a private window), so answers won't be kept after you close the tab. Open the site in a normal window.</span></div>

  <div class="cover">
    <h1>A timed practice exam, graded like the real thing</h1>
    <ul>
      <li>The exam is 38 points in 90 minutes: short answers, a trace, and coding questions in Java, with GIVEN helpers like the real exam.</li>
      <li>Your answers save automatically in this browser. Come back any time; nothing is sent anywhere.</li>
      <li>After you submit, rubrics and reference solutions unlock, and you score yourself item by item. You can also copy a ready-made grading prompt for an AI.</li>
      <li>New here? Read <a href="{DOCS}using-the-site.md">how to use the site</a> and <a href="{DOCS}grading.md">how to grade</a>.</li>
    </ul>
  </div>

  <section class="part" aria-labelledby="exH">
    <div class="part-h"><h2 id="exH">Exams</h2><span>matches the Test 3 scope</span></div>
    <div class="cards" id="cards"></div>
  </section>

  <section class="part" aria-labelledby="hiH">
    <div class="part-h"><h2 id="hiH">Your attempts</h2><span>on this browser</span></div>
    <p class="small" id="historyEmpty">No attempts yet.</p>
    <table class="hist" id="historyTable" hidden>
      <thead><tr><th>Exam</th><th>#</th><th>Started</th><th>Time</th><th>Status</th><th>Self-score</th></tr></thead>
      <tbody id="history"></tbody>
    </table>
  </section>

  <div class="panel" aria-labelledby="bkH">
    <h2 id="bkH">Backup and moving devices</h2>
    <p class="small">Everything is stored in this browser only. Download a backup to keep a copy or to continue on another computer, then import it there. Importing merges: it never deletes attempts.</p>
    <div class="row">
      <button type="button" id="exportAllBtn">Download backup of all exams</button>
      <label class="file-btn"><button type="button" onclick="this.nextElementSibling.click()">Import backup</button><input type="file" id="importAllInput" accept="application/json,.json"></label>
      <span class="spacer"></span>
      <button type="button" id="resetAllBtn" class="danger">Erase all saved answers</button>
    </div>
  </div>
</main>
<div class="toast" id="toast" role="status" aria-live="polite" hidden></div>
{json_script("site-spec", cards)}
<script src="assets/store.js"></script>
<script src="assets/home.js"></script>
</body>
</html>
"""


def main():
    cards = []
    for meta in EXAMS:
        folder = ROOT / "source" / meta["id"]
        ns = runpy.run_path(str(folder / "questions.py"))
        exam_qs, drills = ns["EXAM"], ns.get("DRILLS", [])
        refs = load_refs(folder)
        for q in exam_qs + drills:
            check_points(q)
            for r in q.get("ref", []):
                assert r in refs, (meta["id"], q["id"], r)
        total = sum(q["pts"] for q in exam_qs)
        assert abs(total - 38) < 1e-9, (meta["id"], total)
        out = ROOT / "exams" / (meta["id"] + ".html")
        out.parent.mkdir(exist_ok=True)
        out.write_text(exam_page(meta, exam_qs, drills, refs))
        print("wrote", out.relative_to(ROOT), "-", len(exam_qs), "questions,", len(drills), "drills")
        cards.append(dict(id=meta["id"], title=meta["title"], topics=meta["topics"], minutes=meta["minutes"],
                          total=total, count=len(exam_qs), drills=len(drills), questionIds=[q["id"] for q in exam_qs]))
    (ROOT / "index.html").write_text(index_page(cards))
    print("wrote index.html")


if __name__ == "__main__":
    main()
