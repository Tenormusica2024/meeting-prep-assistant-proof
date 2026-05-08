import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_run_demo_writes_expected_outputs():
    result = subprocess.run([sys.executable, "-X", "utf8", "run_demo.py"], cwd=ROOT, text=True, capture_output=True)

    assert result.returncode == 0, result.stderr
    assert "no-participant-send" in result.stdout
    assert (ROOT / "outputs" / "meeting_prep_report.md").exists()
    assert (ROOT / "outputs" / "meeting_prep_report.json").exists()

    data = json.loads((ROOT / "outputs" / "meeting_prep_report.json").read_text(encoding="utf-8"))
    assert data["summary"]["meetings_scanned"] == 5
    assert data["summary"]["confirmation_queue_count"] >= 1
