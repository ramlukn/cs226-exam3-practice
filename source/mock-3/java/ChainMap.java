import java.util.*;

public class ChainMap<K, V> {
  private static class Node<K, V> {
    K key; V value; Node<K, V> next;
    Node(K key, V value) { this.key = key; this.value = value; }
  }
  private static final double MAX_LOAD_FACTOR = 0.75;
  private static final int[] PRIMES = {7, 17, 37, 79, 163};
  private int primeIndex;
  private Node<K, V>[] buckets;
  private int size;

  @SuppressWarnings("unchecked")
  ChainMap() { buckets = (Node<K, V>[]) new Node[PRIMES[0]]; }

  private int indexFor(K key) { return Math.floorMod(key.hashCode(), buckets.length); }

  public boolean put(K key, V value) {
    if (key == null || value == null) throw new IllegalArgumentException();
    int i = indexFor(key);
    for (Node<K, V> curr = buckets[i]; curr != null; curr = curr.next) {
      if (curr.key.equals(key)) { curr.value = value; return false; }
    }
    Node<K, V> node = new Node<>(key, value);
    node.next = buckets[i];
    buckets[i] = node;
    size++;
    if ((double) size / buckets.length > MAX_LOAD_FACTOR) rehash();
    return true;
  }

  public boolean remove(K key) {
    int i = indexFor(key);
    Node<K, V> prev = null, curr = buckets[i];
    while (curr != null) {
      if (curr.key.equals(key)) {
        if (prev == null) buckets[i] = curr.next; else prev.next = curr.next;
        size--; return true;
      }
      prev = curr; curr = curr.next;
    }
    return false;
  }

  // <REF Q5>
  public V get(K key) {
    if (key == null) throw new IllegalArgumentException();
    int i = Math.floorMod(key.hashCode(), buckets.length);   // or indexFor(key)
    Node<K, V> curr = buckets[i];
    while (curr != null) {
      if (curr.key.equals(key)) return curr.value;
      curr = curr.next;
    }
    return null;                     // also covers an empty bucket
  }
  // </REF Q5>

  // <REF D2>
  @SuppressWarnings("unchecked")
  private void rehash() {
    Node<K, V>[] old = buckets;
    int capacity = (primeIndex + 1 < PRIMES.length)
        ? PRIMES[++primeIndex]
        : 2 * old.length + 1;
    buckets = (Node<K, V>[]) new Node[capacity];
    for (Node<K, V> head : old) {
      Node<K, V> curr = head;
      while (curr != null) {
        Node<K, V> next = curr.next;   // save before relinking
        int i = indexFor(curr.key);    // uses the NEW length
        curr.next = buckets[i];        // relink at the head
        buckets[i] = curr;
        curr = next;
      }
    }
  }
  // </REF D2>

  public Iterator<K> iterator() { return new KeyIterator(); }

  // <REF Q9>
  private class KeyIterator implements Iterator<K> {
    private Node<K, V> curr;   // the node next() returns, or null when done
    private int slot;          // the next bucket to look at

    KeyIterator() {
      advance();               // land on the first entry
    }

    private void advance() {
      if (curr != null) curr = curr.next;
      while (curr == null && slot < buckets.length) {
        curr = buckets[slot];
        slot++;
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
  // </REF Q9>

  int capacity() { return buckets.length; }
  int size() { return size; }

  public static void main(String[] args) {
    Random rnd = new Random(2);
    for (int t = 0; t < 400; t++) {
      ChainMap<Integer, Integer> m = new ChainMap<>();
      HashMap<Integer, Integer> ref = new HashMap<>();
      int ops = rnd.nextInt(300);
      for (int o = 0; o < ops; o++) {
        int k = rnd.nextInt(200) - 50;
        int op = rnd.nextInt(4);
        if (op < 2) { int v = rnd.nextInt(); if (m.put(k, v) != !ref.containsKey(k)) throw new AssertionError("put"); ref.put(k, v); }
        else if (op == 2) { if (m.remove(k) != (ref.remove(k) != null)) throw new AssertionError("rm"); }
        else { if (!Objects.equals(m.get(k), ref.get(k))) throw new AssertionError("get"); }
      }
      if (m.size() != ref.size()) throw new AssertionError("size");
      List<Integer> keys = new ArrayList<>();
      Iterator<Integer> it = m.iterator();
      while (it.hasNext()) keys.add(it.next());
      try { it.next(); throw new AssertionError("no NSEE"); } catch (NoSuchElementException e) {}
      Collections.sort(keys);
      List<Integer> rk = new ArrayList<>(ref.keySet()); Collections.sort(rk);
      if (!keys.equals(rk)) throw new AssertionError("iter");
      if ((double) m.size() / m.capacity() > 0.75) throw new AssertionError("load");
    }
    // the mock's trace check: 6 keys in 7 slots rehash to 17
    ChainMap<Integer, String> m = new ChainMap<>();
    for (int k : new int[]{3, 10, 17, 24, 5, 31}) m.put(k, "x");
    System.out.println("cap after 6 puts = " + m.capacity());
    System.out.println("ChainMap OK");
  }
}
