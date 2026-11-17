import java.util.*;

public class TopK {
  // <REF Q10>
  public static List<Integer> topK(int[] a, int k) {
    if (a == null || k < 0) throw new IllegalArgumentException();
    PriorityQueue<Integer> pq = new PriorityQueue<>();   // MIN-heap of the k largest seen so far
    for (int x : a) {
      if (pq.size() < k) {
        pq.add(x);
      } else if (k > 0 && x > pq.peek()) {   // beats the smallest of the current top k
        pq.remove();
        pq.add(x);
      }
    }
    List<Integer> out = new ArrayList<>();
    while (!pq.isEmpty()) out.add(pq.remove());   // comes out smallest first
    Collections.reverse(out);                     // largest first
    return out;
  }
  // </REF Q10>

  public static void main(String[] args) {
    Random rnd = new Random(10);
    for (int t = 0; t < 5000; t++) {
      int[] a = new int[rnd.nextInt(30)];
      for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(25) - 5;
      int k = rnd.nextInt(35);
      Integer[] s = Arrays.stream(a).boxed().toArray(Integer[]::new);
      Arrays.sort(s, Collections.reverseOrder());
      List<Integer> want = Arrays.asList(s).subList(0, Math.min(k, s.length));
      if (!topK(a, k).equals(want)) throw new AssertionError("topK " + Arrays.toString(a) + " k=" + k);
    }
    try { topK(new int[]{1}, -1); throw new AssertionError("no IAE"); } catch (IllegalArgumentException e) {}
    System.out.println("TopK OK");
  }
}
