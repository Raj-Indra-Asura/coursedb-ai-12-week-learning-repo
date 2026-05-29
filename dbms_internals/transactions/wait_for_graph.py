"""
Wait-For Graph Deadlock Detector

Week 9: Transactions, ACID, Concurrency

Detects deadlocks using wait-for graph cycle detection.

Learning Objectives:
- Understand transaction dependencies
- Build wait-for graph
- Detect cycles (deadlocks)
- Visualize deadlock scenarios

Wait-For Graph:
- Nodes: Transactions
- Edges: T1 → T2 if T1 is waiting for T2
- Deadlock: Cycle in graph

Example:
T1 holds lock on X, waits for Y
T2 holds lock on Y, waits for X
→ Cycle: T1 → T2 → T1 (DEADLOCK!)

TODO (Week 9):
1. Implement graph representation
2. Implement cycle detection (DFS)
3. Visualize wait-for graph
4. Test with deadlock scenarios
"""

from typing import List, Dict, Set, Optional
from dataclasses import dataclass
from collections import defaultdict, deque


@dataclass
class Transaction:
    """Represents a transaction"""
    tx_id: str
    holds: List[str]  # Resources this transaction holds
    waits_for: List[str]  # Resources this transaction waits for


class WaitForGraph:
    """
    Wait-For Graph for Deadlock Detection

    Example Usage:
    >>> graph = WaitForGraph()
    >>> graph.add_transaction("T1", holds=["X"], waits_for=["Y"])
    >>> graph.add_transaction("T2", holds=["Y"], waits_for=["X"])
    >>> graph.detect_deadlock()
    True
    >>> graph.get_deadlock_cycle()
    ['T1', 'T2', 'T1']
    """

    def __init__(self):
        # Adjacency list: tx_id → [tx_ids that this tx waits for]
        self.graph: Dict[str, List[str]] = defaultdict(list)
        # Resource ownership: resource → tx_id that holds it
        self.resource_owner: Dict[str, str] = {}
        # Transactions
        self.transactions: Dict[str, Transaction] = {}

    def add_transaction(self, tx_id: str, holds: List[str], waits_for: List[str]):
        """
        Add transaction to wait-for graph

        Args:
            tx_id: Transaction ID
            holds: Resources currently held
            waits_for: Resources waiting for
        """
        # Store transaction
        self.transactions[tx_id] = Transaction(tx_id, holds, waits_for)

        # Record resource ownership
        for resource in holds:
            self.resource_owner[resource] = tx_id

        # (Re)build the wait-for edges. Building from scratch here makes the
        # graph independent of the order in which transactions are added: an
        # edge T_a -> T_b is created whenever T_a waits for a resource held by
        # T_b, regardless of which was added first.
        self._rebuild_edges()

    def _rebuild_edges(self) -> None:
        """Recompute all wait-for edges from the current ownership map."""
        self.graph = defaultdict(list)
        for tx_id, transaction in self.transactions.items():
            for resource in transaction.waits_for:
                blocking_tx = self.resource_owner.get(resource)
                if blocking_tx is not None and blocking_tx != tx_id:
                    if blocking_tx not in self.graph[tx_id]:
                        self.graph[tx_id].append(blocking_tx)

    def detect_deadlock(self) -> bool:
        """
        Detect if deadlock exists (cycle in graph)

        Algorithm: Depth-First Search (DFS) with cycle detection

        Returns:
            True if deadlock exists, False otherwise
        """
        # TODO (Week 9): Implement cycle detection
        visited = set()
        rec_stack = set()

        def has_cycle_dfs(node: str, path: List[str]) -> bool:
            """DFS to detect cycle"""
            if node in rec_stack:
                # Found cycle!
                return True
            if node in visited:
                return False

            visited.add(node)
            rec_stack.add(node)

            for neighbor in self.graph.get(node, []):
                if has_cycle_dfs(neighbor, path + [neighbor]):
                    return True

            rec_stack.remove(node)
            return False

        # Check all nodes for cycles (snapshot keys: the graph is a defaultdict
        # and DFS lookups must not mutate it during iteration).
        for tx_id in list(self.graph):
            if tx_id not in visited:
                if has_cycle_dfs(tx_id, [tx_id]):
                    return True

        return False

    def get_deadlock_cycle(self) -> Optional[List[str]]:
        """
        Find and return a deadlock cycle if it exists

        Returns:
            List of transaction IDs in cycle, or None
        """
        # TODO (Week 9): Implement cycle extraction
        visited = set()
        rec_stack = []

        def find_cycle_dfs(node: str) -> Optional[List[str]]:
            if node in rec_stack:
                # Found cycle! Extract it
                cycle_start = rec_stack.index(node)
                return rec_stack[cycle_start:] + [node]

            if node in visited:
                return None

            visited.add(node)
            rec_stack.append(node)

            for neighbor in self.graph.get(node, []):
                cycle = find_cycle_dfs(neighbor)
                if cycle:
                    return cycle

            rec_stack.pop()
            return None

        for tx_id in list(self.graph):
            cycle = find_cycle_dfs(tx_id)
            if cycle:
                return cycle

        return None

    def visualize(self):
        """
        Print wait-for graph

        Example Output:
        T1 → T2 (T1 waits for T2)
        T2 → T1 (T2 waits for T1)
        """
        print("=== Wait-For Graph ===")
        print()

        if not self.graph:
            print("(empty)")
            return

        for tx_id, waits_for_txs in self.graph.items():
            if waits_for_txs:
                for other_tx in waits_for_txs:
                    print(f"{tx_id} → {other_tx}")
            else:
                print(f"{tx_id} (not waiting)")

        print()

        # Show deadlock if exists
        if self.detect_deadlock():
            cycle = self.get_deadlock_cycle()
            print("⚠️  DEADLOCK DETECTED!")
            print(f"Cycle: {' → '.join(cycle)}")
        else:
            print("✓ No deadlock")


def demo_deadlock_detection():
    """
    Demonstrate deadlock detection

    Scenario 1: Simple Deadlock
    - T1 holds X, waits for Y
    - T2 holds Y, waits for X
    → Cycle: T1 → T2 → T1

    Scenario 2: No Deadlock
    - T1 holds X, waits for Y
    - T2 holds Y (no wait)
    - T3 waits for X
    → No cycle
    """
    print("=== Scenario 1: Simple Deadlock ===")
    print()

    graph1 = WaitForGraph()
    graph1.add_transaction("T1", holds=["X"], waits_for=["Y"])
    graph1.add_transaction("T2", holds=["Y"], waits_for=["X"])
    graph1.visualize()

    print("\n" + "="*50 + "\n")

    print("=== Scenario 2: No Deadlock ===")
    print()

    graph2 = WaitForGraph()
    graph2.add_transaction("T1", holds=["X"], waits_for=["Y"])
    graph2.add_transaction("T2", holds=["Y"], waits_for=[])
    graph2.add_transaction("T3", holds=[], waits_for=["X"])
    graph2.visualize()

    print("\n" + "="*50 + "\n")

    print("=== Scenario 3: Three-Way Deadlock ===")
    print()

    graph3 = WaitForGraph()
    graph3.add_transaction("T1", holds=["A"], waits_for=["B"])
    graph3.add_transaction("T2", holds=["B"], waits_for=["C"])
    graph3.add_transaction("T3", holds=["C"], waits_for=["A"])
    graph3.visualize()


if __name__ == "__main__":
    demo_deadlock_detection()
