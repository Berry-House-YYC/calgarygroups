#!/usr/bin/env python3

import argparse
import csv
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


def yaml_quote(value: str) -> str:
    value = value if value is not None else ""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_flow_list(values: List[str]) -> str:
    return "[" + ", ".join(yaml_quote(v) for v in values) + "]"


def slugify(value: str) -> str:
    value = (value or "").strip().lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "untitled"


def split_multi(value: str) -> List[str]:
    if not value:
        return []
    # Split on commas, slashes, and pipes.
    parts = re.split(r"[,/|]", value)
    return [p.strip() for p in parts if p.strip()]


INTEREST_MAP: Dict[str, str] = {
    "culture": "arts-culture",
    "arts": "arts-culture",
    "markets": "arts-culture",
    "markets events": "arts-culture",
    "markets/events": "arts-culture",
    "poverty": "social-impact",
    "general social issues": "social-impact",
    "activism": "social-impact",
    "anti-racism": "social-impact",
    "2slgbtq+": "lgbtq2s",
    "2slgbtq": "lgbtq2s",
    "tech": "education",
    "capacity building": "education",
    "economics finance": "education",
    "economics/finance": "education",
    "marketing": "education",
    "health": "health-wellness",
    "mental health": "health-wellness",
    "hobby rec": "sports-rec",
    "hobby/rec": "sports-rec",
    "environment": "environment",
    "urban issues": "social-impact",
}


