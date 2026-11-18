import java.util.*;

public class MinHeap<T extends Comparable<T>> {
  private T[] heap;
  private int size;

  @SuppressWarnings("unchecked") MinHeap() { heap = (T[]) new Comparable[1]; }
  private void swap(int i, int j) { T t = heap[i]; heap[i] = heap[j]; heap[j] = t; }
  Object at(int i) { return heap[i]; }
  T remove() {
    T b = heap[0]; heap[0] = heap[size - 1]; heap[--size] = null; int i = 0;
    while (2 * i + 1 < size) { int c = 2 * i + 1; if (c + 1 < size && heap[c + 1].compareTo(heap[c]) < 0) c++; if (heap[i].compareTo(heap[c]) <= 0) break; swap(i, c); i = c; }
    return b;
  }

  // <REF Q7>
  public void insert(T x) {
    if (x == null) throw new IllegalArgumentException();
    if (size == heap.length) {
      heap = Arrays.copyOf(heap, 2 * heap.length);   // full: double the array
    }
    heap[size] = x;                                   // new value at the first free slot
    size++;
    swim(size - 1);
  }

  private void swim(int i) {
    while (i > 0) {
      int parent = (i - 1) / 2;
      if (heap[i].compareTo(heap[parent]) >= 0) break;   // parent is no bigger: done
      swap(i, parent);
      i = parent;
    }
  }
  // </REF Q7>

  // <REF Q8>
  public static <T extends Comparable<T>> boolean isMinHeap(T[] a, int size) {
    if (a == null || size < 0 || size > a.length) throw new IllegalArgumentException();
    for (int i = 1; i < size; i++) {                  // every non-root node...
      if (a[i].compareTo(a[(i - 1) / 2]) < 0) {       // ...must be at least its parent
        return false;
      }
    }
    return true;                                      // size 0 or 1: trivially a heap
  }
  // </REF Q8>

  public static void main(String[] args) {
    Random rnd = new Random(27);
    for (int t = 0; t < 3000; t++) {
      MinHeap<Integer> h = new MinHeap<>();
      PriorityQueue<Integer> ref = new PriorityQueue<>();
      int n = rnd.nextInt(60);
      for (int o = 0; o < n; o++) { int x = rnd.nextInt(30); h.insert(x); ref.add(x); }
      Integer[] arr = new Integer[h.size]; for (int i = 0; i < h.size; i++) arr[i] = (Integer) h.at(i);
      if (!isMinHeap(arr, h.size)) throw new AssertionError("isMinHeap false negative");
      while (!ref.isEmpty()) if (!h.remove().equals(ref.remove())) throw new AssertionError("order");
      Integer[] r = new Integer[rnd.nextInt(12) + 1];
      for (int i = 0; i < r.length; i++) r[i] = rnd.nextInt(5);
      int sz = rnd.nextInt(r.length + 1);
      boolean want = true; for (int i = 1; i < sz; i++) if (r[i] < r[(i - 1) / 2]) want = false;
      if (isMinHeap(r, sz) != want) throw new AssertionError("isMinHeap");
    }
    try { new MinHeap<Integer>().insert(null); throw new AssertionError("no IAE"); } catch (IllegalArgumentException e) {}
    System.out.println("MinHeap OK");
  }
}
