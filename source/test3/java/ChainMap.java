import java.util.*;

public class ChainMap<K, V> {
  private static class Node<K, V> {
    K key; V value; Node<K, V> next;
    Node(K key, V value, Node<K, V> next) { this.key = key; this.value = value; this.next = next; }
  }
  private Node<K, V>[] buckets;
  private int size;

  @SuppressWarnings("unchecked") ChainMap(int m) { buckets = (Node<K, V>[]) new Node[m]; }
  private int indexFor(K key) { return Math.floorMod(key.hashCode(), buckets.length); }
  V put(K key, V value) {
    int i = indexFor(key);
    for (Node<K, V> n = buckets[i]; n != null; n = n.next) if (n.key.equals(key)) { V o = n.value; n.value = value; return o; }
    buckets[i] = new Node<>(key, value, buckets[i]); size++; return null;
  }

  // <REF Q7>
  public V remove(K key) {
    if (key == null) throw new IllegalArgumentException();
    int i = indexFor(key);
    Node<K, V> prev = null, curr = buckets[i];
    while (curr != null && !curr.key.equals(key)) {   // walk with a trailing pointer
      prev = curr;
      curr = curr.next;
    }
    if (curr == null) return null;                    // not in this chain
    if (prev == null) buckets[i] = curr.next;         // removing the head
    else prev.next = curr.next;                       // removing from the middle or end
    size--;
    return curr.value;
  }
  // </REF Q7>

  public static void main(String[] args) {
    Random rnd = new Random(7);
    for (int t = 0; t < 2000; t++) {
      ChainMap<Integer, Integer> m = new ChainMap<>(7);
      Map<Integer, Integer> ref = new HashMap<>();
      for (int o = 0; o < 150; o++) {
        int k = rnd.nextInt(40) - 10;
        if (rnd.nextBoolean()) { int v = rnd.nextInt(); if (!Objects.equals(m.put(k, v), ref.put(k, v))) throw new AssertionError("put"); }
        else if (!Objects.equals(m.remove(k), ref.remove(k))) throw new AssertionError("remove");
        if (m.size != ref.size()) throw new AssertionError("size");
        int c = 0; for (Node<Integer, Integer> b : m.buckets) for (Node<Integer, Integer> n = b; n != null; n = n.next) { c++; if (!n.value.equals(ref.get(n.key))) throw new AssertionError("content"); }
        if (c != ref.size()) throw new AssertionError("count");
      }
    }
    System.out.println("ChainMap OK");
  }
}