def normalize_key(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def map_interests(focus_type: str) -> List[str]:
    raw_items = split_multi(focus_type)
    out: List[str] = []
    for item in raw_items:
        key = normalize_key(item)
        if not key:
            continue
        mapped = INTEREST_MAP.get(key)
        if mapped:
            out.append(mapped)
        else:
            out.append(slugify(item))
    # Deduplicate, preserve order
    seen = set()
    deduped: List[str] = []
    for t in out:
        if t in seen:
            continue
        seen.add(t)
        deduped.append(t)
    return deduped


def infer_age_range(audience: str) -> str:
    a = normalize_key(audience)
    if "seniors" in a:
        return "seniors"
    if "youth" in a or "under 30" in a:
        return "youth"
    return "all-ages"


def infer_identity_focused(audience: str) -> bool:
    a = normalize_key(audience)
    flags = [
        "immigrants",
        "poc",
        "2slgbtq",
        "women",
        "indigenous",
    ]
    return any(f in a for f in flags)


def infer_type(org_type: str, focus_type: str) -> str:
    ot = normalize_key(org_type)
    ft = normalize_key(focus_type)

    if "club" in ot:
        return "club"

    activist_signals = ["activism", "anti racism", "anti-racism", "environment", "urban issues"]
    if any(s in ft for s in activist_signals) and ("grassroots" in ot or "chapter" in ot or not ot):
        return "activist-group"

    if "grassroots" in ot or "chapter" in ot:
        return "grassroots-initiative"

    return "resource"


def folder_for_type(site_type: str) -> str:
    if site_type == "club":
        return "clubs"
    if site_type == "activist-group":
        return "activist-groups"
    if site_type == "grassroots-initiative":
        return "grassroots-initiatives"
    return "resources"


def parse_contact_fields(row: Dict[str, str], website_column: str) -> Tuple[Optional[str], Optional[str]]:
    website = (row.get(website_column) or "").strip() or None
    email_field = (row.get("Email") or "").strip()

    email = None
    if email_field:
        if email_field.startswith("http://") or email_field.startswith("https://"):
            # Sometimes the CSV uses this column for contact links.
            website = website or email_field
        elif "@" in email_field and " " not in email_field:
            email = email_field

    return website, email


def build_markdown(row: Dict[str, str], website_column: str) -> Tuple[str, str, str]:
    name = (row.get("Organization Name") or "").strip()
    focus_type = (row.get("Focus/Type") or "").strip()
    org_type = (row.get("Organization Type") or "").strip()
    audience = (row.get("Audience") or "").strip()
    notes = (row.get("Notes") or "").strip()

    site_type = infer_type(org_type, focus_type)
    interests = map_interests(focus_type)
    age_range = infer_age_range(audience)
    identity_focused = infer_identity_focused(audience)

    # Status is about the organization being active/inactive, not whether it should appear on the site.
    # We only mark inactive if the notes explicitly mention it.
    status = "inactive" if "inactive" in normalize_key(notes) else "active"

    website, email = parse_contact_fields(row, website_column)

    # Very conservative defaults until we have better data.
    meeting_format = "in-person"
    location_area = "city-wide"

    front_matter_lines = [
        "---",
        "layout: layouts/organization.njk",
        f"name: {yaml_quote(name)}",
        f"type: {yaml_quote(site_type)}",
        f"interests: {yaml_flow_list(interests)}",
        f"age_range: {yaml_quote(age_range)}",
        f"identity_focused: {str(bool(identity_focused)).lower()}",
        f"meeting_format: {yaml_quote(meeting_format)}",
        f"location_area: {yaml_quote(location_area)}",
        f"status: {yaml_quote(status)}",
        "permalink: \"/organizations/{{ page.fileSlug }}/\"",
        "---",
        "",
    ]

    # Minimal description placeholder.
    description_bits: List[str] = []
    if focus_type:
        description_bits.append(f"Focused on {focus_type}.")
    if audience:
        description_bits.append(f"Audience: {audience}.")
    description = " ".join(description_bits) or "Community organization in Calgary."

    body_lines = [
        description,
        "",
        "**Contact Info:**",
    ]
    if website:
        body_lines.append(f"- Website: {website}")
    if email:
        body_lines.append(f"- Email: {email}")

    if notes:
        body_lines.extend(["", "**Notes:**", notes])

    md = "\n".join(front_matter_lines + body_lines).rstrip() + "\n"

    folder = folder_for_type(site_type)
    filename = f"{slugify(name)}.md"
    return folder, filename, md


@dataclass
class WriteStats:
    created: int = 0
    skipped_existing: int = 0


def write_markdown_files(
    csv_path: str,
    out_root: str,
    website_column: str,
    overwrite: bool,
    only_flag: Optional[str],
) -> WriteStats:
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    stats = WriteStats()

    for row in rows:
        name = (row.get("Organization Name") or "").strip()
        if not name:
            continue

        if only_flag is not None:
            flag = (row.get("Calgary Groups Site") or "").strip().upper()
            if flag != only_flag.upper():
                continue

        folder, filename, md = build_markdown(row, website_column)
        out_dir = os.path.join(out_root, folder)
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, filename)

        if os.path.exists(out_path) and not overwrite:
            stats.skipped_existing += 1
            continue

        with open(out_path, "w", encoding="utf-8", newline="") as outf:
            outf.write(md)
        stats.created += 1

    return stats


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert Organizations CSV rows into markdown files under src/content/organizations."
    )
    parser.add_argument(
        "--csv",
        dest="csv_path",
        default=os.path.join("docs", "Mass Organization CRM - Organizations.csv"),
        help="Path to the Organizations CSV",
    )
    parser.add_argument(
        "--out-root",
        dest="out_root",
        default=os.path.join("src", "content", "organizations"),
        help="Output root directory (default: src/content/organizations)",
    )
    parser.add_argument(
        "--website-column",
        dest="website_column",
        default="Website",
        help="Column name holding website URLs (default: Website)",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing markdown files",
    )
    parser.add_argument(
        "--only-site-flag",
        dest="only_flag",
        default=None,
        help="Only emit rows where 'Calgary Groups Site' equals this value (e.g. Y)",
    )

    args = parser.parse_args()

    stats = write_markdown_files(
        csv_path=args.csv_path,
        out_root=args.out_root,
        website_column=args.website_column,
        overwrite=args.overwrite,
        only_flag=args.only_flag,
    )

    print(f"Created/updated: {stats.created}")
    if not args.overwrite:
        print(f"Skipped existing: {stats.skipped_existing}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
