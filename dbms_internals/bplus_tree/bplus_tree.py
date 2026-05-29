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

from dataclasses import dataclass
from typing import Any, Optional


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
    keys: list[int]
    children: list  # List[BPlusTreeNode] for internal, List[any] for leaf
    is_leaf: bool
    next: Optional["BPlusTreeNode"] = None  # Only for leaf nodes

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
        self.root = BPlusTreeNode(order=order, keys=[], children=[], is_leaf=True)

    def insert(self, key: int, value: Any = None):
        """
        Insert key-value pair into B+ tree

        Steps:
        1. Find correct leaf node
        2. Insert key in sorted order
        3. If leaf is full, split it
        4. Propagate split up the tree if needed

        Learning Note:
        - Insertion always happens at leaf level
        - Splits propagate upward only when needed
        - Tree grows from leaf to root, not root to leaf
        """
        if value is None:
            value = f"value_{key}"

        # Find leaf node
        leaf = self._find_leaf(key)

        # Insert into leaf
        self._insert_into_leaf(leaf, key, value)

        # Check if leaf is overfull and needs split
        if len(leaf.keys) >= self.order:
            self._split_leaf_and_propagate(leaf, key)

    def _find_leaf(self, key: int) -> BPlusTreeNode:
        """
        Find leaf node where key should be inserted

        Algorithm:
        1. Start at root
        2. If leaf, return it
        3. Find correct child based on key comparisons
        4. Recurse to child

        Time Complexity: O(log n)
        """
        node = self.root

        while not node.is_leaf:
            # Find correct child
            child_index = 0
            for i, k in enumerate(node.keys):
                if key >= k:
                    child_index = i + 1

            node = node.children[child_index]

        return node

    def _insert_into_leaf(self, leaf: BPlusTreeNode, key: int, value: Any):
        """
        Insert key-value pair into leaf node (in sorted order)

        Learning Note:
        - Maintains sorted order for efficient search
        - Updates value if key already exists
        """
        # Check if key already exists (update case)
        if key in leaf.keys:
            index = leaf.keys.index(key)
            leaf.children[index] = value
            return

        # Find insertion position (maintain sorted order)
        insert_pos = len(leaf.keys)
        for i, k in enumerate(leaf.keys):
            if key < k:
                insert_pos = i
                break

        # Insert key and value
        leaf.keys.insert(insert_pos, key)
        leaf.children.insert(insert_pos, value)

    def _split_leaf_and_propagate(self, leaf: BPlusTreeNode, key: int):
        """
        Split a full leaf node and propagate split upward

        Algorithm:
        1. Split leaf into two halves
        2. Create new right node
        3. Link leaves (for range scans)
        4. Insert middle key into parent
        5. If parent is full, split parent (recursive)

        Learning Note:
        - Leaf split: copy middle key up (data stays in leaf)
        - Internal split: push middle key up (remove from node)
        """
        # Find parent path from root to this leaf
        parent, parent_index = self._find_parent(self.root, leaf, key)

        # Split the leaf
        mid = len(leaf.keys) // 2
        split_key = leaf.keys[mid]

        # Create new right node
        new_right = BPlusTreeNode(
            order=self.order,
            keys=leaf.keys[mid:],
            children=leaf.children[mid:],
            is_leaf=True,
            next=leaf.next,
        )

        # Update original leaf (becomes left node)
        leaf.keys = leaf.keys[:mid]
        leaf.children = leaf.children[:mid]
        leaf.next = new_right

        # Insert split key into parent
        if parent is None:
            # Root was a leaf, create new root
            new_root = BPlusTreeNode(
                order=self.order, keys=[split_key], children=[leaf, new_right], is_leaf=False
            )
            self.root = new_root
        else:
            # Insert into existing parent
            self._insert_into_internal(parent, split_key, new_right, parent_index)

    def _find_parent(
        self, current: BPlusTreeNode, target: BPlusTreeNode, key: int
    ) -> tuple[BPlusTreeNode | None, int]:
        """
        Find parent of target node

        Returns:
            (parent_node, child_index) or (None, -1) if target is root
        """
        if current == target:
            return None, -1

        if current.is_leaf:
            return None, -1

        # Check if target is a direct child
        for i, child in enumerate(current.children):
            if child == target:
                return current, i

        # Recurse to correct child
        child_index = 0
        for i, k in enumerate(current.keys):
            if key >= k:
                child_index = i + 1

        if child_index < len(current.children):
            return self._find_parent(current.children[child_index], target, key)

        return None, -1

    def _insert_into_internal(
        self, node: BPlusTreeNode, key: int, right_child: BPlusTreeNode, child_index: int
    ):
        """
        Insert key and right child into internal node

        Args:
            node: Internal node to insert into
            key: Separator key to insert
            right_child: New right child node produced by the split
            child_index: Index of the left child (the node that was split)
                within ``node.children``

        Learning Note:
        - The left child sits at ``node.children[child_index]``; the separator
          key therefore belongs at ``node.keys[child_index]`` and the new right
          child immediately after it at ``node.children[child_index + 1]``.
        """
        node.keys.insert(child_index, key)
        node.children.insert(child_index + 1, right_child)

        # Check if node needs split
        if len(node.keys) >= self.order:
            self._split_internal_and_propagate(node, key)

    def _split_internal_and_propagate(self, node: BPlusTreeNode, key: int):
        """
        Split a full internal node

        Learning Note:
        - Middle key is PUSHED UP (not copied)
        - Different from leaf split (which copies key up)
        """
        parent, parent_index = self._find_parent(self.root, node, key)

        mid = len(node.keys) // 2
        push_up_key = node.keys[mid]

        # Create new right node
        new_right = BPlusTreeNode(
            order=self.order,
            keys=node.keys[mid + 1 :],
            children=node.children[mid + 1 :],
            is_leaf=False,
        )

        # Update original node (becomes left)
        node.keys = node.keys[:mid]
        node.children = node.children[: mid + 1]

        # Insert into parent
        if parent is None:
            # Create new root
            new_root = BPlusTreeNode(
                order=self.order, keys=[push_up_key], children=[node, new_right], is_leaf=False
            )
            self.root = new_root
        else:
            self._insert_into_internal(parent, push_up_key, new_right, parent_index)

    def _split_leaf(self, node: BPlusTreeNode) -> tuple[int, BPlusTreeNode]:
        """
        Split a full leaf node (legacy method for compatibility)

        Returns:
            (middle_key, new_right_node)
        """
        mid = len(node.keys) // 2
        split_key = node.keys[mid]

        new_right = BPlusTreeNode(
            order=self.order,
            keys=node.keys[mid:],
            children=node.children[mid:],
            is_leaf=True,
            next=node.next,
        )

        node.keys = node.keys[:mid]
        node.children = node.children[:mid]
        node.next = new_right

        return split_key, new_right

    def _split_internal(self, node: BPlusTreeNode) -> tuple[int, BPlusTreeNode]:
        """
        Split a full internal node (legacy method for compatibility)

        Returns:
            (push_up_key, new_right_node)
        """
        mid = len(node.keys) // 2
        push_up_key = node.keys[mid]

        new_right = BPlusTreeNode(
            order=self.order,
            keys=node.keys[mid + 1 :],
            children=node.children[mid + 1 :],
            is_leaf=False,
        )

        node.keys = node.keys[:mid]
        node.children = node.children[: mid + 1]

        return push_up_key, new_right

    def search(self, key: int) -> Any | None:
        """
        Search for a key in the B+ tree

        Returns:
            Value associated with key, or None if not found

        Algorithm:
        1. Start at root
        2. Navigate to correct child using key comparisons
        3. Repeat until reaching leaf
        4. Search for key in leaf

        Time Complexity: O(log n)
        """
        node = self.root

        # Navigate to leaf
        while not node.is_leaf:
            child_index = 0
            for i, k in enumerate(node.keys):
                if key >= k:
                    child_index = i + 1

            node = node.children[child_index]

        # Search in leaf
        if key in node.keys:
            index = node.keys.index(key)
            return node.children[index]

        return None

    def range_search(self, start_key: int, end_key: int) -> list[tuple[int, Any]]:
        """
        Range query: find all keys in [start_key, end_key]

        This is where B+ trees shine!

        Algorithm:
        1. Find leaf containing start_key
        2. Scan leaves left-to-right using next pointers
        3. Collect all keys until end_key

        Time Complexity: O(log n + k) where k = result size

        Learning Note:
        - Leaf nodes are linked = efficient range scans
        - No need to traverse tree for each key
        - This is why B+ trees beat hash indexes for ranges
        """
        results = []

        # Find starting leaf
        node = self.root
        while not node.is_leaf:
            child_index = 0
            for i, k in enumerate(node.keys):
                if start_key >= k:
                    child_index = i + 1
            node = node.children[child_index]

        # Scan leaves using next pointers
        while node is not None:
            for i, key in enumerate(node.keys):
                if start_key <= key <= end_key:
                    results.append((key, node.children[i]))
                elif key > end_key:
                    return results

            node = node.next

        return results

    def visualize(self, node: BPlusTreeNode | None = None, level: int = 0):
        """
        Print tree structure

        Example Output:
        Level 0 (root): keys=[10, 20]
          Level 1 (leaf): keys=[5, 10]
          Level 1 (internal): keys=[15]
          Level 1 (leaf): keys=[20, 30]

        Learning Note:
        - Indentation shows tree depth
        - All leaves at same level (balanced)
        """
        if node is None:
            node = self.root

        indent = "  " * level
        node_type = "leaf" if node.is_leaf else "internal"
        if level == 0:
            node_type = "root"

        print(f"{indent}Level {level} ({node_type}): keys={node.keys}")

        if not node.is_leaf:
            for child in node.children:
                self.visualize(child, level + 1)


