# Question specs for the mock. Reference code comes from java/*.java <REF id> blocks.

EXAM = [
dict(id="Q1", pts=2.5, kind="code", ref=["Q1"],
 prompt="""<p>This quicksort always uses <code>a[hi]</code> as the pivot, so on an array that is already sorted every partition is as lopsided as possible and the sort takes O(n²). Change the private <code>quickSort</code> so it uses the <b>median of <code>a[lo]</code>, <code>a[mid]</code> and <code>a[hi]</code></b> as the pivot. Do not change <code>partition</code>.</p>""",
 stub="""public static void quickSort(int[] a) {
  quickSort(a, 0, a.length - 1);
}

// GIVEN: private static void swap(int[] a, int i, int j)
// GIVEN: private static int partition(int[] a, int lo, int hi)
//        Lomuto: partitions around a[hi] and returns the pivot's final index

private static void quickSort(int[] a, int lo, int hi) {
  if (lo >= hi) return;
  int p = partition(a, lo, hi);
  quickSort(a, lo, p - 1);
  quickSort(a, p + 1, hi);
}""",
 rubric=[(0.5, "Computes the middle of the <i>current range</i> (<code>lo + (hi - lo) / 2</code>), not of the whole array"),
         (1, "Picks the median of <code>a[lo]</code>, <code>a[mid]</code>, <code>a[hi]</code> correctly for every order of the three values"),
         (0.75, "Moves the chosen value into <code>a[hi]</code> before calling <code>partition</code>, so partition still works unchanged"),
         (0.25, "Keeps the base case and both recursive calls"),
         ("alt", "Alternative: random pivot"),
         (1.75, "Swaps a random index in <code>[lo, hi]</code> into <code>a[hi]</code> (or shuffles once up front). Expected O(n log n) on every input, but not the median-of-three that was asked for")],
 pen=[(-0.5, "Picks a median but still partitions around the old <code>a[hi]</code> (never moves it), so sorted input is still O(n²)"),
      (-0.125, "Minor logic or major syntax errors showing lack of understanding")],
 note="""<p>After the three swaps, a sorted range puts its true median at <code>hi</code>, so each partition splits it in half: O(n log n). An array of all-equal values is still O(n²) with Lomuto, because every element lands on one side.</p>"""),

dict(id="Q2", pts=2.5, kind="text",
 prompt="""<p>A class overrides <code>equals</code> but not <code>hashCode</code>. State the rule that connects <code>equals</code> and <code>hashCode</code>. Then give an example where this class breaks our <code>HashMap</code>, and explain exactly why the lookup goes wrong.</p>""",
 rubric=[(1, "States the rule: if <code>a.equals(b)</code> then <code>a.hashCode() == b.hashCode()</code>. (Equal hash codes do not have to mean equal objects.)"),
         (1, "Gives an example: for instance <code>put(new Point(1, 2), \"a\")</code> and then <code>get(new Point(1, 2))</code>, where the two Points are equal but are different objects"),
         (0.5, "Explains what goes wrong: the inherited hashCode is identity-based, so the two equal keys usually hash to different buckets. get searches the wrong bucket, never calls equals on the stored key, and returns null (or put stores a duplicate key)")],
 pen=[(-0.125, "Says the map breaks or the key gets lost but does not say why. Award the explanation item above and then apply this penalty")],
 ref_html="""<p>Rule: equal objects must have equal hash codes. Example: <code>Point</code> overrides equals to compare x and y but keeps Object's hashCode. <code>m.put(new Point(1, 2), "a")</code> then <code>m.get(new Point(1, 2))</code>: the second Point's hash code is unrelated to the first's, so <code>floorMod(hash, m)</code> picks a different bucket (or a different probe path), get never reaches the stored key, and it returns null. A second put with an equal key would store a duplicate. Fix: <code>return Objects.hash(x, y);</code></p>"""),

dict(id="Q3", pts=2, kind="text",
 prompt="""<p>The course's open-addressing map: linear probing, Integer keys hash to themselves, 7 slots, tombstones, and after storing a new key it rehashes if <code>used &gt; m/2</code> (to the next prime, 17, if also <code>size &gt; m/2</code>, otherwise at the same size). Rehash reinserts live entries in old-slot order.</p>
<p>(a) From empty: <code>put 9, put 16, put 5, remove 16, put 23, put 2</code>. Where does 23 go? Give the final table with its size.</p>
<p>(b) From empty: <code>put 9, put 16, put 5, remove 9, put 12</code>. Give the final table, <code>size</code> and <code>used</code>.</p>""",
 rubric=[(0.5, "(a) 23 reuses the tombstone in slot 3 (probes 2, 3†, then empty 4, and goes back to the first tombstone)"),
         (0.5, "(a) 2 lands in slot 4, which makes used = size = 4 &gt; 3.5, so the table grows to 17"),
         (0.5, "(a) Final 17-slot table: 2:2, 5:5, 6:23, 9:9"),
         (0.5, "(b) 12 goes to slot 6, used = 4 &gt; 3.5 but size = 3, so a same-size rehash gives 2:16, 5:5, 6:12 with size = used = 3")],
 pen=[(-0.25, "Stores 23 in the first tombstone without probing on to the empty slot, and says so as the rule")],
 ref_html="""<pre class="show">(a) 9→2   16→2,3 → 3   5→5            used 3  size 3
    remove 16: slot 3 = 16†               used 3  size 2
    put 23: 2 (9), 3 (†, remember), 4 empty → store in 3     used 3  size 3
    put 2:  2, 3, 4 empty → store in 4    used 4 &gt; 3.5, size 4 &gt; 3.5 → grow to 17
    rehash in slot order: 9→9, 23→6, 2→2, 5→5
    final m=17: 2:2  5:5  6:23  9:9       size 4  used 4

(b) after put 9, 16, 5:  2:9  3:16  5:5
    remove 9: slot 2 = 9†                 used 3  size 2
    put 12: 5 (5), 6 empty → store in 6   used 4 &gt; 3.5, size 3 → same-size rehash
    slot order: 3:16→2, 5:5→5, 6:12→5 taken→6
    final m=7: 2:16  5:5  6:12            size 3  used 3</pre>"""),

dict(id="Q4", pts=4, kind="code", ref=["Q4"],
 prompt="""<p><code>heap[0..size-1]</code> holds a binary heap in the usual array layout (root at index 0). Anything from index <code>size</code> on is leftover and must be ignored. Return true if these values satisfy the <b>min-heap order property</b>. The layout already makes the tree complete, so only order needs checking.</p>""",
 stub="""// Assume heap != null and 0 <= size <= heap.length
public static boolean isMinHeap(int[] heap, int size) {
  // TODO
}""",
 rubric=[(0.75, "An empty heap and a one-element heap are valid (returns true)"),
         (1, "Checks <i>every</i> node against its parent (or every internal node against both children), not only the root"),
         (0.75, "Uses the right index arithmetic: parent <code>(i - 1) / 2</code>, or children <code>2i + 1</code> and <code>2i + 2</code>"),
         (0.75, "Stays inside <code>size</code>: never reads <code>heap[size]</code> or beyond; a right child exists only if <code>2i + 2 &lt; size</code>"),
         (0.75, "Returns false on any violation and true only after checking everything")],
 pen=[(-0.5, "Uses <code>heap.length</code> instead of <code>size</code>, so leftover values are checked"),
      (-0.5, "Uses 1-based formulas (<code>2i</code>, <code>2i + 1</code>, <code>i / 2</code>) on the 0-based array"),
      (-0.125, "Minor logic or major syntax errors showing lack of understanding")],
 note="""<p>Checking each node against its parent is the shortest version: every parent–child edge is checked exactly once, and there are no bounds cases for missing children. O(n).</p>"""),

dict(id="Q5", pts=3, kind="code", ref=["Q5"],
 prompt="""<p>Implement <code>get</code> for the course's separate-chaining <code>HashMap</code>. Return the value for <code>key</code>, or <code>null</code> if it isn't there. Throw <code>IllegalArgumentException</code> for a null key. Your solution must be <b>iterative</b> and look in only one bucket.</p>""",
 stub="""public class HashMap<K, V> implements Map<K, V> {
  private static class Node<K, V> {
    K key; V value; Node<K, V> next;
  }
  private Node<K, V>[] buckets;
  private int size;

  public V get(K key) {
    // TODO
  }
}""",
 rubric=[(0.5, "Throws <code>IllegalArgumentException</code> for a null key"),
         (0.5, "Finds the bucket with <code>Math.floorMod(key.hashCode(), buckets.length)</code>"),
         (0.5, "Starts at the head of that bucket"),
         (0.5, "Loops until it falls off the chain (<code>curr != null</code>), moving with <code>curr = curr.next</code>"),
         (0.5, "Compares keys with <code>equals</code> and returns that node's value on a match"),
         (0.5, "Returns null after the loop, which also covers an empty bucket")],
 pen=[(-0.75, "Solution is recursive"),
      (-0.5, "Searches every bucket instead of only the key's bucket"),
      (-0.25, "Uses <code>%</code> without floorMod, so a negative hash code gives a negative index"),
      (-0.25, "Compares keys with <code>==</code>"),
      (-0.125, "Minor logic or major syntax errors showing lack of understanding")]),

dict(id="Q6", pts=6, kind="code", ref=["Q6"],
 prompt="""<p>Implement <code>probe</code> and <code>put</code> for the course's open-addressing map (linear probing, tombstones).</p>
<ul><li><code>probe(key)</code> returns the key's slot if a live entry holds it. Otherwise it returns where a new key should go: the <b>first tombstone</b> on the probe path, or the empty slot that ended the path if there was none.</li>
<li><code>put</code> returns true if the key was new and false if it replaced a value. It keeps <code>size</code> and <code>used</code> correct and calls <code>rehashIfNeeded()</code> after storing a new key. Null keys or values throw <code>IllegalArgumentException</code>.</li></ul>""",
 stub="""public class OpenAddressingMap<K, V> implements Map<K, V> {
  private static class Entry<K, V> {
    K key; V value; boolean deleted;   // deleted == true means tombstone
    Entry(K key, V value) { this.key = key; this.value = value; }
  }
  private Entry<K, V>[] slots;
  private int size;   // live entries
  private int used;   // live entries + tombstones

  // GIVEN: private int indexFor(K key)              floorMod(key.hashCode(), slots.length)
  // GIVEN: private boolean holdsKey(int i, K key)   slots[i] is a live entry for key
  // GIVEN: private void rehashIfNeeded()            applies the used/size rule

  private int probe(K key) {
    // TODO
  }

  public boolean put(K key, V value) {
    // TODO
  }
}""",
 rubric=[(0.5, "probe starts at <code>indexFor(key)</code>"),
         (0.5, "probe loops until it reaches an empty (null) slot"),
         (0.75, "Records the <i>first</i> tombstone only, and keeps probing past it"),
         (0.5, "Never matches a key against a tombstone (checks <code>deleted</code> before comparing)"),
         (0.5, "Returns the slot right away when a live entry's key <code>equals</code> the key"),
         (0.5, "Steps with wraparound: <code>i = (i + 1) % slots.length</code>"),
         (0.75, "Returns the first tombstone if there was one, otherwise the empty slot"),
         (0.25, "put throws <code>IllegalArgumentException</code> for a null key or value"),
         (0.5, "If <code>holdsKey(i, key)</code>, replaces the value and returns false"),
         (0.5, "Increments <code>used</code> only when the slot was empty (reusing a tombstone doesn't change it)"),
         (0.25, "Stores a new Entry and increments <code>size</code>"),
         (0.5, "Calls <code>rehashIfNeeded()</code> after storing, then returns true")],
 pen=[(-1, "probe returns at the first tombstone without probing on, so a key stored past the tombstone can be added a second time"),
      (-0.25, "Calls <code>rehashIfNeeded()</code> before the new key is stored"),
      (-0.125, "Minor logic or major syntax errors showing lack of understanding")]),

dict(id="Q7", pts=4, kind="code", ref=["Q7"],
 prompt="""<p>Implement <code>sink</code> for the array-based min-heap. It moves the value at index <code>i</code> down until the order property holds. It is called by <code>remove</code> after the last value is moved to the root.</p>""",
 stub="""public class ArrayHeap<T extends Comparable<T>> {
  private T[] heap;
  private int size;

  // GIVEN: private int compare(T a, T b)     negative if a has higher priority
  // GIVEN: private int leftChild(int i)      2i + 1
  // GIVEN: private int rightChild(int i)     2i + 2
  // GIVEN: private void swap(int i, int j)

  private void sink(int i) {
    // TODO
  }
}""",
 rubric=[(1, "Loops while <code>i</code> has at least a left child (<code>leftChild(i) &lt; size</code>)"),
         (1, "Picks the <b>smaller</b> child, checking that the right child exists before reading it"),
         (0.75, "Stops once <code>heap[i]</code> is no larger than that child"),
         (0.75, "Swaps with the smaller child and continues from the child's index"),
         (0.5, "Uses <code>size</code>, not <code>heap.length</code>, for the bounds")],
 pen=[(-1, "The student writes a coherent max-heap sink (always swaps with the larger child). Read the items above in mirror image, award the ones earned, then apply this penalty"),
      (-0.125, "Minor logic or major syntax errors showing lack of understanding")],
 note="""<p>Recursion is fine here. The order of the two comparisons matters: find the smaller child first, then compare it with the parent.</p>"""),

dict(id="Q8", pts=5, kind="code", ref=["Q8"],
 prompt="""<p>Finish the indexed min-heap (adaptive priority queue). Implement <code>swap</code>, which must keep the index map in sync, and <code>changePriority</code>, which changes an item's priority and restores the heap order. Throw <code>IllegalArgumentException</code> for null arguments and <code>NoSuchElementException</code> if the item isn't in the heap.</p>""",
 stub="""public class IndexedArrayHeap<T, P extends Comparable<P>> {
  private static class Entry<T, P> {
    T item; P priority;
  }
  private Entry<T, P>[] heap;
  private int size;
  private Map<T, Integer> index;   // item -> its slot in heap; a hash map

  // GIVEN: private void swim(int i)    both call swap to move entries
  // GIVEN: private void sink(int i)

  private void swap(int i, int j) {
    // TODO
  }

  public void changePriority(T item, P priority) {
    // TODO
  }
}""",
 rubric=[(0.25, "Throws <code>IllegalArgumentException</code> when item or priority is null"),
         (0.5, "Finds the item's slot through the index map"),
         (0.5, "Throws <code>NoSuchElementException</code> when the item isn't in the map"),
         (0.5, "Saves the old priority before overwriting it"),
         (0.5, "Stores the new priority in the entry"),
         (0.75, "Swims when the new priority is more urgent (smaller)"),
         (0.75, "Sinks when the new priority is less urgent (larger)"),
         (0.25, "Moves nothing when the priority is unchanged. Calling <code>sink(i)</code> then <code>swim(i)</code> without comparing earns this item and the two above"),
         (1, "swap exchanges the entries and updates the map for <b>both</b> moved items")],
 pen=[(-1, "Finds the item by scanning the heap array (O(n)) instead of using the map"),
      (-0.125, "Minor logic or major syntax errors showing lack of understanding")]),

dict(id="Q9", pts=4, kind="code", ref=["Q9"],
 prompt="""<p>Write the key iterator for the separate-chaining <code>HashMap</code>. It visits slot 0, 1, 2, … and walks each bucket from its head. It must use O(1) extra space (don't copy the keys anywhere), and a full iteration must take O(n + m). <code>next()</code> throws <code>NoSuchElementException</code> when no keys are left.</p>""",
 stub="""// inside HashMap<K, V>, which has the field Node<K, V>[] buckets

private class KeyIterator implements Iterator<K> {
  // TODO: fields

  KeyIterator() {
    // TODO
  }

  @Override
  public boolean hasNext() {
    // TODO
  }

  @Override
  public K next() {
    // TODO
  }
}""",
 rubric=[(0.5, "Keeps the current node and the next slot to look at as fields"),
         (0.75, "The constructor moves to the first entry, skipping empty buckets"),
         (0.5, "<code>hasNext</code> returns true exactly when keys are left (for example, <code>curr != null</code>)"),
         (1, "<code>next</code> returns the current node's key"),
         (1, "<code>next</code> then moves on: to <code>curr.next</code> in the same bucket, or else to the head of the next non-empty bucket"),
         (0.25, "<code>next</code> throws <code>NoSuchElementException</code> when no keys are left")],
 pen=[(-0.5, "Uses O(n) space: copies all the keys (or nodes) into a list, array or stack when it is created. Grade the items above adapted for that approach, then apply this penalty"),
      (-0.125, "Minor logic or major syntax errors showing lack of understanding")],
 note="""<p><code>slot</code> only ever increases, which is why a full pass is O(n + m).</p>"""),

dict(id="Q10", pts=5, kind="code", ref=["Q10"],
 prompt="""<p>Return the number of vertices that are <b>at most k edges</b> from <code>start</code> in an undirected graph, counting <code>start</code> itself. Use the course's <code>Graph</code>. Each vertex may be put in your waiting structure at most once, and the graph must not be modified. You may use <code>java.util</code> collections or the course's Queue.</p>""",
 stub="""// GIVEN: public class Graph<V> {
//          public Iterable<V> neighbors(V v)    the vertices adjacent to v
//        }

// Assume start is a vertex of g and k >= 0
public static <V> int countWithinHops(Graph<V> g, V start, int k) {
  // TODO
}""",
 rubric=[(0.5, "Creates a queue"),
         (0.25, "Enqueues the start vertex"),
         (0.5, "Keeps each vertex's distance, for example in a <code>Map&lt;V, Integer&gt;</code>"),
         (0.25, "Sets the start's distance to 0, which also marks it as visited"),
         (0.5, "Loops while the queue is not empty"),
         (0.25, "Takes the front vertex and dequeues it"),
         (0.5, "Iterates over <code>g.neighbors(v)</code>"),
         (0.75, "Before it enqueues a neighbor, checks that it is unvisited and marks it visited"),
         (0.5, "Sets the neighbor's distance to the current vertex's distance plus 1"),
         (0.5, "Counts only vertices at most k away: stops expanding at distance k, doesn't enqueue distance k + 1, or counts distances ≤ k afterward"),
         (0.5, "Counts every reached vertex once, including the start, and returns the count")],
 pen=[(-1, "Uses a stack or recursion instead of a queue. DFS does not find the fewest-edges distance, so it can wrongly leave out vertices"),
      (-0.5, "Modifies the graph, for example removing edges to mark vertices visited"),
      (-0.125, "Minor logic or major syntax errors showing lack of understanding")],
),
]

