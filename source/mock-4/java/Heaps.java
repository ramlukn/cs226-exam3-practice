import java.util.*;

public class Heaps {
  static class ArrayHeap<T extends Comparable<T>> {
    private T[] heap;
    private int size;
    @SuppressWarnings("unchecked") ArrayHeap() { heap = (T[]) new Comparable[2]; }
    private int compare(T a, T b) { return a.compareTo(b); }
    private int parent(int i) { return (i - 1) / 2; }
    private void swap(int i, int j) { T t = heap[i]; heap[i] = heap[j]; heap[j] = t; }
    T best() { return heap[0]; }
    void remove() {
      heap[0] = heap[size - 1]; heap[size - 1] = null; size--;
      int i = 0;
      while (2 * i + 1 < size) {
        int b = 2 * i + 1;
        if (b + 1 < size && compare(heap[b + 1], heap[b]) < 0) b++;
        if (compare(heap[i], heap[b]) <= 0) break;
        swap(i, b); i = b;
      }
    }

    // <REF Q4>
    public void insert(T x) {
      if (x == null) throw new IllegalArgumentException();
      if (size == heap.length) heap = Arrays.copyOf(heap, 2 * heap.length);  // full: grow
      heap[size] = x;
      size++;
      swim(size - 1);
    }

    private void swim(int i) {
      while (i > 0 && compare(heap[i], heap[parent(i)]) < 0) {  // smaller than my parent
        swap(i, parent(i));
        i = parent(i);
      }
    }
    // </REF Q4>
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
    private void swap(int i, int j) {
      Entry<T, P> t = heap[i]; heap[i] = heap[j]; heap[j] = t;
      index.put(heap[i].item, i); index.put(heap[j].item, j);
    }
    void add(T item, P p) { heap[size] = new Entry<>(item, p); index.put(item, size); size++; swim(size - 1); }
    P bestPriority() { return heap[0].priority; }
    T best() { return heap[0].item; }

    // <REF Q8>
    public void remove(T item) {
      if (item == null) throw new IllegalArgumentException();
      Integer i = index.get(item);
      if (i == null) throw new NoSuchElementException();
      swap(i, size - 1);              // item moves to the last slot; swap updates the map
      index.remove(item);             // item is gone from the map...
      heap[size - 1] = null;          // ...and from the array
      size--;
      if (i < size) {                 // a filler from the bottom now sits at i:
        swim(i);                      //   it may be smaller than its new parent
        sink(i);                      //   or larger than its new children
      }
    }
    // </REF Q8>

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
        if (ref.isEmpty() || rnd.nextInt(3) > 0) { int x = rnd.nextInt(50); h.insert(x); ref.add(x); }
        else { if (!h.best().equals(ref.peek())) throw new AssertionError("heap"); h.remove(); ref.remove(); }
      }
      IndexedHeap<Integer, Integer> ih = new IndexedHeap<>();
      Map<Integer, Integer> pr = new HashMap<>();
      for (int o = 0; o < 150; o++) {
        int item = rnd.nextInt(40);
        if (!pr.containsKey(item) && rnd.nextInt(2) == 0) { int p = rnd.nextInt(100); ih.add(item, p); pr.put(item, p); }
        else if (pr.containsKey(item)) { ih.remove(item); pr.remove(item); }
        ih.check();
        if (!pr.isEmpty() && ih.bestPriority() != Collections.min(pr.values())) throw new AssertionError("best");
      }
      try { ih.remove(999); throw new AssertionError("no NSEE"); } catch (NoSuchElementException e) {}
    }
    // a case where the filler must SWIM: removing 90 must pull 6 up past 50
    IndexedHeap<String, Integer> s = new IndexedHeap<>();
    String[] names = {"a","b","c","d","e","f","g"}; int[] ps = {1, 50, 2, 60, 90, 3, 6};
    for (int k = 0; k < 7; k++) s.add(names[k], ps[k]);
    s.remove("e"); s.check();
    System.out.println("Heaps OK");
  }
}
