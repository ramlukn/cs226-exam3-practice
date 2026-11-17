# Question specs for the Test 3 practice exam. Reference code comes from java/*.java <REF id> blocks.
SYN = (-0.125, "Minor logic or major syntax errors showing lack of understanding")

EXAM = [
dict(id="Q1", pts=3, kind="text",
 prompt="""<p>A binary <b>min</b>-heap is stored in an array with the root at index 0 (children of i at 2i + 1 and 2i + 2). Starting from empty:</p>
<p>(a) Insert 6, 4, 9, 2, 7, 1 in that order. Write the array after <b>each</b> insert. (b) Then call <code>remove()</code> twice. Write the value returned and the array after each call.</p>""",
 rubric=[(0.25, "After 6, 4: [4, 6]"),
         (0.25, "After 9: [4, 6, 9]"),
         (0.5, "After 2: [2, 4, 9, 6] (2 swims from index 3 past 6 and 4)"),
         (0.25, "After 7: [2, 4, 9, 6, 7]"),
         (0.5, "After 1: [1, 4, 2, 6, 7, 9] (1 swims from index 5 past 9 and 2)"),
         (0.5, "First remove returns 1, array [2, 4, 9, 6, 7]"),
         (0.75, "Second remove returns 2, array [4, 6, 9, 7]")],
 pen=[(-0.25, "Sinks toward the larger child, or swims by comparing with a sibling instead of the parent. Apply once")],
 ref_html="""<pre class="show">insert 6: [6]
insert 4: [4, 6]                 4 &lt; parent 6 → swap
insert 9: [4, 6, 9]
insert 2: [2, 4, 9, 6]           at 3, parent 1 (6) → swap; at 1, parent 0 (4) → swap
insert 7: [2, 4, 9, 6, 7]        parent 1 (4) is smaller → stays
insert 1: [1, 4, 2, 6, 7, 9]     at 5, parent 2 (9) → swap; at 2, parent 0 (2) → swap

remove → 1:  last (9) to root: [9, 4, 2, 6, 7]
             children 4, 2 → smaller is 2 → swap: [2, 4, 9, 6, 7]   (9 at index 2 is a leaf)
remove → 2:  last (7) to root: [7, 4, 9, 6]
             children 4, 9 → swap with 4: [4, 7, 9, 6]
             child of index 1 is 6 &lt; 7 → swap: [4, 6, 9, 7]</pre>"""),

dict(id="Q2", pts=3, kind="text",
 prompt="""<p>In-place heapsort on <code>a = [3, 9, 2, 7, 5, 8, 1]</code>, using a <b>max</b>-heap with the root at index 0.</p>
<p>(a) Bottom-up heapify sinks indices from <code>n/2 - 1</code> down to 0. Which indices does it sink, and what is the array after each one? (b) Then do the first <b>two</b> rounds of the sort phase (swap the root with the last heap slot, shrink the heap by one, sink the root). Write the array after each round and mark which part is sorted. (c) Why does ascending order use a <b>max</b>-heap?</p>""",
 rubric=[(0.25, "(a) Sinks indices 2, 1, 0 (n/2 - 1 = 2)"),
         (0.5, "(a) After index 2: [3, 9, 8, 7, 5, 2, 1]; index 1 changes nothing (9 ≥ 7, 5)"),
         (0.5, "(a) After index 0: [9, 7, 8, 3, 5, 2, 1] (3 sinks past 9, then past 7)"),
         (0.5, "(b) Round 1: [8, 7, 2, 3, 5, 1 | 9]"),
         (0.75, "(b) Round 2: [7, 5, 2, 3, 1 | 8, 9]"),
         (0.5, "(c) Each round puts the largest remaining value at the end of the unsorted part, so the sorted part grows from the right in ascending order")],
 pen=[(-0.25, "Sinks with the full array length after a swap, pulling sorted values back into the heap")],
 ref_html="""<pre class="show">heapify, n = 7, start at 7/2 - 1 = 2
  i=2: 2 vs children 8, 1 → swap with 8   [3, 9, 8, 7, 5, 2, 1]
  i=1: 9 vs children 7, 5 → stays          [3, 9, 8, 7, 5, 2, 1]
  i=0: 3 vs 9, 8 → swap with 9             [9, 3, 8, 7, 5, 2, 1]
       3 vs 7, 5 → swap with 7             [9, 7, 8, 3, 5, 2, 1]
round 1: swap 9 ↔ 1 → [1, 7, 8, 3, 5, 2 | 9], sink 1 in size 6
         1 vs 7, 8 → 8; then 1 vs 2 → 2    [8, 7, 2, 3, 5, 1 | 9]
round 2: swap 8 ↔ 1 → [1, 7, 2, 3, 5 | 8, 9], sink 1 in size 5
         1 vs 7, 2 → 7; then 1 vs 3, 5 → 5 [7, 5, 2, 3, 1 | 8, 9]</pre>
<p>(c) The root of a max-heap is the largest value left, and the free slot after each swap is the end of the unsorted part, so values land in their final ascending positions from right to left.</p>"""),

dict(id="Q3", pts=3, kind="text",
 prompt="""<p>The course's separate-chaining map: Integer keys hash to themselves, index = <code>key % m</code>, new keys go at the <b>head</b> of their chain, and m starts at 7. After inserting a new key, if <code>size / m &gt; 0.75</code> it rehashes to the next prime, 17, by walking the old buckets from 0 upward, each chain from head to tail, and inserting each node at the head of its new chain.</p>
<p>Insert 8, 15, 3, 22, 12, 29 in that order. (a) Draw the buckets (as <code>i: a → b → …</code>) just <b>before</b> 29 is inserted. (b) Does inserting 29 cause a rehash? Show the check. (c) Draw the final table. (d) After that, how many key comparisons does <code>get(29)</code> make?</p>""",
 rubric=[(0.75, "(a) 1: 22 → 15 → 8, 3: 3, 5: 12 (newest at the head)"),
         (0.5, "(b) Yes: size 6, 6/7 ≈ 0.86 &gt; 0.75 (after 5 keys it was 5/7 ≈ 0.71, no rehash)"),
         (0.5, "(c) Reinsert order is 29, 22, 15, 8, 3, 12 (bucket 1 head to tail, then 3, then 5)"),
         (0.75, "(c) Final m = 17: 3: 3, 5: 22, 8: 8, 12: 12 → 29, 15: 15"),
         (0.5, "(d) 2: 12 is at the head of bucket 12, then 29")],
 pen=[(-0.25, "Inserts at the tail instead of the head. Apply once")],
 ref_html="""<pre class="show">8 % 7 = 1   15 % 7 = 1   3 % 7 = 3   22 % 7 = 1   12 % 7 = 5   29 % 7 = 1
(a) before 29, size 5 (5/7 = 0.71):
    1: 22 → 15 → 8     3: 3     5: 12
(b) insert 29 → 1: 29 → 22 → 15 → 8; size 6, 6/7 = 0.86 &gt; 0.75 → rehash to 17
(c) walk: 29, 22, 15, 8 (bucket 1), 3, 12
    29 % 17 = 12   22 % 17 = 5   15 % 17 = 15   8 % 17 = 8   3   12 % 17 = 12
    3: 3     5: 22     8: 8     12: 12 → 29     15: 15
(d) get(29): bucket 12, compare with 12, then 29 → 2 comparisons</pre>"""),

dict(id="Q4", pts=3, kind="text",
 prompt="""<p>The course's open-addressing map: linear probing, Integer keys hash to themselves, <b>11</b> slots, tombstones (†). It rehashes only when <code>used &gt; m/2</code>, which won't happen here. Starting from empty: <code>put 4, put 15, put 26, put 7, remove 15</code>.</p>
<p>(a) Write the table as <code>slot:key</code> pairs with <code>size</code> and <code>used</code>. (b) List the slots <code>get(26)</code> probes, and say why it can't stop at slot 5. (c) List the slots <code>get(37)</code> probes, and what it returns. (d) Then <code>put 37</code>: which slot does it go in, and what are <code>size</code> and <code>used</code> now? (e) Suppose <code>remove</code> had set slot 5 to <code>null</code> instead of a tombstone. What would <code>get(26)</code> return, and why?</p>""",
 rubric=[(0.5, "(a) 4:4, 5:15†, 6:26, 7:7; size 3, used 4"),
         (0.5, "(b) 4, 5†, 6 (found). A tombstone means \"something was here\", so a key further along the probe path may still exist"),
         (0.75, "(c) 4, 5†, 6, 7, 8 (empty) → null. Only an empty slot ends the search"),
         (0.75, "(d) Slot 5, the first tombstone (after probing on to the empty slot 8 to make sure 37 isn't present); size 4, used 4"),
         (0.5, "(e) null (wrong): the search for 26 would stop at the empty slot 5 before reaching slot 6")],
 pen=[(-0.25, "Gives keys without slot numbers, or treats a tombstone as the end of a search. Apply once")],
 ref_html="""<pre class="show">put 4 → 4    put 15 → 15 % 11 = 4, taken → 5    put 26 → 4, 5 → 6    put 7 → 7
remove 15 → 5 becomes 15†
(a) 4:4  5:15†  6:26  7:7      size 3, used 4
(b) get 26: 4 (4), 5 (†, keep going), 6 (26) → found
(c) get 37: 37 % 11 = 4 → 4, 5†, 6, 7, 8 empty → null
(d) put 37: same path; first tombstone was 5, ends at empty 8 (not present) → store at 5
    size 4, used 4 (reusing a tombstone doesn't change used)
(e) get 26 would probe 4, then 5 = null → stop → null, though 26 is at 6</pre>"""),

dict(id="Q5", pts=3, kind="text",
 prompt="""<pre class="show">public class Point {
  private final int x, y;
  public Point(int x, int y) { this.x = x; this.y = y; }
  @Override
  public boolean equals(Object o) {
    if (!(o instanceof Point)) return false;
    Point p = (Point) o;
    return x == p.x &amp;&amp; y == p.y;
  }
  // no hashCode
}</pre>
<p>(a) After <code>map.put(new Point(1, 2), "A")</code> on a <code>java.util.HashMap</code>, what does <code>map.get(new Point(1, 2))</code> most likely return? Explain. (b) State the rule this class breaks. (c) Write a good <code>hashCode</code> for <code>Point</code>. (d) A classmate writes <code>return 7;</code>. Is it correct? What does it do to <code>get</code>'s running time? (e) Another writes <code>return x + y;</code>. Give two unequal points that collide. Does that make the map return wrong answers?</p>""",
 rubric=[(0.5, "(a) null: the default hashCode is based on object identity, so the two equal points almost certainly land in different buckets and get never calls equals on the stored one"),
         (0.5, "(b) Equal objects must have equal hash codes (override hashCode whenever you override equals)"),
         (0.75, "(c) Combines both fields, e.g. <code>31 * x + y</code> or <code>Objects.hash(x, y)</code>, using only the fields equals uses"),
         (0.75, "(d) Correct (equal points get equal codes) but every key collides into one bucket: get becomes O(n)"),
         (0.5, "(e) e.g. (1, 2) and (2, 1). Still correct: collisions only cost time, because equals decides matches")],
 pen=[(-0.25, "Says a collision makes get return the wrong value")],
 ref_html="""<pre class="show">@Override
public int hashCode() {
  return 31 * x + y;        // or Objects.hash(x, y)
}</pre>
<p>The contract only goes one way: <code>a.equals(b)</code> ⇒ <code>a.hashCode() == b.hashCode()</code>. Unequal objects may share a code; that is a collision, which the map handles with equals. A constant hashCode keeps the rule but turns the table into one long chain.</p>"""),

dict(id="Q6", pts=5, kind="code", ref=["Q6"],
 prompt="""<p>Implement <code>get</code> and <code>remove</code> for the course's open-addressing map (linear probing, tombstones), writing the probe loop yourself in each. <code>get</code> returns the value or <code>null</code>. <code>remove</code> returns the removed value or <code>null</code> if the key wasn't there. Keep <code>size</code> and <code>used</code> correct. Null keys throw <code>IllegalArgumentException</code>.</p>""",
 stub="""public class OpenAddressingMap<K, V> implements Map<K, V> {
  private static class Entry<K, V> {
    K key; V value; boolean deleted;   // deleted == true means tombstone
  }
  private Entry<K, V>[] slots;
  private int size;   // live entries
  private int used;   // live entries + tombstones

  // GIVEN: private int indexFor(K key)   floorMod(key.hashCode(), slots.length)

  public V get(K key) {
    // TODO
  }

  public V remove(K key) {
    // TODO
  }
}""",
 rubric=[(0.25, "Both throw <code>IllegalArgumentException</code> for a null key"),
         (0.5, "Both start at <code>indexFor(key)</code>"),
         (0.75, "Both loop until an empty (null) slot, not until the first tombstone"),
         (0.75, "Both skip tombstones when matching: <code>!slots[i].deleted &amp;&amp; slots[i].key.equals(key)</code>"),
         (0.5, "Both step with <code>i = (i + 1) % slots.length</code>"),
         (0.5, "get returns the value on a match, null after the loop"),
         (0.75, "remove marks the entry <code>deleted = true</code> (doesn't set the slot to null)"),
         (0.5, "remove decrements <code>size</code> and leaves <code>used</code> unchanged"),
         (0.5, "remove returns the old value, or null if not found")],
 pen=[(-1, "remove sets the slot to null, breaking the search for keys further along"),
      (-0.5, "Stops searching at a tombstone"),
      (-0.25, "Compares keys with <code>==</code>"),
      SYN],
 note="""<p><code>used</code> counts slots that aren't null. A tombstone is still not null, so removing a key changes <code>size</code> but not <code>used</code>. Only a rehash clears tombstones.</p>"""),

dict(id="Q7", pts=4, kind="code", ref=["Q7"],
 prompt="""<p>Implement <code>remove</code> for the separate-chaining map. Unlink the key's node from its chain and return its value, or return <code>null</code> if the key isn't there. Handle a key at the head of the chain, in the middle, and at the end. Null keys throw <code>IllegalArgumentException</code>.</p>""",
 stub="""public class HashMap<K, V> implements Map<K, V> {
  private static class Node<K, V> {
    K key; V value; Node<K, V> next;
  }
  private Node<K, V>[] buckets;
  private int size;

  // GIVEN: private int indexFor(K key)   floorMod(key.hashCode(), buckets.length)

  public V remove(K key) {
    // TODO
  }
}""",
 rubric=[(0.25, "Throws <code>IllegalArgumentException</code> for a null key"),
         (0.5, "Finds the bucket with <code>indexFor(key)</code>"),
         (0.75, "Walks the chain keeping a <code>prev</code> pointer (or checks <code>curr.next</code> ahead)"),
         (0.5, "Matches with <code>equals</code>"),
         (0.75, "Head case: <code>buckets[i] = curr.next</code>"),
         (0.5, "Middle or end: <code>prev.next = curr.next</code>"),
         (0.5, "Decrements size only when a node is removed"),
         (0.25, "Returns the removed value, or null when not found")],
 pen=[(-0.5, "Doesn't handle the head separately, so removing the first node either crashes on a null prev or leaves it in place"),
      (-0.25, "Compares keys with <code>==</code>"),
      SYN]),

dict(id="Q8", pts=4, kind="code", ref=["Q8"],
 prompt="""<p>Implement <code>remove()</code> for the array-based <b>min</b>-heap (root at index 0): remove and return the smallest value. Write <code>sink</code> too. Throw <code>NoSuchElementException</code> if the heap is empty, and don't leave a stale reference in the array.</p>""",
 stub="""public class ArrayHeap<T extends Comparable<T>> {
  private T[] heap;   // heap[0..size-1], root at 0
  private int size;

  // GIVEN: private void swap(int i, int j)

  public T remove() {
    // TODO
  }

  private void sink(int i) {
    // TODO
  }
}""",
 rubric=[(0.25, "Throws <code>NoSuchElementException</code> when <code>size == 0</code>"),
         (0.25, "Saves <code>heap[0]</code> to return"),
         (0.5, "Moves the last value to the root, nulls the old last slot, decrements size"),
         (0.25, "Calls <code>sink(0)</code> and returns the saved value"),
         (0.5, "sink loops while i has a left child: <code>2 * i + 1 &lt; size</code>"),
         (0.75, "Picks the <b>smaller</b> child, checking <code>2 * i + 2 &lt; size</code> before using the right one"),
         (0.75, "Stops when <code>heap[i]</code> ≤ that child, otherwise swaps"),
         (0.75, "Continues from the child's index (<code>i = c</code>)")],
 pen=[(-0.5, "Compares with <code>&lt;</code>/<code>&gt;</code> on objects instead of <code>compareTo</code>"),
      (-0.25, "Uses <code>heap.length</code> instead of <code>size</code> as the bound"),
      SYN]),

dict(id="Q9", pts=5, kind="code", ref=["Q9"],
 prompt="""<p>The indexed (adaptive) min-priority queue keeps <code>where</code>, a map from each item to its index in the heap array. Implement <code>remove(item)</code>, which removes <b>any</b> item (not just the minimum) in O(log n) and keeps <code>where</code> correct. Throw <code>IllegalArgumentException</code> if the item isn't in the queue.</p>""",
 stub="""public class IndexedMinPQ<T> {
  private static class Entry<T> {
    T item; int priority;
  }
  private Entry<T>[] heap;              // heap[0..size-1], root at 0
  private int size;
  private Map<T, Integer> where;        // item -> its index in heap

  // GIVEN: private void swap(int i, int j)   swaps entries AND updates where for both
  // GIVEN: private void swim(int i)
  // GIVEN: private void sink(int i)

  public void remove(T item) {
    // TODO
  }
}""",
 rubric=[(0.5, "Looks up the index with <code>where.get(item)</code>"),
         (0.25, "Throws <code>IllegalArgumentException</code> when it isn't there"),
         (0.75, "Swaps the item's slot with the last slot (<code>size - 1</code>)"),
         (0.75, "Removes the item from <code>where</code>"),
         (0.5, "Nulls the old last slot and decrements size"),
         (0.75, "Skips the fix-up when the removed item was in the last slot"),
         (1, "Restores order at index i with <b>both</b> <code>swim(i)</code> and <code>sink(i)</code> (the moved entry may need to go either way)"),
         (0.5, "Uses the GIVEN swap so the moved entry's map index is updated")],
 pen=[(-0.5, "Only sinks (or only swims) after the move"),
      (-0.5, "Searches the array for the item instead of using the map (O(n))"),
      (-0.25, "Leaves the removed item in <code>where</code>"),
      SYN],
 note="""<p>Unlike <code>removeMin</code>, the hole can be anywhere, so the last entry that fills it may be smaller than its new parent (needs swim) or larger than its new children (needs sink). Calling both is safe: at most one of them moves anything.</p>"""),

dict(id="Q10", pts=5, kind="code", ref=["Q10"],
 prompt="""<p>Return the <code>k</code> largest values of <code>a</code>, largest first (duplicates count separately). If <code>a</code> has fewer than k values, return all of them. It must run in O(n log k) time with O(k) extra space: use a <code>java.util.PriorityQueue</code> that never holds more than k values. Throw <code>IllegalArgumentException</code> if <code>a</code> is null or k is negative.</p>""",
 stub="""// You may use java.util.PriorityQueue, ArrayList, List, Collections
public static List<Integer> topK(int[] a, int k) {
  // TODO
}""",
 rubric=[(0.25, "Throws <code>IllegalArgumentException</code> for null or negative k"),
         (1, "Uses a <b>min</b>-heap (the default PriorityQueue): its root is the smallest of the current top k"),
         (0.75, "Adds freely while it holds fewer than k values"),
         (1, "Once full, adds x only if <code>x &gt; peek()</code>, removing the root first"),
         (0.75, "Never holds more than k values"),
         (0.5, "Handles k = 0 without crashing"),
         (0.75, "Empties the queue into a list and reverses it, so the largest is first")],
 pen=[(-1, "Puts all n values into the queue (O(n log n) time, O(n) space)"),
      (-0.5, "Uses a max-heap of size k, which throws away the largest values instead of the smallest"),
      (-0.5, "Sorts the whole array"),
      SYN],
 note="""<p>The counter-intuitive part: to keep the <i>largest</i> k you use a <i>min</i>-heap, because the value you may need to throw out next is the smallest of the ones you're keeping. Each of the n values costs at most one O(log k) remove and add.</p>"""),
]

DRILLS = []
