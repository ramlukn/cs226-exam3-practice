# How to grade

The rubrics are written the way CS226's graders grade: **you start at 0 and earn points**, rather than starting at full marks and losing them. Grading yourself the same way tells you what you'd actually get on the exam.

## How a rubric works

Each question's rubric has two parts.

**Items** (green, `+`): each is something the answer must do, worth a fixed number of points.

```
+0.5   probe starts at indexFor(key)
+1     find keeps going past tombstones: only null ends the search
+0.75  remove marks the entry deleted, it does not set the slot to null
```

**Penalties** (red, `−`): taken off at the end, for specific mistakes that the items don't already cover.

```
−1     probe returns at the first tombstone without probing on
−0.75  Solution is recursive (when iterative was asked for)
−0.125 Minor logic or major syntax errors showing lack of understanding
```

Some rubrics also have an **Alternative** heading: a different approach that earns a different set of items (usually fewer points, because it isn't what was asked).

The score is **items earned − penalties**, never below 0 or above the question's points.

## Rules the graders follow

- **An item is earned if the answer does that thing, correctly, as written.** Not "would have, with one more line." If the idea is there but broken, it isn't earned.
- **Partial items** are fine only when an item clearly has separate parts (for example "loops while i > 0 *and* compares with the parent"). Give the share for the part that's right, and write down why.
- **Syntax barely counts.** At most **−0.125 per question** for syntax errors that show a misunderstanding (`index[x] = i` on a `Map`, `new T[n]`, calling a method that doesn't exist). Missing semicolons and small typos cost nothing. Never take away an item only because of syntax.
- **Logic counts fully.** A loop that never advances, a condition that's backwards, a field that's never updated (`size`, `used`, the index map): those lose the items they affect.
- **Mirror-image solutions** (for example a correct max-heap where a min-heap was asked) earn the matching items, then lose the stated penalty.
- **Don't double-count.** If a mistake already cost an item, don't also take the penalty for the same mistake, unless the rubric says to.

## Self-grading, step by step

1. **Submit** the attempt. Rubrics unlock under each question.
2. For each question, before you look at the reference solution, **trace a tiny input** through your answer: 2 or 3 elements, plus one edge case (empty, the last element, a key past a tombstone). Write down what it actually does.
3. Go through the rubric **one item at a time**. For each item ask: does my answer, as written, do exactly this? Yes means full points; no means 0; clearly half-right on a two-part item means part.
4. Apply the penalties that fit.
5. Type the result into **Your score**. The total at the bottom updates and is saved with the attempt.
6. Only now read the reference solution, and compare it line by line with yours.

**Be strict.** The point is to find what costs you points before the real exam does. If you can't tell whether an item is earned, it probably isn't.

## Common ways to lose points on these exams

| Mistake | What it costs |
|---|---|
| Comparing keys with `==` instead of `.equals` | An item or −0.25 |
| `%` without `Math.floorMod` (a negative hash code gives a negative index) | −0.25 |
| Integer division in a load-factor check: `size / buckets.length` | An item or −0.25 |
| Stopping an open-addressing search at a tombstone | Usually −1 |
| Setting a removed slot to `null` instead of marking it deleted | An item, and later searches break |
| Forgetting to update `size`, `used` or the index map | The matching item |
| Reading `heap[child]` before checking `child < size` | The bounds item |
| A loop condition that's backwards (`<` vs `>`, `&&` vs `\|\|`) | Most of the question |
| Recursion where iteration was required | −0.75 |
| A stack or DFS where BFS (a queue) was needed | −1 |
| Copying everything into a list when O(1) extra space was required | −0.5 |
| Answering something other than what was asked (no slot number, no example) | That item |

## Grading with an AI

After submitting, press **Copy grading prompt**. It copies one message with:

- grading rules matching the ones above;
- every question, its rubric, penalties and reference solution;
- your answers (and any extra drills you attempted).

Paste it into Claude or another AI chat and send. You'll get each question scored item by item, with a one-line fix, a total and the habits that cost the most.

Then **check its work**. An AI can be too generous ("the idea is there") or misread code. Two quick checks:

- For any item it marked as earned, find the exact line in your answer that earns it.
- For any crash or infinite loop it claims, trace the input it names.

If its score and yours differ by more than about 2 points, go through the questions where you disagree item by item.

## Grading a friend (or being graded by one)

1. After submitting, press **Download answers (.md)**. The file has each question, the rubric, the reference solution, the answer and the self-score.
2. Send it to your friend. They grade each question against the rubric in the file, writing the score next to the self-score.
3. Go through every question where the two scores differ. Those are usually the mistakes you don't see in your own code.

Swapping like this works best when you've both taken the same exam.

## What the score means

38 points, like the real exam. As a rough guide:

| Score | Reading |
|---|---|
| 30+ | Ready. Spend the remaining time on speed and on the topics you lost points in |
| 22–30 | The ideas are there; the points are going to details. Redo the questions you lost the most on, from a blank attempt |
| Under 22 | Re-study the topics behind your lowest questions, then retake the exam as a new attempt a few days later |

Retaking matters more than the first score. Use **New attempt** so both scores stay on the home page and you can compare.
