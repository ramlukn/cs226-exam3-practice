import java.util.*;

public class OAMap<K, V> {
  private static class Entry<K, V> {
    K key; V value; boolean deleted;
    Entry(K key, V value) { this.key = key; this.value = value; }
  }
  private Entry<K, V>[] slots;
  private int size, used;

  @SuppressWarnings("unchecked") OAMap(int m) { slots = (Entry<K, V>[]) new Entry[m]; }
  private int indexFor(K key) { return Math.floorMod(key.hashCode(), slots.length); }
  V put(K key, V value) {
    int i = indexFor(key), tomb = -1;
    while (slots[i] != null) {
      if (slots[i].deleted) { if (tomb < 0) tomb = i; }
      else if (slots[i].key.equals(key)) { V o = slots[i].value; slots[i].value = value; return o; }
      i = (i + 1) % slots.length;
    }
    if (tomb >= 0) slots[tomb] = new Entry<>(key, value); else { slots[i] = new Entry<>(key, value); used++; }
    size++;
    if (used > slots.length / 2) rehash(size > slots.length / 2 ? 2 * slots.length + 1 : slots.length);
    return null;
  }
  V get(K key) {
    for (int i = indexFor(key); slots[i] != null; i = (i + 1) % slots.length)
      if (!slots[i].deleted && slots[i].key.equals(key)) return slots[i].value;
    return null;
  }
  V remove(K key) {
    for (int i = indexFor(key); slots[i] != null; i = (i + 1) % slots.length)
      if (!slots[i].deleted && slots[i].key.equals(key)) { slots[i].deleted = true; size--; return slots[i].value; }
    return null;
  }

  // <REF Q6>
  @SuppressWarnings("unchecked")
  private void rehash(int newCapacity) {
    Entry<K, V>[] old = slots;
    slots = (Entry<K, V>[]) new Entry[newCapacity];   // indexFor now uses the new length
    for (int j = 0; j < old.length; j++) {
      Entry<K, V> e = old[j];
      if (e == null || e.deleted) continue;           // tombstones are dropped
      int i = indexFor(e.key);
      while (slots[i] != null) {                      // new table has no tombstones:
        i = (i + 1) % slots.length;                   // just find the first empty slot
      }
      slots[i] = e;                                   // reuse the entry object
    }
    used = size;                                      // no tombstones left; size unchanged
  }
  // </REF Q6>

  public static void main(String[] args) {
    Random rnd = new Random(36);
    for (int t = 0; t < 2000; t++) {
      OAMap<Integer, Integer> m = new OAMap<>(7);
      Map<Integer, Integer> ref = new HashMap<>();
      for (int o = 0; o < 200; o++) {
        int k = rnd.nextInt(60) - 15, c = rnd.nextInt(3);
        if (c == 0) { int v = rnd.nextInt(); if (!Objects.equals(m.put(k, v), ref.put(k, v))) throw new AssertionError("put"); }
        else if (c == 1) { if (!Objects.equals(m.remove(k), ref.remove(k))) throw new AssertionError("remove"); }
        else if (!Objects.equals(m.get(k), ref.get(k))) throw new AssertionError("get");
        int u = 0, s = 0; for (Entry<Integer, Integer> e : m.slots) if (e != null) { u++; if (!e.deleted) s++; }
        if (u != m.used || s != m.size || s != ref.size()) throw new AssertionError("counts");
        if (m.used > m.slots.length / 2) throw new AssertionError("load");
      }
    }
    System.out.println("OAMap OK");
  }
}
