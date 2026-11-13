import java.util.*;

public class OAMap<K, V> implements Iterable<V> {
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
    if (used > slots.length / 2.0) {
      if (size > slots.length / 2.0) rehash(primeIndex + 1 < PRIMES.length ? PRIMES[++primeIndex] : 2 * slots.length + 1);
      else rehash(slots.length);
    }
    return true;
  }

  @SuppressWarnings("unchecked")
  private void rehash(int capacity) {
    Entry<K, V>[] old = slots;
    slots = (Entry<K, V>[]) new Entry[capacity];
    used = 0;
    for (Entry<K, V> e : old) if (e != null && !e.deleted) { slots[probe(e.key)] = e; used++; }
  }

  // <REF Q6>
  private int find(K key) {
    int i = indexFor(key);
    while (slots[i] != null) {                 // only an empty slot ends the search
      if (!slots[i].deleted && slots[i].key.equals(key)) return i;
      i = (i + 1) % slots.length;              // tombstone or other key: keep going
    }
    return -1;
  }

  public boolean containsKey(K key) {
    if (key == null) throw new IllegalArgumentException();
    return find(key) != -1;
  }

  public V remove(K key) {
    if (key == null) throw new IllegalArgumentException();
    int i = find(key);
    if (i == -1) return null;
    V old = slots[i].value;
    slots[i].deleted = true;                   // tombstone, NOT null
    size--;                                    // used stays the same
    return old;
  }
  // </REF Q6>

  public Iterator<V> iterator() { return new ValueIterator(); }

  // <REF Q7>
  private class ValueIterator implements Iterator<V> {
    private int i;                         // the slot next() returns from

    ValueIterator() {
      skip();                              // land on the first live entry
    }

    private void skip() {                  // move past empty slots AND tombstones
      while (i < slots.length && (slots[i] == null || slots[i].deleted)) i++;
    }

    @Override
    public boolean hasNext() {
      return i < slots.length;
    }

    @Override
    public V next() {
      if (!hasNext()) throw new NoSuchElementException();
      V value = slots[i].value;
      i++;
      skip();
      return value;
    }
  }
  // </REF Q7>

  String show() {
    StringBuilder sb = new StringBuilder("m=" + slots.length + " size=" + size + " used=" + used + " ");
    for (int i = 0; i < slots.length; i++) if (slots[i] != null) sb.append(i).append(':').append(slots[i].key).append(slots[i].deleted ? "†" : "").append(' ');
    return sb.toString();
  }

  public static void main(String[] args) {
    Random rnd = new Random(3);
    for (int t = 0; t < 400; t++) {
      OAMap<Integer, Integer> m = new OAMap<>();
      HashMap<Integer, Integer> ref = new HashMap<>();
      for (int o = 0; o < 300; o++) {
        int k = rnd.nextInt(120) - 20, op = rnd.nextInt(3);
        if (op == 0) { int v = rnd.nextInt(); m.put(k, v); ref.put(k, v); }
        else if (op == 1) { if (!Objects.equals(m.remove(k), ref.remove(k))) throw new AssertionError("rm"); }
        else { if (m.containsKey(k) != ref.containsKey(k)) throw new AssertionError("contains"); }
      }
      List<Integer> vs = new ArrayList<>();
      Iterator<Integer> it = m.iterator();
      while (it.hasNext()) { it.hasNext(); vs.add(it.next()); }
      try { it.next(); throw new AssertionError("no NSEE"); } catch (NoSuchElementException e) {}
      List<Integer> rv = new ArrayList<>(ref.values());
      Collections.sort(vs); Collections.sort(rv);
      if (!vs.equals(rv)) throw new AssertionError("iter");
    }
    OAMap<Integer, String> m = new OAMap<>();
    for (int k : new int[]{3, 10, 17}) m.put(k, "x");
    m.remove(10);
    System.out.println("after remove 10: " + m.show());
    m.put(24, "x");
    System.out.println("after put 24:    " + m.show());
    m.put(31, "x");
    System.out.println("after put 31:    " + m.show());
    System.out.println("OAMap OK");
  }
}
