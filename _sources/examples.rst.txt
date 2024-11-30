Usage Examples
==============

Basic Usage
-----------

Using Self-Priority Items
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from simpledsa import PriorityQueue

    # Create a min-heap
    pq = PriorityQueue()

    # Add items using their values as priorities
    pq.extend([3, 1, 4])

    # Items come out in priority order
    while pq:
        print(pq.pop())  # prints: 1, 3, 4

Using Explicit Priorities
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from simpledsa import PriorityQueue

    pq = PriorityQueue()

    # Add items with explicit priorities
    tasks = [
        ("urgent task", 1),
        ("normal task", 2),
        ("low priority task", 3)
    ]
    pq.extend_with_priority(tasks)

    while pq:
        task = pq.pop()
        print(task)  # prints tasks in priority order

Advanced Usage
--------------

Max Heap
~~~~~~~~

.. code-block:: python

    from simpledsa import PriorityQueue, priority_functions

    # Create a max-heap
    pq = PriorityQueue(priority_functions.reverse)

    pq.extend([1, 3, 2])
    while pq:
        print(pq.pop())  # prints: 3, 2, 1

Custom Priority Functions
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from simpledsa import PriorityQueue, priority_functions

    # Priority by string length
    pq = PriorityQueue(priority_functions.by_length)

    pq.extend(["a", "ccc", "bb"])
    while pq:
        print(pq.pop())  # prints: "a", "bb", "ccc"
