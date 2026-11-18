# Question specs for Test 3 Practice Exam 3. Reference code comes from java/*.java <REF id> blocks.
SYN = (-0.125, "Minor logic or major syntax errors showing lack of understanding")

EXAM = [
dict(id="Q1", pts=3, kind="text",
 prompt="""<p>A binary <b>max</b>-heap is stored in an array with the root at index 0. Starting from empty:</p>
<p>(a) Insert 3, 8, 5, 10, 1, 9 in that order. Write the array after <b>each</b> insert. (b) Then call <code>remove()</code> twice. Write the value returned and the array after each call.</p>""",
 rubric=[(0.25, "After 3, 8: [8, 3]"),
         (0.25, "After 5: [8, 3, 5]"),
         (0.5, "After 10: [10, 8, 5, 3] (10 swims past 3 and 8)"),
         (0.25, "After 1: [10, 8, 5, 3, 1]"),
         (0.5, "After 9: [10, 8, 9, 3, 1, 5] (9 swims past 5, stops under 10)"),
         (0.5, "First remove returns 10, array [9, 8, 5, 3, 1]"),
         (0.75, "Second remove returns 9, array [8, 3, 5, 1]")],
 pen=[(-0.25, "Sinks toward the smaller child (min-heap habit). Apply once")],
 ref_html="""<pre class="show">insert 3:  [3]
insert 8:  [8, 3]                 8 &gt; parent 3 → swap
insert 5:  [8, 3, 5]
insert 10: [10, 8, 5, 3]          at 3, parent 1 (3) → swap; at 1, parent 0 (8) → swap
insert 1:  [10, 8, 5, 3, 1]
insert 9:  [10, 8, 9, 3, 1, 5]    at 5, parent 2 (5) → swap; parent 0 (10) is bigger → stop

remove → 10: last (5) to root: [5, 8, 9, 3, 1]; children 8, 9 → larger 9 → [9, 8, 5, 3, 1]
remove → 9:  last (1) to root: [1, 8, 5, 3]; children 8, 5 → 8 → [8, 1, 5, 3]
             child of index 1 is 3 &gt; 1 → swap → [8, 3, 5, 1]</pre>"""),

dict(id="Q2", pts=3, kind="text",
 prompt="""<p>The course's separate-chaining map: 7 buckets, Integer keys hash to themselves, index = <code>Math.floorMod(key, 7)</code>, new keys at the <b>head</b> of the chain. No rehash happens here.</p>
<p>(a) Insert 9, -5, 16, -3, 4 in that order. Draw the buckets (<code>i: a → b → …</code>). (b) What does Java's <code>-5 % 7</code> evaluate to, and what would go wrong if the map used <code>%</code> instead of <code>floorMod</code>? (c) Then <code>remove(-5)</code> and <code>remove(4)</code>. For each, say whether it unlinks a head node or a later node, and draw the final buckets. (d) Then how many key comparisons does <code>get(9)</code> make?</p>""",
 rubric=[(0.5, "(a) floorMod values: 9 → 2, -5 → 2, 16 → 2, -3 → 4, 4 → 4"),
         (0.5, "(a) 2: 16 → -5 → 9, 4: 4 → -3"),
         (0.5, "(b) -5: <code>%</code> keeps the sign of the left side, so a negative hashCode gives a negative index and <code>buckets[-5]</code> throws ArrayIndexOutOfBoundsException"),
         (0.5, "(c) remove(-5) unlinks a middle node (16.next = 9); remove(4) unlinks the head (buckets[4] = -3)"),
         (0.5, "(c) Final: 2: 16 → 9, 4: -3"),
         (0.5, "(d) 2 (16, then 9)")],
 pen=[(-0.25, "Inserts at the tail instead of the head. Apply once")],
 ref_html="""<pre class="show">floorMod(9, 7) = 2    floorMod(-5, 7) = 2    floorMod(16, 7) = 2
floorMod(-3, 7) = 4   floorMod(4, 7) = 4
(a) 2: 16 → -5 → 9      4: 4 → -3
(b) -5 % 7 == -5 in Java → buckets[-5] → ArrayIndexOutOfBoundsException
    floorMod always returns 0..m-1
(c) remove(-5): prev = 16, so 16.next = 9          → 2: 16 → 9
    remove(4): it is the head, so buckets[4] = -3    → 4: -3
(d) get(9): bucket 2, compare 16, then 9 → 2</pre>"""),

dict(id="Q3", pts=3, kind="text",
 prompt="""<p>An open-addressing map with linear probing, <b>11</b> slots, Integer keys hashing to themselves, no removals and no rehash.</p>
<p>(a) Put 22, 33, 1, 13, 2 in that order. Write the table (<code>slot:key</code>) and the number of slots each put examines. (b) How many slots does <code>get(44)</code> examine, and what does it return? (c) Keys 1, 13 and 2 hash to different slots from 22 and 33, yet they still collide. Name this effect and explain it with this example. (d) Why does the course keep the table at most half full?</p>""",
 rubric=[(0.5, "(a) 0:22, 1:33, 2:1, 3:13, 4:2"),
         (0.5, "(a) Slots examined: 22 → 1, 33 → 2, 1 → 2, 13 → 2, 2 → 3"),
         (0.75, "(b) 44 hashes to 0: examines 0, 1, 2, 3, 4, 5 (empty) = 6 slots, returns null"),
         (0.75, "(c) Primary clustering: occupied slots form one run, and any key hashing anywhere into the run must probe to its end, which makes the run longer still"),
         (0.5, "(d) Clusters (and so probe lengths) grow quickly as the table fills; at load ≤ 1/2 the expected probes stay O(1)")],
 pen=[(-0.25, "Counts only the collisions, not the slot where the key is found or stored. Apply once")],
 ref_html="""<pre class="show">22 % 11 = 0 → 0                       (1 slot)
33 % 11 = 0 → 0 taken, 1              (2)
 1 % 11 = 1 → 1 taken, 2              (2)
13 % 11 = 2 → 2 taken, 3              (2)
 2 % 11 = 2 → 2, 3 taken, 4           (3)
(b) get 44: 0, 1, 2, 3, 4 hold other keys, 5 is empty → 6 slots → null</pre>
<p>(c) Slots 0–4 are one cluster. 1 and 13 never collided with their own home keys; they collided with keys that spilled over from slot 0. Every key that lands in the cluster extends it.</p>"""),

dict(id="Q4", pts=3, kind="text",
 prompt="""<p>About in-place heapsort (max-heap, root at 0, bottom-up heapify, then repeatedly swap the root with the end of the heap and sink):</p>
<p>(a) What is its worst-case running time? Account for both phases. (b) How much extra space does it use? (c) Is it stable? Show what it does to <code>[1a, 1b]</code> (two equal keys, a before b). (d) Sorting by adding everything to a <code>java.util.PriorityQueue</code> and removing it all is also O(n log n). What does in-place heapsort do better?</p>""",
 rubric=[(0.75, "(a) O(n log n): heapify is O(n), then n - 1 rounds of swap + sink, each O(log n)"),
         (0.5, "(b) O(1) extra: it rearranges the array itself"),
         (1, "(c) Not stable: heapify leaves [1a, 1b] (1b isn't larger); the first round swaps root and end → [1b, 1a], reversing the equal keys"),
         (0.75, "(d) Uses O(1) extra space instead of O(n) for the queue (and needs no copying back)")],
 pen=[(-0.25, "Says heapsort is O(n) because heapify is O(n)")]),

dict(id="Q5", pts=3, kind="text",
 prompt="""<pre class="show">public class Point {
  public int x, y;                       // NOT final
  // equals compares x and y; hashCode returns 31 * x + y
}

Point p = new Point(1, 2);
Map&lt;Point, String&gt; map = new HashMap&lt;&gt;();
map.put(p, "A");
p.x = 5;</pre>
<p>(a) What does <code>map.get(p)</code> most likely return? Explain using buckets. (b) What does <code>map.get(new Point(1, 2))</code> return? Explain. (c) What is <code>map.size()</code>, and can the entry still be reached with <code>get</code>? (d) Give two ways to avoid this.</p>""",
 rubric=[(0.75, "(a) null: p's hashCode is now 31·5 + 2 = 157, so get looks in a different bucket from where the entry was stored (31 + 2 = 33)"),
         (0.75, "(b) null: it hashes to the right bucket, but the stored key now equals (5, 2), so equals fails"),
         (0.5, "(c) 1: the entry is still in the table, but no key can reach it with get (only iteration finds it)"),
         (1, "(d) Make key fields final (immutable keys); or remove the entry before changing the key and put it back after")],
 pen=[(-0.25, "Says the map rehashes or updates the entry automatically when the key changes")]),

dict(id="Q6", pts=5, kind="code", ref=["Q6"],
 prompt="""<p>Implement <code>rehash(newCapacity)</code> for the course's open-addressing map (linear probing, tombstones). Move every <b>live</b> entry into a new array of the given length and drop the tombstones. Don't call <code>put</code>: write the probe yourself. Leave <code>size</code> and <code>used</code> correct.</p>""",
 stub="""public class OpenAddressingMap<K, V> implements Map<K, V> {
  private static class Entry<K, V> {
    K key; V value; boolean deleted;   // deleted == true means tombstone
  }
  private Entry<K, V>[] slots;
  private int size;   // live entries
  private int used;   // live entries + tombstones

  // GIVEN: private int indexFor(K key)   floorMod(key.hashCode(), slots.length)

  private void rehash(int newCapacity) {
    // TODO
  }
}""",
 rubric=[(0.5, "Keeps a reference to the old array"),
         (0.5, "Allocates the new array (e.g. <code>(Entry&lt;K, V&gt;[]) new Entry[newCapacity]</code>) and assigns it to <code>slots</code> before reinserting"),
         (0.5, "Visits every old slot"),
         (0.75, "Skips null slots <b>and</b> tombstones"),
         (0.75, "Computes each home slot with the <b>new</b> length (indexFor after slots is replaced)"),
         (0.75, "Probes forward with wraparound <code>(i + 1) % slots.length</code> to the first null slot"),
         (0.5, "Stores the entry there (reusing it is fine)"),
         (0.75, "Sets <code>used = size</code> and leaves size unchanged")],
 pen=[(-0.5, "Copies tombstones into the new table"),
      (-0.5, "Indexes with the old length"),
      (-0.25, "Calls put"),
      SYN],
 note="""<p>The new table has no tombstones and no duplicate keys, so the probe only has to find the first empty slot: no equals checks needed. After the rehash every non-null slot is live, which is why <code>used</code> becomes <code>size</code>.</p>"""),

dict(id="Q7", pts=4, kind="code", ref=["Q7"],
 prompt="""<p>Implement <code>rehash</code> for the separate-chaining map. It moves to the next prime in <code>PRIMES</code> (or <code>2m + 1</code> once the list runs out) and moves every <b>existing node</b> into its new bucket, inserting at the head. Don't create new nodes.</p>""",
 stub="""public class HashMap<K, V> implements Map<K, V> {
  private static class Node<K, V> {
    K key; V value; Node<K, V> next;
  }
  private static final int[] PRIMES = {7, 17, 37, 79, 163, 331, 673};
  private int primeIndex;          // buckets.length == PRIMES[primeIndex] while in range
  private Node<K, V>[] buckets;
  private int size;

  // GIVEN: private int indexFor(K key)   floorMod(key.hashCode(), buckets.length)

  private void rehash() {
    // TODO
  }
}""",
 rubric=[(0.5, "New capacity: <code>PRIMES[++primeIndex]</code> while in range, otherwise <code>2 * m + 1</code>"),
         (0.5, "Keeps a reference to the old array and allocates the new one before reinserting"),
         (0.5, "Visits every old bucket and every node in its chain"),
         (0.75, "Saves <code>curr.next</code> before relinking the node"),
         (0.75, "Computes the new bucket with the <b>new</b> length"),
         (0.75, "Inserts at the head of that new bucket: <code>curr.next = buckets[i]; buckets[i] = curr;</code>"),
         (0.25, "Leaves <code>size</code> unchanged")],
 pen=[(-0.5, "Creates new nodes (or calls put) instead of moving the existing ones"),
      (-0.25, "Indexes with the old length"),
      SYN],
 note="""<p>Two classic bugs: using <code>PRIMES[primeIndex++]</code> (that's the <i>current</i> size), and setting <code>buckets[i] = curr</code> without <code>curr.next = buckets[i]</code> (the node drags its old chain along).</p>"""),

dict(id="Q8", pts=4, kind="code", ref=["Q8"],
 prompt="""<p>Implement in-place heapsort: sort <code>a</code> into ascending order using O(1) extra space and O(n log n) time. Write the helper <code>sink(a, i, n)</code> for a <b>max</b>-heap stored in <code>a[0..n-1]</code> (children of i at 2i + 1 and 2i + 2), then <code>heapSort</code> using it.</p>""",
 stub="""public static void heapSort(int[] a) {
  // TODO
}

private static void sink(int[] a, int i, int n) {
  // TODO: max-heap in a[0..n-1]
}""",
 rubric=[(0.25, "sink loops while i has a child: <code>2 * i + 1 &lt; n</code> (bounded by n, not a.length)"),
         (0.5, "sink picks the <b>larger</b> child, checking the right child exists"),
         (0.5, "sink stops when <code>a[i]</code> is at least that child, otherwise swaps and continues from the child"),
         (0.75, "Builds the max-heap bottom-up: sink from <code>n / 2 - 1</code> down to 0"),
         (0.5, "Loops <code>end</code> from n - 1 down to 1"),
         (0.75, "Swaps <code>a[0]</code> (the max) with <code>a[end]</code>"),
         (0.75, "Then sinks the root within the shrunk heap: <code>sink(a, 0, end)</code>")],
 pen=[(-0.5, "Uses a min-heap, or a second array or PriorityQueue (not in place)"),
      (-0.5, "Sinks with the full length after each swap, pulling sorted values back into the heap"),
      SYN],
 note="""<p>After each swap, <code>a[end..n-1]</code> is sorted and must stay out of the heap, which is why sink takes the heap size as a parameter.</p>"""),

dict(id="Q9", pts=5, kind="code", ref=["Q9"],
 prompt="""<p>An <b>indexed</b> min-priority queue keeps <code>where</code>, a map from each item to its index in the heap array. Implement <code>swap</code>, which every swim and sink step uses, and <code>changePriority</code>, which gives an item already in the queue a new priority and restores the heap order in O(log n). Throw <code>IllegalArgumentException</code> if the item isn't in the queue.</p>""",
 stub="""public class IndexedMinPQ<T> {
  private static class Entry<T> {
    T item; int priority;
  }
  private Entry<T>[] heap;              // heap[0..size-1], root at 0
  private int size;
  private Map<T, Integer> where;        // item -> its index in heap

  // GIVEN: private void swim(int i)    uses swap
  // GIVEN: private void sink(int i)    uses swap

  private void swap(int i, int j) {
    // TODO
  }

  public void changePriority(T item, int priority) {
    // TODO
  }
}""",
 rubric=[(0.75, "swap exchanges the two entries in the array"),
         (1.25, "swap updates <code>where</code> for <b>both</b> moved items, using their new indices"),
         (0.75, "changePriority finds the index with <code>where.get(item)</code> (no linear search)"),
         (0.25, "Throws <code>IllegalArgumentException</code> when the item isn't in the map"),
         (0.5, "Saves the old priority, then stores the new one in the entry"),
         (0.75, "Smaller new priority: <code>swim(i)</code>"),
         (0.75, "Larger new priority: <code>sink(i)</code> (or calls both)")],
 pen=[(-0.5, "Searches the heap array for the item (O(n))"),
      (-0.5, "Removes and reinserts the item instead of swimming or sinking it in place"),
      (-0.25, "Swims or sinks in only one direction, whatever the change"),
      SYN],
 note="""<p>The map is only correct if <i>every</i> move goes through <code>swap</code>, and swap moves two items, so both need new map entries. In a min-heap a smaller priority can only break the order with the parent (swim); a larger one only with the children (sink).</p>"""),

dict(id="Q10", pts=5, kind="code", ref=["Q10"],
 prompt="""<p>Return the <code>k</code> values that occur <b>most often</b> in <code>a</code>, in any order. If fewer than k distinct values exist, return all of them; if several values tie for the last place, any of them may be chosen. With n values and d distinct ones it must run in O(n + d log k) expected time: count with a <code>HashMap</code>, then pick with a <code>PriorityQueue</code> that never holds more than k entries. Throw <code>IllegalArgumentException</code> if <code>a</code> is null or k is negative.</p>""",
 stub="""// You may use java.util.HashMap, Map, PriorityQueue, ArrayList, List
public static List<Integer> topKFrequent(int[] a, int k) {
  // TODO
}""",
 rubric=[(0.25, "Throws <code>IllegalArgumentException</code> for null or negative k"),
         (1, "Counts with a HashMap, e.g. <code>count.put(x, count.getOrDefault(x, 0) + 1)</code>"),
         (0.75, "PriorityQueue entries carry both the value and its count (e.g. <code>int[]{value, count}</code> or Map.Entry)"),
         (0.75, "Orders the queue by count, <b>least</b> frequent at the root (min-heap by count)"),
         (1, "Adds while fewer than k entries; once full, replaces the root only when the new count is larger"),
         (0.5, "Handles k = 0 without crashing"),
         (0.75, "Returns the values (not the counts) of what is left in the queue")],
 pen=[(-1, "Puts all d entries in the queue, or sorts all the counts"),
      (-0.5, "Orders by value instead of count"),
      SYN],
 note="""<p>Hashing plus a heap: the map turns n values into d (value, count) pairs in O(n), then it's top k on the counts. Keeping the k <i>most</i> frequent means the one to throw out next is the <i>least</i> frequent kept, so it sits at the root of a min-heap.</p>"""),
]

DRILLS = []
