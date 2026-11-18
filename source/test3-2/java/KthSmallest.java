import java.util.*;

public class KthSmallest {
  // <REF Q10>
  public static int kthSmallest(int[] a, int k) {
    if (a == null || k < 1 || k > a.length) throw new IllegalArgumentException();
    // MAX-heap of the k smallest values seen so far: its root is the largest of them
    PriorityQueue<Integer> pq = new PriorityQueue<>(Collections.reverseOrder());
    for (int x : a) {
      if (pq.size() < k) {
        pq.add(x);
      } else if (x < pq.peek()) {   // x beats the largest of the kept k
        pq.remove();
        pq.add(x);
      }
    }
    return pq.peek();               // largest of the k smallest = the k-th smallest
  }
  // </REF Q10>

  public static void main(String[] args) {
    Random rnd = new Random(29);
    for (int t = 0; t < 5000; t++) {
      int[] a = new int[rnd.nextInt(30) + 1];
      for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(20) - 5;
      int k = rnd.nextInt(a.length) + 1;
      int[] s = a.clone(); Arrays.sort(s);
      if (kthSmallest(a, k) != s[k - 1]) throw new AssertionError("kth");
    }
    for (int bad : new int[]{0, 4}) { try { kthSmallest(new int[]{1, 2, 3}, bad); throw new AssertionError("no IAE"); } catch (IllegalArgumentException e) {} }
    System.out.println("KthSmallest OK");
  }
}
