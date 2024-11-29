"""Simple Weighted Directed Graph."""
from typing import Callable, Generic, TypeVar

from priority_queue import PriorityQueue

T = TypeVar("T")
W = TypeVar("W")


# TODO not sure about the "Weighted",
# maybe there can be a default weight 1 for unweighted connected graphs
class WeightedDirectedGraph(Generic[T, W]):
    """
    A Weighted Directed Graph implementation.

    Args:
        edges: list[tuple[T, T, W]] | None: List of edges.
            Each edge is expected should be a tuple with format:
            (source_node, destination_node, weight of edge)
    """

    def __init__(self, edges: list[tuple[T, T, W]] | None = None):
        """Init a Weighted Directed Graph."""
        if not edges:
            edges = []
        self._edges = edges
        self._adj: dict[T, list[tuple[T, W]]] = self._make_adj()

    def _make_adj(self) -> dict[T, list[tuple[T, W]]]:
        """
        Build an adjacency list from a list of edges.

        Args:
            edges: list of edges with format
                (source_node, destination_node, weight of edge)

        Returns:
            An adjacency list with format
                {source_node: [(destination_node, weigth of edge)]}
        """
        adj: dict[T, list[tuple[T, W]]] = {}
        for src, dst, w in self._edges:
            if src not in adj:
                adj[src] = []
            if dst not in adj:
                adj[dst] = []
            adj[src].append((dst, w))
        return adj

    @classmethod
    def from_adjacency_list(cls, adjacency_list: dict[T, list[tuple[T, W]]]):
        """
        Create a WeightedDirectedGraph from an adjacency list.

        Args:
            Adjacency list: An adjacency list with format
                {source_node: [(destination_node, weigth of edge)]}

        Returns:
            New WeightedDirectedGraph.
        """
        graph = cls()
        graph._adj = adjacency_list
        return graph

    # TODO 1: need a way to get the priority when popping/peeking from heap
    # TODO 2: vanilla Dijkstra implementation for now, can be optimized
    def dijkstra(self, source: T, key_func: Callable = lambda x: x) -> dict[T, W]:
        """
        Compute the shortest path from source node to all nodes using Dijkstra's algorithm.

        Args:
            source: source node to from which the shortest paths are computed
            key_func: custom comparator,
                e.g. `lambda x: -x` to compute longest paths

        Returns:
            The shortest paths from the source node to all other reachable nodes
            If a node is unreachable, then it is not in the output
        """
        pq = PriorityQueue.from_items_with_priority(
            [(source, 0)]
        )  # W should be of int or float, not sure how to check that
        shortest_paths = {}
        while pq:
            curr_node, curr_distance = pq.pop(get_priority=True)  # See TODO 1 above
            if curr_node in shortest_paths:
                continue
            shortest_paths[curr_node] = curr_distance
            for nei, nei_distance in self._adj[curr_node]:
                pq.push((nei, curr_distance + nei_distance))
        return shortest_paths
