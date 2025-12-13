# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2025-12-13

- Initial project scaffolding (11ty + Tailwind)
- Added baseline site pages and organization content structure
- Added scripts to:
  - Merge URLs from `docs/urls.md` into the Organizations CSV (`scripts/merge_urls_into_csv.py`)
  - Generate organization markdown files from the CSV (`scripts/csv_to_organizations.py`)
- Fixed directory Alpine initialization by avoiding raw JSON inside the `x-data` attribute
- Added repo documentation and hygiene files (`README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.editorconfig`, `.nvmrc`)
- Added dual licensing (MIT for code, CC BY 4.0 for content)
