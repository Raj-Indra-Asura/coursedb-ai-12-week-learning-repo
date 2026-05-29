"""
Hash Index Simulator

Week 7: Indexing, B+ Tree, Hashing

Educational hash index implementation for learning.

Learning Objectives:
- Understand hash function basics
- Learn collision handling strategies
- Compare hash indexes with B+ trees
- Understand trade-offs (equality vs range queries)

Hash Index Properties:
- O(1) average lookup time (amazing for equality!)
- Cannot handle range queries (no ordering)
- Collision handling needed
- Simple structure (array of buckets)

Why Hash Indexes?
- Fast equality searches: WHERE id = 42
- Memory efficient
- Simple implementation

When NOT to use Hash Indexes?
- Range queries: WHERE salary > 50000
- ORDER BY queries
- Inequality searches: WHERE age < 30

TODO (Week 7):
1. Implement hash function
2. Handle collisions (chaining)
3. Implement insert
4. Implement search
5. Visualize bucket distribution
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class HashBucket:
    """
    Single bucket in hash index
    Uses chaining for collision handling
    """

    key_value_pairs: list[tuple[int, Any]] = field(default_factory=list)

    def insert(self, key: int, value: Any):
        """Insert or update key-value pair"""
        # Check if key exists (update)
        for i, (k, _v) in enumerate(self.key_value_pairs):
            if k == key:
                self.key_value_pairs[i] = (key, value)
                return

        # New key (append)
        self.key_value_pairs.append((key, value))

    def search(self, key: int) -> Any | None:
        """Search for key in bucket"""
        for k, v in self.key_value_pairs:
            if k == key:
                return v
        return None

    def delete(self, key: int) -> bool:
        """Delete key from bucket"""
        for i, (k, _v) in enumerate(self.key_value_pairs):
            if k == key:
                del self.key_value_pairs[i]
                return True
        return False


class HashIndex:
    """
    Hash Index Implementation

    Uses simple modulo hash function: key % bucket_count
    Collision handling: Chaining (linked list per bucket)

    Example:
    >>> index = HashIndex(bucket_count=10)
    >>> index.insert(42, "answer")
    >>> index.search(42)
    'answer'
    """

    def __init__(self, bucket_count: int = 10):
        """
        Initialize hash index

        Args:
            bucket_count: Number of buckets (array size)
                         Trade-off: More buckets = fewer collisions but more memory
        """
        self.bucket_count = bucket_count
        self.buckets: list[HashBucket] = [HashBucket() for _ in range(bucket_count)]
        self.total_keys = 0

    def _hash(self, key: int) -> int:
        """
        Hash function: key % bucket_count

        Properties:
        - Deterministic: same key → same bucket
        - Uniform distribution (ideally)
        - Fast to compute

        Real databases use more sophisticated hash functions
        (e.g., MurmurHash, xxHash)
        """
        return key % self.bucket_count

    def insert(self, key: int, value: Any = None):
        """
        Insert key-value pair

        Steps:
        1. Compute hash: bucket_index = key % bucket_count
        2. Insert into bucket (handles collisions via chaining)

        Time Complexity:
        - Average: O(1)
        - Worst (all keys collide): O(n)
        """
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]

        # Check if this is a new key. We test key membership directly rather
        # than relying on the searched value, because a stored value may itself
        # be ``None`` (which would otherwise be indistinguishable from "absent").
        is_new = all(k != key for k, _ in bucket.key_value_pairs)

        bucket.insert(key, value)

        if is_new:
            self.total_keys += 1

    def search(self, key: int) -> Any | None:
        """
        Search for key

        Steps:
        1. Compute hash
        2. Search in bucket

        Time Complexity: O(1) average, O(n) worst case
        """
        bucket_index = self._hash(key)
        return self.buckets[bucket_index].search(key)

    def delete(self, key: int) -> bool:
        """Delete key from index"""
        bucket_index = self._hash(key)
        if self.buckets[bucket_index].delete(key):
            self.total_keys -= 1
            return True
        return False

    def visualize(self):
        """
        Visualize bucket distribution

        Shows which keys ended up in which buckets
        Helps understand collision patterns
        """
        print(f"=== Hash Index (buckets={self.bucket_count}, keys={self.total_keys}) ===")
        print()

        for i, bucket in enumerate(self.buckets):
            if bucket.key_value_pairs:
                keys = [k for k, v in bucket.key_value_pairs]
                print(f"Bucket {i}: {keys}")
            else:
                print(f"Bucket {i}: (empty)")

        # Calculate statistics
        non_empty = sum(1 for b in self.buckets if b.key_value_pairs)
        max_chain = max(len(b.key_value_pairs) for b in self.buckets)
        avg_chain = self.total_keys / non_empty if non_empty > 0 else 0

        print()
        print("Statistics:")
        print(f"  Non-empty buckets: {non_empty}/{self.bucket_count}")
        print(f"  Max chain length: {max_chain}")
        print(f"  Avg chain length: {avg_chain:.2f}")
        print(f"  Load factor: {self.total_keys / self.bucket_count:.2f}")

    def compare_with_bplus_tree(self):
        """
        Educational comparison with B+ tree

        Hash Index vs B+ Tree:
        - Equality search: Hash wins (O(1) vs O(log n))
        - Range search: B+ tree wins (O(log n + k) vs impossible)
        - Ordering: B+ tree maintains, hash doesn't
        - Memory: Hash can use less memory
        """
        print("\n=== Hash Index vs B+ Tree ===")
        print()
        print("| Operation           | Hash Index | B+ Tree      |")
        print("|---------------------|------------|--------------|")
        print("| Equality (WHERE =)  | O(1) ✓     | O(log n)     |")
        print("| Range (WHERE < >)   | Not supported | O(log n+k) ✓ |")
        print("| ORDER BY            | Not supported | O(n) ✓       |")
        print("| Sorted scan         | Not supported | O(k) ✓       |")
        print("| Memory usage        | Low ✓      | Medium       |")
        print()
        print("Use hash index when:")
        print("  - Only equality searches")
        print("  - No range queries needed")
        print("  - No sorting needed")
        print()
        print("Use B+ tree when:")
        print("  - Range queries needed")
        print("  - Sorting needed")
        print("  - General purpose")


def demo_hash_index():
    """
    Demonstrate hash index

    Test with keys that will collide
    """
    print("=== Hash Index Demo ===")
    print("Bucket count: 10")
    print("Hash function: key % 10")
    print()

    index = HashIndex(bucket_count=10)

    # Insert keys
    keys = [12, 22, 32, 5, 15, 25, 7, 17]

    print("Inserting keys:", keys)
    for key in keys:
        index.insert(key, f"value_{key}")
        print(f"  {key} → bucket {key % 10}")

    print()
    index.visualize()

    # Test search
    print("\n=== Search Examples ===")
    test_keys = [12, 99, 25]
    for key in test_keys:
        result = index.search(key)
        print(f"Search {key}: {result}")

    # Show comparison
    index.compare_with_bplus_tree()


if __name__ == "__main__":
    demo_hash_index()
