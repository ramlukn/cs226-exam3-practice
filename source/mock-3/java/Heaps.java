import java.util.*;

public class Heaps {
  static class ArrayHeap<T extends Comparable<T>> {
    private T[] heap;
    private int size;
    @SuppressWarnings("unchecked") ArrayHeap() { heap = (T[]) new Comparable[200]; }
    private int compare(T a, T b) { return a.compareTo(b); }
    private int leftChild(int i) { return 2 * i + 1; }
    private int rightChild(int i) { return 2 * i + 2; }
    private int parent(int i) { return (i - 1) / 2; }
    private void swap(int i, int j) { T t = heap[i]; heap[i] = heap[j]; heap[j] = t; }
    private void swim(int i) { while (i > 0 && compare(heap[i], heap[parent(i)]) < 0) { swap(i, parent(i)); i = parent(i); } }
    void add(T x) { heap[size] = x; size++; swim(size - 1); }
    T best() { return heap[0]; }
    void remove() { heap[0] = heap[size - 1]; heap[size - 1] = null; size--; if (size > 0) sink(0); }

    // <REF Q7>
    private void sink(int i) {
      while (leftChild(i) < size) {                  // i has at least one child
        int best = leftChild(i);
        int right = rightChild(i);
        if (right < size && compare(heap[right], heap[best]) < 0) {
          best = right;                              // the smaller child
        }
        if (compare(heap[i], heap[best]) <= 0) break; // order holds: stop
        swap(i, best);
        i = best;
      }
    }
    // </REF Q7>
  }

  static class IndexedHeap<T, P extends Comparable<P>> {
    private static class Entry<T, P> {
      T item; P priority;
      Entry(T item, P priority) { this.item = item; this.priority = priority; }
    }
    private Entry<T, P>[] heap;
    private int size;
    private Map<T, Integer> index = new HashMap<>();

    @SuppressWarnings("unchecked") IndexedHeap() { heap = (Entry<T, P>[]) new Entry[200]; }
    private int compare(int i, int j) { return heap[i].priority.compareTo(heap[j].priority); }
    private void swim(int i) { while (i > 0 && compare(i, (i - 1) / 2) < 0) { swap(i, (i - 1) / 2); i = (i - 1) / 2; } }
    private void sink(int i) {
      while (2 * i + 1 < size) {
        int b = 2 * i + 1;
        if (b + 1 < size && compare(b + 1, b) < 0) b++;
        if (compare(i, b) <= 0) break;
        swap(i, b); i = b;
      }
    }
    void add(T item, P p) { heap[size] = new Entry<>(item, p); index.put(item, size); size++; swim(size - 1); }
    T best() { return heap[0].item; }
    P bestPriority() { return heap[0].priority; }
    void removeBest() { index.remove(heap[0].item); heap[0] = heap[size - 1]; heap[size - 1] = null; size--; if (size > 0) { index.put(heap[0].item, 0); sink(0); } }

    // <REF Q8>
    private void swap(int i, int j) {
      Entry<T, P> temp = heap[i];
      heap[i] = heap[j];
      heap[j] = temp;
      index.put(heap[i].item, i);    // BOTH moved entries get their new slot
      index.put(heap[j].item, j);
    }

    public void changePriority(T item, P priority) {
      if (item == null || priority == null) throw new IllegalArgumentException();
      Integer i = index.get(item);                     // O(1) expected, no scan
      if (i == null) throw new NoSuchElementException();
      P old = heap[i].priority;
      heap[i].priority = priority;
      if (priority.compareTo(old) < 0) swim(i);        // more urgent: can only beat its parent
      else if (priority.compareTo(old) > 0) sink(i);   // less urgent: may lose to a child
    }                                                  // equal: nothing moves
    // </REF Q8>

    // <REF D7>
    public void remove(T item) {
      if (item == null) throw new IllegalArgumentException();
      Integer i = index.get(item);
      if (i == null) throw new NoSuchElementException();
      swap(i, size - 1);                 // the item moves to the last slot
      index.remove(heap[size - 1].item);
      heap[size - 1] = null;
      size--;
      if (i < size) {                    // the filler at i may be too big or too small
        sink(i);
        swim(i);
      }
    }
    // </REF D7>

    void check() {
      if (index.size() != size) throw new AssertionError("index size");
      for (int k = 0; k < size; k++) {
        if (index.get(heap[k].item) != k) throw new AssertionError("index slot");
        if (k > 0 && compare(k, (k - 1) / 2) < 0) throw new AssertionError("order");
      }
    }
  }

  public static void main(String[] args) {
    Random rnd = new Random(4);
    for (int t = 0; t < 500; t++) {
      ArrayHeap<Integer> h = new ArrayHeap<>();
      PriorityQueue<Integer> ref = new PriorityQueue<>();
      for (int o = 0; o < 150; o++) {
        if (ref.isEmpty() || rnd.nextInt(3) > 0) { int x = rnd.nextInt(50); h.add(x); ref.add(x); }
        else { if (!h.best().equals(ref.peek())) throw new AssertionError("heap"); h.remove(); ref.remove(); }
      }
      IndexedHeap<Integer, Integer> ih = new IndexedHeap<>();
      Map<Integer, Integer> pr = new HashMap<>();
      for (int o = 0; o < 150; o++) {
        int item = rnd.nextInt(40);
        int op = rnd.nextInt(4);
        if (op == 0 && !pr.containsKey(item)) { int p = rnd.nextInt(100); ih.add(item, p); pr.put(item, p); }
        else if (op == 1 && pr.containsKey(item)) { int p = rnd.nextInt(100); ih.changePriority(item, p); pr.put(item, p); }
        else if (op == 2 && pr.containsKey(item)) { ih.remove(item); pr.remove(item); }
        else if (op == 3 && !pr.isEmpty()) {
          int min = Collections.min(pr.values());
          if (ih.bestPriority() != min) throw new AssertionError("best");
          pr.remove(ih.best()); ih.removeBest();
        }
        ih.check();
      }
      try { ih.changePriority(999, 1); throw new AssertionError("no NSEE"); } catch (NoSuchElementException e) {}
    }
    System.out.println("Heaps OK");
  }
}
