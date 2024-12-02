"""Simple Priority Queue."""
import heapq
from typing import (
    Any,
    Callable,
    Generic,
    Iterator,
    List,
    Optional,
    Tuple,
    TypeVar,
    cast,
)

T = TypeVar("T")
P = TypeVar("P")


class PriorityQueue(Generic[T, P]):
    """
    A flexible Priority Queue implementation supporting both min-heap and max-heap behavior.

    Items can either carry their own priority or be assigned one explicitly.

    Args:
        key_func (Callable, optional): Function to extract priority from items.
            Default is the identity function (item is its own priority).
            For max-heap behavior, use: priority_functions.reverse
    """

    def __init__(self, key_func: Callable = lambda x: x):
        """Init a Priority Queue."""
        self._heap: List[Tuple[Any, int, T]] = []
        self._index = 0  # Used for stable sorting when priorities are equal
        self._key_func = key_func

    def push(self, item: T, priority: Optional[P] = None) -> None:
        """
        Add an item to the priority queue.

        Args:
            item: The item to be added
            priority (optional): External priority value. If not provided,
                               the item's own value will be used as priority
        """
        actual_priority: P = priority if priority is not None else cast(P, item)
        transformed_priority = self._key_func(actual_priority)
        heapq.heappush(self._heap, (transformed_priority, self._index, item))
        self._index += 1

    def extend(self, items: List[T]) -> None:
        """
        Add multiple items to the queue, using each item as its own priority.

        Args:
            items: Sequence of items to add

        Examples:
            >>> pq = PriorityQueue()
            >>> pq.extend([3, 1, 4])
            >>> list(pq.pop_all())
            [1, 3, 4]
        """
        for item in items:
            self.push(item)

    def extend_with_priority(self, items: List[Tuple[T, P]]) -> None:
        """
        Add multiple items with explicit priorities to the queue.

        Args:
            items: Sequence of (item, priority) tuples

        Examples:
            >>> pq = PriorityQueue()
            >>> pq.extend_with_priority([("task1", 2), ("task2", 1)])
            >>> list(pq.pop_all())
            ['task2', 'task1']
        """
        for item, priority in items:
            self.push(item, priority)

    def pop(self, get_key: bool = False) -> T | tuple[T, P]:
        """
        Remove and return the highest priority item.

        Returns:
            The item with the highest priority

        Raises:
            IndexError: If the queue is empty
        """
        if self.is_empty():
            raise IndexError("pop from an empty priority queue")

        key, _, root = heapq.heappop(self._heap)
        if get_key:
            return root, key
        return root

    def peek(self, get_key: bool = False) -> T | tuple[T, P]:
        """
        Return the highest priority item without removing it.

        Returns:
            The item with the highest priority

        Raises:
            IndexError: If the queue is empty
        """
        if self.is_empty():
            raise IndexError("peek at an empty priority queue")
        key, _, root = self._heap[0]
        if get_key:
            return root, key
        return root

    def is_empty(self) -> bool:
        """Check if the priority queue is empty."""
        return len(self._heap) == 0

    def __len__(self) -> int:
        """Return the number of items in the queue."""
        return len(self._heap)

    def __bool__(self) -> bool:
        """Return True if the queue is not empty."""
        return bool(self._heap)

    def __iter__(self) -> Iterator[T]:
        """
        Iterate through items in priority order without removing them.

        Returns:
            Iterator yielding items in priority order
        """
        return iter(item for _, _, item in sorted(self._heap))

    def __str__(self) -> str:
        """Return the string representation of the list of items in priority order."""
        return str(list(self.__iter__()))

    def pop_all(self, get_key: bool = False) -> Iterator[T] | Iterator[tuple[T, P]]:
        """
        Iterate through and remove all items in priority order.

        Returns:
            Iterator yielding items in priority order
        """
        while self:
            yield self.pop(get_key)

    def __enter__(self) -> "PriorityQueue[T, P]":
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager, clearing the queue."""
        self._heap.clear()
        self._index = 0

    @classmethod
    def from_items(
        cls, items: List[T], key_func: Callable = lambda x: x
    ) -> "PriorityQueue[T, P]":
        """
        Create a PriorityQueue from a list of items.

        Args:
            items: List of items to add to the queue
            key_func: Optional priority function

        Returns:
            New PriorityQueue containing the items
        """
        pq = cls(key_func)
        pq.extend(items)
        return pq

    @classmethod
    def from_items_with_priority(
        cls, pairs: List[Tuple[T, P]], key_func: Callable = lambda x: x
    ) -> "PriorityQueue[T, P]":
        """
        Create a PriorityQueue from a list of (item, priority) pairs.

        Args:
            pairs: List of (item, priority) tuples
            key_func: Optional priority function

        Returns:
            New PriorityQueue containing the items
        """
        pq = cls(key_func)
        pq.extend_with_priority(pairs)
        return pq

    @classmethod
    def merge(cls, queues: List["PriorityQueue[T, P]"]) -> "PriorityQueue[T, P]":
        """
        Merge multiple PriorityQueues into a new one.

        Args:
            queues: List of PriorityQueues to merge

        Returns:
            New PriorityQueue containing all items

        Note:
            All queues must use the same key_func
        """
        if not queues:
            return cls()

        # Use the key_func from the first queue
        merged = cls(queues[0]._key_func)
        for queue in queues:
            if queue._key_func != merged._key_func:
                raise ValueError("All queues must use the same key_func")
            merged._heap.extend(queue._heap)

        # Reheapify the merged heap
        heapq.heapify(merged._heap)
        return merged
