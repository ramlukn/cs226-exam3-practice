import java.util.*;

public class ChainMap<K, V> {
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

  @SuppressWarnings("unchecked")
  private void rehash() {
    Node<K, V>[] old = buckets;
    int capacity = (primeIndex + 1 < PRIMES.length) ? PRIMES[++primeIndex] : 2 * old.length + 1;
    buckets = (Node<K, V>[]) new Node[capacity];
    for (Node<K, V> head : old) {
      for (Node<K, V> curr = head; curr != null; ) {
        Node<K, V> next = curr.next;
        int i = indexFor(curr.key);
        curr.next = buckets[i];
        buckets[i] = curr;
        curr = next;
      }
    }
  }

  // <REF Q5>
  public V put(K key, V value) {
    if (key == null || value == null) throw new IllegalArgumentException();
    int i = Math.floorMod(key.hashCode(), buckets.length);
    for (Node<K, V> curr = buckets[i]; curr != null; curr = curr.next) {
      if (curr.key.equals(key)) {          // key exists: replace
        V old = curr.value;
        curr.value = value;
        return old;
      }
    }
    Node<K, V> node = new Node<>(key, value);
    node.next = buckets[i];                // new node goes at the head: O(1)
    buckets[i] = node;
    size++;
    if ((double) size / buckets.length > 0.75) rehash();   // double, not int, division
    return null;
  }
  // </REF Q5>

  public V get(K key) {
    for (Node<K, V> c = buckets[indexFor(key)]; c != null; c = c.next) if (c.key.equals(key)) return c.value;
    return null;
  }

  public static void main(String[] args) {
    Random rnd = new Random(2);
    for (int t = 0; t < 400; t++) {
      ChainMap<Integer, Integer> m = new ChainMap<>();
      HashMap<Integer, Integer> ref = new HashMap<>();
      for (int o = 0; o < 300; o++) {
        int k = rnd.nextInt(200) - 50, v = rnd.nextInt();
        if (!Objects.equals(m.put(k, v), ref.put(k, v))) throw new AssertionError("put");
        int q = rnd.nextInt(200) - 50;
        if (!Objects.equals(m.get(q), ref.get(q))) throw new AssertionError("get");
        if ((double) m.size / m.buckets.length > 0.75) throw new AssertionError("load");
      }
    }
    System.out.println("ChainMap OK");
  }
}
