# SimpleDSA

[![PyPI version](https://badge.fury.io/py/simpledsa.svg)](https://badge.fury.io/py/simpledsa)
[![Python Package](https://github.com/dsalathe/simpledsa/actions/workflows/python-package.yml/badge.svg)](https://github.com/dsalathe/simpledsa/actions/workflows/python-package.yml)
[![codecov](https://codecov.io/gh/dsalathe/simpledsa/branch/main/graph/badge.svg)](https://codecov.io/gh/dsalathe/simpledsa)
[![Documentation Status](https://readthedocs.org/projects/simpledsa/badge/?version=latest)](https://simpledsa.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/simpledsa.svg)](https://pypi.org/project/simpledsa/)

A simple and intuitive implementation of data structures and algorithms in Python.

## Installation

```bash
pip install simpledsa
```

## Usage

### Priority Queue

```python
from simpledsa import PriorityQueue

# Create a min-heap priority queue (smaller values have higher priority)
pq = PriorityQueue()

# Create a max-heap priority queue (larger values have higher priority)
max_pq = PriorityQueue(lambda x: -x)

# Using items as their own priority
pq.push(3)
pq.push(1)
pq.push(4)
print(pq.pop())  # Output: 1 (smallest value has highest priority)
print(pq.pop())  # Output: 3
print(pq.pop())  # Output: 4

# Using explicit priorities
task_queue = PriorityQueue()
task_queue.push("Write docs", priority=2)
task_queue.push("Fix bug", priority=1)
task_queue.push("Add feature", priority=3)

print(task_queue.pop())  # Output: "Fix bug" (priority 1)
print(task_queue.pop())  # Output: "Write docs" (priority 2)
print(task_queue.pop())  # Output: "Add feature" (priority 3)

# Check if queue is empty
if not pq:
    print("Queue is empty")

# Get length of queue
print(len(pq))  # Output: 0

# Peek at highest priority item without removing it
task_queue.push("Important task", priority=1)
print(task_queue.peek())  # Output: "Important task"
```

## Advanced Usage Examples

### Context Manager (with statement)

```python
from simpledsa import PriorityQueue

# Queue is automatically cleared when exiting the with block
with PriorityQueue() as pq:
    pq.push("task1", 1)
    pq.push("task2", 2)
    process_tasks(pq)  # process tasks here
# queue is now empty

# Great for temporary task processing
with PriorityQueue() as pq:
    pq.extend(tasks)
    while pq:
        process(pq.pop())
```

### Batch Operations

```python
# Add multiple items at once
pq = PriorityQueue()
pq.extend([1, 2, 3])  # items as their own priorities
pq.extend([("task1", 1), ("task2", 2)])  # For (item, priority) pairs

# Create queue from items
pq = PriorityQueue.from_items([1, 2, 3])

# Create queue from (item, priority) pairs
pq = PriorityQueue.from_items_with_priority([("task1", 1), ("task2", 2)])
```

### Iteration

```python
# Non-destructive iteration (keeps items in queue)
pq = PriorityQueue.from_items([3, 1, 4, 1, 5])
for item in pq:
    print(item)  # prints in priority order: 1, 1, 3, 4, 5

# Destructive iteration (removes items)
for item in pq.pop_all():
    process(item)  # process items in priority order
```

### Queue Merging

```python
# Merge multiple queues
pq1 = PriorityQueue.from_items([1, 3, 5])
pq2 = PriorityQueue.from_items([2, 4, 6])
merged = PriorityQueue.merge([pq1, pq2])
```

### Priority Functions

```python
from simpledsa import PriorityQueue, priority_functions

# Max heap (larger values have higher priority)
max_pq = PriorityQueue(priority_functions.reverse)
max_pq.extend([1, 2, 3])
print(max_pq.pop())  # 3

# Priority by length
length_pq = PriorityQueue(priority_functions.by_length)
length_pq.extend(["a", "ccc", "bb"])
print(length_pq.pop())  # "a" (shortest)

# Priority by attribute
class Task:
    def __init__(self, name, priority):
        self.name = name
        self.priority = priority

task_pq = PriorityQueue(priority_functions.by_attr('priority'))
tasks = [Task("A", 2), Task("B", 1), Task("C", 3)]
task_pq.extend(tasks)
```

### Features

- Supports both min-heap (default) and max-heap behavior
- Items can serve as their own priority or have explicit priorities
- Stable sorting: items with equal priorities maintain their insertion order
- Standard Python container operations: `len()`, boolean evaluation
- O(log n) push and pop operations
- O(1) peek and is_empty operations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Development

### Setting up development environment

```bash
# Clone the repository
git clone https://github.com/dsalathe/simpledsa.git
cd simpledsa

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Run tests
poetry run pytest

# Format code
poetry run black .
poetry run isort .

# Type checking
poetry run mypy simpledsa
```

### Building documentation

```bash
cd docs
poetry run make html
```

The documentation will be available in `docs/_build/html`.

### Publishing a new version

1. Update version in pyproject.toml
2. Create and push a new tag:

```bash
git tag v0.1.1
git push origin v0.1.1
```

The GitHub Action will automatically build and publish to PyPI.
