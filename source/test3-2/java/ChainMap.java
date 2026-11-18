import java.util.*;

public class ChainMap<K, V> {
  private static class Node<K, V> {
    K key; V value; Node<K, V> next;
    Node(K key, V value) { this.key = key; this.value = value; }
  }
  private static final int[] PRIMES = {7, 17, 37, 79, 163, 331};
  private int primeIndex;
  private Node<K, V>[] buckets;
  private int size;

  @SuppressWarnings("unchecked") ChainMap() { buckets = (Node<K, V>[]) new Node[PRIMES[0]]; }
  private int indexFor(K key) { return Math.floorMod(key.hashCode(), buckets.length); }
  @SuppressWarnings("unchecked") private void rehash() {
    Node<K, V>[] old = buckets;
    buckets = (Node<K, V>[]) new Node[primeIndex + 1 < PRIMES.length ? PRIMES[++primeIndex] : 2 * old.length + 1];
    for (Node<K, V> b : old) for (Node<K, V> c = b, nx; c != null; c = nx) { nx = c.next; int i = indexFor(c.key); c.next = buckets[i]; buckets[i] = c; }
  }
  V get(K key) {
    for (Node<K, V> c = buckets[indexFor(key)]; c != null; c = c.next) if (c.key.equals(key)) return c.value;
    return null;
  }

  // <REF Q6>
  public V put(K key, V value) {
    if (key == null || value == null) throw new IllegalArgumentException();
    int i = indexFor(key);
    for (Node<K, V> curr = buckets[i]; curr != null; curr = curr.next) {
      if (curr.key.equals(key)) {          // already there: replace, size unchanged
        V old = curr.value;
        curr.value = value;
        return old;
      }
    }
    Node<K, V> n = new Node<>(key, value);
    n.next = buckets[i];                   // new node at the head of the chain
    buckets[i] = n;
    size++;
    if (size > 0.75 * buckets.length) {   // after adding, check the load factor
      rehash();
    }
    return null;
  }
  // </REF Q6>

  public static void main(String[] args) {
    Random rnd = new Random(26);
    for (int t = 0; t < 1000; t++) {
      ChainMap<Integer, Integer> m = new ChainMap<>();
      Map<Integer, Integer> ref = new HashMap<>();
      int n = rnd.nextInt(300);
      for (int o = 0; o < n; o++) {
        int k = rnd.nextInt(400) - 100, v = rnd.nextInt();
        if (!Objects.equals(m.put(k, v), ref.put(k, v))) throw new AssertionError("put");
        if (m.size != ref.size() || m.size > 0.75 * m.buckets.length) throw new AssertionError("size/load");
      }
      for (int k : ref.keySet()) if (!m.get(k).equals(ref.get(k))) throw new AssertionError("get");
      int c = 0; for (Node<Integer, Integer> b : m.buckets) for (Node<Integer, Integer> x = b; x != null; x = x.next) c++;
      if (c != ref.size()) throw new AssertionError("count");
    }
    System.out.println("ChainMap OK");
  }
}
