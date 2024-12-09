"""Simple Weighted Directed Graph."""
from copy import deepcopy
from typing import Callable, Dict, Generic, List, Set, Tuple, TypeVar

from priority_queue import PriorityQueue

T = TypeVar("T")
W = TypeVar("W", int, float)


class WeightedDirectedGraph(Generic[T, W]):
    """
    A Weighted Directed Graph implementation.

    Args:
        edges: List[Tuple[T, T, W]] | None: list of edges.
            Each edge is expected should be a tuple with format:
            (source_node, destination_node, weight).
            Edges should be unique. However nodes can be connected
            by multiple edges with different weights.
    """

    def __init__(self, edges: List[Tuple[T, T, W]] | None = None):
        """Init a Weighted Directed Graph."""
        if not edges:
            edges = []
        if len(set(edges)) != len(edges):
            raise ValueError(
                "Try to inset duplicate edges (source_node, destination_node, weight)"
            )
        self._edges: Set[Tuple[T, T, W]] = set(edges)
        self._adj: Dict[T, List[Tuple[T, W]]] = self._make_adj()

    def _make_adj(self) -> Dict[T, List[Tuple[T, W]]]:
        """
        Build an adjacency list from a list of edges.

        Args:
            edges: list of edges with format
                (source_node, destination_node, weight of edge)

        Returns:
            An adjacency list with format
                {source_node: [(destination_node, weigth of edge)]}
        """
        adj: Dict[T, List[Tuple[T, W]]] = {}
        for src, dst, w in self._edges:
            if src not in adj:
                adj[src] = []
            if dst not in adj:
                adj[dst] = []
            adj[src].append((dst, w))
        return adj

    def add_edge(self, edge: Tuple[T, T, W]) -> None:
        """Add edge (source, destination, weight) to the graph."""
        if edge in self._edges:
            raise ValueError(
                "Try to insert duplicate edges (source_node, destination_node, weight)"
            )
        self._edges.add(edge)
        src, dst, w = edge
        if src not in self._adj:
            self._adj[src] = []
        if dst not in self._adj:
            self._adj[dst] = []
        self._adj[src].append((dst, w))

    def get_adjacency_list(self) -> Dict[T, List[Tuple[T, W]]]:
        """Return the value of the adjacency list."""
        return deepcopy(self._adj)

    @classmethod
    def from_adjacency_list(cls, adjacency_list: Dict[T, List[Tuple[T, W]]]):
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

    def __str__(self) -> str:
        """Return the string representation of the adjacency list."""
        return str(self._adj)

    def dijkstra(self, source: T, key_func: Callable = lambda x: x) -> Dict[T, W]:
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
        pq = PriorityQueue.from_items_with_priority([(source, 0)])
        shortest_paths = {}
        while pq:
            curr_node, curr_distance = pq.pop_with_priority()
            if curr_node in shortest_paths:
                continue
            shortest_paths[curr_node] = curr_distance
            for nei_node, nei_distance in self._adj[curr_node]:
                pq.push(nei_node, curr_distance + nei_distance)
        return shortest_paths