DRILLS = [
dict(id="D1", pts=3, kind="code", ref=["D1"],
 prompt="""<p>Write the Lomuto <code>partition</code>: pivot <code>a[hi]</code>, values smaller than the pivot end up to its left and the rest to its right. Return the pivot's final index.</p>""",
 stub="""// GIVEN: private static void swap(int[] a, int i, int j)

private static int partition(int[] a, int lo, int hi) {
  // TODO
}""",
 rubric=[(1, "Takes <code>pivot = a[hi]</code> and starts the boundary <code>i</code> at <code>lo</code>"),
         (1, "Scans <code>j</code> from lo to hi − 1, swapping <code>a[j]</code> into the left region and advancing <code>i</code> when <code>a[j] &lt; pivot</code>"),
         (0.5, "Finishes with <code>swap(a, i, hi)</code>"),
         (0.5, "Returns <code>i</code>")]),

dict(id="D2", pts=4, kind="code", ref=["D2"],
 prompt="""<p>Write <code>rehash()</code> for the chained <code>HashMap</code>. Grow to the next size in <code>PRIMES</code> (past the end of the list, use 2m + 1) and move every node to its new bucket. Reuse the nodes; don't call put.</p>""",
 stub="""private static final int[] PRIMES = {7, 17, 37, 79, 163, 331, 673, 1361, 2729, 5471};
private int primeIndex;              // buckets.length == PRIMES[primeIndex] while in range
private Node<K, V>[] buckets;

// GIVEN: private int indexFor(K key)   floorMod(key.hashCode(), buckets.length)

private void rehash() {
  // TODO
}""",
 rubric=[(0.5, "Keeps a reference to the old array"),
         (0.75, "Takes the next prime from the list, or 2m + 1 past its end"),
         (0.5, "Allocates the new array and assigns it to <code>buckets</code> before computing indices"),
         (0.75, "Walks every node of every old bucket"),
         (0.75, "Saves <code>curr.next</code> before relinking the node"),
         (0.75, "Computes the index with the <b>new</b> length and links the node at the head of its new bucket")]),

dict(id="D3", pts=4, kind="code", ref=["D3"],
 prompt="""<p>Sort <code>a</code> in ascending order with in-place heapsort: build a max-heap bottom-up, then repeatedly move the max to the end. Write the max-heap <code>sink</code> too. O(1) extra space.</p>""",
 stub="""// GIVEN: private static void swap(int[] a, int i, int j)

public static void heapSort(int[] a) {
  // TODO
}

private static void sink(int[] a, int i, int size) {
  // TODO
}""",
 rubric=[(1, "Builds the heap by sinking indices n/2 − 1 down to 0"),
         (1, "Sortdown: for end = n − 1 down to 1, swaps <code>a[0]</code> with <code>a[end]</code>"),
         (1, "After each swap, sinks index 0 within the shrunk size (<code>end</code>), not <code>a.length</code>"),
         (1, "sink picks the <b>larger</b> child, respects <code>size</code>, and stops when the parent is at least as large")]),

dict(id="D4", pts=2, kind="code", ref=["D4"],
 prompt="""<p>Using the same <code>probe</code> and <code>holdsKey</code> as Q6, write <code>get</code> and <code>remove</code> for the open-addressing map. <code>remove</code> returns true if it removed the key.</p>""",
 stub="""// GIVEN: private int probe(K key)
// GIVEN: private boolean holdsKey(int i, K key)

public V get(K key) {
  // TODO
}

public boolean remove(K key) {
  // TODO
}""",
 rubric=[(0.5, "Both throw <code>IllegalArgumentException</code> for a null key and use one <code>probe</code> call"),
         (0.5, "get returns the value only if <code>holdsKey</code>, else null"),
         (0.5, "remove marks the entry <code>deleted = true</code> instead of setting the slot to null"),
         (0.5, "remove decrements <code>size</code> but not <code>used</code>, and returns false for a missing key")]),

dict(id="D5", pts=3, kind="code", ref=["D5"],
 prompt="""<p>Return the k-th largest value in <code>a</code> (k = 1 is the maximum) in O(n log k) time, using <code>java.util.PriorityQueue</code> (a min-heap). Throw <code>IllegalArgumentException</code> unless 1 ≤ k ≤ a.length.</p>""",
 stub="""public static int kthLargest(int[] a, int k) {
  // TODO
}""",
 rubric=[(1, "Keeps a <b>min</b>-heap of at most k values"),
         (1, "After adding each value, removes the smallest whenever the heap holds more than k"),
         (0.5, "Returns the heap's minimum (<code>peek</code>) at the end"),
         (0.5, "Validates k")]),

dict(id="D6", pts=4, kind="code", ref=["D6"],
 prompt="""<p>Return the number of connected components of an undirected graph. Use DFS with a visited set.</p>""",
 stub="""// GIVEN: Graph<V> has  Iterable<V> vertices()  and  Iterable<V> neighbors(V v)

public static <V> int countComponents(Graph<V> g) {
  // TODO
}""",
 rubric=[(1, "Keeps one visited set across all searches"),
         (1, "Loops over every vertex and starts a new search only from unvisited ones"),
         (1, "Counts one component per search started"),
         (1, "The DFS marks a vertex visited and recurses only into unvisited neighbors")]),

dict(id="D7", pts=3, kind="code", ref=["D7"],
 prompt="""<p>For the indexed heap from Q8, write <code>remove(T item)</code>, which removes any item (for example, a cancelled job), not just the root.</p>""",
 stub="""// GIVEN: swap (keeps the map in sync), swim, sink, Map<T, Integer> index

public void remove(T item) {
  // TODO
}""",
 rubric=[(0.5, "Looks up the slot in the map; throws for a null or missing item"),
         (1, "Swaps the item into the last slot, removes it from the map, clears the slot and decrements size"),
         (1, "If a real gap was filled (<code>i &lt; size</code>), calls both sink and swim at i, because the filler can be too big <i>or</i> too small"),
         (0.5, "Doesn't touch slot i when the removed item was already last")]),

dict(id="D8", pts=2, kind="code", ref=["D8"],
 prompt="""<p>Return true if <code>a</code> has two equal values whose indices differ by at most k. One pass, O(n) expected time.</p>""",
 stub="""public static boolean nearbyDuplicate(int[] a, int k) {
  // TODO
}""",
 rubric=[(1, "Keeps a hash map from value to the most recent index where it was seen"),
         (0.5, "Returns true when the current index minus the stored index is at most k"),
         (0.5, "Updates the stored index on every step, so the closest earlier copy is used")]),
]
