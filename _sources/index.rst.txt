SimpleDSA Documentation
=======================

SimpleDSA is a simple and intuitive implementation of common data structures and algorithms in Python.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   examples
   api
   changelog

Installation
------------

.. code-block:: bash

   pip install simpledsa

Quick Start
-----------

.. code-block:: python

   from simpledsa import PriorityQueue

   # Create a priority queue
   pq = PriorityQueue()

   # Add items
   pq.push(2)
   pq.extend([3, 1, 4])

   # Process items in priority order
   while pq:
       print(pq.pop())  # prints: 1, 2, 3, 4
