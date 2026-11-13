# Question specs for Mock Test 4. Reference code comes from java/*.java <REF id> blocks.

SYN = (-0.125, "Minor logic or major syntax errors showing lack of understanding")

EXAM = [
dict(id="Q1", pts=2.5, kind="text",
 prompt="""<p><code>Person</code> has fields <code>String name</code>, <code>int age</code> and <code>long id</code>. Its <code>equals</code> returns true when <b>name and age</b> are equal; it ignores <code>id</code>. For each <code>hashCode</code> below, say whether it obeys the hashCode contract, and if it does, whether it is a good choice for our <code>HashMap</code>. One sentence each.</p>
<ol type="a">
<li><code>return age;</code></li>
<li><code>return Objects.hash(name, age, id);</code></li>
<li><code>return 0;</code></li>
<li><code>return (int) (Math.random() * 1000);</code></li>
<li><code>return Objects.hash(name, age);</code></li>
</ol>""",
 rubric=[(0.5, "(a) Legal: equal Persons have equal ages. Weak: everyone with the same age collides, so buckets get long"),
         (0.5, "(b) Illegal: two equal Persons with different ids get different hash codes, so lookups miss"),
         (0.5, "(c) Legal but terrible: every key lands in one bucket, so get and put become O(n)"),
         (0.5, "(d) Illegal: not consistent, the same object gives a different hash each call, so even the stored object can't be found"),
         (0.5, "(e) Legal and good: uses exactly the fields equals uses and spreads keys out")],
 pen=[(-0.125, "Right verdict with no reason or a wrong reason. Award the item, then apply this penalty once")],
 ref_html="""<p>The test for <i>legal</i> is one question: can two objects that are <code>equals</code> ever get different hash codes? (b) can, through <code>id</code>; (d) can, even for one object. The test for <i>good</i> is how well unequal keys spread out: (c) puts everything in one bucket, (a) groups by age, (e) mixes both fields. Rule of thumb: hash exactly the fields <code>equals</code> compares.</p>"""),

dict(id="Q2", pts=2.5, kind="text",
 prompt="""<p>In an indexed min-heap, a student's <code>swap(i, j)</code> exchanges the two entries but only runs <code>index.put(heap[i].item, i)</code>; it never updates the map for the entry that moved to <code>j</code>.</p>
<p>(a) Starting from empty, give a short sequence of operations after which <code>changePriority</code> changes the <b>wrong item's</b> priority, and say which item it changes.</p>
<p>(b) What is the running time of <code>changePriority</code> with a correct map, and what would it be if the heap had no map at all?</p>
<p>(c) When the new priority is <b>smaller</b> than the old one, why is <code>swim</code> enough, with no <code>sink</code>?</p>""",
 rubric=[(0.5, "(a) Explains the cause: the item that moved to <code>j</code> keeps its old slot number in the map"),
         (0.75, "(a) A concrete sequence that shows it, e.g. insert A:5, insert B:3 (B swims, <code>swap(1, 0)</code> leaves B→1 in the map), then <code>changePriority(B, 9)</code> changes A, which is now in slot 1"),
         (0.5, "(b) O(log n) with the map (O(1) expected lookup, then one swim or sink); O(n) without it, because finding the item is a scan"),
         (0.75, "(c) Its children were ≥ the old priority, which is ≥ the new one, so the order below it still holds; only the edge to its parent can break")],
 pen=[(-0.125, "The sequence in (a) depends on which index the student's swap updates and gets it backwards, but the idea is right")],
 ref_html="""<p>(a) insert A:5 → slot 0, map A→0. insert B:3 → slot 1, then B swims with <code>swap(1, 0)</code>. Now heap is B, A. The broken swap updates only <code>heap[1].item</code> = A→1, so the map still says B→1. <code>changePriority(B, 9)</code> looks up slot 1 and changes <b>A</b>. (If the swap is called as <code>swap(0, 1)</code> it updates B and leaves A wrong instead: either way one item points at the other's slot.)</p>
<p>(b) O(log n) vs O(n). (c) Before the change, each child ≥ old priority. The new priority is smaller, so each child is still ≥ it. Only the parent can now be larger.</p>"""),

dict(id="Q3", pts=2, kind="text",
 prompt="""<p>The course's open-addressing map: linear probing, Integer keys hash to themselves, 7 slots, tombstones. After storing a new key it rehashes if <code>used &gt; m/2</code>: to the next prime, 17, if also <code>size &gt; m/2</code>, otherwise at the same size. Rehash reinserts live entries in old-slot order. Write tables as <code>slot:key</code> pairs and mark tombstones with †.</p>
<p>From empty: <code>put 3, put 10, put 17, remove 10</code>.</p>
<p>(a) List, in order, the slots that <code>get(17)</code> looks at, and the slots that <code>get(10)</code> looks at.</p>
<p>(b) Then <code>put 24, put 31</code>. Where does 24 go? Give the final table with <code>size</code> and <code>used</code>.</p>""",
 rubric=[(0.5, "(a) <code>get(17)</code>: 3, 4†, 5 (found). It does not stop at the tombstone in slot 4"),
         (0.5, "(a) <code>get(10)</code>: 3, 4†, 5, 6 (empty, so not found). Only an empty slot ends the search"),
         (0.5, "(b) 24 probes 3, 4†, 5, 6 (empty) and goes back to the tombstone in slot 4; <code>used</code> stays 3"),
         (0.5, "(b) 31 lands in slot 6, so used = size = 4 &gt; 3.5 and the table grows to 17. Final: 0:17, 3:3, 7:24, 14:31 with size = used = 4")],
 pen=[(-0.25, "Gives values in an array with no slot numbers, or a table of the wrong length, so the grader can't tell which slot holds what")],
 ref_html="""<pre class="show">put 3:  slot 3                              used 1  size 1
put 10: 3 taken → 4                          used 2  size 2
put 17: 3, 4 taken → 5                       used 3  size 3   (3 &gt; 3.5? no)
remove 10: slot 4 = 10†                      used 3  size 2

(a) get(17): 3 (key 3), 4 (†, keep going), 5 → found
    get(10): 3, 4 (†, keep going), 5 (key 17), 6 (empty) → not found

(b) put 24: 3, 4 (†, remember), 5, 6 empty → store in 4    used 3  size 3
    put 31: 3, 4, 5, 6 empty → store in 6                   used 4  size 4
            used 4 &gt; 3.5 and size 4 &gt; 3.5 → grow to 17
    rehash in old-slot order: 3→3, 24→7, 17→0, 31→14
    final m=17: 0:17  3:3  7:24  14:31      size 4  used 4</pre>"""),

dict(id="Q4", pts=4, kind="code", ref=["Q4"],
 prompt="""<p>Implement <code>insert</code> and the <code>swim</code> it calls for the array-based min-heap. Null values throw <code>IllegalArgumentException</code>. When the array is full, double its length before inserting.</p>""",
 stub="""public class ArrayHeap<T extends Comparable<T>> {
  private T[] heap;   // heap[0..size-1], root at 0
  private int size;

  // GIVEN: private int compare(T a, T b)     negative if a has higher priority
  // GIVEN: private int parent(int i)         (i - 1) / 2
  // GIVEN: private void swap(int i, int j)

  public void insert(T x) {
    // TODO
  }

  private void swim(int i) {
    // TODO
  }
}""",
 rubric=[(0.25, "Throws <code>IllegalArgumentException</code> for null"),
         (0.5, "Grows when <code>size == heap.length</code> (e.g. <code>Arrays.copyOf(heap, 2 * heap.length)</code>), before writing"),
         (0.5, "Places x at index <code>size</code>, increments size, and swims from the new last index"),
         (0.75, "swim loops while <code>i &gt; 0</code> (the root has no parent)"),
         (0.75, "Continues only while the node is smaller than its parent: <code>compare(heap[i], heap[parent(i)]) &lt; 0</code>"),
         (0.75, "Swaps with the parent and moves up: <code>i = parent(i)</code>"),
         (0.5, "Stops as soon as the node is not smaller than its parent (no extra swaps)")],
 pen=[(-0.5, "Compare is backwards (swims while the node is larger): a coherent max-heap swim. Award the items in mirror image, then apply this"),
      SYN],
 note="""<p>Say the loop as a sentence first: "while I'm not the root and I'm smaller than my parent, swap up." Translate <code>compare(a, b) &lt; 0</code> as <code>a &lt; b</code>.</p>"""),

dict(id="Q5", pts=4, kind="code", ref=["Q5"],
 prompt="""<p>Implement <code>put</code> for the course's separate-chaining <code>HashMap</code>. If the key is already there, replace its value and return the <b>old</b> value. Otherwise add it at the <b>head</b> of its bucket and return <code>null</code>. After adding a new key, call <code>rehash()</code> if the load factor <code>size / buckets.length</code> is now above 0.75. Null keys or values throw <code>IllegalArgumentException</code>.</p>""",
 stub="""public class HashMap<K, V> implements Map<K, V> {
  private static class Node<K, V> {
    K key; V value; Node<K, V> next;
    Node(K key, V value) { this.key = key; this.value = value; }
  }
  private Node<K, V>[] buckets;
  private int size;

  // GIVEN: private void rehash()   grows buckets and reinserts every node

  public V put(K key, V value) {
    // TODO
  }
}""",
 rubric=[(0.25, "Throws <code>IllegalArgumentException</code> for a null key or value"),
         (0.5, "Finds the bucket with <code>Math.floorMod(key.hashCode(), buckets.length)</code>"),
         (0.5, "Walks that bucket's chain until null"),
         (1, "On an <code>equals</code> match: saves the old value, replaces it, returns the old value (size unchanged)"),
         (0.75, "Otherwise inserts a new node at the head: <code>node.next = buckets[i]; buckets[i] = node;</code>"),
         (0.25, "Increments size only for a new key"),
         (0.5, "Checks the load factor with real division after adding, and calls <code>rehash()</code>"),
         (0.25, "Returns null for a new key")],
 pen=[(-0.25, "Integer division <code>size / buckets.length</code>, which is 0 until the table is full, so it never rehashes in time"),
      (-0.25, "Compares keys with <code>==</code>"),
      (-0.25, "Uses <code>%</code> without floorMod"),
      SYN]),

dict(id="Q6", pts=6, kind="code", ref=["Q6"],
 prompt="""<p>For the course's open-addressing map, write a private helper <code>find(key)</code> that returns the slot holding a <b>live</b> entry for <code>key</code>, or <code>-1</code> if there is none. Then use it to implement <code>containsKey</code> and <code>remove</code>. <code>remove</code> returns the removed value, or <code>null</code> if the key wasn't there. Null keys throw <code>IllegalArgumentException</code>. There is no <code>probe</code> or <code>holdsKey</code> in this question: write the search yourself.</p>""",
 stub="""public class OpenAddressingMap<K, V> implements Map<K, V> {
  private static class Entry<K, V> {
    K key; V value; boolean deleted;   // deleted == true means tombstone
  }
  private Entry<K, V>[] slots;
  private int size;   // live entries
  private int used;   // live entries + tombstones

  // GIVEN: private int indexFor(K key)   floorMod(key.hashCode(), slots.length)

  private int find(K key) {
    // TODO
  }

  public boolean containsKey(K key) {
    // TODO
  }

  public V remove(K key) {
    // TODO
  }
}""",
 rubric=[(0.5, "find starts at <code>indexFor(key)</code>"),
         (0.5, "find loops until it reaches an empty (null) slot"),
         (1, "find keeps going past tombstones (and past other keys): only null ends the search"),
         (0.5, "Checks <code>deleted</code> before comparing keys, so a tombstone never matches"),
         (0.75, "Steps with wraparound: <code>i = (i + 1) % slots.length</code>"),
         (0.25, "Returns -1 after the loop"),
         (0.5, "containsKey throws for null and returns <code>find(key) != -1</code>"),
         (0.25, "remove returns null when find gives -1"),
         (0.75, "remove marks the entry deleted (a tombstone), it does <i>not</i> set the slot to null"),
         (0.5, "remove decrements size and leaves used alone"),
         (0.5, "remove returns the removed value (saved before or after marking)")],
 pen=[(-0.5, "remove decrements <code>used</code> (the slot is still not null, so used must stay)"),
      (-0.25, "Compares keys with <code>==</code>"),
      (-0.5, "Steps with <code>% size</code> or any length other than <code>slots.length</code>"),
      SYN],
 note="""<p>Setting the slot to null would cut the probe path: any key stored past it becomes unreachable. That is the whole reason tombstones exist. The loop always ends because the rehash rule keeps <code>used ≤ m/2</code>, so there is always a null slot.</p>"""),

dict(id="Q7", pts=4, kind="code", ref=["Q7"],
 prompt="""<p>Write the value iterator for the open-addressing map. It visits slots 0, 1, 2, … and returns the value of every <b>live</b> entry, skipping empty slots and tombstones. Use O(1) extra space. <code>hasNext</code> must not change what <code>next</code> will return. <code>next()</code> throws <code>NoSuchElementException</code> when no values are left.</p>""",
 stub="""// inside OpenAddressingMap<K, V>, which has the field Entry<K, V>[] slots

private class ValueIterator implements Iterator<V> {
  // TODO fields

  ValueIterator() {
    // TODO
  }

  @Override
  public boolean hasNext() {
    // TODO
  }

  @Override
  public V next() {
    // TODO
  }
}""",
 rubric=[(0.5, "Keeps a single slot index as the field (the slot the next value comes from)"),
         (1, "Skipping moves past slots that are null <b>or</b> tombstones, and stops at <code>slots.length</code>"),
         (0.5, "The constructor skips to the first live entry"),
         (0.5, "<code>hasNext</code> returns <code>i &lt; slots.length</code> (or an equivalent that has no side effect)"),
         (0.75, "<code>next</code> returns that slot's <b>value</b> (not the Entry, not the key)"),
         (0.5, "<code>next</code> then moves to the following live entry"),
         (0.25, "<code>next</code> throws <code>NoSuchElementException</code> when no values are left")],
 pen=[(-0.5, "Copies the values into a list or array first (O(n) space). Grade the items for that approach, then apply this"),
      (-0.5, "<code>hasNext</code> advances the index, so calling it twice skips a value"),
      SYN]),

dict(id="Q8", pts=5, kind="code", ref=["Q8"],
 prompt="""<p>Implement <code>remove(item)</code> for the indexed min-heap: it removes that item, wherever it is in the heap, in O(log n). Throw <code>IllegalArgumentException</code> for null and <code>NoSuchElementException</code> if the item isn't in the heap.</p>""",
 stub="""public class IndexedArrayHeap<T, P extends Comparable<P>> {
  private static class Entry<T, P> {
    T item; P priority;
  }
  private Entry<T, P>[] heap;
  private int size;
  private Map<T, Integer> index;   // item -> its slot in heap; a hash map

  // GIVEN: private void swap(int i, int j)   swaps entries AND updates index for both
  // GIVEN: private void swim(int i)
  // GIVEN: private void sink(int i)

  public void remove(T item) {
    // TODO
  }
}""",
 rubric=[(0.25, "Throws <code>IllegalArgumentException</code> for null"),
         (0.5, "Finds the slot with <code>index.get(item)</code>"),
         (0.5, "Throws <code>NoSuchElementException</code> when the item isn't in the map"),
         (0.75, "Swaps the item with the last entry (<code>size - 1</code>)"),
         (0.75, "Removes the item from the index map"),
         (0.5, "Clears the last slot and decrements size"),
         (0.5, "Only repairs order when the removed slot is still inside the heap (<code>i &lt; size</code>)"),
         (1.25, "Calls <b>both</b> swim(i) and sink(i): the filler from the bottom can be too small for its new parent or too large for its new children. Award 0.5 for only one of them")],
 pen=[(-1, "Finds the item by scanning the heap array (O(n)) instead of using the map"),
      SYN],
 note="""<p>Why both: the last entry came from a different branch of the tree. Example priorities 1, 50, 2, 60, 90, 3, 6 (array order): removing 90 at slot 4 moves 6 there, and 6 is smaller than its new parent 50, so it has to swim. Removing an item near the top usually needs sink instead.</p>"""),

dict(id="Q9", pts=3, kind="code", ref=["Q9"],
 prompt="""<p>Write <code>partition</code> for quicksort using <b><code>a[lo]</code></b> as the pivot (not <code>a[hi]</code>). Afterwards everything left of the pivot is smaller than it, everything right of it is ≥ it, and you return the pivot's final index. Work in place in one left-to-right pass.</p>""",
 stub="""// GIVEN: private static void swap(int[] a, int i, int j)

private static int partition(int[] a, int lo, int hi) {
  // TODO
}""",
 rubric=[(0.5, "Takes <code>pivot = a[lo]</code>"),
         (0.5, "Starts the boundary at <code>lo</code> (the end of the &lt; region)"),
         (0.5, "Scans <code>j</code> from <code>lo + 1</code> through <code>hi</code> inclusive"),
         (0.75, "When <code>a[j] &lt; pivot</code>: grows the boundary and swaps a[j] into it"),
         (0.5, "After the loop, swaps the pivot from <code>lo</code> into the boundary slot"),
         (0.25, "Returns the pivot's final index")],
 pen=[(-0.5, "Partitions around <code>a[hi]</code> instead of <code>a[lo]</code>, which is not what was asked"),
      SYN],
 note="""<p>Mirror of the course's Lomuto: the pivot sits at the left end, so the boundary starts <i>on</i> it and is incremented before each swap. Trace <code>[4, 7, 1, 9, 2]</code>: after the loop it is <code>[4, 1, 2, 9, 7]</code> with boundary 2, then the final swap gives <code>[2, 1, 4, 9, 7]</code> and returns 2.</p>"""),

dict(id="Q10", pts=5, kind="code", ref=["Q10"],
 prompt="""<p>Return a shortest path (fewest edges) from <code>start</code> to <code>target</code> in an undirected graph, as a list of vertices from <code>start</code> to <code>target</code> inclusive. If <code>start</code> equals <code>target</code>, return a list holding just <code>start</code>. If <code>target</code> can't be reached, return an empty list. Each vertex may enter your waiting structure at most once, and the graph must not be modified.</p>""",
 stub="""// GIVEN: public class Graph<V> {
//          public Iterable<V> neighbors(V v)    the vertices adjacent to v
//        }

// Assume start and target are vertices of g
public static <V> List<V> shortestPath(Graph<V> g, V start, V target) {
  // TODO
}""",
 rubric=[(0.5, "Creates a queue and enqueues start"),
         (0.5, "Keeps a parent (or came-from) map; start is in it, which marks it visited"),
         (0.5, "Loops while the queue is not empty, dequeuing from the front"),
         (0.5, "Iterates over <code>g.neighbors(v)</code>"),
         (0.75, "Before enqueueing a neighbor: checks it is unvisited, records its parent, marks it visited"),
         (0.5, "Returns an empty list when target was never reached"),
         (1, "Builds the path by walking parent links back from target to start"),
         (0.5, "Reverses it so the list starts at start"),
         (0.25, "start == target gives a one-element list")],
 pen=[(-1, "Uses a stack or recursion instead of a queue: DFS does not give the fewest edges"),
      (-0.5, "Modifies the graph"),
      SYN],
 note="""<p>Stopping as soon as target is dequeued is optional. BFS reaches every vertex for the first time by a shortest route, so the parent links form shortest paths either way.</p>"""),
]

DRILLS = []
