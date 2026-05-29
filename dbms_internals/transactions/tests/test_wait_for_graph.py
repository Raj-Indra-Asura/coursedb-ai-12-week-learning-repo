"""Tests for wait-for-graph deadlock detection."""

from dbms_internals.transactions.wait_for_graph import WaitForGraph


def test_cycle_detection_true_positive() -> None:
    graph = WaitForGraph()
    graph.add_transaction("T1", holds=["X"], waits_for=["Y"])
    graph.add_transaction("T2", holds=["Y"], waits_for=["X"])
    assert graph.detect_deadlock() is True


def test_no_cycle_case() -> None:
    graph = WaitForGraph()
    graph.add_transaction("T1", holds=["X"], waits_for=[])
    graph.add_transaction("T2", holds=["Y"], waits_for=["X"])
    assert graph.detect_deadlock() is False


def test_get_deadlock_cycle_returns_cycle() -> None:
    graph = WaitForGraph()
    graph.add_transaction("T1", holds=["X"], waits_for=["Y"])
    graph.add_transaction("T2", holds=["Y"], waits_for=["X"])
    cycle = graph.get_deadlock_cycle()
    assert cycle is not None
    assert "T1" in cycle and "T2" in cycle


def test_no_cycle_returns_none() -> None:
    graph = WaitForGraph()
    graph.add_transaction("T1", holds=["X"], waits_for=[])
    assert graph.get_deadlock_cycle() is None


def test_multi_cycle_case() -> None:
    # Two independent deadlock cycles: T1<->T2 and T3<->T4.
    graph = WaitForGraph()
    graph.add_transaction("T1", holds=["A"], waits_for=["B"])
    graph.add_transaction("T2", holds=["B"], waits_for=["A"])
    graph.add_transaction("T3", holds=["C"], waits_for=["D"])
    graph.add_transaction("T4", holds=["D"], waits_for=["C"])
    assert graph.detect_deadlock() is True
    cycle = graph.get_deadlock_cycle()
    assert cycle is not None


def test_three_way_cycle() -> None:
    graph = WaitForGraph()
    graph.add_transaction("T1", holds=["A"], waits_for=["B"])
    graph.add_transaction("T2", holds=["B"], waits_for=["C"])
    graph.add_transaction("T3", holds=["C"], waits_for=["A"])
    assert graph.detect_deadlock() is True


def test_self_contained_no_wait() -> None:
    graph = WaitForGraph()
    graph.add_transaction("T1", holds=["A"], waits_for=[])
    assert graph.detect_deadlock() is False


def test_visualize_runs(capsys) -> None:
    graph = WaitForGraph()
    graph.add_transaction("T1", holds=["A"], waits_for=["B"])
    graph.add_transaction("T2", holds=["B"], waits_for=["A"])
    graph.visualize()
    captured = capsys.readouterr()
    assert captured.out
