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
      else if (slots[i].key.equals(key)) { V old = slots[i].value; slots[i].value = value; return old; }
      i = (i + 1) % slots.length;
    }
    if (tomb >= 0) slots[tomb] = new Entry<>(key, value); else { slots[i] = new Entry<>(key, value); used++; }
    size++;
    if (used > slots.length / 2) rehash(size > slots.length / 2 ? 2 * slots.length + 1 : slots.length);
    return null;
  }
  @SuppressWarnings("unchecked") private void rehash(int m) {
    Entry<K, V>[] old = slots; slots = (Entry<K, V>[]) new Entry[m]; size = 0; used = 0;
    for (Entry<K, V> e : old) if (e != null && !e.deleted) put(e.key, e.value);
  }

  // <REF Q6>
  public V get(K key) {
    if (key == null) throw new IllegalArgumentException();
    int i = indexFor(key);
    while (slots[i] != null) {                       // only an empty slot ends the search
      if (!slots[i].deleted && slots[i].key.equals(key)) return slots[i].value;
      i = (i + 1) % slots.length;                    // tombstone or other key: keep going
    }
    return null;
  }

  public V remove(K key) {
    if (key == null) throw new IllegalArgumentException();
    int i = indexFor(key);
    while (slots[i] != null) {
      if (!slots[i].deleted && slots[i].key.equals(key)) {
        V old = slots[i].value;
        slots[i].deleted = true;                     // tombstone, NOT null: keeps later probe paths intact
        size--;                                      // used stays the same: the slot is still taken
        return old;
      }
      i = (i + 1) % slots.length;
    }
    return null;
  }
  // </REF Q6>

  public static void main(String[] args) {
    Random rnd = new Random(6);
    for (int t = 0; t < 2000; t++) {
      OAMap<Integer, Integer> m = new OAMap<>(7);
      Map<Integer, Integer> ref = new HashMap<>();
      for (int o = 0; o < 200; o++) {
        int k = rnd.nextInt(40) - 10, c = rnd.nextInt(3);
        if (c == 0) { int v = rnd.nextInt(); if (!Objects.equals(m.put(k, v), ref.put(k, v))) throw new AssertionError("put"); }
        else if (c == 1) { if (!Objects.equals(m.remove(k), ref.remove(k))) throw new AssertionError("remove"); }
        else { if (!Objects.equals(m.get(k), ref.get(k))) throw new AssertionError("get"); }
        if (m.size != ref.size()) throw new AssertionError("size");
        int u = 0; for (Entry<Integer, Integer> e : m.slots) if (e != null) u++;
        if (u != m.used) throw new AssertionError("used");
      }
    }
    System.out.println("OAMap OK");
  }
}
