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
  T removeMin() { T b = heap[0].item; remove(b); return b; }
  private void swap(int i, int j) {
    Entry<T> t = heap[i]; heap[i] = heap[j]; heap[j] = t;
    where.put(heap[i].item, i); where.put(heap[j].item, j);
  }
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
  public void remove(T item) {
    Integer i = where.get(item);
    if (i == null) throw new IllegalArgumentException();
    int last = size - 1;
    swap(i, last);                 // item goes to the end; the last entry fills its slot
    where.remove(item);            // forget the removed item
    heap[last] = null;
    size--;
    if (i < size) {                // unless we removed the last slot itself,
      swim(i);                     // the moved entry may be smaller than its new parent
      sink(i);                     // or larger than its new children
    }
  }
  // </REF Q9>

  public static void main(String[] args) {
    Random rnd = new Random(9);
    for (int t = 0; t < 3000; t++) {
      IndexedPQ<Integer> pq = new IndexedPQ<>(50);
      Map<Integer, Integer> ref = new HashMap<>();
      for (int o = 0; o < 100; o++) {
        int c = rnd.nextInt(3);
        if (c == 0 && ref.size() < 50) { int x = rnd.nextInt(60); if (!ref.containsKey(x)) { int p = rnd.nextInt(40); pq.insert(x, p); ref.put(x, p); } }
        else if (c == 1 && !ref.isEmpty()) { int x = new ArrayList<>(ref.keySet()).get(rnd.nextInt(ref.size())); pq.remove(x); ref.remove(x); }
        else if (!ref.isEmpty()) { int min = Collections.min(ref.values()); int got = pq.removeMin(); if (ref.get(got) != min) throw new AssertionError("min"); ref.remove(got); }
        if (pq.size != ref.size() || pq.where.size() != ref.size()) throw new AssertionError("size");
        for (int i = 0; i < pq.size; i++) {
          if (pq.where.get(pq.heap[i].item) != i) throw new AssertionError("where");
          if (i > 0 && pq.heap[i].priority < pq.heap[(i - 1) / 2].priority) throw new AssertionError("order");
        }
      }
      try { pq.remove(-1); throw new AssertionError("no IAE"); } catch (IllegalArgumentException e) {}
    }
    System.out.println("IndexedPQ OK");
  }
}
