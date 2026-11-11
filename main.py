"""A beginner-friendly file integrity monitor using SHA-256."""

import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_TARGET = BASE_DIR / "monitored"
DEFAULT_BASELINE = BASE_DIR / "baseline.json"


def sha256_file(path: Path) -> str:
    """Return the SHA-256 hash of a file, reading it in small chunks."""
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_snapshot(target: Path) -> dict:
    """Create a relative-path -> SHA-256 mapping for all files in target."""
    snapshot = {}
    for path in sorted(target.rglob("*")):
        if path.is_file():
            relative_path = str(path.relative_to(target))
            snapshot[relative_path] = sha256_file(path)
    return snapshot


def load_baseline(baseline_path: Path) -> dict:
    with baseline_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_baseline(baseline_path: Path, snapshot: dict) -> None:
    data = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files": snapshot,
    }
    with baseline_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
    print(f"[+] Baseline saved: {baseline_path}")


def compare_snapshots(old: dict, new: dict) -> None:
    old_files = set(old)
    new_files = set(new)

    added = sorted(new_files - old_files)
    deleted = sorted(old_files - new_files)
    modified = sorted(
        path for path in old_files & new_files if old[path] != new[path]
    )

    print("\n=== File Integrity Report ===")
    if not (added or deleted or modified):
        print("[OK] No changes detected.")
        return

    for path in added:
        print(f"[NEW]      {path}")
    for path in modified:
        print(f"[MODIFIED] {path}")
    for path in deleted:
        print(f"[DELETED]  {path}")

    print(
        f"\nSummary: {len(added)} new, "
        f"{len(modified)} modified, {len(deleted)} deleted."
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Detect added, modified, and deleted files using SHA-256."
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=DEFAULT_TARGET,
        help="Folder to monitor (default: ./monitored)",
    )
    parser.add_argument(
        "--baseline",
        type=Path,
        default=DEFAULT_BASELINE,
        help="Baseline JSON file (default: ./baseline.json)",
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Create or replace the baseline with the current folder state.",
    )
    args = parser.parse_args()

    target = args.target.resolve()
    baseline_path = args.baseline.resolve()

    if not target.exists() or not target.is_dir():
        raise SystemExit(f"Error: target folder does not exist: {target}")

    current_snapshot = build_snapshot(target)

    if args.init:
        save_baseline(baseline_path, current_snapshot)
        return

    if not baseline_path.exists():
        raise SystemExit(
            "No baseline found. Run: python main.py --init"
        )

    baseline_data = load_baseline(baseline_path)
    baseline_files = baseline_data.get("files", {})
    compare_snapshots(baseline_files, current_snapshot)


if __name__ == "__main__":
    main()
