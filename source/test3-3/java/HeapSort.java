import java.util.*;

public class HeapSort {
  // <REF Q8>
  // Max-heap in a[0..n-1]: moves a[i] down until it is >= both children.
  private static void sink(int[] a, int i, int n) {
    while (2 * i + 1 < n) {
      int b = 2 * i + 1;                     // left child
      if (b + 1 < n && a[b + 1] > a[b]) b++; // the larger child
      if (a[i] >= a[b]) break;
      int t = a[i]; a[i] = a[b]; a[b] = t;
      i = b;
    }
  }

  public static void heapSort(int[] a) {
    int n = a.length;
    for (int i = n / 2 - 1; i >= 0; i--) {   // 1. heapify bottom-up: O(n)
      sink(a, i, n);
    }
    for (int end = n - 1; end > 0; end--) {  // 2. move the max to the end, shrink the heap
      int t = a[0]; a[0] = a[end]; a[end] = t;
      sink(a, 0, end);                       // heap is now a[0..end-1]
    }
  }
  // </REF Q8>

  public static void main(String[] args) {
    Random rnd = new Random(10);
    for (int t = 0; t < 5000; t++) {
      int[] a = new int[rnd.nextInt(40)];
      for (int i = 0; i < a.length; i++) a[i] = rnd.nextInt(25) - 5;
      int[] s = a.clone(); Arrays.sort(s);
      heapSort(a);
      if (!Arrays.equals(a, s)) throw new AssertionError("sort");
    }
    System.out.println("HeapSort OK");
  }
}
