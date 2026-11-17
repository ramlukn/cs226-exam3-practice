import java.util.*;

public class DynArray<T> {
  private T[] data;
  private int size;

  @SuppressWarnings("unchecked") DynArray() { data = (T[]) new Object[1]; }
  void add(T x) { if (size == data.length) data = Arrays.copyOf(data, 2 * data.length); data[size++] = x; }
  T get(int i) { return data[i]; }
  int capacity() { return data.length; }
  boolean slotEmpty(int i) { return data[i] == null; }

  // <REF Q9>
  public T remove(int index) {
    if (index < 0 || index >= size) throw new IndexOutOfBoundsException();
    T removed = data[index];                 // save before it's overwritten
    for (int i = index; i < size - 1; i++) {
      data[i] = data[i + 1];                 // shift everything after it one left
    }
    data[size - 1] = null;                   // no stale reference at the old end
    size--;
    return removed;
  }
  // </REF Q9>

  public static void main(String[] args) {
    Random rnd = new Random(17);
    for (int t = 0; t < 2000; t++) {
      DynArray<Integer> d = new DynArray<>();
      List<Integer> ref = new ArrayList<>();
      for (int o = 0; o < 60; o++) {
        if (ref.isEmpty() || rnd.nextInt(3) > 0) { int x = rnd.nextInt(100); d.add(x); ref.add(x); }
        else { int i = rnd.nextInt(ref.size()); if (!d.remove(i).equals(ref.remove(i))) throw new AssertionError("rm"); }
        if (d.size != ref.size()) throw new AssertionError("size");
        for (int i = 0; i < ref.size(); i++) if (!d.get(i).equals(ref.get(i))) throw new AssertionError("order");
        for (int i = d.size; i < d.capacity(); i++) if (!d.slotEmpty(i)) throw new AssertionError("stale");
      }
      try { d.remove(d.size); throw new AssertionError("no IOOBE"); } catch (IndexOutOfBoundsException e) {}
      try { d.remove(-1); throw new AssertionError("no IOOBE"); } catch (IndexOutOfBoundsException e) {}
    }
    System.out.println("DynArray OK");
  }
}
