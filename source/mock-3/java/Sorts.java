import java.util.*;

public class Sorts {
  static long comparisons = 0;

  static void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }

  // <REF Q1>
  private static void quickSort(int[] a, int lo, int hi) {
    if (lo >= hi) return;
    int mid = lo + (hi - lo) / 2;
    if (a[mid] < a[lo]) swap(a, mid, lo);
    if (a[hi] < a[lo]) swap(a, hi, lo);    // a[lo] is now the smallest of the three
    if (a[mid] < a[hi]) swap(a, mid, hi);  // a[hi] is now the median of the three
    int p = partition(a, lo, hi);
    quickSort(a, lo, p - 1);
    quickSort(a, p + 1, hi);
  }
  // </REF Q1>

  // <REF D1>
  private static int partition(int[] a, int lo, int hi) {
    int pivot = a[hi];
    int i = lo;                      // a[lo..i-1] < pivot
    for (int j = lo; j < hi; j++) {  // a[i..j-1] >= pivot
      comparisons++;
      if (a[j] < pivot) {
        swap(a, i, j);
        i++;
      }
    }
    swap(a, i, hi);                  // pivot between the two regions
    return i;
  }
  // </REF D1>

  // <REF D3>
  public static void heapSort(int[] a) {
    int n = a.length;
    for (int i = n / 2 - 1; i >= 0; i--) sink(a, i, n);   // buildHeap: O(n)
    for (int end = n - 1; end > 0; end--) {
      swap(a, 0, end);       // max goes to the sorted tail
      sink(a, 0, end);       // heap is now a[0..end-1]
    }
  }

  private static void sink(int[] a, int i, int size) {
    while (2 * i + 1 < size) {
      int best = 2 * i + 1;
      if (best + 1 < size && a[best + 1] > a[best]) best++;   // larger child
      if (a[i] >= a[best]) break;
      swap(a, i, best);
      i = best;
    }
  }
  // </REF D3>

  // <REF D5>
  public static int kthLargest(int[] a, int k) {
    if (k < 1 || k > a.length) throw new IllegalArgumentException();
    PriorityQueue<Integer> pq = new PriorityQueue<>();   // min-heap of the k largest so far
    for (int x : a) {
      pq.add(x);
      if (pq.size() > k) pq.remove();                    // drop the smallest
    }
    return pq.peek();                                    // smallest of the k largest
  }
  // </REF D5>

  // <REF D8>
  public static boolean nearbyDuplicate(int[] a, int k) {
    Map<Integer, Integer> last = new HashMap<>();   // value -> latest index seen
    for (int i = 0; i < a.length; i++) {
      Integer j = last.get(a[i]);
      if (j != null && i - j <= k) return true;
      last.put(a[i], i);
    }
    return false;
  }
  // </REF D8>

  // <REF Q4>
  public static boolean isMinHeap(int[] heap, int size) {
    for (int i = 1; i < size; i++) {           // every node except the root
      if (heap[i] < heap[(i - 1) / 2]) return false;
    }
    return true;                               // also covers size 0 and 1
  }
  // </REF Q4>

  static boolean bruteMinHeap(int[] h, int size) {
    for (int i = 0; i < size; i++) {
      int l = 2 * i + 1, r = 2 * i + 2;
      if (l < size && h[l] < h[i]) return false;
      if (r < size && h[r] < h[i]) return false;
    }
    return true;
  }

  public static void main(String[] args) {
    Random rnd = new Random(1);
    for (int t = 0; t < 3000; t++) {
      int n = rnd.nextInt(40);
      int[] a = new int[n];
      for (int i = 0; i < n; i++) a[i] = rnd.nextInt(t % 2 == 0 ? 10 : 1000);
      int[] e = a.clone(); Arrays.sort(e);
      int[] q = a.clone(); quickSort(q, 0, n - 1);
      int[] h = a.clone(); heapSort(h);
      if (!Arrays.equals(e, q)) throw new AssertionError("quick " + Arrays.toString(a));
      if (!Arrays.equals(e, h)) throw new AssertionError("heap " + Arrays.toString(a));
      if (n > 0) {
        int k = 1 + rnd.nextInt(n);
        if (kthLargest(a, k) != e[n - k]) throw new AssertionError("kth");
      }
      int k2 = rnd.nextInt(5);
      boolean bd = false;
      for (int i = 0; i < n; i++) for (int j = i + 1; j <= i + k2 && j < n; j++) if (a[i] == a[j]) bd = true;
      if (nearbyDuplicate(a, k2) != bd) throw new AssertionError("dup");
      int size = n == 0 ? 0 : rnd.nextInt(n + 1);
      int[] hp = a.clone();
      if (t % 3 == 0) { Arrays.sort(hp, 0, size); }
      if (isMinHeap(hp, size) != bruteMinHeap(hp, size)) throw new AssertionError("isMinHeap");
    }
    // median-of-three on sorted / reverse-sorted input should be ~n log n comparisons
    for (int n : new int[]{1 << 12, 1 << 14}) {
      int[] s = new int[n]; for (int i = 0; i < n; i++) s[i] = i;
      comparisons = 0; quickSort(s, 0, n - 1); long c1 = comparisons;
      int[] r = new int[n]; for (int i = 0; i < n; i++) r[i] = n - i;
      comparisons = 0; quickSort(r, 0, n - 1); long c2 = comparisons;
      System.out.println("n=" + n + " sorted cmp=" + c1 + " reverse cmp=" + c2 + " n*log2n=" + (long) (n * (Math.log(n) / Math.log(2))));
    }
    System.out.println("Sorts OK");
  }
}
