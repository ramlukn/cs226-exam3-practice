import java.util.*;

public class OAMap<K, V> {
  private static class Entry<K, V> {
    K key; V value; boolean deleted;
    Entry(K key, V value) { this.key = key; this.value = value; }
  }
  private static final double MAX_LOAD_FACTOR = 0.5;
  private static final int[] PRIMES = {7, 17, 37, 79, 163};
  private int primeIndex;
  private Entry<K, V>[] slots;
  private int size;   // live entries
  private int used;   // live entries + tombstones

  @SuppressWarnings("unchecked")
  OAMap(int startIndex) { primeIndex = startIndex; slots = (Entry<K, V>[]) new Entry[PRIMES[startIndex]]; }

  private int indexFor(K key) { return Math.floorMod(key.hashCode(), slots.length); }

  private boolean holdsKey(int i, K key) {
    return slots[i] != null && !slots[i].deleted && slots[i].key.equals(key);
  }

  private void rehashIfNeeded() {
    if (used > MAX_LOAD_FACTOR * slots.length) {
      if (size > MAX_LOAD_FACTOR * slots.length) {
        int capacity = (primeIndex + 1 < PRIMES.length) ? PRIMES[++primeIndex] : 2 * slots.length + 1;
        rehash(capacity);
      } else {
        rehash(slots.length);
      }
    }
  }

  @SuppressWarnings("unchecked")
  private void rehash(int capacity) {
    Entry<K, V>[] old = slots;
    slots = (Entry<K, V>[]) new Entry[capacity];
    used = 0;
    for (Entry<K, V> e : old) {
      if (e != null && !e.deleted) { slots[probe(e.key)] = e; used++; }
    }
  }

  // <REF Q6>
  private int probe(K key) {
    int i = indexFor(key);
    int firstTombstone = -1;
    while (slots[i] != null) {                       // an empty slot ends the path
      if (slots[i].deleted) {
        if (firstTombstone == -1) firstTombstone = i; // remember only the first
      } else if (slots[i].key.equals(key)) {
        return i;                                    // live match
      }
      i = (i + 1) % slots.length;                    // linear step, wraps around
    }
    return (firstTombstone != -1) ? firstTombstone : i;
  }

  public boolean put(K key, V value) {
    if (key == null || value == null) throw new IllegalArgumentException();
    int i = probe(key);
    if (holdsKey(i, key)) {
      slots[i].value = value;                        // key exists: replace
      return false;
    }
    if (slots[i] == null) used++;                    // reusing a tombstone keeps used the same
    slots[i] = new Entry<>(key, value);
    size++;
    rehashIfNeeded();                                // after the new key is stored
    return true;
  }
  // </REF Q6>

  // <REF D4>
  public V get(K key) {
    if (key == null) throw new IllegalArgumentException();
    int i = probe(key);
    return holdsKey(i, key) ? slots[i].value : null;
  }

  public boolean remove(K key) {
    if (key == null) throw new IllegalArgumentException();
    int i = probe(key);
    if (!holdsKey(i, key)) return false;
    slots[i].deleted = true;       // tombstone: used stays the same
    size--;
    return true;
  }
  // </REF D4>

  String show() {
    StringBuilder sb = new StringBuilder("m=" + slots.length + " size=" + size + " used=" + used + " ");
    for (int i = 0; i < slots.length; i++) if (slots[i] != null) sb.append(i).append(':').append(slots[i].key).append(slots[i].deleted ? "†" : "").append(' ');
    return sb.toString();
  }

  public static void main(String[] args) {
    Random rnd = new Random(3);
    for (int t = 0; t < 400; t++) {
      OAMap<Integer, Integer> m = new OAMap<>(0);
      HashMap<Integer, Integer> ref = new HashMap<>();
      int ops = rnd.nextInt(300);
      for (int o = 0; o < ops; o++) {
        int k = rnd.nextInt(120) - 20;
        int op = rnd.nextInt(4);
        if (op < 2) { int v = rnd.nextInt(); if (m.put(k, v) != !ref.containsKey(k)) throw new AssertionError("put"); ref.put(k, v); }
        else if (op == 2) { if (m.remove(k) != (ref.remove(k) != null)) throw new AssertionError("rm"); }
        else { if (!Objects.equals(m.get(k), ref.get(k))) throw new AssertionError("get"); }
        if (m.used > m.slots.length / 2.0) throw new AssertionError("used");
      }
    }
    // the mock's Q3 traces: m = 7
    OAMap<Integer, String> m = new OAMap<>(0);
    for (int k : new int[]{9, 16, 5}) m.put(k, "x");
    m.remove(16);
    System.out.println("A after remove 16: " + m.show());
    m.put(23, "x");
    System.out.println("A after put 23:    " + m.show());
    m.put(2, "x");
    System.out.println("A after put 2:     " + m.show());
    OAMap<Integer, String> b = new OAMap<>(0);
    for (int k : new int[]{9, 16, 5}) b.put(k, "x");
    b.remove(9);
    b.put(12, "x");
    System.out.println("B after put 12:    " + b.show());
    System.out.println("OAMap OK");
  }
}
