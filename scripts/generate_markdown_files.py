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
    # Split on commas
    parts = re.split(r",", value)
    return [p.strip() for p in parts if p.strip()]


# New interest mapping for the updated CSV structure
INTEREST_MAP: Dict[str, str] = {
    "2slgbtq+": "lgbtq2s",
    "2slgbtq": "lgbtq2s",
    "anti-racism": "anti-racism",
    "anti racism": "anti-racism",
    "arts & culture": "arts-culture",
    "arts and culture": "arts-culture",
    "arts": "arts-culture",
    "culture": "arts-culture",
    "children & youth": "youth",
    "children and youth": "youth",
    "youth": "youth",
    "disability": "disability/neurodivergent",
    "disability/neurodivergent": "disability/neurodivergent",
    "environment": "environment",
    "health & wellness": "health-wellness",
    "health and wellness": "health-wellness",
    "health": "health-wellness",
    "mental health": "health-wellness",
    "indigenous": "indigenous",
    "int'l": "social-impact",
    "international": "social-impact",
    "low-income": "low-income",
    "low income": "low-income",
    "poverty": "low-income",
    "science & tech": "tech",
    "science and tech": "tech",
    "tech": "tech",
    "seniors": "seniors",
    "social impact": "social-impact",
    "activism": "social-impact",
    "sports & rec": "sports-rec",
    "sports and rec": "sports-rec",
    "hobby rec": "sports-rec",
    "hobby/rec": "sports-rec",
    "urban issues": "urban-issues",
    "women+": "women+",
    "women": "women+",
    "book": "book",
    "gen": "general",
    "general": "general",
    "capacity building": "education",
    "education": "education",
}


def normalize_key(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9+'/&]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def map_interests(interests_str: str) -> List[str]:
    """Map interests from CSV to site taxonomy."""
    raw_items = split_multi(interests_str)
    out: List[str] = []
    for item in raw_items:
        key = normalize_key(item)
        if not key:
            continue
        mapped = INTEREST_MAP.get(key)
        if mapped:
            out.append(mapped)
        else:
            # Use slugified version if no mapping found
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


# Organization type mapping: CSV values -> site taxonomy
ORG_TYPE_MAP: Dict[str, str] = {
    "npo": "Nonprofit",
    "nonprofit": "Nonprofit",
    "chapter": "Chapter",
    "grassroots": "Grassroots",
    "club": "Social Club",
    "social club": "Social Club",
    "small business": "Small Business",
    "cooperative": "Cooperative",
    "social enterprise": "Cooperative",  # Map to Cooperative for now
    "resource": "Nonprofit",  # Default resources to Nonprofit
}


def map_org_type(org_type_str: str) -> str:
    """Map organization type from CSV to site taxonomy."""
    if not org_type_str:
        return "Nonprofit"  # Default
    
    # Handle combinations like "Chapter, NPO" - take first value
    parts = split_multi(org_type_str)
    if parts:
        org_type_str = parts[0]
    
    key = normalize_key(org_type_str)
    return ORG_TYPE_MAP.get(key, "Nonprofit")


def folder_for_type(site_type: str) -> str:
    """Map site type to folder structure."""
    folder_map = {
        "Nonprofit": "nonprofit",
        "Grassroots": "grassroots",
        "Social Club": "social-club",
        "Chapter": "chapter",
        "Cooperative": "cooperative",
        "Small Business": "small-business",
    }
    return folder_map.get(site_type, "nonprofit")


def infer_age_range(audience: str) -> str:
    """Infer age range from audience description."""
    a = normalize_key(audience)
    if "seniors" in a or "senior" in a:
        return "seniors"
    if "youth" in a or "under 30" in a or "children" in a:
        return "young-adult"
    return "all-ages"


def infer_identity_focused(audience: str, interests: str) -> bool:
    """Determine if organization is identity-focused."""
    combined = normalize_key(audience + " " + interests)
    flags = [
        "immigrants",
        "poc",
        "2slgbtq",
        "lgbtq",
        "women",
        "indigenous",
        "low income",
        "disability",
    ]
    return any(f in combined for f in flags)


def parse_contact_fields(row: Dict[str, str], website_column: str) -> Tuple[Optional[str], Optional[str]]:
    """Extract website and email from CSV row."""
    website = (row.get(website_column) or "").strip() or None
    email_field = (row.get("Email") or "").strip()

    email = None
    if email_field:
        if email_field.startswith("http://") or email_field.startswith("https://"):
            # Sometimes the CSV uses this column for contact links
            website = website or email_field
        elif "@" in email_field and " " not in email_field:
            email = email_field

    return website, email


def build_markdown(row: Dict[str, str], website_column: str) -> Tuple[str, str, str]:
    """Build markdown content from CSV row."""
    name = (row.get("Organization Name") or "").strip()
    interests_str = (row.get("Interests") or "").strip()
    org_type_str = (row.get("Organization Type") or "").strip()
    audience = (row.get("Audience") or "").strip()
    description_scraped = (row.get("Description (Scraped)") or "").strip()
    extra_comments = (row.get("Extra Comments") or "").strip()

    # Map to site taxonomy
    site_type = map_org_type(org_type_str)
    interests = map_interests(interests_str)
    age_range = infer_age_range(audience)
    identity_focused = infer_identity_focused(audience, interests_str)

    # Status defaults to active
    status = "active"

    website, email = parse_contact_fields(row, website_column)

    # Conservative defaults for fields we don't have
    meeting_format = "in-person"
    location_area = "city-wide"

    # Build frontmatter
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
        'permalink: "/organizations/{{ page.fileSlug }}/"',
        "---",
        "",
    ]

    # Build description
    description_parts: List[str] = []
    
    if description_scraped:
        description_parts.append(description_scraped)
    elif interests_str:
        description_parts.append(f"Focused on {interests_str}.")
    
    if not description_parts:
        description_parts.append("Community organization in Calgary.")

    body_lines = [
        "\n\n".join(description_parts),
        "",
        '<div class="org-contact-info">',
        "  <strong>Contact Info:</strong>",
        "  <ul class=\"list-none pl-0\">",
    ]
    
    if website:
        body_lines.append(f"    <li>Website: <a href=\"{website}\" target=\"_blank\">{website}</a></li>")
    if email:
        body_lines.append(f"    <li>Email: <a href=\"mailto:{email}\">{email}</a></li>")

    body_lines.extend([
        "  </ul>",
        "</div>",
    ])

    if extra_comments:
        body_lines.extend(["", "**Notes:**", extra_comments])

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
    """Convert CSV rows to markdown files."""
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    stats = WriteStats()

    for row in rows:
        name = (row.get("Organization Name") or "").strip()
        if not name:
            continue

        # Filter by site flag if specified
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
        default=os.path.join("docs", "UPDATED", "Calgary Groups - Organizations.with_urls.csv"),
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
