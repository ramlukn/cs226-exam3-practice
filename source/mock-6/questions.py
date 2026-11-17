# Question specs for Mock Test 6. Reference code comes from java/*.java <REF id> blocks.

SYN = (-0.125, "Minor logic or major syntax errors showing lack of understanding")

EXAM = [
dict(id="Q1", pts=2.5, kind="text",
 prompt="""<p>A student's iterator over <code>int[] a = {10, 20, 30}</code>:</p>
<pre class="show">private int i = 0;
public boolean hasNext() { return i++ &lt; a.length; }
public Integer next()    { return a[i - 1]; }</pre>
<p>(a) What does a for-each loop over it print? (b) A caller writes <code>if (it.hasNext() &amp;&amp; it.hasNext()) System.out.println(it.next());</code> on a fresh iterator. What does it print, and why? (c) State the rule this iterator breaks. (d) Fix it: rewrite both methods.</p>""",
 rubric=[(0.5, "(a) 10 20 30: a for-each calls hasNext exactly once before each next, so the extra increment lines up"),
         (0.75, "(b) Prints 20: each hasNext call moves i, so the second call skips 10"),
         (0.75, "(c) hasNext must not change the iterator's state: callers may call it any number of times before next"),
         (0.5, "(d) <code>hasNext</code> returns <code>i &lt; a.length</code>; <code>next</code> checks hasNext (throwing NoSuchElementException), then returns <code>a[i++]</code>")],
 pen=[(-0.125, "Right outputs with no reason")],
 ref_html="""<p>(a) 10 20 30. (b) First hasNext: 0 &lt; 3, i becomes 1. Second: 1 &lt; 3, i becomes 2. <code>next()</code> returns <code>a[1]</code> = 20. (c) <code>hasNext</code> only looks; <code>next</code> is the only method that moves. (d)</p>
<pre class="show">public boolean hasNext() { return i &lt; a.length; }
public Integer next() {
  if (!hasNext()) throw new NoSuchElementException();
  return a[i++];
}</pre>"""),

dict(id="Q2", pts=2.5, kind="text",
 prompt="""<p>Give the running time of each operation, and say in a few words why. Say whether it is worst case, expected or amortized.</p>
<ol type="a">
<li><code>add</code> at the end of a dynamic array that doubles its capacity when full</li>
<li><code>find</code> in an AVL tree with n keys</li>
<li><code>find</code> in a plain (unbalanced) binary search tree with n keys</li>
<li><code>remove</code> (the best value) from a binary heap with n values</li>
<li><code>get</code> in a separate-chaining hash map whose load factor stays at most 0.75</li>
</ol>""",
 rubric=[(0.5, "(a) O(1) amortized: a resize copies n values, but it happens only after n cheap adds, so the copying averages out to a constant per add (worst case for one add is O(n))"),
         (0.5, "(b) O(log n) worst case: rotations keep the height within a constant factor of log n"),
         (0.5, "(c) O(n) worst case: inserting keys in sorted order builds a tree that is just a chain"),
         (0.5, "(d) O(log n) worst case: the last value moves to the root and sinks at most the height of the tree"),
         (0.5, "(e) O(1) expected: with a good hash function the average chain has at most 0.75 nodes; O(n) worst case if every key lands in one bucket")],
 pen=[(-0.125, "Right bounds but doesn't say which kind (worst, expected, amortized) or gives no reason. Apply once")],
 ref_html="""<p>(a) O(1) amortized, O(n) for the one add that triggers a resize. Doubling means resizes at sizes 1, 2, 4, …, n, which copy about 2n values in total over n adds. (b) O(log n) worst case. (c) O(n) worst case, e.g. inserting 1, 2, 3, … gives a right-leaning chain. (d) O(log n) worst case. (e) O(1) expected, O(n) worst case.</p>"""),

dict(id="Q3", pts=2, kind="text",
 prompt="""<p>The course's open-addressing map: linear probing, Integer keys hash to themselves, 7 slots, tombstones. After storing a new key it rehashes if <code>used &gt; m/2</code>: to 17 if also <code>size &gt; m/2</code>, otherwise at the same size. Rehash reinserts live entries in old-slot order. Write tables as <code>slot:key</code> pairs and mark tombstones with †.</p>
<p>From empty: <code>put 5, put 12, put 19, remove 12, remove 5</code>.</p>
<p>(a) Then <code>put 26</code>. List the slots it probes and the slot it is stored in. (b) Give <code>size</code> and <code>used</code> right after that put. (c) Then <code>put 1</code>. Does a rehash happen, and of which kind? (d) Give the final table with <code>size</code> and <code>used</code>.</p>""",
 rubric=[(0.5, "(a) Probes 5†, 6†, 0 (key 19), 1 (empty), then stores in slot 5, the first tombstone"),
         (0.5, "(b) size 2, used 3 (reusing a tombstone doesn't raise used)"),
         (0.5, "(c) 1 goes in slot 1, so used = 4 &gt; 3.5 but size = 3, which isn't: a same-size rehash"),
         (0.5, "(d) Final 7-slot table: 1:1, 5:19, 6:26, with size = used = 3")],
 pen=[(-0.25, "Gives keys without slot numbers, or stores 26 at a tombstone without probing to the empty slot")],
 ref_html="""<pre class="show">put 5:  slot 5            put 12: 5 → 6            put 19: 5, 6 → 0
        used 3  size 3
remove 12: 6 = 12†        remove 5: 5 = 5†         used 3  size 1

(a) put 26: 26 % 7 = 5 → 5† (first tombstone, remember), 6†, 0 (19), 1 empty
            → store in slot 5
(b) size 2, used 3
(c) put 1: slot 1 empty → store. used 4 &gt; 3.5, size 3 → same-size rehash
(d) old-slot order: 0:19 → 5,  1:1 → 1,  5:26 → 5 taken → 6
    final m=7: 1:1  5:19  6:26     size 3  used 3</pre>"""),

dict(id="Q4", pts=4, kind="code", ref=["Q4"],
 prompt="""<p>Write a key iterator for the separate-chaining <code>HashMap</code> that visits the buckets in <b>reverse</b> order: bucket <code>m - 1</code> first, down to bucket 0. Within a bucket, walk the chain from head to tail. Use O(1) extra space; a full iteration takes O(n + m). <code>hasNext</code> must not change anything, and <code>next()</code> throws <code>NoSuchElementException</code> when no keys are left.</p>""",
 stub="""// inside HashMap<K, V>, which has the field Node<K, V>[] buckets
// Node<K, V> has fields key, value, next

private class ReverseKeyIterator implements Iterator<K> {
  // TODO fields

  ReverseKeyIterator() {
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
 rubric=[(0.5, "Fields: the current node and the next bucket to look at, starting at <code>buckets.length - 1</code>"),
         (0.75, "The constructor moves to the first key, skipping empty buckets"),
         (0.5, "<code>hasNext</code> returns <code>curr != null</code>, with no side effects"),
         (0.75, "<code>next</code> returns the current node's <b>key</b>"),
         (0.5, "Moves along the chain with <code>curr.next</code>"),
         (0.75, "When a chain ends, loops down to the next non-empty bucket, stopping below 0"),
         (0.25, "Throws <code>NoSuchElementException</code> when no keys are left")],
 pen=[(-0.5, "Copies the keys into a list or array first (O(n) space)"),
      (-0.5, "Visits buckets from 0 upward instead of in reverse"),
      SYN],
 note="""<p>Identical to the usual key iterator except the bucket index starts at <code>buckets.length - 1</code>, counts down, and stops at <code>slot &gt;= 0</code>. Writing <code>advance()</code> once and calling it from both the constructor and <code>next</code> covers every case.</p>"""),

dict(id="Q5", pts=4, kind="code", ref=["Q5"],
 prompt="""<p>Implement <code>rehash</code> for the separate-chaining <code>HashMap</code>. It moves to the next prime in <code>PRIMES</code> (or <code>2m + 1</code> once the list runs out) and moves every <b>existing node</b> into its new bucket, inserting at the head. Don't create new nodes.</p>""",
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
 rubric=[(0.5, "Picks the new capacity: advances <code>primeIndex</code>, or <code>2m + 1</code> past the end of the list"),
         (0.5, "Keeps a reference to the old array and allocates the new one before reinserting"),
         (0.5, "Visits every old bucket and every node in its chain"),
         (0.75, "Saves <code>curr.next</code> before relinking the node"),
         (0.75, "Computes the new bucket with the <b>new</b> length"),
         (0.75, "Inserts at the head: <code>curr.next = buckets[i]; buckets[i] = curr;</code>"),
         (0.25, "Leaves <code>size</code> unchanged")],
 pen=[(-0.5, "Creates new nodes (or calls put, which does) instead of moving the existing ones"),
      (-0.25, "Indexes with the old length"),
      SYN],
 note="""<p>Without saving <code>next</code> first, the line <code>curr.next = buckets[i]</code> cuts the old chain, and the rest of it is lost.</p>"""),

dict(id="Q6", pts=6, kind="code", ref=["Q6"],
 prompt="""<p>Implement <code>put</code> for the course's open-addressing map, <b>without</b> a <code>probe</code> helper: write the search inline. Return the old value if the key was there (replacing it), otherwise <code>null</code>. A new key goes in the first tombstone on its probe path if there is one, otherwise in the empty slot that ended the path. Keep <code>size</code> and <code>used</code> correct and call <code>rehashIfNeeded()</code> after storing a new key. Null keys or values throw <code>IllegalArgumentException</code>.</p>""",
 stub="""public class OpenAddressingMap<K, V> implements Map<K, V> {
  private static class Entry<K, V> {
    K key; V value; boolean deleted;   // deleted == true means tombstone
    Entry(K key, V value) { this.key = key; this.value = value; }
  }
  private Entry<K, V>[] slots;
  private int size;   // live entries
  private int used;   // live entries + tombstones

  // GIVEN: private int indexFor(K key)       floorMod(key.hashCode(), slots.length)
  // GIVEN: private void rehashIfNeeded()     applies the used/size rule

  public V put(K key, V value) {
    // TODO
  }
}""",
 rubric=[(0.25, "Throws <code>IllegalArgumentException</code> for a null key or value"),
         (0.5, "Starts at <code>indexFor(key)</code>"),
         (0.75, "Loops until an empty (null) slot"),
         (0.75, "Remembers only the <b>first</b> tombstone and keeps searching past it"),
         (0.75, "Never matches a key against a tombstone"),
         (0.75, "On a live <code>equals</code> match: replaces the value and returns the old one (no size or used change)"),
         (0.5, "Steps with <code>i = (i + 1) % slots.length</code>"),
         (0.75, "Stores a new key in the first tombstone if there was one, otherwise in the empty slot"),
         (0.5, "Increments <code>used</code> only when it filled an empty slot; increments <code>size</code> either way"),
         (0.5, "Calls <code>rehashIfNeeded()</code> after storing, then returns null")],
 pen=[(-1, "Stores at the first tombstone without searching on, so a key further along can end up stored twice"),
      (-0.25, "Calls <code>rehashIfNeeded()</code> before the key is stored, or on a replace"),
      (-0.25, "Compares keys with <code>==</code>"),
      SYN]),

dict(id="Q7", pts=4, kind="code", ref=["Q7"],
 prompt="""<p>Write a constructor for the array-based min-heap that builds a heap from an array of items in <b>O(n)</b> time using bottom-up heapify. Don't change the caller's array. Throw <code>IllegalArgumentException</code> if it is null.</p>""",
 stub="""public class ArrayHeap<T extends Comparable<T>> {
  private T[] heap;   // heap[0..size-1], root at 0
  private int size;

  // GIVEN: private void sink(int i)   uses heap and size

  public ArrayHeap(T[] items) {
    // TODO
  }
}""",
 rubric=[(0.25, "Throws <code>IllegalArgumentException</code> for null"),
         (0.75, "Copies the items into the heap's own array (e.g. <code>Arrays.copyOf</code>), so the caller's array isn't changed"),
         (0.5, "Sets <code>size</code> to the number of items before sinking"),
         (1, "Sinks from index <code>size / 2 - 1</code> down to 0"),
         (0.75, "Goes from the bottom up (the root last), so each sink starts with both subtrees already heaps"),
         (0.75, "Doesn't insert the items one by one with swim (that is O(n log n))")],
 pen=[(-0.5, "Sinks from the root down to the leaves (top-down): the result isn't always a heap"),
      SYN],
 note="""<p>Indices from <code>size / 2</code> on are leaves, which are already heaps, so the loop starts at the last internal node. An empty array gives <code>size / 2 - 1 = -1</code>, so the loop doesn't run at all.</p>"""),

dict(id="Q8", pts=5, kind="code", ref=["Q8"],
 prompt="""<p>Each row of <code>lists</code> is sorted in ascending order. Return all their values in one ascending list. With k rows and n values in total, it must run in O(n log k): use a <code>java.util.PriorityQueue</code> that never holds more than k entries. Rows may be empty.</p>""",
 stub="""// You may use java.util.PriorityQueue, ArrayList, List

public static List<Integer> mergeSorted(int[][] lists) {
  // TODO
}""",
 rubric=[(0.5, "Creates a PriorityQueue ordered by value (e.g. a comparator on <code>int[]{value, row, index}</code>)"),
         (1, "Seeds it with the first value of every non-empty row, along with which row and position it came from"),
         (0.5, "Loops while the queue is not empty"),
         (0.75, "Removes the smallest entry and appends its value to the result"),
         (1, "Adds the next value from the <b>same row</b> (if there is one)"),
         (0.5, "Skips empty rows without crashing"),
         (0.75, "Never holds more than one entry per row, so the queue size stays ≤ k")],
 pen=[(-1, "Puts all n values into the queue at once (O(n log n), queue of size n)"),
      (-0.5, "Concatenates and sorts instead of merging"),
      SYN],
 note="""<p>Each value enters and leaves the queue once, and the queue holds at most k entries, so each operation is O(log k): O(n log k) in total. Storing the row and position with the value is what lets you find "the next one from the same row".</p>"""),

dict(id="Q9", pts=3, kind="code", ref=["Q9"],
 prompt="""<p>Implement <code>remove(index)</code> for the course's dynamic array: remove and return the value at <code>index</code>, shifting everything after it one place left so there are no gaps. Throw <code>IndexOutOfBoundsException</code> if <code>index</code> is not a valid position. Don't leave a stale reference in the array.</p>""",
 stub="""public class DynamicArray<T> {
  private T[] data;   // data[0..size-1] are the values
  private int size;

  public T remove(int index) {
    // TODO
  }
}""",
 rubric=[(0.5, "Throws <code>IndexOutOfBoundsException</code> when <code>index &lt; 0</code> or <code>index &gt;= size</code> (not <code>data.length</code>)"),
         (0.5, "Saves the value at <code>index</code> before it is overwritten"),
         (0.75, "Shifts <code>data[i] = data[i + 1]</code> for i from <code>index</code> up to <code>size - 2</code>, left to right"),
         (0.5, "Sets the old last slot <code>data[size - 1]</code> to null"),
         (0.5, "Decrements size"),
         (0.25, "Returns the saved value")],
 pen=[(-0.5, "Shifts right to left (or in the wrong direction), overwriting values before they are moved"),
      (-0.25, "Copies into a new array on every remove (O(n) extra space each time)"),
      SYN],
 note="""<p>The shift has to go left to right: each slot is overwritten by its right neighbor, which hasn't been touched yet. The loop stops at <code>size - 2</code> because slot <code>size - 1</code> has no right neighbor; it gets set to null instead. O(n) worst case (removing index 0).</p>"""),

dict(id="Q10", pts=5, kind="code", ref=["Q10"],
 prompt="""<p>Finish the AVL tree's balancing code: <code>updateHeight</code>, <code>rotateRight</code> and <code>rebalance</code>. A leaf has height 0 and an empty subtree has height -1. <code>rebalance(n)</code> is called on the way back up after an insert; it fixes <code>n</code> if its balance factor is outside -1..1 (all four cases) and returns the root of the fixed subtree.</p>""",
 stub="""public class AvlTreeMap<K extends Comparable<K>, V> {
  private static class Node<K, V> {
    K key; V value; Node<K, V> left, right; int height;
  }

  // GIVEN: private int height(Node<K, V> n)             -1 for null, otherwise n.height
  // GIVEN: private Node<K, V> rotateLeft(Node<K, V> n)  mirror image of rotateRight; returns the new subtree root

  private void updateHeight(Node<K, V> n) {
    // TODO
  }

  private Node<K, V> rotateRight(Node<K, V> n) {
    // TODO
  }

  private Node<K, V> rebalance(Node<K, V> n) {
    // TODO
  }
}""",
 rubric=[(0.25, "updateHeight: <code>1 + max(height(left), height(right))</code>, using the null-safe <code>height</code>"),
         (0.25, "rotateRight takes <code>child = n.left</code>"),
         (0.5, "Moves child's right subtree under n: <code>n.left = child.right</code>"),
         (0.5, "Puts n under child: <code>child.right = n</code>"),
         (0.75, "Updates n's height <b>before</b> child's (child's height depends on n's)"),
         (0.5, "Returns child, the new root of the subtree"),
         (0.5, "rebalance computes the balance factor <code>height(n.left) - height(n.right)</code>"),
         (0.75, "Left-heavy (&gt; 1) and the left child leans right: first <code>n.left = rotateLeft(n.left)</code>"),
         (0.5, "Left-heavy: then returns <code>rotateRight(n)</code>"),
         (0.5, "Right-heavy (&lt; -1): the mirror image, with <code>n.right = rotateRight(n.right)</code> when the right child leans left, then <code>rotateLeft(n)</code>; returns n unchanged when balanced")],
 pen=[(-0.5, "Doesn't use a returned root (e.g. calls <code>rotateLeft(n.left)</code> without assigning it to <code>n.left</code>)"),
      (-0.25, "Reads <code>n.left.height</code> directly, which crashes when a child is null"),
      SYN],
 note="""<p>Picture for rotateRight: n has left child c, and c has right subtree T. After the rotation c is on top, n is c's right child, and T (whose keys are between c and n) becomes n's left subtree. Only n and c change height, and n is now the lower one, so update it first.</p>"""),

]

DRILLS = []
