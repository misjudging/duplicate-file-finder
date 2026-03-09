from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from pathlib import Path


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=Path, default=Path.cwd())
    args = parser.parse_args()

    target = args.path.resolve()
    files = [p for p in target.rglob("*") if p.is_file() and ".git" not in p.parts]

    groups: dict[str, list[Path]] = defaultdict(list)
    for file_path in files:
        groups[sha256_file(file_path)].append(file_path)

    duplicates = [paths for paths in groups.values() if len(paths) > 1]

    if not duplicates:
        print("No duplicates found.")
        return

    print("Duplicate groups:")
    for i, group in enumerate(duplicates, start=1):
        print(f"\nGroup {i} ({len(group)} files):")
        for path in group:
            print(f"- {path}")


if __name__ == "__main__":
    main()
