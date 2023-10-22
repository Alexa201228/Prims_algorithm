import heapq
from concurrent.futures import ProcessPoolExecutor

import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]

    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

    def prim_mst(self, v):
        min_spanning_tree = []
        visited = [False] * self.V
        heap = [(0, v)]  # (weight, vertex)

        while heap:
            weight, u = heapq.heappop(heap)

            if visited[u]:
                continue

            visited[u] = True
            for neighbor, w in self.graph[u]:
                if not visited[neighbor]:
                    heapq.heappush(heap, (w, neighbor))
                    min_spanning_tree.append((u, neighbor, w))

        return min_spanning_tree

    def parallel_mst(self):
        shared_pos = {}

        with ProcessPoolExecutor() as executor:
            results = list(executor.map(self.prim_mst, range(self.V)))

        # Merge results
        min_spanning_tree = [edge for result in results for edge in result]

        # Create a graph and add edges
        shared_graph = nx.Graph()
        for u, v, weight in min_spanning_tree:
            shared_graph.add_edge(u, v, weight=weight)

        return min_spanning_tree, shared_graph


if __name__ == "__main__":

    g = Graph(5)
    g.add_edge(0, 1, 2)
    g.add_edge(0, 3, 6)
    g.add_edge(1, 2, 3)
    g.add_edge(1, 3, 8)
    g.add_edge(1, 4, 5)
    g.add_edge(2, 4, 7)
    g.add_edge(3, 4, 9)

    min_spanning_tree, G = g.parallel_mst()

    # Compute node positions using spring layout
    pos = nx.spring_layout(G)

    # Draw the graph with positions
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700)
    labels = {(u, v): G[u][v]['weight'] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='red', width=2)

    plt.show()
