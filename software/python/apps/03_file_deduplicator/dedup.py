"""Find duplicate files by content hash, using a size-first pre-filter."""

import argparse
import hashlib
from collections import defaultdict
from pathlib import Path


def hash_file(path: Path, chunk_size: int = 65536) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_duplicates(root: Path) -> dict[str, list[Path]]:
    by_size: dict[int, list[Path]] = defaultdict(list)
    for path in root.rglob("*"):
        if path.is_file():
            by_size[path.stat().st_size].append(path)

    candidates = [paths for paths in by_size.values() if len(paths) > 1]

    by_hash: dict[str, list[Path]] = defaultdict(list)
    for group in candidates:
        for path in group:
            by_hash[hash_file(path)].append(path)

    return {h: paths for h, paths in by_hash.items() if len(paths) > 1}


def main():
    parser = argparse.ArgumentParser(description="Find (and optionally delete) duplicate files")
    parser.add_argument("directory", type=Path)
    parser.add_argument("--delete", action="store_true", help="delete duplicates, keeping the first found per group")
    args = parser.parse_args()

    duplicates = find_duplicates(args.directory)

    if not duplicates:
        print("No duplicates found.")
        return

    total_wasted = 0
    for file_hash, paths in duplicates.items():
        size = paths[0].stat().st_size
        wasted = size * (len(paths) - 1)
        total_wasted += wasted

        print(f"\n{file_hash[:12]}... ({len(paths)} copies, {size} bytes each):")
        for i, path in enumerate(paths):
            marker = "[KEEP]" if i == 0 else "[DUP] "
            print(f"  {marker} {path}")
            if args.delete and i > 0:
                path.unlink()
                print(f"         -> deleted")

    print(f"\nTotal duplicate groups: {len(duplicates)}")
    print(f"Total wasted space{'  (would be reclaimed)' if not args.delete else ' reclaimed'}: {total_wasted} bytes")


if __name__ == "__main__":
    main()
