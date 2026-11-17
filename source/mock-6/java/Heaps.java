import java.util.*;

public class Heaps {
  static class ArrayHeap<T extends Comparable<T>> {
    private T[] heap;
    private int size;
    private int compare(T a, T b) { return a.compareTo(b); }
    private void swap(int i, int j) { T t = heap[i]; heap[i] = heap[j]; heap[j] = t; }
    private void sink(int i) {
      while (2 * i + 1 < size) {
        int b = 2 * i + 1;
        if (b + 1 < size && compare(heap[b + 1], heap[b]) < 0) b++;
        if (compare(heap[i], heap[b]) <= 0) break;
        swap(i, b); i = b;
      }
    }

    // <REF Q7>
    public ArrayHeap(T[] items) {
      if (items == null) throw new IllegalArgumentException();
      heap = Arrays.copyOf(items, Math.max(1, items.length));   // copy: don't change the caller's array
      size = items.length;
      for (int i = size / 2 - 1; i >= 0; i--) {                 // last internal node up to the root
        sink(i);
      }
    }
    // </REF Q7>

    T remove() { T b = heap[0]; heap[0] = heap[size - 1]; heap[size - 1] = null; size--; if (size > 0) sink(0); return b; }
  }

  // <REF Q8>
  public static List<Integer> mergeSorted(int[][] lists) {
    List<Integer> out = new ArrayList<>();
    // each entry is {value, which list, position in that list}, smallest value first
    PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> Integer.compare(x[0], y[0]));
    for (int r = 0; r < lists.length; r++) {
      if (lists[r].length > 0) pq.add(new int[]{lists[r][0], r, 0});   // first of every non-empty list
    }
    while (!pq.isEmpty()) {
      int[] e = pq.remove();                      // the smallest remaining value overall
      out.add(e[0]);
      int r = e[1], next = e[2] + 1;
      if (next < lists[r].length) {
        pq.add(new int[]{lists[r][next], r, next});   // replace it with the next one from the same list
      }
    }
    return out;
  }
  // </REF Q8>

  public static void main(String[] args) {
    Random rnd = new Random(14);
    for (int t = 0; t < 2000; t++) {
      int n = rnd.nextInt(30);
      Integer[] a = new Integer[n];
      for (int i = 0; i < n; i++) a[i] = rnd.nextInt(20);
      Integer[] copy = a.clone();
      ArrayHeap<Integer> h = new ArrayHeap<>(a);
      if (!Arrays.equals(a, copy)) throw new AssertionError("mutated");
      for (int i = 1; i < h.size; i++) if (h.heap[i] < h.heap[(i - 1) / 2]) throw new AssertionError("order");
      Integer[] s = copy.clone(); Arrays.sort(s);
      for (int i = 0; i < n; i++) if (!h.remove().equals(s[i])) throw new AssertionError("drain");
      int k = rnd.nextInt(6);
      int[][] lists = new int[k][];
      List<Integer> all = new ArrayList<>();
      for (int r = 0; r < k; r++) { int len = rnd.nextInt(6); lists[r] = new int[len]; for (int j = 0; j < len; j++) { lists[r][j] = rnd.nextInt(30); all.add(lists[r][j]); } Arrays.sort(lists[r]); }
      Collections.sort(all);
      if (!mergeSorted(lists).equals(all)) throw new AssertionError("merge");
    }
    System.out.println("Heaps OK");
  }
}
