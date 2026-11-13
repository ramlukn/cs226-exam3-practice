import java.util.*;

public class Graphs {
  static class Graph<V> {
    private final Map<V, Set<V>> adj = new LinkedHashMap<>();
    void addVertex(V v) { if (!adj.containsKey(v)) adj.put(v, new LinkedHashSet<>()); }
    void addEdge(V u, V v) { addVertex(u); addVertex(v); adj.get(u).add(v); adj.get(v).add(u); }
    Iterable<V> neighbors(V v) { return adj.get(v); }
    Iterable<V> vertices() { return adj.keySet(); }
    int numVertices() { return adj.size(); }
  }

  // <REF Q7>
  public static <V> boolean isConnected(Graph<V> g) {
    if (g.numVertices() == 0) return true;
    V start = g.vertices().iterator().next();   // any vertex works
    Set<V> visited = new HashSet<>();
    Queue<V> queue = new ArrayDeque<>();
    visited.add(start);
    queue.add(start);
    while (!queue.isEmpty()) {
      V v = queue.remove();
      for (V w : g.neighbors(v)) {
        if (!visited.contains(w)) {
          visited.add(w);
          queue.add(w);
        }
      }
    }
    return visited.size() == g.numVertices();   // reached everyone?
  }
  // </REF Q7>

  // <REF Q10>
  public static <V> List<List<V>> levels(Graph<V> g, V start) {
    List<List<V>> result = new ArrayList<>();
    Set<V> visited = new HashSet<>();
    List<V> current = new ArrayList<>();
    visited.add(start);
    current.add(start);
    while (!current.isEmpty()) {
      result.add(current);                      // every vertex at this distance
      List<V> next = new ArrayList<>();
      for (V v : current) {
        for (V w : g.neighbors(v)) {
          if (!visited.contains(w)) {           // check AND mark when first seen
            visited.add(w);
            next.add(w);
          }
        }
      }
      current = next;                           // one level further out
    }
    return result;
  }
  // </REF Q10>

  public static void main(String[] args) {
    Random rnd = new Random(11);
    for (int t = 0; t < 2000; t++) {
      int n = 1 + rnd.nextInt(14);
      Graph<Integer> g = new Graph<>();
      int[][] d = new int[n][n];
      for (int[] r : d) Arrays.fill(r, 1 << 20);
      for (int i = 0; i < n; i++) { g.addVertex(i); d[i][i] = 0; }
      int e = rnd.nextInt(2 * n);
      for (int i = 0; i < e; i++) { int u = rnd.nextInt(n), v = rnd.nextInt(n); if (u != v) { g.addEdge(u, v); d[u][v] = d[v][u] = 1; } }
      for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
      boolean conn = true; for (int j = 0; j < n; j++) if (d[0][j] >= (1 << 20)) conn = false;
      if (isConnected(g) != conn) throw new AssertionError("conn");
      int s = rnd.nextInt(n);
      List<List<Integer>> lv = levels(g, s);
      int seen = 0;
      for (int L = 0; L < lv.size(); L++) for (int v : lv.get(L)) { seen++; if (d[s][v] != L) throw new AssertionError("level"); }
      int want = 0; for (int j = 0; j < n; j++) if (d[s][j] < (1 << 20)) want++;
      if (seen != want) throw new AssertionError("count");
    }
    if (!isConnected(new Graph<Integer>())) throw new AssertionError("empty");
    System.out.println("Graphs OK");
  }
}
