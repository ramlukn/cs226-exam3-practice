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
    void insert(T x) { heap[size] = x; size++; int i = size - 1; while (i > 0 && compare(heap[i], heap[parent(i)]) < 0) { swap(i, parent(i)); i = parent(i); } }
    private void sink(int i) {
      while (leftChild(i) < size) {
        int b = leftChild(i);
        if (rightChild(i) < size && compare(heap[rightChild(i)], heap[b]) < 0) b = rightChild(i);
        if (compare(heap[i], heap[b]) <= 0) break;
        swap(i, b); i = b;
      }
    }

    // <REF Q4>
    public T remove() {
      if (size == 0) throw new NoSuchElementException();
      T best = heap[0];               // save before overwriting
      heap[0] = heap[size - 1];       // last value moves to the root
      heap[size - 1] = null;          // no stale reference left behind
      size--;
      if (size > 0) sink(0);          // restore order from the top
      return best;
    }
    // </REF Q4>

    String show() { return Arrays.toString(Arrays.copyOf(heap, size)); }
  }

  static class IndexedHeap<T, P extends Comparable<P>> {
    private static class Entry<T, P> {
      T item; P priority;
      Entry(T item, P priority) { this.item = item; this.priority = priority; }
    }
    private Entry<T, P>[] heap;
    private int size;
    private Map<T, Integer> index = new HashMap<>();

    @SuppressWarnings("unchecked") IndexedHeap() { heap = (Entry<T, P>[]) new Entry[2]; }
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

    // <REF Q8>
    public void insert(T item, P priority) {
      if (item == null || priority == null) throw new IllegalArgumentException();
      if (index.containsKey(item)) throw new IllegalArgumentException();   // items are unique
      if (size == heap.length) heap = Arrays.copyOf(heap, 2 * heap.length);
      heap[size] = new Entry<>(item, priority);
      index.put(item, size);          // record the slot BEFORE swimming
      size++;
      swim(size - 1);
    }

    public T removeBest() {
      if (size == 0) throw new NoSuchElementException();
      T best = heap[0].item;
      swap(0, size - 1);              // best moves to the end; swap updates the map
      index.remove(best);
      heap[size - 1] = null;
      size--;
      if (size > 0) sink(0);
      return best;
    }
    // </REF Q8>

    void check() {
      if (index.size() != size) throw new AssertionError("index size");
      for (int k = 0; k < size; k++) {
        if (index.get(heap[k].item) != k) throw new AssertionError("slot");
        if (k > 0 && compare(k, (k - 1) / 2) < 0) throw new AssertionError("order");
      }
    }
  }

  public static void main(String[] args) {
    Random rnd = new Random(7);
    for (int t = 0; t < 500; t++) {
      ArrayHeap<Integer> h = new ArrayHeap<>();
      PriorityQueue<Integer> ref = new PriorityQueue<>();
      for (int o = 0; o < 150; o++) {
        if (ref.isEmpty() || rnd.nextInt(3) > 0) { int x = rnd.nextInt(50); h.insert(x); ref.add(x); }
        else if (!h.remove().equals(ref.remove())) throw new AssertionError("remove");
      }
      while (!ref.isEmpty()) if (!h.remove().equals(ref.remove())) throw new AssertionError("drain");
      try { h.remove(); throw new AssertionError("no NSEE"); } catch (NoSuchElementException e) {}
      IndexedHeap<Integer, Integer> ih = new IndexedHeap<>();
      Map<Integer, Integer> pr = new HashMap<>();
      for (int o = 0; o < 150; o++) {
        int item = rnd.nextInt(40);
        if (rnd.nextInt(3) > 0) {
          if (pr.containsKey(item)) { try { ih.insert(item, 1); throw new AssertionError("dup"); } catch (IllegalArgumentException e) {} }
          else { int p = rnd.nextInt(100); ih.insert(item, p); pr.put(item, p); }
        } else if (!pr.isEmpty()) {
          int min = Collections.min(pr.values());
          int got = ih.removeBest();
          if (pr.remove(got) != min) throw new AssertionError("best");
        }
        ih.check();
      }
    }
    ArrayHeap<Integer> tr = new ArrayHeap<>();
    for (int x : new int[]{5, 3, 8, 1, 9, 2}) tr.insert(x);
    System.out.println("trace heap after inserts: " + tr.show());
    tr.remove();
    System.out.println("trace heap after remove:  " + tr.show());
    System.out.println("Heaps OK");
  }
}
