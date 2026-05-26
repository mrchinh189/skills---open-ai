"""Kiểm tra script standalone trong skill hoadon-vat."""
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "skills" / ".business-vn" / "hoadon-vat" / "scripts" / "validate_mst.py"


def test_script_valid():
    r = subprocess.run([sys.executable, str(SCRIPT), "0101248141"], capture_output=True, text=True)
    assert r.returncode == 0
    assert "VALID" in r.stdout


def test_script_invalid():
    r = subprocess.run([sys.executable, str(SCRIPT), "0101248140"], capture_output=True, text=True)
    assert r.returncode == 1
    assert "INVALID" in r.stdout
