import java.util.*;

public class Graphs {
  static class Graph<V> {
    private final Map<V, Set<V>> adj = new HashMap<>();
    void addVertex(V v) { if (!adj.containsKey(v)) adj.put(v, new HashSet<>()); }
    void addEdge(V u, V v) { addVertex(u); addVertex(v); adj.get(u).add(v); adj.get(v).add(u); }
    Iterable<V> neighbors(V v) { return adj.get(v); }
    Iterable<V> vertices() { return adj.keySet(); }
  }

  // <REF Q10>
  public static <V> int countWithinHops(Graph<V> g, V start, int k) {
    Map<V, Integer> dist = new HashMap<>();      // doubles as the visited set
    Queue<V> queue = new ArrayDeque<>();
    dist.put(start, 0);
    queue.add(start);
    int count = 0;
    while (!queue.isEmpty()) {
      V v = queue.remove();
      count++;                                   // every dequeued vertex is within k
      if (dist.get(v) == k) continue;            // don't expand past k hops
      for (V w : g.neighbors(v)) {
        if (!dist.containsKey(w)) {              // check AND mark before enqueueing
          dist.put(w, dist.get(v) + 1);
          queue.add(w);
        }
      }
    }
    return count;
  }
  // </REF Q10>

  // <REF D6>
  public static <V> int countComponents(Graph<V> g) {
    Set<V> visited = new HashSet<>();
    int components = 0;
    for (V v : g.vertices()) {
      if (!visited.contains(v)) {
        components++;            // v starts a component nobody has reached yet
        dfs(g, v, visited);
      }
    }
    return components;
  }

  private static <V> void dfs(Graph<V> g, V v, Set<V> visited) {
    visited.add(v);
    for (V w : g.neighbors(v)) {
      if (!visited.contains(w)) dfs(g, w, visited);
    }
  }
  // </REF D6>

  public static void main(String[] args) {
    Random rnd = new Random(5);
    for (int t = 0; t < 2000; t++) {
      int n = 1 + rnd.nextInt(15);
      Graph<Integer> g = new Graph<>();
      int[][] d = new int[n][n];
      for (int[] r : d) Arrays.fill(r, 1 << 20);
      for (int i = 0; i < n; i++) { g.addVertex(i); d[i][i] = 0; }
      int e = rnd.nextInt(2 * n);
      for (int i = 0; i < e; i++) { int u = rnd.nextInt(n), v = rnd.nextInt(n); if (u != v) { g.addEdge(u, v); d[u][v] = d[v][u] = 1; } }
      for (int k = 0; k < n; k++) for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = Math.min(d[i][j], d[i][k] + d[k][j]);
      int s = rnd.nextInt(n), k = rnd.nextInt(5);
      int want = 0; for (int j = 0; j < n; j++) if (d[s][j] <= k) want++;
      if (countWithinHops(g, s, k) != want) throw new AssertionError("hops");
      Set<Integer> seen = new HashSet<>(); int comps = 0;
      for (int i = 0; i < n; i++) if (seen.add(i)) { comps++; for (int j = 0; j < n; j++) if (d[i][j] < (1 << 20)) seen.add(j); }
      if (countComponents(g) != comps) throw new AssertionError("comps");
    }
    System.out.println("Graphs OK");
  }
}
