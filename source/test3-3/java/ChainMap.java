import java.util.*;

public class ChainMap<K, V> implements Iterable<K> {
  private static class Node<K, V> {
    K key; V value; Node<K, V> next;
    Node(K key, V value) { this.key = key; this.value = value; }
  }
  private static final int[] PRIMES = {7, 17, 37, 79, 163};
  private int primeIndex;
  private Node<K, V>[] buckets;
  private int size;

  @SuppressWarnings("unchecked")
  ChainMap() { buckets = (Node<K, V>[]) new Node[PRIMES[0]]; }
  private int indexFor(K key) { return Math.floorMod(key.hashCode(), buckets.length); }

  public void put(K key, V value) {
    int i = indexFor(key);
    for (Node<K, V> c = buckets[i]; c != null; c = c.next) if (c.key.equals(key)) { c.value = value; return; }
    Node<K, V> n = new Node<>(key, value); n.next = buckets[i]; buckets[i] = n; size++;
    if ((double) size / buckets.length > 0.75) rehash();
  }
  public V get(K key) {
    for (Node<K, V> c = buckets[indexFor(key)]; c != null; c = c.next) if (c.key.equals(key)) return c.value;
    return null;
  }

  // <REF Q7>
  @SuppressWarnings("unchecked")
  private void rehash() {
    Node<K, V>[] old = buckets;
    int capacity = (primeIndex + 1 < PRIMES.length)
        ? PRIMES[++primeIndex]
        : 2 * old.length + 1;
    buckets = (Node<K, V>[]) new Node[capacity];   // indexFor now uses the new length
    for (int b = 0; b < old.length; b++) {
      Node<K, V> curr = old[b];
      while (curr != null) {
        Node<K, V> next = curr.next;               // save it: relinking overwrites curr.next
        int i = indexFor(curr.key);
        curr.next = buckets[i];                    // insert at the head of the new bucket
        buckets[i] = curr;
        curr = next;
      }
    }                                              // size is unchanged: same nodes, new places
  }
  // </REF Q7>

  public Iterator<K> iterator() { return new ReverseKeyIterator(); }

  // <REF Q4>
  private class ReverseKeyIterator implements Iterator<K> {
    private Node<K, V> curr;                 // node next() returns; null means done
    private int slot = buckets.length - 1;   // next bucket to examine, counting DOWN

    ReverseKeyIterator() {
      advance();                             // land on the first key
    }

    private void advance() {
      if (curr != null) curr = curr.next;    // same chain: step along it
      while (curr == null && slot >= 0) {    // chain over: find the next non-empty bucket below
        curr = buckets[slot];
        slot--;
      }
    }

    @Override
    public boolean hasNext() {
      return curr != null;
    }

    @Override
    public K next() {
      if (!hasNext()) throw new NoSuchElementException();
      K key = curr.key;
      advance();
      return key;
    }
  }
  // </REF Q4>

  public static void main(String[] args) {
    Random rnd = new Random(12);
    for (int t = 0; t < 400; t++) {
      ChainMap<Integer, Integer> m = new ChainMap<>();
      HashMap<Integer, Integer> ref = new HashMap<>();
      int n = rnd.nextInt(200);
      for (int o = 0; o < n; o++) { int k = rnd.nextInt(300) - 60, v = rnd.nextInt(); m.put(k, v); ref.put(k, v); }
      for (int k : ref.keySet()) if (!m.get(k).equals(ref.get(k))) throw new AssertionError("get");
      List<Integer> got = new ArrayList<>(), want = new ArrayList<>();
      Iterator<Integer> it = m.iterator();
      while (it.hasNext()) { it.hasNext(); got.add(it.next()); }
      try { it.next(); throw new AssertionError("no NSEE"); } catch (NoSuchElementException e) {}
      for (int b = m.buckets.length - 1; b >= 0; b--) for (Node<Integer, Integer> c = m.buckets[b]; c != null; c = c.next) want.add(c.key);
      if (!got.equals(want)) throw new AssertionError("order");
      if (m.size != ref.size() || (double) m.size / m.buckets.length > 0.75) throw new AssertionError("size");
    }
    System.out.println("ChainMap OK");
  }
}
