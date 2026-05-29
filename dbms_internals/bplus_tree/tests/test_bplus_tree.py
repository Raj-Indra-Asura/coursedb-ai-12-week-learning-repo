"""Tests for the educational B+ tree implementation."""

import random

from dbms_internals.bplus_tree.bplus_tree import BPlusTree, BPlusTreeNode


def _height(node: BPlusTreeNode) -> int:
    if node.is_leaf:
        return 1
    return 1 + max(_height(child) for child in node.children)


def test_insert_and_search_all_keys_random_order() -> None:
    tree = BPlusTree(order=4)
    keys = list(range(1, 51))
    shuffled = keys[:]
    random.Random(42).shuffle(shuffled)
    for key in shuffled:
        tree.insert(key)
    for key in keys:
        assert tree.search(key) is not None


def test_search_missing_key_returns_none() -> None:
    tree = BPlusTree(order=3)
    tree.insert(10)
    assert tree.search(999) is None


def test_range_query() -> None:
    tree = BPlusTree(order=4)
    for key in range(1, 51):
        tree.insert(key)
    results = tree.range_search(10, 20)
    found_keys = [k for k, _ in results]
    assert found_keys == list(range(10, 21))


def test_repeated_key_update_does_not_duplicate() -> None:
    tree = BPlusTree(order=3)
    tree.insert(5, "first")
    tree.insert(5, "second")
    # The value associated with the key should reflect the latest insert and
    # a single range scan should not return the key twice.
    results = tree.range_search(5, 5)
    assert len(results) == 1
    assert tree.search(5) == "second"


def test_split_creates_internal_root() -> None:
    tree = BPlusTree(order=3)
    for key in [10, 20, 30, 40, 50]:
        tree.insert(key)
    # After enough inserts the root must have split and is no longer a leaf.
    assert tree.root.is_leaf is False


def test_tree_height_bound() -> None:
    n = 50
    order = 4
    tree = BPlusTree(order=order)
    for key in range(1, n + 1):
        tree.insert(key)
    height = _height(tree.root)
    # Height of a B+ tree is bounded by log_ceil(n) base ceil(order/2).
    import math

    max_height = math.ceil(math.log(n, math.ceil(order / 2))) + 1
    assert 1 <= height <= max_height


def test_invalid_order_raises() -> None:
    import pytest

    with pytest.raises(ValueError):
        BPlusTree(order=2)


def test_visualize_runs(capsys) -> None:
    tree = BPlusTree(order=4)
    for key in range(1, 20):
        tree.insert(key, f"v{key}")
    tree.visualize()
    captured = capsys.readouterr()
    assert captured.out  # produced some output
