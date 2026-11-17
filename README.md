# CS226 Exam 3 practice

Four timed mock exams for CS226 (Data Structures, Java) Exam 3: heaps, priority queues, hashing, sorting and graphs. They follow the shape and grading style of the real exams: 38 points in 90 minutes, short answers and a trace, then coding questions with GIVEN helpers.

**Open the site: https://ramlukn.github.io/cs226-exam3-practice/**

Nothing to install and no account. Your answers save automatically in your own browser.

## The exams

| Exam | Covers |
|---|---|
| Mock Test 3 | Median-of-three quicksort, the equals/hashCode rule, an open-addressing trace, `isMinHeap`, chained `get`, open-addressing `probe` and `put`, `sink`, the indexed heap's `swap` and `changePriority`, a chained key iterator, BFS within k hops. Plus 8 untimed extra drills. |
| Mock Test 4 | Judging `hashCode` choices, an indexed-heap swap bug, a tombstone trace, heap `insert` and `swim`, chained `put`, open-addressing `find` and `remove`, a value iterator, indexed-heap `remove(item)`, partition with `a[lo]` as pivot, BFS shortest path. |
| Mock Test 5 | Quicksort worst cases, bottom-up heapify, chaining and heap traces, heap `remove`, chained `remove`, open-addressing `rehash`, `isConnected`, indexed-heap `insert` and `removeBest`, quickselect, BFS levels. |
| Mock Test 6 | The iterator contract, BFS visited-marking and why DFS gets distances wrong, a tombstone-reuse and same-size-rehash trace, a reverse-order key iterator, chained `rehash`, open-addressing `put` without a `probe` helper, an O(n) heapify constructor, merging k sorted lists with a PriorityQueue, Lomuto partition, connected-component labels. |

Each one is 10 questions worth 38 points. Take them in order if you can; each targets mistakes that are common on the one before.

## How it works

1. Open an exam from the home page and start. The timer runs while the tab is visible; you can pause it.
2. Write answers in the boxes. Code boxes have line numbers, Tab indents, and Enter keeps your indentation.
3. Everything saves as you type, in this browser only. The status at the top says when it last saved.
4. Submit when done. Each question's rubric and reference solution unlock, and you score yourself item by item.
5. Want a second opinion? Copy the grading prompt into Claude (or another AI), or send your answers file to a friend.

Read more:

- [How to use the site](docs/using-the-site.md): attempts, saving, backups, moving to another computer, troubleshooting.
- [How to grade](docs/grading.md): how the rubrics work, how to self-grade honestly, and how to get an AI or a friend to grade you.
- [Maintaining the exams](docs/maintaining.md): how the pages are built and how the reference solutions are tested.

## Privacy

There is no server. Answers are stored in your browser's local storage and never leave your computer unless you download a backup or copy them yourself.

## About

Unofficial, student-made practice. The questions are original, written in the style of the course's exams; they aren't past exam questions, and they don't come from the course staff. Every reference solution is compiled and checked against Java's own collections with randomized tests (`tools/test_java.sh`), but if you think an answer or rubric is wrong, open an issue.
