# test_fleet_report.py
from fleet_report import fleet_summary

SAMPLE = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def test_summary_counts_due_cars():
    # Only VOS-4471 is nearly worn, so exactly one car is due.
    assert fleet_summary(SAMPLE)["due"] == 1


def test_summary_handles_missing_last_service_reading():
    # VOS-7788 has no last_service_km reading — the report must not crash, and the
    # car must NOT be counted as due (unknown service history ≠ overdue).
    fleet = [
        {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
        {"id": "VOS-7788", "odometer": 92000},
    ]
    summary = fleet_summary(fleet)          # must not raise KeyError
    assert summary["count"] == 2
    assert summary["due"] == 1              # VOS-4471 is due; VOS-7788 must NOT be counted
