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

  // <REF Q5>
  public V remove(K key) {
    if (key == null) throw new IllegalArgumentException();
    int i = Math.floorMod(key.hashCode(), buckets.length);
    Node<K, V> prev = null;
    Node<K, V> curr = buckets[i];
    while (curr != null) {
      if (curr.key.equals(key)) {
        if (prev == null) buckets[i] = curr.next;   // removing the head
        else prev.next = curr.next;                 // removing from the middle or end
        size--;
        return curr.value;
      }
      prev = curr;                                  // move BOTH pointers
      curr = curr.next;
    }
    return null;
  }
  // </REF Q5>

  String show() {
    StringBuilder sb = new StringBuilder("m=" + buckets.length + " size=" + size + "  ");
    for (int i = 0; i < buckets.length; i++) if (buckets[i] != null) {
      sb.append(i).append(": ");
      for (Node<K, V> c = buckets[i]; c != null; c = c.next) sb.append(c.key).append(c.next != null ? " → " : "");
      sb.append("   ");
    }
    return sb.toString();
  }

  public static void main(String[] args) {
    Random rnd = new Random(8);
    for (int t = 0; t < 400; t++) {
      ChainMap<Integer, Integer> m = new ChainMap<>();
      HashMap<Integer, Integer> ref = new HashMap<>();
      for (int o = 0; o < 300; o++) {
        int k = rnd.nextInt(150) - 40, op = rnd.nextInt(3);
        if (op == 0) { int v = rnd.nextInt(); m.put(k, v); ref.put(k, v); }
        else if (op == 1) { if (!Objects.equals(m.remove(k), ref.remove(k))) throw new AssertionError("rm"); }
        else if (!Objects.equals(m.get(k), ref.get(k))) throw new AssertionError("get");
        if (m.size != ref.size()) throw new AssertionError("size");
      }
    }
    ChainMap<Integer, String> m = new ChainMap<>();
    int[] keys = {3, 20, 10, 37, 17, 24};
    for (int k = 0; k < keys.length; k++) {
      if (k == keys.length - 1) System.out.println("before last put: " + m.show());
      m.put(keys[k], "x");
    }
    System.out.println("after last put:  " + m.show());
    System.out.println("ChainMap OK");
  }
}
