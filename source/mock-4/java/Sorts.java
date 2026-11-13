import java.util.*;

public class Sorts {
  static void swap(int[] a, int i, int j) { int t = a[i]; a[i] = a[j]; a[j] = t; }

  static void quickSort(int[] a, int lo, int hi) {
    if (lo >= hi) return;
    int p = partition(a, lo, hi);
    quickSort(a, lo, p - 1);
    quickSort(a, p + 1, hi);
  }

  // <REF Q9>
  private static int partition(int[] a, int lo, int hi) {
    int pivot = a[lo];
    int i = lo;                          // a[lo+1..i] < pivot
    for (int j = lo + 1; j <= hi; j++) { // a[i+1..j-1] >= pivot
      if (a[j] < pivot) {
        i++;
        swap(a, i, j);
      }
    }
    swap(a, lo, i);                      // pivot goes between the two regions
    return i;
  }
  // </REF Q9>

  public static void main(String[] args) {
    Random rnd = new Random(1);
    for (int t = 0; t < 3000; t++) {
      int n = rnd.nextInt(40);
      int[] a = new int[n];
      for (int i = 0; i < n; i++) a[i] = rnd.nextInt(15);
      if (n > 0) {
        int[] b = a.clone();
        int lo = rnd.nextInt(n), hi = lo + rnd.nextInt(n - lo);
        int pv = b[lo];
        int p = partition(b, lo, hi);
        if (b[p] != pv) throw new AssertionError("pivot");
        for (int i = lo; i < p; i++) if (b[i] >= pv) throw new AssertionError("left");
        for (int i = p + 1; i <= hi; i++) if (b[i] < pv) throw new AssertionError("right");
      }
      int[] s = a.clone(); Arrays.sort(s);
      quickSort(a, 0, n - 1);
      if (!Arrays.equals(a, s)) throw new AssertionError("sort");
    }
    System.out.println("Sorts OK");
  }
}
