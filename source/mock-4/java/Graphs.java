import java.util.*;

public class Graphs {
  static class Graph<V> {
    private final Map<V, Set<V>> adj = new HashMap<>();
    void addVertex(V v) { if (!adj.containsKey(v)) adj.put(v, new LinkedHashSet<>()); }
    void addEdge(V u, V v) { addVertex(u); addVertex(v); adj.get(u).add(v); adj.get(v).add(u); }
    Iterable<V> neighbors(V v) { return adj.get(v); }
  }

  // <REF Q10>
  public static <V> List<V> shortestPath(Graph<V> g, V start, V target) {
    Map<V, V> parent = new HashMap<>();       // also the visited set
    Queue<V> queue = new ArrayDeque<>();
    parent.put(start, null);                  // start has no parent
    queue.add(start);
    while (!queue.isEmpty()) {
      V v = queue.remove();
      if (v.equals(target)) break;            // first time we reach it is by a shortest path
      for (V w : g.neighbors(v)) {
        if (!parent.containsKey(w)) {         // check AND mark before enqueueing
          parent.put(w, v);
          queue.add(w);
        }
      }
    }
    List<V> path = new ArrayList<>();
    if (!parent.containsKey(target)) return path;   // unreachable: empty list
    for (V v = target; v != null; v = parent.get(v)) path.add(v);   // walk back
    Collections.reverse(path);                // start first
    return path;
  }
  // </REF Q10>

  public static void main(String[] args) {
    Random rnd = new Random(5);
    for (int t = 0; t < 2000; t++) {
      int n = 1 + rnd.nextInt(15);
      Graph<Integer> g = new Graph<>();
      int[][] d = new int[n][n];
      for (int[] r : d) Arrays.fill(r, 1 << 20);
      for (int i = 0; i < n; i++) { g.addVertex(i); d[i][i] = 0; }
      int e = rnd.nextInt(2 * n);
      boolean[][] edge = new boolean[n][n];
      for (int i = 0; i < e; i++) { int u = rnd.nextInt(n), v = rnd.nextInt(n); if (u != v) { g.addEdge(u, v); d[u][v] = d[v][u] = 1; edge[u][v] = edge[v][u] = true; } }
      for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
      int s = rnd.nextInt(n), tt = rnd.nextInt(n);
      List<Integer> p = shortestPath(g, s, tt);
      if (d[s][tt] >= (1 << 20)) { if (!p.isEmpty()) throw new AssertionError("unreach"); continue; }
      if (p.size() != d[s][tt] + 1 || p.get(0) != s || p.get(p.size() - 1) != tt) throw new AssertionError("len");
      for (int i = 0; i + 1 < p.size(); i++) if (!edge[p.get(i)][p.get(i + 1)]) throw new AssertionError("edge");
    }
    System.out.println("Graphs OK");
  }
}
