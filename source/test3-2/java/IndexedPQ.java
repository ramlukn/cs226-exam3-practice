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
  public void insert(T item, int priority) {
    if (item == null || where.containsKey(item)) throw new IllegalArgumentException();
    heap[size] = new Entry<>(item, priority);
    where.put(item, size);         // record its index BEFORE swim (swim's swaps read the map's entries)
    size++;
    swim(size - 1);
  }

  public T removeMin() {
    if (size == 0) throw new NoSuchElementException();
    T best = heap[0].item;
    swap(0, size - 1);             // min goes to the end; last entry to the root
    where.remove(best);            // AFTER the swap, which would have re-added it
    heap[size - 1] = null;
    size--;
    if (size > 0) sink(0);
    return best;
  }
  // </REF Q9>

  public static void main(String[] args) {
    Random rnd = new Random(28);
    for (int t = 0; t < 3000; t++) {
      IndexedPQ<Integer> pq = new IndexedPQ<>(60);
      Map<Integer, Integer> ref = new HashMap<>();
      for (int o = 0; o < 100; o++) {
        if (rnd.nextInt(3) > 0 && ref.size() < 60) {
          int x = rnd.nextInt(80), p = rnd.nextInt(40);
          if (ref.containsKey(x)) { try { pq.insert(x, p); throw new AssertionError("dup"); } catch (IllegalArgumentException e) {} }
          else { pq.insert(x, p); ref.put(x, p); }
        } else if (!ref.isEmpty()) {
          int min = Collections.min(ref.values()); int got = pq.removeMin();
          if (ref.get(got) != min) throw new AssertionError("min"); ref.remove(got);
        }
        if (pq.where.size() != ref.size()) throw new AssertionError("where size");
        for (int i = 0; i < pq.size; i++) if (pq.where.get(pq.heap[i].item) != i) throw new AssertionError("where");
      }
      while (!ref.isEmpty()) ref.remove(pq.removeMin());
      try { pq.removeMin(); throw new AssertionError("no NSEE"); } catch (NoSuchElementException e) {}
    }
    System.out.println("IndexedPQ OK");
  }
}
