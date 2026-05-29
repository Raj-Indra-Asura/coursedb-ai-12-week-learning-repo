"""Tests for the educational hash index implementation."""

from dbms_internals.hash_index.hash_index import HashIndex


def test_insert_and_search() -> None:
    index = HashIndex(bucket_count=10)
    index.insert(42, "answer")
    assert index.search(42) == "answer"


def test_search_missing_key_returns_none() -> None:
    index = HashIndex(bucket_count=10)
    assert index.search(7) is None


def test_collision_chaining() -> None:
    index = HashIndex(bucket_count=5)
    # 3 and 8 both hash to bucket 3 (key % 5).
    index.insert(3, "a")
    index.insert(8, "b")
    assert index.search(3) == "a"
    assert index.search(8) == "b"
    assert index._hash(3) == index._hash(8)


def test_update_existing_key() -> None:
    index = HashIndex(bucket_count=10)
    index.insert(1, "old")
    index.insert(1, "new")
    assert index.search(1) == "new"
    assert index.total_keys == 1


def test_delete_key() -> None:
    index = HashIndex(bucket_count=10)
    index.insert(5, "v")
    assert index.delete(5) is True
    assert index.search(5) is None
    assert index.total_keys == 0


def test_delete_missing_key_returns_false() -> None:
    index = HashIndex(bucket_count=10)
    assert index.delete(123) is False


def test_total_keys_counts_unique() -> None:
    index = HashIndex(bucket_count=10)
    for key in [1, 2, 3, 3, 2]:
        index.insert(key)
    assert index.total_keys == 3


def test_visualize_runs(capsys) -> None:
    index = HashIndex(bucket_count=10)
    for key in [12, 22, 32, 5]:
        index.insert(key, f"value_{key}")
    index.visualize()
    captured = capsys.readouterr()
    assert "Hash Index" in captured.out


def test_compare_with_bplus_tree_runs(capsys) -> None:
    index = HashIndex(bucket_count=10)
    index.compare_with_bplus_tree()
    captured = capsys.readouterr()
    assert "B+ Tree" in captured.out
