import java.util.*;

public class Sorts {
  static void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }

  // <REF Q9>
  private static int partition(int[] a, int lo, int hi) {
    int pivot = a[hi];
    int i = lo;                        // a[lo..i-1] < pivot
    for (int j = lo; j < hi; j++) {    // a[i..j-1] >= pivot
      if (a[j] < pivot) {
        swap(a, i, j);
        i++;
      }
    }
    swap(a, i, hi);                    // pivot goes between the two regions
    return i;
  }
  // </REF Q9>

  static void quickSort(int[] a, int lo, int hi) { if (lo >= hi) return; int p = partition(a, lo, hi); quickSort(a, lo, p - 1); quickSort(a, p + 1, hi); }

  public static void main(String[] args) {
    Random rnd = new Random(15);
    for (int t = 0; t < 3000; t++) {
      int n = 1 + rnd.nextInt(40);
      int[] a = new int[n];
      for (int i = 0; i < n; i++) a[i] = rnd.nextInt(15);
      int[] b = a.clone();
      int lo = rnd.nextInt(n), hi = lo + rnd.nextInt(n - lo);
      int pv = b[hi], p = partition(b, lo, hi);
      if (b[p] != pv) throw new AssertionError("pivot");
      for (int i = lo; i < p; i++) if (b[i] >= pv) throw new AssertionError("left");
      for (int i = p + 1; i <= hi; i++) if (b[i] < pv) throw new AssertionError("right");
      int[] s = a.clone(); Arrays.sort(s); quickSort(a, 0, n - 1);
      if (!Arrays.equals(a, s)) throw new AssertionError("sort");
    }
    int[] tr = {6, 2, 9, 1, 7, 4};
    int p = partition(tr, 0, 5);
    System.out.println("trace " + Arrays.toString(tr) + " p=" + p);
    System.out.println("Sorts OK");
  }
}
