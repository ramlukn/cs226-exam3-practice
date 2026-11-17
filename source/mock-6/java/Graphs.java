import java.util.*;

public class Graphs {
  static class Graph<V> {
    private final Map<V, Set<V>> adj = new LinkedHashMap<>();
    void addVertex(V v) { if (!adj.containsKey(v)) adj.put(v, new LinkedHashSet<>()); }
    void addEdge(V u, V v) { addVertex(u); addVertex(v); adj.get(u).add(v); adj.get(v).add(u); }
    Iterable<V> neighbors(V v) { return adj.get(v); }
    Iterable<V> vertices() { return adj.keySet(); }
  }

  // <REF Q10>
  public static <V> Map<V, Integer> componentIds(Graph<V> g) {
    Map<V, Integer> id = new HashMap<>();        // also the visited set
    int next = 0;
    for (V s : g.vertices()) {
      if (id.containsKey(s)) continue;           // already in a component we found
      id.put(s, next);                           // s starts a new component
      Queue<V> queue = new ArrayDeque<>();
      queue.add(s);
      while (!queue.isEmpty()) {
        V v = queue.remove();
        for (V w : g.neighbors(v)) {
          if (!id.containsKey(w)) {              // check AND mark before enqueueing
            id.put(w, next);
            queue.add(w);
          }
        }
      }
      next++;                                    // only after the whole component is labeled
    }
    return id;
  }
  // </REF Q10>

  public static void main(String[] args) {
    Random rnd = new Random(16);
    for (int t = 0; t < 2000; t++) {
      int n = rnd.nextInt(14);
      Graph<Integer> g = new Graph<>();
      int[][] d = new int[n][n];
      for (int[] r : d) Arrays.fill(r, 1 << 20);
      for (int i = 0; i < n; i++) { g.addVertex(i); d[i][i] = 0; }
      int e = n == 0 ? 0 : rnd.nextInt(2 * n);
      for (int i = 0; i < e; i++) { int u = rnd.nextInt(n), v = rnd.nextInt(n); if (u != v) { g.addEdge(u, v); d[u][v] = d[v][u] = 1; } }
      for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
      Map<Integer, Integer> id = componentIds(g);
      if (id.size() != n) throw new AssertionError("all");
      Set<Integer> ids = new HashSet<>(id.values());
      for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if ((d[i][j] < (1 << 20)) != (id.get(i).equals(id.get(j)))) throw new AssertionError("same");
      for (int c = 0; c < ids.size(); c++) if (!ids.contains(c)) throw new AssertionError("numbering");
    }
    System.out.println("Graphs OK");
  }
}
