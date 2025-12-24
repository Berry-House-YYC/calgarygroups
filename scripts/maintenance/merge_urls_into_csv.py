#!/usr/bin/env python3

import argparse
import csv
import difflib
import os
import re
import sys
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple


LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def normalize_name(value: str) -> str:
    value = (value or "").strip().lower()
    # Replace non-alphanumeric with spaces, collapse whitespace.
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def name_from_markdown_line(line: str) -> str:
    # Replace markdown links with their visible text (if any).
    def _repl(match: re.Match) -> str:
        text = (match.group(1) or "").strip()
        return text

    replaced = LINK_RE.sub(_repl, line)
    replaced = replaced.strip()
    replaced = re.sub(r"\s+", " ", replaced)
    return replaced


def url_from_markdown_line(line: str) -> Optional[str]:
    matches = LINK_RE.findall(line)
    if not matches:
        return None
    # Prefer the URL for the last *non-empty text* link; otherwise just use the last URL.
    best_url = None
    for text, url in matches:
        if (text or "").strip():
            best_url = url
    if best_url:
        return best_url.strip()
    return matches[-1][1].strip()


def parse_urls_md(md_path: str) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    with open(md_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line:
                continue
            # Ignore the stray HTML/CSS snippet at the end of the file.
            if line.startswith("td ") or line.startswith("br "):
                continue

            url = url_from_markdown_line(line)
            if not url:
                continue

            name = name_from_markdown_line(line)
            if not name:
                continue

            norm = normalize_name(name)
            if not norm:
                continue

            mapping[norm] = url
    return mapping


@dataclass
class MergeStats:
    matched_exact: int = 0
    matched_fuzzy: int = 0
    skipped_existing: int = 0
    unmatched_csv_rows: int = 0


def best_fuzzy_match(target: str, candidates: Iterable[str]) -> Tuple[Optional[str], float]:
    # difflib ratio is in [0, 1]
    best_key = None
    best_ratio = 0.0
    for c in candidates:
        r = difflib.SequenceMatcher(a=target, b=c).ratio()
        if r > best_ratio:
            best_ratio = r
            best_key = c
    return best_key, best_ratio


def merge_urls_into_csv(
    csv_path: str,
    urls_md_path: str,
    out_path: str,
    column: str,
    overwrite: bool,
    fuzzy: bool,
    fuzzy_threshold: float,
) -> MergeStats:
    url_map = parse_urls_md(urls_md_path)

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise RuntimeError("CSV has no header row")
        fieldnames = list(reader.fieldnames)

        if column not in fieldnames:
            fieldnames.append(column)

        rows = list(reader)

    # Build normalized org names for CSV.
    csv_name_to_index: Dict[str, int] = {}
    for idx, row in enumerate(rows):
        name = (row.get("Organization Name") or "").strip()
        norm = normalize_name(name)
        if norm and norm not in csv_name_to_index:
            csv_name_to_index[norm] = idx

    stats = MergeStats()

    # First pass: exact normalized matches.
    for norm_name, url in url_map.items():
        idx = csv_name_to_index.get(norm_name)
        if idx is None:
            continue
        existing = (rows[idx].get(column) or "").strip()
        if existing and not overwrite:
            stats.skipped_existing += 1
            continue
        rows[idx][column] = url
        stats.matched_exact += 1

    # Second pass: fuzzy matching for URLs not applied.
    if fuzzy:
        for norm_name, url in url_map.items():
            if norm_name in csv_name_to_index:
                continue
            best_key, ratio = best_fuzzy_match(norm_name, csv_name_to_index.keys())
            if not best_key or ratio < fuzzy_threshold:
                continue
            idx = csv_name_to_index[best_key]
            existing = (rows[idx].get(column) or "").strip()
            if existing and not overwrite:
                continue
            rows[idx][column] = url
            stats.matched_fuzzy += 1

    # Count CSV rows still lacking a URL.
    for row in rows:
        existing = (row.get(column) or "").strip()
        if not existing:
            stats.unmatched_csv_rows += 1

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return stats


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Merge URLs from docs/urls.md into the Organizations CSV (adds a new column if missing)."
    )
    parser.add_argument(
        "--csv",
        dest="csv_path",
        default=os.path.join("docs", "Mass Organization CRM - Organizations.csv"),
        help="Path to the Organizations CSV",
    )
    parser.add_argument(
        "--urls",
        dest="urls_path",
        default=os.path.join("docs", "urls.md"),
        help="Path to urls.md",
    )
    parser.add_argument(
        "--out",
        dest="out_path",
        default=None,
        help="Output CSV path (default: alongside input with .with_urls.csv suffix)",
    )
    parser.add_argument(
        "--column",
        dest="column",
        default="Website",
        help="Column name to write URLs into (default: Website)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing values in the URL column",
    )
    parser.add_argument(
        "--fuzzy",
        action="store_true",
        help="Enable fuzzy name matching (uses difflib; safest when names are close)",
    )
    parser.add_argument(
        "--fuzzy-threshold",
        type=float,
        default=0.92,
        help="Fuzzy match threshold in [0,1] (default: 0.92)",
    )

    args = parser.parse_args()

    if args.out_path:
        out_path = args.out_path
    else:
        base, ext = os.path.splitext(args.csv_path)
        out_path = f"{base}.with_urls{ext or '.csv'}"

    stats = merge_urls_into_csv(
        csv_path=args.csv_path,
        urls_md_path=args.urls_path,
        out_path=out_path,
        column=args.column,
        overwrite=args.overwrite,
        fuzzy=args.fuzzy,
        fuzzy_threshold=args.fuzzy_threshold,
    )

    print(f"Wrote: {out_path}")
    print(f"Exact matches: {stats.matched_exact}")
    if args.fuzzy:
        print(f"Fuzzy matches: {stats.matched_fuzzy}")
    if not args.overwrite:
        print(f"Skipped existing: {stats.skipped_existing}")
    print(f"Rows still missing '{args.column}': {stats.unmatched_csv_rows}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
