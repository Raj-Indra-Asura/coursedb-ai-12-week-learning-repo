"""
B+ Tree Educational Implementation

Week 7: Indexing, B+ Tree, Hashing

This is an EDUCATIONAL B+ tree implementation for learning purposes.
NOT intended for production use.

Learning Objectives:
- Understand B+ tree structure (internal nodes + leaf nodes)
- Learn how node splits work
- Visualize tree growth during insertion
- Understand why B+ trees are good for range queries

B+ Tree Properties:
- All data stored in leaf nodes
- Internal nodes store only keys for navigation
- Leaf nodes are linked (good for range scans)
- Self-balancing (height remains log(n))
- Order (m): Maximum children per node

Why B+ Trees for Databases?
- Minimize disk I/O (each node = one disk page)
- Efficient range queries (linked leaves)
- All data at same depth (predictable performance)
- High fanout reduces tree height

TODO (Week 7):
1. Implement Node class (internal and leaf)
2. Implement insert operation
3. Handle node splits
4. Implement search operation
5. Add visualization
6. Test with keys: 10, 20, 5, 6, 12, 30, 7
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class BPlusTreeNode:
    """
    B+ Tree Node

    For internal nodes:
    - keys: navigation keys
    - children: pointers to child nodes
    - is_leaf: False

    For leaf nodes:
    - keys: actual data keys
    - children: actual data values (or record pointers)
    - is_leaf: True
    - next: pointer to next leaf (for range scans)
    """
    order: int  # Maximum children
    keys: List[int]
    children: List  # List[BPlusTreeNode] for internal, List[any] for leaf
    is_leaf: bool
    next: Optional['BPlusTreeNode'] = None  # Only for leaf nodes

    def is_full(self) -> bool:
        """Check if node is full and needs to split"""
        return len(self.keys) >= self.order - 1


class BPlusTree:
    """
    B+ Tree Implementation

    Example Usage:
    >>> tree = BPlusTree(order=3)  # Each node can have 2-3 children
    >>> tree.insert(10)
    >>> tree.insert(20)
    >>> tree.insert(5)
    >>> tree.visualize()
    """

    def __init__(self, order: int = 3):
        """
        Initialize B+ tree

        Args:
            order: Maximum number of children per node
                  Typical database: 100-200 (one disk page)
                  Our educational example: 3 (easier to visualize)
        """
        if order < 3:
            raise ValueError("Order must be at least 3")

        self.order = order
        self.root = BPlusTreeNode(
            order=order,
            keys=[],
            children=[],
            is_leaf=True
        )

    def insert(self, key: int, value: any = None):
        """
        Insert key-value pair into B+ tree

        Steps:
        1. Find correct leaf node
        2. Insert key in sorted order
        3. If leaf is full, split it
        4. Propagate split up the tree if needed

        TODO (Week 7): Implement insertion logic
        """
        # TODO (Week 7): Implement insert
        pass

    def _split_leaf(self, node: BPlusTreeNode) -> Tuple[int, BPlusTreeNode]:
        """
        Split a full leaf node

        Returns:
            (middle_key, new_right_node)

        Algorithm:
        1. Split keys into two halves
        2. Create new right node
        3. Link nodes (for range scans)
        4. Return middle key to parent

        TODO (Week 7): Implement leaf split
        """
        pass

    def _split_internal(self, node: BPlusTreeNode) -> Tuple[int, BPlusTreeNode]:
        """
        Split a full internal node

        TODO (Week 7): Implement internal node split
        """
        pass

    def search(self, key: int) -> Optional[any]:
        """
        Search for a key in the B+ tree

        Returns:
            Value associated with key, or None if not found

        Algorithm:
        1. Start at root
        2. Navigate to correct child using key comparisons
        3. Repeat until reaching leaf
        4. Search for key in leaf

        TODO (Week 7): Implement search
        """
        pass

    def range_search(self, start_key: int, end_key: int) -> List[Tuple[int, any]]:
        """
        Range query: find all keys in [start_key, end_key]

        This is where B+ trees shine!

        Algorithm:
        1. Find leaf containing start_key
        2. Scan leaves left-to-right using next pointers
        3. Collect all keys until end_key

        TODO (Week 7): Implement range search
        """
        pass

    def visualize(self, node: Optional[BPlusTreeNode] = None, level: int = 0):
        """
        Print tree structure

        Example Output:
        Level 0 (root): [10, 20]
          Level 1 (leaf): [5, 10]
          Level 1 (leaf): [20, 30]

        TODO (Week 7): Implement visualization
        """
        if node is None:
            node = self.root

        indent = "  " * level
        node_type = "leaf" if node.is_leaf else "internal"
        print(f"{indent}Level {level} ({node_type}): {node.keys}")

        if not node.is_leaf:
            for child in node.children:
                self.visualize(child, level + 1)


# TODO (Week 7): Add test cases
def demo_bplus_tree():
    """
    Demonstrate B+ tree insertion

    Test sequence: 10, 20, 5, 6, 12, 30, 7

    Expected behavior:
    - Insert 10, 20, 5 → all fit in root (order=3)
    - Insert 6 → root splits
    - Continue inserting and observe splits
    """
    print("=== B+ Tree Demo ===")
    print("Order: 3 (max 3 children per node)")
    print()

    tree = BPlusTree(order=3)
    keys = [10, 20, 5, 6, 12, 30, 7]

    for key in keys:
        print(f"Inserting {key}...")
        tree.insert(key)
        tree.visualize()
        print()


if __name__ == "__main__":
    demo_bplus_tree()
