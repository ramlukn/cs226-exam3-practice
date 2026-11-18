import java.util.*;

public class TopFrequent {
  // <REF Q10>
  public static List<Integer> topKFrequent(int[] a, int k) {
    if (a == null || k < 0) throw new IllegalArgumentException();
    Map<Integer, Integer> count = new HashMap<>();            // 1. count: O(n) expected
    for (int x : a) {
      count.put(x, count.getOrDefault(x, 0) + 1);
    }
    // 2. MIN-heap by count of {value, count}: root = least frequent of the kept k
    PriorityQueue<int[]> pq = new PriorityQueue<>((p, q) -> Integer.compare(p[1], q[1]));
    for (Map.Entry<Integer, Integer> e : count.entrySet()) {
      int[] pair = {e.getKey(), e.getValue()};
      if (pq.size() < k) {
        pq.add(pair);
      } else if (k > 0 && pair[1] > pq.peek()[1]) {           // more frequent than the weakest kept
        pq.remove();
        pq.add(pair);
      }
    }
    List<Integer> out = new ArrayList<>();
    for (int[] pair : pq) out.add(pair[0]);                   // any order is fine
    return out;
  }
  // </REF Q10>

  public static void main(String[] args) {
    Random rnd = new Random(40);
    for (int t = 0; t < 5000; t++) {
      int[] a = new int[rnd.nextInt(40)];
      for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(12) - 3;
      int k = rnd.nextInt(15);
      Map<Integer, Integer> c = new HashMap<>(); for (int x : a) c.merge(x, 1, Integer::sum);
      List<Integer> got = topKFrequent(a, k);
      if (got.size() != Math.min(k, c.size()) || new HashSet<>(got).size() != got.size()) throw new AssertionError("size");
      int minIn = Integer.MAX_VALUE, maxOut = 0;
      for (int v : c.keySet()) { if (got.contains(v)) minIn = Math.min(minIn, c.get(v)); else maxOut = Math.max(maxOut, c.get(v)); }
      if (!got.isEmpty() && maxOut > minIn) throw new AssertionError("not top k");
    }
    try { topKFrequent(new int[]{1}, -1); throw new AssertionError("no IAE"); } catch (IllegalArgumentException e) {}
    System.out.println("TopFrequent OK");
  }
}
