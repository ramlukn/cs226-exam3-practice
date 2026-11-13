import java.util.*;

public class Sorts {
  static void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }
  static int partition(int[] a, int lo, int hi) {
    int pivot = a[hi], i = lo;
    for (int j = lo; j < hi; j++) if (a[j] < pivot) { swap(a, i, j); i++; }
    swap(a, i, hi);
    return i;
  }

  // <REF Q9>
  public static int kthSmallest(int[] a, int k) {
    if (k < 0 || k >= a.length) throw new IllegalArgumentException();
    int lo = 0, hi = a.length - 1;
    while (true) {
      int p = partition(a, lo, hi);     // a[p] is in its final sorted place
      if (p == k) return a[p];
      if (k < p) hi = p - 1;            // answer is left of the pivot
      else lo = p + 1;                  // answer is right of the pivot
    }
  }
  // </REF Q9>

  public static void main(String[] args) {
    Random rnd = new Random(10);
    for (int t = 0; t < 5000; t++) {
      int n = 1 + rnd.nextInt(30);
      int[] a = new int[n];
      for (int i = 0; i < n; i++) a[i] = rnd.nextInt(12);
      int[] s = a.clone(); Arrays.sort(s);
      int k = rnd.nextInt(n);
      if (kthSmallest(a, k) != s[k]) throw new AssertionError("kth");
    }
    System.out.println("Sorts OK");
  }
}
