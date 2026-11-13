# Maintaining the exams

The site is static HTML, built by one Python script from the files in `source/`. GitHub Pages serves the repository as it is, so the built pages are committed.

## Layout

```
index.html               home page (built)
exams/mock-N.html        exam pages (built)
assets/site.css          styles for every page
assets/store.js          saving: local storage, attempts, backup import/export
assets/exam.js           exam page: editor, timer, autosave, submit, grading export
assets/home.js           home page: exam cards, attempt history, backups
source/mock-N/
  questions.py           prompts, starter code, rubrics, penalties, notes
  java/*.java            reference solutions + randomized tests
tools/build.py           builds index.html and exams/*.html
tools/test_java.sh       compiles and runs every reference solution's tests
```

## Building

Needs Python 3 and a JDK (11 or newer).

```bash
./tools/test_java.sh     # every reference solution must print "... OK"
python3 tools/build.py   # rewrites index.html and exams/*.html
```

`build.py` refuses to build if a rubric's items don't add up to the question's points, if an exam isn't 38 points, or if a question names a reference solution that doesn't exist.

To preview locally, serve the folder (opening the files directly also works, but some browsers give `file://` pages their own storage):

```bash
python3 -m http.server 8799
```

Then open http://127.0.0.1:8799/.

## Question format

Each entry in `EXAM` (or `DRILLS`) in `questions.py` is a dict:

| Key | Meaning |
|---|---|
| `id` | `Q1` … `Q10` (drills: `D1` …) |
| `pts` | Points |
| `kind` | `"code"` (editor with starter code) or `"text"` (plain answer box) |
| `prompt` | HTML for the question |
| `stub` | Starter code for code questions |
| `ref` | Names of `// <REF name>` blocks in `java/*.java` shown as the reference solution |
| `ref_html` | HTML reference answer, for text questions |
| `rubric` | List of `(points, text)` items; the points must add up to `pts`. An `("alt", heading)` entry starts an alternative approach whose items aren't counted in the sum |
| `pen` | List of `(-points, text)` penalties |
| `note` | Extra explanation shown under the reference solution |

Reference solutions live between markers in a Java file that also tests them:

```java
// <REF Q5>
public V get(K key) { ... }
// </REF Q5>
```

Lines containing `comparisons++` are dropped from what students see (they're test instrumentation).

## Adding an exam

1. Copy a `source/mock-N` folder, rewrite `questions.py`, and write the reference solutions with tests in `java/`.
2. Add the exam to `EXAMS` at the top of `tools/build.py`.
3. Run the tests and the build, and commit everything including the built HTML.

## Saved data format

Each exam's attempts are stored under the local-storage key `cs226-practice:v1:<exam id>`:

```json
{ "v": 1, "exam": "mock-4", "currentId": "a_...",
  "attempts": [ { "id": "a_...", "createdAt": 0, "updatedAt": 0,
                  "answers": { "Q1": "..." }, "scores": { "Q1": 2.5 },
                  "elapsed": 1234, "submitted": true, "submittedAt": "2026-..." } ] }
```

Answers equal to the untouched starter code aren't stored. Backups wrap these as `{ "format": "cs226-practice-backup", "v": 1, "exams": { "<id>": ... } }`. Renaming an exam's `id` would orphan people's saved answers, so don't.
