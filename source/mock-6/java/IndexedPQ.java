import java.util.*;

public class IndexedPQ<T> {
  private static class Entry<T> {
    T item; int priority;
    Entry(T item, int priority) { this.item = item; this.priority = priority; }
  }
  private Entry<T>[] heap;
  private int size;
  private Map<T, Integer> where = new HashMap<>();

  @SuppressWarnings("unchecked") IndexedPQ(int cap) { heap = (Entry<T>[]) new Entry[cap]; }
  void insert(T item, int p) { heap[size] = new Entry<>(item, p); where.put(item, size); size++; swim(size - 1); }
  T removeMin() { T b = heap[0].item; swap(0, size - 1); where.remove(b); heap[--size] = null; if (size > 0) sink(0); return b; }
  private void swim(int i) {
    while (i > 0 && heap[i].priority < heap[(i - 1) / 2].priority) { swap(i, (i - 1) / 2); i = (i - 1) / 2; }
  }
  private void sink(int i) {
    while (2 * i + 1 < size) {
      int b = 2 * i + 1;
      if (b + 1 < size && heap[b + 1].priority < heap[b].priority) b++;
      if (heap[i].priority <= heap[b].priority) break;
      swap(i, b); i = b;
    }
  }

  // <REF Q9>
  private void swap(int i, int j) {
    Entry<T> t = heap[i]; heap[i] = heap[j]; heap[j] = t;
    where.put(heap[i].item, i);              // both moved entries get their new index
    where.put(heap[j].item, j);
  }

  public void changePriority(T item, int priority) {
    Integer i = where.get(item);             // O(1): no searching the heap
    if (i == null) throw new IllegalArgumentException();
    int old = heap[i].priority;
    heap[i].priority = priority;
    if (priority < old) swim(i);             // smaller is better in a min-heap: move up
    else sink(i);                            // larger: move down
  }
  // </REF Q9>

  public static void main(String[] args) {
    Random rnd = new Random(9);
    for (int t = 0; t < 2000; t++) {
      IndexedPQ<Integer> pq = new IndexedPQ<>(40);
      Map<Integer, Integer> ref = new HashMap<>();
      for (int o = 0; o < 80; o++) {
        int c = rnd.nextInt(3);
        if (c == 0 && ref.size() < 40) { int x = rnd.nextInt(60); if (!ref.containsKey(x)) { int p = rnd.nextInt(50); pq.insert(x, p); ref.put(x, p); } }
        else if (c == 1 && !ref.isEmpty()) { int x = new ArrayList<>(ref.keySet()).get(rnd.nextInt(ref.size())); int p = rnd.nextInt(50); pq.changePriority(x, p); ref.put(x, p); }
        else if (!ref.isEmpty()) { int min = Collections.min(ref.values()); int got = pq.removeMin(); if (ref.get(got) != min) throw new AssertionError("min"); ref.remove(got); }
        for (int i = 0; i < pq.size; i++) {
          if (pq.where.get(pq.heap[i].item) != i) throw new AssertionError("where");
          if (i > 0 && pq.heap[i].priority < pq.heap[(i - 1) / 2].priority) throw new AssertionError("order");
        }
      }
      try { pq.changePriority(-5, 1); throw new AssertionError("no IAE"); } catch (IllegalArgumentException e) {}
    }
    System.out.println("IndexedPQ OK");
  }
}
