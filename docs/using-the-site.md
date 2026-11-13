# How to use the site

Site: https://ramlukn.github.io/cs226-exam3-practice/

## Taking an exam

- **Start** an exam from its card on the home page. The card says whether you haven't started, are in progress (and how much time you've used), or have submitted (and your self-score).
- **Timer.** 90 minutes, counting down at the top. It only runs while the exam tab is visible, so switching tabs pauses it. **Pause** stops it on purpose. It turns amber with 10 minutes left and red with negative time once you go over; it never locks you out.
- **Code boxes** behave like a small editor: line numbers, **Tab** inserts 2 spaces, **Enter** keeps the current indentation and adds a level after `{`. **Reset to stub** (click twice) puts the starter code back.
- **TODO counter.** The top bar counts the `// TODO` lines still left in the coding stubs, so you can see at a glance what you haven't touched.
- **GIVEN** helpers exist already. Call them; don't rewrite them.

Exam conditions: closed book, no running code. If you want the practice to predict the real exam, keep it that way.

## Saving

Everything saves automatically in **this browser**, about half a second after you stop typing, and again whenever you leave a box, switch tabs or close the page.

The status at the top tells you where you stand:

| Status | Meaning |
|---|---|
| Ready. Answers save as you type | First visit to this exam on this browser |
| Saving… | You just typed; it will save in a moment |
| Saved 3:41:07 PM | Saved at that time |
| Restored from Nov 13, 3:40 PM | You came back, and your answers were loaded |
| Not saving: storage blocked | The browser refuses to store anything (usually a private or incognito window). Use **Download backup** before closing the tab, or reopen the site in a normal window |
| Couldn't save. Download a backup now. | The browser refused one save (for example, storage full). Download a backup |

Saved answers stay until you delete them, clear your browser's site data, or use **Erase all saved answers** on the home page. They are tied to this browser on this computer: another browser or device won't see them unless you move them with a backup.

## Attempts

You can take each exam more than once and keep every attempt.

- The **Attempt** menu shows every attempt with its date and status or self-score. Choosing one loads it (answers, scores, time used).
- **New attempt** (click twice) starts a blank attempt with a fresh timer. Earlier attempts stay in the menu.
- **Delete this attempt** (click twice) removes the attempt you're looking at. If it's the only one, the button says **Clear this attempt** and empties it instead.

The home page's **Your attempts** table lists every attempt you've started, across all exams, with time used and self-score.

## Submitting

**Submit exam** asks once to confirm (and warns if answers are still blank). After you submit:

- each question shows its **rubric and reference solution**;
- each question gets a **Your score** box, and the total at the bottom adds them up;
- the timer stops.

You can still edit answers after submitting, and changes keep saving. See [How to grade](grading.md) for how to score.

## Backups and moving to another computer

A backup is a small `.json` file with every attempt: answers, scores, time used.

- **On an exam page:** *Download backup* saves that exam's attempts.
- **On the home page:** *Download backup of all exams* saves everything.
- **Import backup** (either page) loads a backup file into this browser.

Importing **merges**; it never deletes anything. Attempts you don't have are added. If the same attempt exists in both places, the copy that was edited more recently wins. Importing the same file twice is harmless.

To continue on another computer: download a backup, open the site there, import it.

Download a backup now and then anyway. Browsers can clear site data (for example after a long time unused, or when you clear history).

## Several tabs

If the same exam is open in two tabs, an edit in one shows up in the other. If you were typing in both at once, a bar appears asking whether to **load the other tab's version** or **keep yours**. Simplest is to use one tab per exam.

## Grading files

After submitting:

- **Copy grading prompt** copies the questions, rubrics, reference solutions and your answers as one prompt for an AI. See [How to grade](grading.md#grading-with-an-ai).
- **Download answers (.md)** saves the same material (plus your self-scores) as a Markdown file to send to a friend or keep.

## Troubleshooting

| Problem | Fix |
|---|---|
| My answers are gone | Check the **Attempt** menu: you may be on a different attempt. Check you're in the same browser and not a private window. If you have a backup, import it |
| "Storage blocked" | You're probably in a private or incognito window, or site data is blocked for github.io. Use a normal window, or download a backup before you close the tab |
| Timer didn't move | It only runs while the tab is visible and not paused. That's deliberate |
| Rubrics don't show | They unlock after you submit that attempt. A new attempt hides them again until you submit it |
| Copy grading prompt did nothing | Some browsers block clipboard access; a text box with the prompt appears instead, already selected. Press Cmd+C or Ctrl+C |
| I want to start completely fresh | Home page → **Erase all saved answers** (click twice). This can't be undone, so download a backup first if unsure |
