import java.util.*;

public class OAMap<K, V> {
  private static class Entry<K, V> {
    K key; V value; boolean deleted;
    Entry(K key, V value) { this.key = key; this.value = value; }
  }
  private static final int[] PRIMES = {7, 17, 37, 79, 163};
  private int primeIndex;
  private Entry<K, V>[] slots;
  private int size;
  private int used;

  @SuppressWarnings("unchecked")
  OAMap() { slots = (Entry<K, V>[]) new Entry[PRIMES[0]]; }
  private int indexFor(K key) { return Math.floorMod(key.hashCode(), slots.length); }
  private boolean holdsKey(int i, K key) { return slots[i] != null && !slots[i].deleted && slots[i].key.equals(key); }
  private int probe(K key) {
    int i = indexFor(key), firstTombstone = -1;
    while (slots[i] != null) {
      if (slots[i].deleted) { if (firstTombstone == -1) firstTombstone = i; }
      else if (slots[i].key.equals(key)) return i;
      i = (i + 1) % slots.length;
    }
    return firstTombstone != -1 ? firstTombstone : i;
  }
  public boolean put(K key, V value) {
    int i = probe(key);
    if (holdsKey(i, key)) { slots[i].value = value; return false; }
    if (slots[i] == null) used++;
    slots[i] = new Entry<>(key, value);
    size++;
    rehashIfNeeded();
    return true;
  }
  public V get(K key) { int i = probe(key); return holdsKey(i, key) ? slots[i].value : null; }
  public boolean remove(K key) { int i = probe(key); if (!holdsKey(i, key)) return false; slots[i].deleted = true; size--; return true; }

  // <REF Q6>
  private void rehashIfNeeded() {
    if (used <= slots.length / 2.0) return;            // still under the limit
    if (size > slots.length / 2.0) {                   // really full: grow
      int capacity = (primeIndex + 1 < PRIMES.length)
          ? PRIMES[++primeIndex]
          : 2 * slots.length + 1;
      rehash(capacity);
    } else {
      rehash(slots.length);                            // mostly tombstones: same size
    }
  }

  @SuppressWarnings("unchecked")
  private void rehash(int capacity) {
    Entry<K, V>[] old = slots;
    slots = (Entry<K, V>[]) new Entry[capacity];       // indexFor now uses the new length
    used = 0;
    for (Entry<K, V> e : old) {                        // old-slot order
      if (e == null || e.deleted) continue;            // tombstones are dropped
      int i = indexFor(e.key);
      while (slots[i] != null) i = (i + 1) % slots.length;   // new table has no tombstones
      slots[i] = e;
      used++;
    }                                                  // size is unchanged; now used == size
  }
  // </REF Q6>

  public static void main(String[] args) {
    Random rnd = new Random(9);
    for (int t = 0; t < 400; t++) {
      OAMap<Integer, Integer> m = new OAMap<>();
      HashMap<Integer, Integer> ref = new HashMap<>();
      for (int o = 0; o < 400; o++) {
        int k = rnd.nextInt(400) - 50, op = rnd.nextInt(3);
        if (op == 0) { int v = rnd.nextInt(); if (m.put(k, v) == ref.containsKey(k)) throw new AssertionError("put"); ref.put(k, v); }
        else if (op == 1) { if (m.remove(k) != (ref.remove(k) != null)) throw new AssertionError("rm"); }
        else if (!Objects.equals(m.get(k), ref.get(k))) throw new AssertionError("get");
        if (m.used > m.slots.length / 2.0 || m.size != ref.size()) throw new AssertionError("inv");
      }
    }
    System.out.println("OAMap OK");
  }
}
