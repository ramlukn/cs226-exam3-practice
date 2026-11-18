# Question specs for Test 3 Practice Exam 2. Reference code comes from java/*.java <REF id> blocks.
SYN = (-0.125, "Minor logic or major syntax errors showing lack of understanding")

EXAM = [
dict(id="Q1", pts=3, kind="text",
 prompt="""<p>Binary min-heaps are stored in arrays with the root at index 0.</p>
<p>(a) Which of these are valid min-heaps? For each one that isn't, name a parent and child (by index) that break the rule.</p>
<pre class="show">A: [1, 3, 2, 7, 4, 5]
B: [2, 4, 3, 5, 1, 6]
C: [1, 1, 1, 2]
D: [3, 5, 4, 6, 7, 2]</pre>
<p>(b) In a min-heap of 20 values, which indices can hold the <b>largest</b> value, and why? (c) Which indices can hold the <b>second smallest</b>? (d) What is the height of a heap with 20 values (a single node has height 0)?</p>""",
 rubric=[(0.25, "(a) A is valid"),
         (0.5, "(a) B is not: index 1 (4) has child index 4 (1)"),
         (0.25, "(a) C is valid (equal values are fine)"),
         (0.5, "(a) D is not: index 2 (4) has child index 5 (2)"),
         (0.75, "(b) Only leaves, indices 10 to 19: a node with a child is smaller than or equal to that child, so it can't be the strict maximum"),
         (0.5, "(c) Index 1 or 2: it must be a child of the root"),
         (0.25, "(d) 4 (floor of log2 20)")],
 pen=[(-0.25, "Uses 1-indexed parent/child formulas. Apply once")],
 ref_html="""<pre class="show">children of i: 2i+1, 2i+2      parent of i: (i-1)/2
B: index 4 (1) &lt; parent index 1 (4)   ✗
D: index 5 (2) &lt; parent index 2 (4)   ✗
(b) leaves are indices n/2 .. n-1 = 10 .. 19
(c) the second smallest is smaller than everything except the root, so its parent must be the root → index 1 or 2
(d) levels hold 1, 2, 4, 8 = 15 nodes, the 5th level holds the rest → height 4</pre>"""),

dict(id="Q2", pts=3, kind="text",
 prompt="""<p>An indexed min-priority queue stores entries <code>item:priority</code> in a heap array (root at 0) and a map <code>where</code> from item to index. Starting from empty:</p>
<p><code>insert(A, 5), insert(B, 3), insert(C, 8), insert(D, 1)</code></p>
<p>(a) Write the heap array and the <code>where</code> map. (b) Then <code>changePriority(C, 0)</code>. Write both again. (c) Then <code>removeMin()</code>. What does it return? Write both again.</p>""",
 rubric=[(0.5, "(a) heap [D:1, B:3, C:8, A:5]"),
         (0.5, "(a) where {D→0, B→1, C→2, A→3}"),
         (0.5, "(b) C swims past D: heap [C:0, B:3, D:1, A:5]; where {C→0, B→1, D→2, A→3}"),
         (0.5, "(c) Returns C"),
         (0.5, "(c) A moves to the root and sinks toward the smaller child D: heap [D:1, B:3, A:5]"),
         (0.5, "(c) where {D→0, B→1, A→2}, with C removed")],
 pen=[(-0.25, "A where map that doesn't match the array (an index left stale after a swap). Apply once")],
 ref_html="""<pre class="show">insert A:5  [A5]
insert B:3  [A5, B3] → B swims: [B3, A5]
insert C:8  [B3, A5, C8]
insert D:1  [B3, A5, C8, D1] → swap with A: [B3, D1, C8, A5] → swap with B: [D1, B3, C8, A5]
(a) where: D→0 B→1 C→2 A→3
(b) C:0 at index 2, parent D:1 → swap: [C0, B3, D1, A5]   where C→0 B→1 D→2 A→3
(c) swap root with last: [A5, B3, D1, C0], remove C, size 3: [A5, B3, D1]
    sink A: children B3, D1 → D1 smaller → swap: [D1, B3, A5]
    returns C;  where D→0 B→1 A→2</pre>"""),

dict(id="Q3", pts=3, kind="text",
 prompt="""<p>The course's open-addressing map: linear probing, Integer keys hash to themselves, 7 slots, tombstones (†). After storing a new key, if <code>used &gt; m/2</code> it rehashes: to <b>17</b> slots if also <code>size &gt; m/2</code>, otherwise at the same size. A rehash reinserts the live entries in old-slot order and drops tombstones.</p>
<p>From empty: <code>put 10, put 3, put 17, remove 3</code>.</p>
<p>(a) Write the table (<code>slot:key</code>) with <code>size</code> and <code>used</code>. (b) Then <code>put 24</code>: list the slots it probes, where it is stored, and <code>size</code>/<code>used</code>. (c) Then <code>put 31</code>: where is it stored before any rehash, and which kind of rehash (if any) follows? (d) Write the final table.</p>""",
 rubric=[(0.5, "(a) 3:10, 4:3†, 5:17; size 2, used 3"),
         (0.75, "(b) Probes 3, 4†, 5, 6 (empty); stored in slot 4, the first tombstone; size 3, used 3"),
         (0.5, "(c) Stored in slot 6 (probes 3, 4, 5, 6); size 4, used 4"),
         (0.5, "(c) used 4 &gt; 3.5 and size 4 &gt; 3.5: grows to 17"),
         (0.75, "(d) Reinserts 10, 24, 17, 31: final 0:17, 7:24, 10:10, 14:31")],
 pen=[(-0.25, "Stores at the tombstone without probing on to the empty slot, or treats a tombstone as empty when searching. Apply once")],
 ref_html="""<pre class="show">put 10 → 3     put 3 → 3 taken → 4     put 17 → 3, 4 → 5
remove 3 → 4 = 3†
(a) 3:10  4:3†  5:17      size 2, used 3
(b) put 24 (24 % 7 = 3): 3 (10), 4† (remember), 5 (17), 6 empty → not present → store at 4
    size 3, used 3 (no change: the tombstone slot was already counted)
(c) put 31 (31 % 7 = 3): 3, 4, 5 taken, 6 empty → store at 6; size 4, used 4
    used 4 &gt; 3.5 and size 4 &gt; 3.5 → grow to 17
(d) old-slot order: 3:10 → 10,  4:24 → 7,  5:17 → 0,  6:31 → 14
    final m = 17:  0:17  7:24  10:10  14:31     size 4, used 4</pre>"""),

dict(id="Q4", pts=3, kind="text",
 prompt="""<p>Give the running time, with a few words of reason. Say whether it is worst case or expected where that matters.</p>
<ol type="a">
<li>Building a heap from n items with bottom-up heapify, versus with n calls to <code>insert</code></li>
<li>Finding the <b>largest</b> value in a min-heap of n values</li>
<li><code>changePriority</code> in an indexed priority queue, and in a plain heap with no index map</li>
<li><code>get</code> in an open-addressing map whose load factor stays at most 1/2</li>
<li><code>peek</code> (the best value without removing it) in a binary heap</li>
<li>A full <code>rehash</code> of a separate-chaining map with n keys and m buckets</li>
</ol>""",
 rubric=[(0.5, "(a) Heapify O(n): most nodes are near the bottom and sink only a little. n inserts: O(n log n)"),
         (0.5, "(b) O(n): the max is in one of about n/2 leaves, and the heap order says nothing about which"),
         (0.5, "(c) O(log n) with the map (O(1) lookup, then one swim or sink). Without it O(n) to find the item first"),
         (0.5, "(d) O(1) expected; O(n) worst case when everything clusters"),
         (0.5, "(e) O(1) worst case: it's <code>heap[0]</code>"),
         (0.5, "(f) O(n + m): every bucket is visited and every node moved once")],
 pen=[(-0.125, "Bounds given without any reasons. Apply once")]),

dict(id="Q5", pts=3, kind="text",
 prompt="""<pre class="show">public class Student {
  private String name;
  private int id;
  @Override
  public boolean equals(Object o) {
    if (!(o instanceof Student)) return false;
    return id == ((Student) o).id;        // students are equal when their ids are
  }
}</pre>
<p>For each <code>hashCode</code> below, say whether it is <b>legal</b> (keeps the equals/hashCode contract) and, if legal, whether it is a <b>good</b> choice. One sentence each.</p>
<ol type="i">
<li><code>return id;</code></li>
<li><code>return name.hashCode();</code></li>
<li><code>return id % 10;</code></li>
<li><code>return id + name.length();</code></li>
<li><code>return (int) (Math.random() * 1000);</code></li>
</ol>""",
 rubric=[(0.5, "(i) Legal and good: equal ids give equal codes, and different ids usually differ"),
         (0.5, "(ii) Illegal: two Students with the same id but different names are equal yet get different codes"),
         (0.75, "(iii) Legal (equal ids → equal codes) but poor: only 10 possible codes, so at most 10 buckets are ever used"),
         (0.5, "(iv) Illegal: uses name, which equals ignores"),
         (0.75, "(v) Illegal: the same object gets a different code each call, so even get on the stored object fails")],
 pen=[(-0.25, "Calls a hashCode illegal only because unequal objects can collide. Apply once")],
 ref_html="""<p>The rule: <code>a.equals(b)</code> ⇒ <code>a.hashCode() == b.hashCode()</code>. So hashCode may only use fields that equals uses (here only <code>id</code>), and must give the same answer every time. Collisions between <i>unequal</i> objects are always legal; they only cost time.</p>"""),

dict(id="Q6", pts=5, kind="code", ref=["Q6"],
 prompt="""<p>Implement <code>put</code> for the separate-chaining map. If the key is already there, replace its value and return the old one. Otherwise add a new node at the <b>head</b> of its chain, return <code>null</code>, and if the load factor <code>size / buckets.length</code> is now above 0.75, call the GIVEN <code>rehash()</code>. Null keys or values throw <code>IllegalArgumentException</code>.</p>""",
 stub="""public class HashMap<K, V> implements Map<K, V> {
  private static class Node<K, V> {
    K key; V value; Node<K, V> next;
    Node(K key, V value) { this.key = key; this.value = value; }
  }
  private Node<K, V>[] buckets;
  private int size;

  // GIVEN: private int indexFor(K key)   floorMod(key.hashCode(), buckets.length)
  // GIVEN: private void rehash()         grows the table and moves every node

  public V put(K key, V value) {
    // TODO
  }
}""",
 rubric=[(0.5, "Throws <code>IllegalArgumentException</code> for a null key or value"),
         (0.5, "Computes the bucket with <code>indexFor(key)</code>"),
         (0.75, "Walks the whole chain looking for the key, with <code>equals</code>"),
         (0.75, "On a match: replaces the value and returns the old one, without changing size or rehashing"),
         (0.75, "Creates a new node and links it at the head: <code>n.next = buckets[i]; buckets[i] = n;</code>"),
         (0.5, "Increments size for a new key"),
         (0.75, "Checks the load factor <b>after</b> adding, with floating-point math (e.g. <code>size &gt; 0.75 * buckets.length</code>)"),
         (0.5, "Calls <code>rehash()</code> only when over the limit, then returns null")],
 pen=[(-0.5, "Integer division in the load-factor check (<code>size / buckets.length &gt; 0.75</code> is never true)"),
      (-0.5, "Adds a duplicate node when the key is already present"),
      (-0.25, "Compares keys with <code>==</code>"),
      SYN],
 note="""<p><code>size / buckets.length</code> with two ints is integer division: 6 / 7 is 0. Multiply instead (<code>size &gt; 0.75 * buckets.length</code>) or cast one side to double.</p>"""),

dict(id="Q7", pts=4, kind="code", ref=["Q7"],
 prompt="""<p>Implement <code>insert</code> and <code>swim</code> for the array-based min-heap (root at index 0). When the array is full, double its length first. Null values throw <code>IllegalArgumentException</code>.</p>""",
 stub="""public class ArrayHeap<T extends Comparable<T>> {
  private T[] heap;   // heap[0..size-1], root at 0
  private int size;

  // GIVEN: private void swap(int i, int j)

  public void insert(T x) {
    // TODO
  }

  private void swim(int i) {
    // TODO
  }
}""",
 rubric=[(0.25, "Throws <code>IllegalArgumentException</code> for null"),
         (0.5, "Grows when <code>size == heap.length</code>, e.g. <code>heap = Arrays.copyOf(heap, 2 * heap.length)</code>"),
         (0.5, "Puts x at index <code>size</code>, then increments size"),
         (0.25, "Calls <code>swim</code> on the new value's index"),
         (0.5, "swim: parent index <code>(i - 1) / 2</code>"),
         (0.5, "swim: stops at the root (<code>i &gt; 0</code>)"),
         (0.75, "swim: swaps only while the value is <b>smaller</b> than its parent, using <code>compareTo</code>"),
         (0.75, "swim: continues from the parent's index")],
 pen=[(-0.5, "Compares with <code>&lt;</code>/<code>&gt;</code> on generic values"),
      (-0.25, "Creates a generic array with <code>new T[...]</code>"),
      SYN]),

dict(id="Q8", pts=4, kind="code", ref=["Q8"],
 prompt="""<p>Write a static method that returns <code>true</code> if <code>a[0..size-1]</code> is a valid min-heap (root at 0) and <code>false</code> otherwise. Ignore anything at index <code>size</code> or later. Throw <code>IllegalArgumentException</code> if <code>a</code> is null or <code>size</code> is outside 0..a.length. Run in O(size).</p>""",
 stub="""public static <T extends Comparable<T>> boolean isMinHeap(T[] a, int size) {
  // TODO
}""",
 rubric=[(0.25, "Throws <code>IllegalArgumentException</code> for null or a bad size"),
         (0.75, "Checks <b>every</b> parent-child pair (e.g. every i from 1 to size - 1 against its parent)"),
         (0.75, "Correct index math for 0-indexed heaps: parent <code>(i - 1) / 2</code>, or children <code>2i + 1</code>, <code>2i + 2</code>"),
         (0.75, "Never reads beyond <code>size - 1</code> (checks a child index against size before using it)"),
         (0.5, "Uses <code>compareTo</code>; equal values are allowed"),
         (0.5, "Returns false as soon as one pair is out of order"),
         (0.5, "Returns true otherwise, including size 0 and 1")],
 pen=[(-0.5, "Only compares siblings, or only checks the root"),
      (-0.25, "Uses <code>a.length</code> instead of <code>size</code> as the bound"),
      SYN],
 note="""<p>Checking each child against its parent covers every edge of the tree exactly once, with no bounds trouble: <code>i</code> runs over existing children, and every child has a parent.</p>"""),

dict(id="Q9", pts=5, kind="code", ref=["Q9"],
 prompt="""<p>Implement <code>insert</code> and <code>removeMin</code> for the indexed min-priority queue. Keep <code>where</code> exactly in sync with the array: it must hold every item in the queue, with its current index, and nothing else. <code>insert</code> throws <code>IllegalArgumentException</code> for a null item or one already in the queue (assume the array has room). <code>removeMin</code> throws <code>NoSuchElementException</code> when empty.</p>""",
 stub="""public class IndexedMinPQ<T> {
  private static class Entry<T> {
    T item; int priority;
    Entry(T item, int priority) { this.item = item; this.priority = priority; }
  }
  private Entry<T>[] heap;              // heap[0..size-1], root at 0
  private int size;
  private Map<T, Integer> where;        // item -> its index in heap

  // GIVEN: private void swap(int i, int j)   swaps entries AND updates where for both
  // GIVEN: private void swim(int i)
  // GIVEN: private void sink(int i)

  public void insert(T item, int priority) {
    // TODO
  }

  public T removeMin() {
    // TODO
  }
}""",
 rubric=[(0.5, "insert throws for a null item or one already present (<code>where.containsKey(item)</code>)"),
         (0.5, "insert puts a new Entry at index <code>size</code>"),
         (0.75, "insert records <code>where.put(item, size)</code> before swimming"),
         (0.5, "insert increments size and calls <code>swim</code> on the new index"),
         (0.25, "removeMin throws <code>NoSuchElementException</code> when empty"),
         (0.5, "removeMin saves <code>heap[0].item</code>"),
         (0.5, "removeMin swaps the root with the last entry"),
         (0.75, "removeMin removes the item from <code>where</code> <b>after</b> the swap"),
         (0.75, "removeMin nulls the last slot, decrements size, and sinks the root only if the queue isn't empty, then returns the item")],
 pen=[(-0.5, "Removes from where before swap, so swap puts the removed item back"),
      (-0.5, "Rebuilds or scans where (O(n))"),
      SYN],
 note="""<p>The GIVEN swap writes <i>both</i> items' indices into <code>where</code>, so anything you remove from the map before a swap that touches it comes right back. Rule of thumb: finish moving entries, then delete the map entry.</p>"""),

dict(id="Q10", pts=5, kind="code", ref=["Q10"],
 prompt="""<p>Return the k-th <b>smallest</b> value in <code>a</code> (k = 1 is the minimum; duplicates count separately). It must run in O(n log k) time with O(k) extra space, using a <code>java.util.PriorityQueue</code> that never holds more than k values. Throw <code>IllegalArgumentException</code> if <code>a</code> is null or k is not in 1..a.length.</p>""",
 stub="""// You may use java.util.PriorityQueue, Collections
public static int kthSmallest(int[] a, int k) {
  // TODO
}""",
 rubric=[(0.25, "Throws <code>IllegalArgumentException</code> for null or k outside 1..a.length"),
         (1, "Uses a <b>max</b>-heap, e.g. <code>new PriorityQueue&lt;&gt;(Collections.reverseOrder())</code>"),
         (0.75, "Adds freely while it holds fewer than k values"),
         (1, "Once full, replaces the root only when <code>x &lt; peek()</code>"),
         (0.75, "Never holds more than k values"),
         (1.25, "Returns <code>peek()</code> at the end: the largest of the k smallest")],
 pen=[(-1, "Puts all n values into the queue, or sorts the array"),
      (-0.5, "Uses a min-heap of size k (keeps the k largest instead)"),
      (-0.5, "Removes the root unconditionally once full"),
      SYN],
 note="""<p>Mirror image of top k: to keep the k <i>smallest</i>, the value you'd throw out next is the <i>largest</i> one kept, so it sits at the root of a max-heap. When the loop ends, that root is exactly the k-th smallest.</p>"""),
]

DRILLS = []
