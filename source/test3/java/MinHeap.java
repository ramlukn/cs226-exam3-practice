import java.util.*;

public class MinHeap<T extends Comparable<T>> {
  private T[] heap;
  private int size;

  @SuppressWarnings("unchecked") MinHeap(int cap) { heap = (T[]) new Comparable[cap]; }
  void insert(T x) {
    heap[size] = x; int i = size++;
    while (i > 0 && heap[i].compareTo(heap[(i - 1) / 2]) < 0) { swap(i, (i - 1) / 2); i = (i - 1) / 2; }
  }
  private void swap(int i, int j) { T t = heap[i]; heap[i] = heap[j]; heap[j] = t; }
  boolean slotEmpty(int i) { return heap[i] == null; }
  int capacity() { return heap.length; }

  // <REF Q8>
  public T remove() {
    if (size == 0) throw new NoSuchElementException();
    T best = heap[0];
    heap[0] = heap[size - 1];        // last value moves to the root
    heap[size - 1] = null;           // no stale reference
    size--;
    sink(0);
    return best;
  }

  private void sink(int i) {
    while (2 * i + 1 < size) {                         // i has at least a left child
      int c = 2 * i + 1;
      if (c + 1 < size && heap[c + 1].compareTo(heap[c]) < 0) c++;   // the smaller child
      if (heap[i].compareTo(heap[c]) <= 0) break;      // already in order
      swap(i, c);
      i = c;
    }
  }
  // </REF Q8>

  public static void main(String[] args) {
    Random rnd = new Random(8);
    for (int t = 0; t < 3000; t++) {
      MinHeap<Integer> h = new MinHeap<>(100);
      PriorityQueue<Integer> ref = new PriorityQueue<>();
      for (int o = 0; o < 80; o++) {
        if (ref.isEmpty() || rnd.nextInt(3) > 0) { int x = rnd.nextInt(30); h.insert(x); ref.add(x); }
        else if (!h.remove().equals(ref.remove())) throw new AssertionError("remove");
        for (int i = h.size; i < h.capacity(); i++) if (!h.slotEmpty(i)) throw new AssertionError("stale");
      }
      while (!ref.isEmpty()) if (!h.remove().equals(ref.remove())) throw new AssertionError("drain");
      try { h.remove(); throw new AssertionError("no NSEE"); } catch (NoSuchElementException e) {}
    }
    System.out.println("MinHeap OK");
  }
}