def demo_bplus_tree():
    """
    Demonstrate B+ tree insertion

    Test sequence: 10, 20, 5, 6, 12, 30, 7, 17

    Expected behavior:
    - Insert 10, 20 → both fit in root (order=3)
    - Insert 5 → root splits
    - Continue inserting and observe splits

    Learning Points:
    - Watch how tree grows upward
    - See how keys are redistributed during splits
    - Notice all data stays in leaves
    """
    print("=" * 60)
    print("B+ Tree Demo (Educational)")
    print("=" * 60)
    print("Order: 3 (max 3 children per node)")
    print()

    tree = BPlusTree(order=3)
    keys = [10, 20, 5, 6, 12, 30, 7, 17]

    for key in keys:
        print(f"\n{'='*60}")
        print(f"Inserting: {key}")
        print("=" * 60)
        tree.insert(key)
        tree.visualize()

    # Demonstrate search
    print(f"\n{'='*60}")
    print("Search Examples")
    print("=" * 60)
    test_keys = [10, 12, 99]
    for key in test_keys:
        result = tree.search(key)
        status = "Found" if result else "Not found"
        print(f"Search {key}: {status} → {result}")

    # Demonstrate range search
    print(f"\n{'='*60}")
    print("Range Search Example")
    print("=" * 60)
    print("Range [5, 15]:")
    results = tree.range_search(5, 15)
    for key, value in results:
        print(f"  {key}: {value}")

    print("\n" + "=" * 60)
    print("Key Takeaways:")
    print("=" * 60)
    print("✓ All data in leaf nodes")
    print("✓ Internal nodes guide search")
    print("✓ Balanced tree (all leaves at same depth)")
    print("✓ Range queries efficient (linked leaves)")
    print("✓ Self-balancing (splits maintain balance)")


if __name__ == "__main__":
    demo_bplus_tree()
