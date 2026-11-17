import java.util.*;

public class Avl {
  static class Node {
    int key; Node left, right; int height;   // a leaf has height 0
    Node(int key) { this.key = key; }
  }
  Node root;

  private int height(Node n) { return n == null ? -1 : n.height; }
  private Node rotateLeft(Node n) {
    Node child = n.right; n.right = child.left; child.left = n;
    updateHeight(n); updateHeight(child); return child;
  }

  // <REF Q10>
  private void updateHeight(Node n) {
    n.height = 1 + Math.max(height(n.left), height(n.right));
  }

  private Node rotateRight(Node n) {
    Node child = n.left;
    n.left = child.right;      // child's right subtree moves under n
    child.right = n;           // n becomes child's right child
    updateHeight(n);           // n is now lower: fix it first
    updateHeight(child);       // child's height depends on n's
    return child;              // the new root of this subtree
  }

  private Node rebalance(Node n) {
    int balance = height(n.left) - height(n.right);
    if (balance > 1) {                               // left-heavy
      if (height(n.left.left) < height(n.left.right)) {
        n.left = rotateLeft(n.left);                 // left-right case: straighten it first
      }
      return rotateRight(n);
    }
    if (balance < -1) {                              // right-heavy (mirror image)
      if (height(n.right.right) < height(n.right.left)) {
        n.right = rotateRight(n.right);              // right-left case
      }
      return rotateLeft(n);
    }
    return n;                                        // already balanced
  }
  // </REF Q10>

  Node insert(Node n, int key) {
    if (n == null) return new Node(key);
    if (key < n.key) n.left = insert(n.left, key);
    else if (key > n.key) n.right = insert(n.right, key);
    else return n;
    updateHeight(n);
    return rebalance(n);
  }

  int check(Node n, long lo, long hi) {
    if (n == null) return -1;
    if (n.key <= lo || n.key >= hi) throw new AssertionError("bst");
    int l = check(n.left, lo, n.key), r = check(n.right, n.key, hi);
    if (Math.abs(l - r) > 1) throw new AssertionError("balance");
    if (n.height != 1 + Math.max(l, r)) throw new AssertionError("height");
    return n.height;
  }
  void inorder(Node n, List<Integer> out) { if (n == null) return; inorder(n.left, out); out.add(n.key); inorder(n.right, out); }

  public static void main(String[] args) {
    Random rnd = new Random(18);
    for (int t = 0; t < 2000; t++) {
      Avl a = new Avl(); TreeSet<Integer> ref = new TreeSet<>();
      int n = rnd.nextInt(80);
      for (int i = 0; i < n; i++) {
        int k = t % 3 == 0 ? i : rnd.nextInt(200);   // every third run inserts sorted keys
        a.root = a.insert(a.root, k); ref.add(k);
        a.check(a.root, Long.MIN_VALUE, Long.MAX_VALUE);
      }
      List<Integer> got = new ArrayList<>(); a.inorder(a.root, got);
      if (!got.equals(new ArrayList<>(ref))) throw new AssertionError("keys");
    }
    System.out.println("Avl OK");
  }
}
