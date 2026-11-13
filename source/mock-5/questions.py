# Question specs for Mock Test 5. Reference code comes from java/*.java <REF id> blocks.

SYN = (-0.125, "Minor logic or major syntax errors showing lack of understanding")

EXAM = [
dict(id="Q1", pts=2.5, kind="text",
 prompt="""<p>Quicksort with Lomuto partition always uses <code>a[hi]</code> as the pivot. (a) Explain why it takes O(n²) on an array that is already sorted. (b) Explain what median-of-three pivot selection changes for that input. (c) Give one input on which median-of-three Lomuto quicksort is <i>still</i> O(n²), and say why.</p>""",
 rubric=[(1, "(a) On sorted input <code>a[hi]</code> is the largest value, so partition puts every other element on one side: subproblems of size n−1, n−2, …, which sums to about n²/2 comparisons"),
         (1, "(b) The median of first, middle and last of a sorted range is its true middle value, so each partition splits the range roughly in half: O(n log n)"),
         (0.5, "(c) An array where every value is equal: Lomuto sends everything that isn't strictly smaller to one side, so every split is still n−1 and 0, whatever the pivot")],
 pen=[(-0.125, "Gives the right complexity without the reason (which side the elements go to, or how the subproblem sizes add up)")],
 ref_html="""<p>(a) Sorted input, pivot = max: the left part has n−1 elements, the right part none. The total work is (n−1) + (n−2) + … + 1 = O(n²). (b) Median-of-three picks the middle value of a sorted range, so both halves have about n/2 elements: depth log n, O(n log n). (c) All-equal values (e.g. <code>[4, 4, 4, 4, 4]</code>): no element is <code>&lt;</code> the pivot, so every partition is maximally lopsided again.</p>"""),

dict(id="Q2", pts=2.5, kind="text",
 prompt="""<p>You are given an unsorted array of n values and want to turn it into a min-heap in place. (a) Bottom-up heapify calls <code>sink</code> on some of the indices. Which indices, in what order, and why does it skip the others? (b) Why is bottom-up heapify O(n), while inserting the n values one at a time (each with <code>swim</code>) is O(n log n)?</p>""",
 rubric=[(0.75, "(a) Sinks indices from n/2 − 1 down to 0: the last internal node first, the root last"),
         (0.5, "(a) Skips n/2 … n−1 because those are leaves: a single node is already a valid heap, so there is nothing to sink"),
         (0.75, "(b) Heapify is O(n): about half the nodes are leaves and do no work, a quarter sink at most 1 level, an eighth at most 2, … and that sum is bounded by n"),
         (0.5, "(b) Inserting one at a time is O(n log n): later inserts land at the bottom of a tree of height log n and may swim all the way up")],
 pen=[(-0.125, "Gives the right order or bound without the reason")],
 ref_html="""<p>(a) <code>for (int i = n / 2 - 1; i &gt;= 0; i--) sink(i);</code>. Going from the bottom up means that when <code>sink(i)</code> runs, both of i's subtrees are already heaps, which is exactly what sink needs. (b) The cost of sinking a node is its <i>height</i>, and most nodes are near the bottom: n/4·1 + n/8·2 + n/16·3 + … ≤ n. Swim's cost is a node's <i>depth</i>, and most nodes are deep, so n inserts cost up to n·log n.</p>"""),

dict(id="Q3", pts=2, kind="text",
 prompt="""<p><b>Chaining.</b> The course's separate-chaining map: Integer keys hash to themselves, 7 buckets, new keys go at the <b>head</b> of their bucket, and after a new key is added it rehashes to 17 buckets if <code>size / buckets.length &gt; 0.75</code>. Rehash walks old buckets 0, 1, 2, … and each chain from head to tail, inserting each node at the head of its new bucket.</p>
<p>From empty: <code>put 3, put 20, put 10, put 37, put 17, put 24</code>.</p>
<p>(a) Right after 24 is added, before any rehash, write bucket 3's chain from head to tail.</p>
<p>(b) Does a rehash happen? Write every non-empty bucket of the final table with its chain, head to tail.</p>
<p><b>Heap.</b> (c) Insert <code>5, 3, 8, 1, 9, 2</code> into an empty array-based min-heap and give the array. (d) Then call <code>remove()</code> once and give the array.</p>""",
 rubric=[(0.5, "(a) Bucket 3: 24 → 17 → 10 → 3 (newest at the head)"),
         (0.5, "(b) Yes, 6/7 &gt; 0.75. Final 17 buckets: 0: 17, 3: 20 → 3 → 37, 7: 24, 10: 10"),
         (0.5, "(c) [1, 3, 2, 5, 9, 8]"),
         (0.5, "(d) [2, 3, 8, 5, 9]")],
 pen=[(-0.25, "Gives keys without bucket numbers or arrays without their order, so the grader can't check positions")],
 ref_html="""<pre class="show">(a) 3→b3   20→b6   10→b3   37→b2   17→b3   24→b3
    bucket 3 (head first): 24 → 17 → 10 → 3

(b) size 6 / 7 = 0.857 &gt; 0.75 → rehash to 17
    old b2: 37 → 37 % 17 = 3            new b3: 37
    old b3: 24 → 7, 17 → 0, 10 → 10, 3 → 3   new b3: 3 → 37
    old b6: 20 → 3                      new b3: 20 → 3 → 37
    final:  0: 17   3: 20 → 3 → 37   7: 24   10: 10

(c) 5 | 3 swims over 5 | 8 | 1 swims to the root | 9 | 2 swims over 8
    [1, 3, 2, 5, 9, 8]
(d) remove 1, move 8 to the root, sink: smaller child is 2 (index 2), swap
    [2, 3, 8, 5, 9]</pre>"""),

dict(id="Q4", pts=4, kind="code", ref=["Q4"],
 prompt="""<p>Implement <code>remove</code> for the array-based min-heap: it removes and returns the best (smallest) value. Throw <code>NoSuchElementException</code> if the heap is empty. Don't leave a stale reference in the array.</p>""",
 stub="""public class ArrayHeap<T extends Comparable<T>> {
  private T[] heap;   // heap[0..size-1], root at 0
  private int size;

  // GIVEN: private void sink(int i)

  public T remove() {
    // TODO
  }
}""",
 rubric=[(0.5, "Throws <code>NoSuchElementException</code> when <code>size == 0</code>"),
         (0.75, "Saves the root value before overwriting it"),
         (0.75, "Moves the last value (<code>heap[size - 1]</code>) to the root"),
         (0.5, "Sets the old last slot to null"),
         (0.5, "Decrements size"),
         (0.5, "Calls <code>sink(0)</code> (only when the heap isn't empty afterwards)"),
         (0.5, "Returns the saved value")],
 pen=[(-0.5, "Sinks before moving the last value up, or sinks from the wrong index"),
      SYN]),

dict(id="Q5", pts=4, kind="code", ref=["Q5"],
 prompt="""<p>Implement <code>remove</code> for the course's separate-chaining <code>HashMap</code>. Return the removed value, or <code>null</code> if the key wasn't there. Throw <code>IllegalArgumentException</code> for a null key. Your solution must be iterative and look in only one bucket.</p>""",
 stub="""public class HashMap<K, V> implements Map<K, V> {
  private static class Node<K, V> {
    K key; V value; Node<K, V> next;
  }
  private Node<K, V>[] buckets;
  private int size;

  public V remove(K key) {
    // TODO
  }
}""",
 rubric=[(0.25, "Throws <code>IllegalArgumentException</code> for a null key"),
         (0.5, "Finds the bucket with <code>Math.floorMod(key.hashCode(), buckets.length)</code>"),
         (0.5, "Walks the chain with two pointers (previous and current), advancing both"),
         (0.5, "Compares keys with <code>equals</code>"),
         (0.75, "Removing the head: <code>buckets[i] = curr.next</code>"),
         (0.75, "Removing later in the chain: <code>prev.next = curr.next</code>"),
         (0.25, "Decrements size"),
         (0.5, "Returns the removed value, or null after the loop")],
 pen=[(-0.75, "Solution is recursive"),
      (-0.5, "Searches every bucket"),
      (-0.25, "Compares keys with <code>==</code>"),
      SYN],
 note="""<p>The head case is separate because no node points to the head: the bucket array does. Forgetting it is the most common bug here. A one-node chain is also a head removal.</p>"""),

dict(id="Q6", pts=6, kind="code", ref=["Q6"],
 prompt="""<p>Implement <code>rehashIfNeeded</code> and <code>rehash</code> for the course's open-addressing map. After a new key is stored, <code>put</code> calls <code>rehashIfNeeded()</code>. If <code>used &gt; m/2</code>, it rehashes: to the next prime in <code>PRIMES</code> if also <code>size &gt; m/2</code> (and to <code>2m + 1</code> once the list runs out), otherwise at the same size. <code>rehash(capacity)</code> rebuilds the table at that capacity, keeping live entries in old-slot order and dropping tombstones.</p>""",
 stub="""public class OpenAddressingMap<K, V> implements Map<K, V> {
  private static class Entry<K, V> {
    K key; V value; boolean deleted;   // deleted == true means tombstone
  }
  private static final int[] PRIMES = {7, 17, 37, 79, 163, 331, 673};
  private int primeIndex;              // slots.length == PRIMES[primeIndex] while in range
  private Entry<K, V>[] slots;
  private int size;   // live entries
  private int used;   // live entries + tombstones

  // GIVEN: private int indexFor(K key)   floorMod(key.hashCode(), slots.length)

  private void rehashIfNeeded() {
    // TODO
  }

  private void rehash(int capacity) {
    // TODO
  }
}""",
 rubric=[(0.5, "Does nothing unless <code>used &gt; slots.length / 2</code> (with real, not integer, division)"),
         (0.5, "Grows only when <code>size &gt; slots.length / 2</code> too"),
         (0.5, "Picks the next prime by advancing <code>primeIndex</code>, and <code>2m + 1</code> past the end of the list"),
         (0.5, "Otherwise rehashes at the same size"),
         (0.5, "rehash keeps a reference to the old array and allocates a new one of length <code>capacity</code>"),
         (0.75, "Skips null slots and tombstones; copies live entries in old-slot order"),
         (0.75, "Computes each entry's home slot with the <b>new</b> length (call <code>indexFor</code> after replacing <code>slots</code>)"),
         (0.75, "Linear-probes in the new table until an empty slot, with <code>% slots.length</code>"),
         (0.75, "Resets <code>used</code> to 0 and counts each reinserted entry (so used == size afterwards)"),
         (0.5, "Leaves <code>size</code> unchanged")],
 pen=[(-0.5, "Copies tombstones into the new table"),
      (-0.5, "Places entries at their old index instead of rehashing them"),
      SYN],
 note="""<p>The new table has no tombstones, so the reinsert loop only needs to look for <code>null</code>. Reusing <code>put</code> inside rehash also works if it doesn't double-count size or trigger another rehash.</p>"""),

dict(id="Q7", pts=4, kind="code", ref=["Q7"],
 prompt="""<p>Return true if the undirected graph is connected: every vertex can reach every other vertex. An empty graph counts as connected. Use BFS with the course's queue or <code>java.util</code>, don't modify the graph, and put each vertex in the queue at most once.</p>""",
 stub="""// GIVEN: public class Graph<V> {
//          public Iterable<V> vertices()        every vertex
//          public Iterable<V> neighbors(V v)    the vertices adjacent to v
//          public int numVertices()
//        }

public static <V> boolean isConnected(Graph<V> g) {
  // TODO
}""",
 rubric=[(0.5, "Returns true for a graph with no vertices"),
         (0.5, "Starts from any one vertex (e.g. the first from <code>vertices()</code>)"),
         (0.5, "Uses a visited set and a queue, marking and enqueueing the start"),
         (1, "BFS loop: dequeue, iterate <code>g.neighbors(v)</code>, mark and enqueue each unvisited neighbor"),
         (1, "Returns whether the number of visited vertices equals <code>numVertices()</code>"),
         (0.5, "Runs a single search, not one per vertex (O(V + E))")],
 pen=[(-0.5, "Modifies the graph"),
      SYN],
 note="""<p>In an undirected graph, if one vertex reaches all the others, then every pair is connected through it, so one search is enough.</p>"""),

dict(id="Q8", pts=5, kind="code", ref=["Q8"],
 prompt="""<p>Implement <code>insert</code> and <code>removeBest</code> for the indexed min-heap. <code>insert</code> throws <code>IllegalArgumentException</code> for null arguments or an item that is already in the heap, and doubles the array when it is full. <code>removeBest</code> removes and returns the item with the smallest priority, or throws <code>NoSuchElementException</code> when empty. Keep the index map correct at every step.</p>""",
 stub="""public class IndexedArrayHeap<T, P extends Comparable<P>> {
  private static class Entry<T, P> {
    T item; P priority;
    Entry(T item, P priority) { this.item = item; this.priority = priority; }
  }
  private Entry<T, P>[] heap;
  private int size;
  private Map<T, Integer> index;   // item -> its slot in heap; a hash map

  // GIVEN: private void swap(int i, int j)   swaps entries AND updates index for both
  // GIVEN: private void swim(int i)
  // GIVEN: private void sink(int i)

  public void insert(T item, P priority) {
    // TODO
  }

  public T removeBest() {
    // TODO
  }
}""",
 rubric=[(0.25, "insert throws <code>IllegalArgumentException</code> for null arguments"),
         (0.5, "insert rejects an item already in the heap with <code>index.containsKey(item)</code>"),
         (0.5, "insert grows the array when full"),
         (0.75, "insert stores a new Entry at <code>size</code> and records <code>index.put(item, size)</code> before swimming"),
         (0.5, "insert increments size and swims from the new last slot"),
         (0.25, "removeBest throws <code>NoSuchElementException</code> when empty"),
         (0.5, "removeBest saves the best item and swaps the root with the last entry"),
         (0.75, "removeBest removes the item from the index map"),
         (0.5, "removeBest clears the last slot and decrements size"),
         (0.5, "removeBest sinks from the root only if the heap is not empty, and returns the saved item")],
 pen=[(-1, "Scans the array to find an item instead of using the map"),
      SYN],
 note="""<p>Before you leave each method, list the fields: <code>heap</code>, <code>size</code>, <code>index</code>. Every one of them changes in both methods.</p>"""),

dict(id="Q9", pts=3, kind="code", ref=["Q9"],
 prompt="""<p>Return the value that would be at index <code>k</code> if <code>a</code> were sorted (k = 0 is the smallest), using quickselect with the given <code>partition</code>. Work iteratively. You may reorder <code>a</code>. Throw <code>IllegalArgumentException</code> if <code>k</code> is out of range.</p>""",
 stub="""// GIVEN: private static int partition(int[] a, int lo, int hi)
//        partitions a[lo..hi] around a[hi] and returns the pivot's final index

public static int kthSmallest(int[] a, int k) {
  // TODO
}""",
 rubric=[(0.25, "Throws <code>IllegalArgumentException</code> when k &lt; 0 or k ≥ a.length"),
         (0.5, "Starts with <code>lo = 0, hi = a.length - 1</code> and loops"),
         (0.5, "Partitions the current range and gets the pivot's index p"),
         (0.75, "Returns <code>a[p]</code> when p == k"),
         (0.75, "Continues in only one side: <code>hi = p - 1</code> when k &lt; p, otherwise <code>lo = p + 1</code>"),
         (0.25, "Keeps k as an index into the whole array (doesn't shift it)")],
 pen=[(-0.75, "Solution is recursive"),
      (-0.5, "Sorts the whole array (or recurses into both sides) instead of selecting"),
      SYN],
 note="""<p>After partition, <code>a[p]</code> is exactly where it would be in the sorted array, so p tells you which side k is on. Expected O(n); worst case O(n²) like quicksort.</p>"""),

dict(id="Q10", pts=5, kind="code", ref=["Q10"],
 prompt="""<p>Return the vertices reachable from <code>start</code>, grouped by distance: element 0 is a list holding just <code>start</code>, element 1 lists start's neighbors, element 2 the vertices exactly two edges away, and so on. Unreachable vertices don't appear. The order inside a level doesn't matter. Each vertex appears exactly once.</p>""",
 stub="""// GIVEN: public class Graph<V> {
//          public Iterable<V> neighbors(V v)    the vertices adjacent to v
//        }

// Assume start is a vertex of g
public static <V> List<List<V>> levels(Graph<V> g, V start) {
  // TODO
}""",
 rubric=[(0.5, "Level 0 is a list holding only start; start is marked visited"),
         (0.5, "Uses a visited set (or a distance map)"),
         (1, "Builds each level from the neighbors of the previous level (or uses a distance map and places each vertex at index dist)"),
         (1, "Adds a neighbor only if unvisited, and marks it when it is first added (so it appears once)"),
         (0.5, "Iterates over <code>g.neighbors(v)</code>"),
         (0.75, "Stops when a level comes out empty and doesn't add the empty level"),
         (0.75, "Returns the levels in order of distance")],
 pen=[(-1, "Uses DFS (a stack or recursion) to assign levels: a vertex can be given a distance longer than the shortest"),
      SYN],
 note="""<p>Two equivalent designs: process a whole level at a time (the reference), or run normal BFS with a <code>Map&lt;V, Integer&gt;</code> of distances and append each dequeued vertex to <code>result.get(dist)</code>, adding a new list when dist reaches the current size.</p>"""),
]

DRILLS = []
