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

  private void rehashIfNeeded() {
    if (used <= slots.length / 2.0) return;
    rehash(size > slots.length / 2.0 ? (primeIndex + 1 < PRIMES.length ? PRIMES[++primeIndex] : 2 * slots.length + 1) : slots.length);
  }
  @SuppressWarnings("unchecked")
  private void rehash(int capacity) {
    Entry<K, V>[] old = slots;
    slots = (Entry<K, V>[]) new Entry[capacity];
    used = 0;
    for (Entry<K, V> e : old) {
      if (e == null || e.deleted) continue;
      int i = indexFor(e.key);
      while (slots[i] != null) i = (i + 1) % slots.length;
      slots[i] = e; used++;
    }
  }

  // <REF Q6>
  public V put(K key, V value) {
    if (key == null || value == null) throw new IllegalArgumentException();
    int i = indexFor(key);
    int firstTombstone = -1;
    while (slots[i] != null) {                       // only an empty slot ends the search
      if (slots[i].deleted) {
        if (firstTombstone == -1) firstTombstone = i; // remember the first one, keep going
      } else if (slots[i].key.equals(key)) {
        V old = slots[i].value;                      // key already here: replace
        slots[i].value = value;
        return old;
      }
      i = (i + 1) % slots.length;
    }
    if (firstTombstone != -1) {
      i = firstTombstone;                            // reuse it: used stays the same
    } else {
      used++;                                        // filling an empty slot
    }
    slots[i] = new Entry<>(key, value);
    size++;
    rehashIfNeeded();                                // after the new key is stored
    return null;
  }
  // </REF Q6>

  public V get(K key) {
    int i = indexFor(key);
    while (slots[i] != null) { if (!slots[i].deleted && slots[i].key.equals(key)) return slots[i].value; i = (i + 1) % slots.length; }
    return null;
  }
  public boolean remove(K key) {
    int i = indexFor(key);
    while (slots[i] != null) { if (!slots[i].deleted && slots[i].key.equals(key)) { slots[i].deleted = true; size--; return true; } i = (i + 1) % slots.length; }
    return false;
  }
  String show() {
    StringBuilder sb = new StringBuilder("m=" + slots.length + " size=" + size + " used=" + used + " ");
    for (int i = 0; i < slots.length; i++) if (slots[i] != null) sb.append(i).append(':').append(slots[i].key).append(slots[i].deleted ? "†" : "").append(' ');
    return sb.toString();
  }

  public static void main(String[] args) {
    Random rnd = new Random(13);
    for (int t = 0; t < 400; t++) {
      OAMap<Integer, Integer> m = new OAMap<>();
      HashMap<Integer, Integer> ref = new HashMap<>();
      for (int o = 0; o < 400; o++) {
        int k = rnd.nextInt(300) - 50, op = rnd.nextInt(3);
        if (op == 0) { int v = rnd.nextInt(); if (!Objects.equals(m.put(k, v), ref.put(k, v))) throw new AssertionError("put"); }
        else if (op == 1) { if (m.remove(k) != (ref.remove(k) != null)) throw new AssertionError("rm"); }
        else if (!Objects.equals(m.get(k), ref.get(k))) throw new AssertionError("get");
        if (m.size != ref.size() || m.used > m.slots.length / 2.0) throw new AssertionError("inv");
        int live = 0, nonNull = 0;
        for (Entry<Integer, Integer> e : m.slots) if (e != null) { nonNull++; if (!e.deleted) live++; }
        if (live != m.size || nonNull != m.used) throw new AssertionError("counts");
      }
    }
    OAMap<Integer, String> m = new OAMap<>();
    m.put(5, "x"); m.put(12, "x"); m.put(19, "x");
    System.out.println("after 5,12,19:   " + m.show());
    m.remove(12); m.remove(5);
    System.out.println("after removes:   " + m.show());
    m.put(26, "x");
    System.out.println("after put 26:    " + m.show());
    m.put(1, "x");
    System.out.println("after put 1:     " + m.show());
    System.out.println("OAMap OK");
  }
}
