import unittest

from simpledsa import PriorityQueue, priority_functions


class TestPriorityQueue(unittest.TestCase):
    def setUp(self):
        self.pq = PriorityQueue()
        self.max_pq = PriorityQueue(lambda x: -x)

    def test_empty_queue(self):
        self.assertTrue(self.pq.is_empty())
        self.assertEqual(len(self.pq), 0)
        self.assertFalse(bool(self.pq))

    def test_push_pop_default_priority(self):
        items = [3, 1, 4, 1, 5]
        for item in items:
            self.pq.push(item)

        sorted_items = sorted(items)
        for expected in sorted_items:
            self.assertEqual(self.pq.pop(), expected)

    def test_push_explicit_priority(self):
        items = [("task1", 3), ("task2", 1), ("task3", 4)]
        for item, priority in items:
            self.pq.push(item, priority)

        expected_order = ["task2", "task1", "task3"]
        for expected in expected_order:
            self.assertEqual(self.pq.pop(), expected)

    def test_pop_explicit_priority(self):
        items = [("task1", 3), ("task2", 1), ("task3", 4)]
        for item, priority in items:
            self.pq.push(item, priority)

        expected_order = [("task2", 1), ("task1", 3), ("task3", 4)]
        for expected in expected_order:
            self.assertEqual(self.pq.pop_with_priority(), expected)

    def test_extend(self):
        """Test extending with items using their own priority."""
        pq = PriorityQueue()
        items = [3, 1, 4]
        pq.extend(items)
        assert list(pq.pop_all()) == [1, 3, 4]

    def test_extend_with_priority(self):
        """Test extending with item-priority pairs."""
        pq = PriorityQueue()
        items = [("task1", 2), ("task2", 1), ("task3", 3)]
        pq.extend_with_priority(items)
        assert list(pq.pop_all()) == ["task2", "task1", "task3"]

    def test_extend_empty_sequence(self):
        """Test extending with empty sequences."""
        pq = PriorityQueue()
        pq.extend([])
        pq.extend_with_priority([])
        assert len(pq) == 0

    def test_extend_with_priority_max_heap(self):
        """Test extending with priorities in a max heap."""
        pq = PriorityQueue(priority_functions.reverse)
        items = [("task1", 2), ("task2", 1), ("task3", 3)]
        pq.extend_with_priority(items)
        assert list(pq.pop_all()) == ["task3", "task1", "task2"]

    def test_max_heap(self):
        items = [3, 1, 4, 1, 5]
        for item in items:
            self.max_pq.push(item)

        sorted_items = sorted(items, reverse=True)
        for expected in sorted_items:
            self.assertEqual(self.max_pq.pop(), expected)

    def test_peek(self):
        self.pq.push("task1", 1)
        self.pq.push("task2", 2)
        self.assertEqual(self.pq.peek(), "task1")
        self.assertEqual(len(self.pq), 2)  # Ensure peek didn't remove item

    def test_peek_with_priority(self):
        self.pq.push("task1", 1)
        self.pq.push("task2", 2)
        self.assertEqual(self.pq.peek_with_priority(), ("task1", 1))
        self.assertEqual(len(self.pq), 2)  # Ensure peek didn't remove item

    def test_bool_evaluation(self):
        self.assertFalse(bool(self.pq))
        self.pq.push("task", 1)
        self.assertTrue(bool(self.pq))

    def test_mixed_priorities(self):
        # Test mixing items with and without explicit priorities
        self.pq.push(3)  # item is priority
        self.pq.push("task", 1)  # explicit priority
        self.pq.push(2)  # item is priority

        self.assertEqual(self.pq.pop(), "task")  # priority 1
        self.assertEqual(self.pq.pop(), 2)  # priority 2
        self.assertEqual(self.pq.pop(), 3)  # priority 3

    def test_empty_errors(self):
        with self.assertRaises(IndexError):
            self.pq.pop()
        with self.assertRaises(IndexError):
            self.pq.peek()

    def test_context_manager(self):
        with PriorityQueue() as pq:
            pq.push(1)
            pq.push(2)
            self.assertEqual(len(pq), 2)
        self.assertEqual(len(pq), 0)

    def test_iteration(self):
        items = [3, 1, 4, 1, 5]
        self.pq.extend(items)

        # Non-destructive iteration
        self.assertEqual(list(self.pq), sorted(items))
        self.assertEqual(len(self.pq), len(items))

        # Destructive iteration
        self.assertEqual([x for x in self.pq.pop_all()], sorted(items))
        self.assertEqual(len(self.pq), 0)

    def test_from_items(self):
        items = [3, 1, 4]
        pq = PriorityQueue.from_items(items)
        self.assertEqual([x for x in pq.pop_all()], [1, 3, 4])

    def test_from_pairs(self):
        pairs = [("task1", 2), ("task2", 1), ("task3", 3)]
        pq = PriorityQueue.from_items_with_priority(pairs)
        self.assertEqual([x for x in pq.pop_all()], ["task2", "task1", "task3"])

    def test_merge(self):
        pq1 = PriorityQueue.from_items([1, 3])
        pq2 = PriorityQueue.from_items([2, 4])
        merged = PriorityQueue.merge([pq1, pq2])
        self.assertEqual([x for x in merged.pop_all()], [1, 2, 3, 4])

    def test_merge_with_empty(self):
        merged = PriorityQueue.merge([])
        self.assertEqual(merged._heap, PriorityQueue()._heap)

    def test_merge_different_priority(self):
        pq1 = PriorityQueue(lambda x: -x)
        pq1.extend([1, 3])
        pq2 = PriorityQueue.from_items([2, 4])
        with self.assertRaises(ValueError):
            PriorityQueue.merge([pq1, pq2])

    def test_priority_functions(self):
        # Test reverse (max heap)
        pq = PriorityQueue(priority_functions.reverse)
        pq.extend([1, 2, 3])
        self.assertEqual([x for x in pq.pop_all()], [3, 2, 1])

        # Test by_length
        pq = PriorityQueue(priority_functions.by_length)
        pq.extend(["a", "ccc", "bb"])
        self.assertEqual([x for x in pq.pop_all()], ["a", "bb", "ccc"])

        # Test by_attr
        class Task:
            def __init__(self, name, priority):
                self.name = name
                self.priority = priority

        pq = PriorityQueue(priority_functions.by_attr("priority"))
        tasks = [Task("A", 2), Task("B", 1), Task("C", 3)]
        pq.extend(tasks)
        result = [t.name for t in pq.pop_all()]
        self.assertEqual(result, ["B", "A", "C"])

    def test_pop_all_with_priority(self):
        pairs = [("B", 2), ("A", 1), ("C", 3)]
        pq = PriorityQueue.from_items_with_priority(pairs)
        self.assertEqual(
            [x for x in pq.pop_all_with_priority()], sorted(pairs, key=lambda x: x[1])
        )

    def test_pop_empty_queue_raises_index_error(self):
        with self.assertRaises(IndexError, msg="pop from an empty priority queue"):
            self.pq.pop()

    def test_peek_empty_queue_raises_index_error(self):
        with self.assertRaises(IndexError, msg="peek from an empty priority queue"):
            self.pq.peek()

    def test_pop_with_priority_empty_queue_raises_index_error(self):
        with self.assertRaises(IndexError, msg="pop from an empty priority queue"):
            self.pq.pop_with_priority()

    def test_peek_with_priority_empty_queue_raises_index_error(self):
        with self.assertRaises(IndexError, msg="peek from an empty priority queue"):
            self.pq.peek_with_priority()

    def test_string_representation(self):
        pq = PriorityQueue()
        items = [("B", 3), ("A", 1), ("C", 4)]
        pq.extend_with_priority(items)

        expected_representation = "['A', 'B', 'C']"
        self.assertEqual(str(pq), expected_representation)

        empty_pq = PriorityQueue()
        self.assertEqual(str(empty_pq), "[]")
