# CS226 Exam 3 practice

A timed practice exam for CS226 (Data Structures, Java) Test 3, written for the announced scope: the test covers Dynamic Array through Open Addressing, with the focus on the material not covered in earlier tests (priority queues, binary heaps, heapsort, the indexed priority queue, hashing, separate chaining, open addressing). It follows the shape and grading style of the real exams: 38 points in 90 minutes, short answers and traces, then coding questions with GIVEN helpers.

**Open the site: https://ramlukn.github.io/cs226-exam3-practice/**

Nothing to install and no account. Your answers save automatically in your own browser.

## The exam

| Exam | Covers |
|---|---|
| Test 3 Practice Exam | Heap insert and remove traces, a heapify and heapsort trace, a chaining and rehash trace, an open-addressing tombstone trace, `equals` and `hashCode`, open-addressing `get` and `remove`, chained `remove`, heap `remove` and `sink`, the indexed priority queue's `remove(item)`, top k with a `PriorityQueue`. |

10 questions, 38 points. The earlier mock exams were removed because they included quicksort and graph search, which aren't on Test 3; they are still in the git history.

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
