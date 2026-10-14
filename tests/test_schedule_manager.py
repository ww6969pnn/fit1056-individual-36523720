import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.schedule import ScheduleManager


@pytest.fixture
def manager(tmp_path):
    """Create a fresh ScheduleManager with an isolated data file."""
    data_file = tmp_path / "test_msms.json"
    return ScheduleManager(data_file=str(data_file))


# ---------- Student tests ----------

def test_add_student_success(manager):
    ok = manager.add_student("Alice")
    assert ok is True
    assert len(manager.students) == 1
    assert manager.students[0].name == "Alice"


def test_add_student_empty_name(manager):
    ok = manager.add_student("")
    assert ok is False
    assert len(manager.students) == 0


def test_add_student_name_too_long(manager):
    ok = manager.add_student("A" * 16)
    assert ok is False


def test_add_student_numeric_name(manager):
    ok = manager.add_student("12345")
    assert ok is False


def test_remove_student(manager):
    manager.add_student("Bob")
    ok = manager.remove_student(1)
    assert ok is True
    assert len(manager.students) == 0


def test_remove_nonexistent_student(manager):
    ok = manager.remove_student(999)
    assert ok is False


# ---------- Teacher tests ----------

def test_add_teacher_success(manager):
    ok = manager.add_teacher("Mr. Lee", "piano")
    assert ok is True
    assert len(manager.teachers) == 1


def test_add_teacher_invalid_specialty(manager):
    ok = manager.add_teacher("Mr. Lee", "hacking")
    assert ok is False


# ---------- Payment tests ----------

def test_record_payment_success(manager):
    manager.add_student("Carol")
    ok = manager.record_payment(1, 50.0, "Cash")
    assert ok is True
    history = manager.get_payment_history(1)
    assert len(history) == 1
    assert history[0]["amount"] == 50.0
    assert history[0]["method"] == "Cash"


def test_record_payment_invalid_amount(manager):
    manager.add_student("Dave")
    ok = manager.record_payment(1, -10, "Cash")
    assert ok is False


def test_record_payment_zero_amount(manager):
    manager.add_student("Dave")
    ok = manager.record_payment(1, 0, "Cash")
    assert ok is False


def test_record_payment_unknown_student(manager):
    ok = manager.record_payment(999, 50.0, "Cash")
    assert ok is False


def test_record_payment_invalid_method(manager):
    manager.add_student("Eve")
    ok = manager.record_payment(1, 50.0, "Bitcoin")
    assert ok is False


def test_get_payment_history_multiple(manager):
    manager.add_student("Frank")
    manager.record_payment(1, 30.0, "Cash")
    manager.record_payment(1, 20.0, "Third-Party Payment")
    history = manager.get_payment_history(1)
    assert len(history) == 2
    assert sum(p["amount"] for p in history) == 50.0


# ---------- Persistence tests ----------

def test_data_persists_across_reload(tmp_path):
    data_file = tmp_path / "persist_test.json"

    m1 = ScheduleManager(data_file=str(data_file))
    m1.add_student("Grace")
    m1.record_payment(1, 100.0, "Cash")

    # New manager loading the same file
    m2 = ScheduleManager(data_file=str(data_file))
    assert len(m2.students) == 1
    assert m2.students[0].name == "Grace"
    assert len(m2.finance_log) == 1
    assert m2.finance_log[0]["amount"] == 100.0