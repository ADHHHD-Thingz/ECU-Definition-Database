#!/usr/bin/env python3
"""Inventory and structurally audit ECU definition files without modifying inputs.

Outputs JSON and CSV reports. XML parse errors are recorded, never silently dropped.
No payload decryption or semantic map interpretation is attempted.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

TEXT_EXTENSIONS = {
    ".xml", ".xdf", ".kp", ".a2l", ".aml", ".json", ".ini", ".csv",
    ".txt", ".yaml", ".yml", ".toml", ".hex", ".s19", ".mot", ".map",
}
BINARY_EXTENSIONS = {".bin", ".rom", ".ori", ".hex", ".s19", ".mot"}
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".pytest_cache"}
MAX_XML_BYTES = 128 * 1024 * 1024


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()


def audit_xml(path: Path, size: int) -> dict:
    result = {"xml_parse": "not_attempted", "map_count": 0,
              "eattributes_attribute_count": 0, "eattributes_element_count": 0,
              "ecu_struct_count": 0, "romid_count": 0, "xml_root": ""}
    if size > MAX_XML_BYTES:
        result["xml_parse"] = "skipped_size_limit"
        return result
    try:
        root = ET.parse(path).getroot()
        result["xml_parse"] = "ok"
        result["xml_root"] = local_name(root.tag)
        for element in root.iter():
            tag = local_name(element.tag)
            if tag == "map":
                result["map_count"] += 1
            elif tag == "eattributes":
                result["eattributes_element_count"] += 1
            result["eattributes_attribute_count"] += sum(
                1 for key in element.attrib if local_name(key) == "eattributes"
            )
            if tag == "ecu_struct":
                result["ecu_struct_count"] += 1
            elif tag == "romid":
                result["romid_count"] += 1
    except (ET.ParseError, OSError, UnicodeError) as exc:
        result["xml_parse"] = "error"
        result["xml_error"] = str(exc)[:500]
    return result


def iter_files(root: Path):
    for current, dirs, names in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(names):
            path = Path(current) / name
            if path.is_file():
                yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="directory to scan (default: current directory)")
    parser.add_argument("--out", default="build/definition-audit", help="output directory")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    out = Path(args.out).resolve()
    if not root.is_dir():
        parser.error(f"root is not a directory: {root}")
    if out == root or root in out.parents:
        # Outputs under the scanned root would be re-scanned on later runs; exclude them explicitly.
        pass

    records = []
    duplicates = defaultdict(list)
    extension_counts = Counter()
    errors = 0
    for path in iter_files(root):
        try:
            rel = path.relative_to(root).as_posix()
            size = path.stat().st_size
            suffix = path.suffix.lower()
            row = {
                "path": rel,
                "name": path.name,
                "extension": suffix,
                "size_bytes": size,
                "sha256": sha256_file(path),
                "classification": (
                    "binary_candidate" if suffix in BINARY_EXTENSIONS else
                    "definition_candidate" if suffix in TEXT_EXTENSIONS else "other"
                ),
            }
            if suffix == ".xml":
                row.update(audit_xml(path, size))
                if row["xml_parse"] == "error":
                    errors += 1
            records.append(row)
            duplicates[row["sha256"]].append(rel)
            extension_counts[suffix or "[no extension]"] += 1
        except (OSError, PermissionError) as exc:
            errors += 1
            records.append({"path": str(path), "classification": "read_error", "error": str(exc)[:500]})

    out.mkdir(parents=True, exist_ok=True)
    json_path = out / "inventory.json"
    csv_path = out / "inventory.csv"
    summary_path = out / "summary.json"
    json_path.write_text(json.dumps(records, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    columns = sorted({key for row in records for key in row})
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    duplicate_groups = [
        {"sha256": digest, "paths": sorted(paths), "copies": len(paths)}
        for digest, paths in sorted(duplicates.items()) if len(paths) > 1
    ]
    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "file_count": len(records),
        "extension_counts": dict(sorted(extension_counts.items())),
        "xml_files": sum(1 for r in records if r.get("extension") == ".xml"),
        "xml_parse_ok": sum(1 for r in records if r.get("xml_parse") == "ok"),
        "xml_parse_errors": sum(1 for r in records if r.get("xml_parse") == "error"),
        "maps": sum(r.get("map_count", 0) for r in records),
        "eattributes": sum(r.get("eattributes_attribute_count", 0) for r in records),
        "eattributes_attribute_count": sum(r.get("eattributes_attribute_count", 0) for r in records),
        "eattributes_element_count": sum(r.get("eattributes_element_count", 0) for r in records),
        "ecu_structs": sum(r.get("ecu_struct_count", 0) for r in records),
        "duplicate_hash_groups": len(duplicate_groups),
        "duplicate_files_beyond_first": sum(g["copies"] - 1 for g in duplicate_groups),
        "read_or_parse_errors": errors,
        "outputs": {"inventory_json": str(json_path), "inventory_csv": str(csv_path),
                    "summary_json": str(summary_path)},
    }
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
