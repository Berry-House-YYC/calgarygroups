# Calgary Groups - AI Agent Instructions

## Project Overview

Calgary Groups is a **static site directory** for discovering grassroots organizations and community groups in Calgary. Built with **11ty + Tailwind CSS + Alpine.js**, the site has no backend—data is stored as **markdown files in Git**, ensuring full community ownership.

### Core Architecture

1. **Data Layer**: Organizations stored as `.md` files in `src/content/organizations/{type}/` (type: nonprofit, grassroots, chapter, cooperative, social-club, small-business)
2. **Build Layer**: 11ty collects organization `.md` files, extracts frontmatter (name, type, interests, location, etc.), applies layouts, and generates static HTML
3. **Rendering Layer**: Organization data embedded as JSON in `<template>` tag (`src/index.njk`), then Alpine.js powers client-side search/filtering
4. **Styling**: Tailwind CSS with two color modes (light: cream/dark: coffee backgrounds, orange/cyan accents)

## Critical Developer Workflows

### Start Development
```bash
npm install                  # Install 11ty, Tailwind, Alpine.js
npm run dev                  # Runs 11ty watch + Tailwind watch in parallel
# Visit http://localhost:8080
```

### Production Build
```bash
npm run build                # Optimizes CSS + generates static site
# Output: _site/
```

### Data Import (CSV → Markdown)
```bash
python3 scripts/merge_urls_into_csv.py --fuzzy
python3 scripts/csv_to_organizations.py --csv "path/to.csv" --only-site-flag Y
```
Converts legacy CSVs into markdown organization files. Python scripts handle type/interest mapping heuristics.

### Deployment
Netlify auto-deploys on push. Build command: `npm run build`. Publish dir: `_site/`. Node 20 required.

## Key Files & Their Purposes

| File | Purpose |
|------|---------|
| `.eleventy.js` | Defines Nunjucks filters (`stripHtml`, `extractFirstUrl`, `json`), collections (`organizations`), and directory structure |
| `src/index.njk` | Embeds all organizations as JSON in `<template>`, Alpine.js mounts search/filter UI on it |
| `src/_includes/layouts/base.njk` | Master layout with theme toggle, meta tags, Alpine.js + Tailwind |
| `src/_includes/layouts/organization.njk` | Organization detail page with badges, interest tags, color-coded by org type |
| `src/content/organizations/defaults.json` | Default frontmatter for all org `.md` files (layout, age_range, status, interests) |
| `tailwind.config.cjs` | Brand colors (cream `#f5f5f0`, coffee `#1a1a1a`, orange `#ff6b35`, cyan `#00d9ff`) |
| `netlify.toml` | Build config (Node 20, command, output dir) |

## Content Conventions

### Organization Frontmatter (YAML)
```yaml
name: "Organization Name"
type: "Nonprofit|Grassroots|Social Club|Chapter|Cooperative|Small Business"
interests: ["environment", "social-impact", "tech", ...]  # See full list below
age_range: "youth|young-adult|all-ages|seniors"
identity_focused: true|false
meeting_format: "in-person|online|hybrid"
location_area: "northwest|northeast|southwest|southeast|downtown|online|city-wide"
status: "active|inactive|seasonal"
description: "Optional. Short description (used as meta tag)"
community_submitted: true|false  # Default: false
```

### Valid Interest Tags
`anti-racism`, `arts-culture`, `disability/neurodivergent`, `education`, `environment`, `health-wellness`, `indigenous`, `lgbtq2s`, `low-income`, `seniors`, `social-impact`, `sports-rec`, `tech`, `urban-issues`, `women+`, `youth`, `book`, `general`

Each tag has **icon + color** in `organization.njk` (hardcoded inline styles).

### File Naming
- Location: `src/content/organizations/{type}/{name}.md`
- Naming: lowercase, hyphen-separated, no spaces (e.g., `data-for-good-yyc.md`)
- Frontmatter defines `permalink: /organizations/{{ page.fileSlug }}/` (auto-converted from filename)

### Markdown Body
Body content appears below frontmatter. Contains description and **Contact Info** section with website/email links. Extracted as excerpt for search results via `stripHtml` + `truncate` filters.

## Search & Filtering Pattern

### Data Flow
1. All orgs serialized to JSON in `src/index.njk` template: `[{name, type, interests, age_range, status, meeting_format, location_area, website, excerpt, url}, ...]`
2. JSON embedded in `<template id="organizations-data">` (hidden in DOM)
3. Alpine.js function `directory()` loads this JSON and exposes filter logic
4. Filters query: `type`, `interests` (multi-select), `age_range`, `identity_focused`, `meeting_format`, text search on name + excerpt
5. Filter state persisted to **URL query params** (no separate backend)

### Adding a New Filter
1. Add field to org frontmatter (e.g., `cost: "free|donation|paid"`)
2. Add field to JSON serialization in `src/index.njk`
3. Extend Alpine `directory()` filter logic in `src/index.njk`
4. Add UI control (checkbox/select) in the filter panel

## Color System

**Type badges** (org detail page):
- Nonprofit → blue, Grassroots → green, Social Club → purple, Chapter → indigo, Cooperative → teal, Small Business → amber

**Interest tags** (org detail page):
- Each tag has custom bg/text/border RGB values hardcoded in `organization.njk`
- LGBTQ2S+ has gradient (not solid color)

**Theme**:
- Light: `#f5f5f0` cream bg, `#1a1a1a` dark text
- Dark: `#1a1a1a` coffee bg, `#f5f5f0` light text
- Accents: `#ff6b35` orange (light mode), `#00d9ff` cyan (dark mode)

Theme toggle in header uses `localStorage` for persistence. Script in `base.njk` `<head>` runs before DOM render to prevent flash.

## Common Patterns & Gotchas

### Nunjucks Filters in Eleventy
Custom filters in `.eleventy.js` are available in all templates:
- `json` - safely JSON-encode a value
- `stripHtml` - remove HTML tags (used for excerpts)
- `truncate(value, maxLength=180)` - truncate string + add "…"
- `extractFirstUrl` - extract first URL from markdown body
- `unescape` - decode HTML entities

### Markdown in Nunjucks
`markdownTemplateEngine: "njk"` means org `.md` files are processed as Nunjucks first, then Markdown. You can use Nunjucks variables (e.g., `{{ name }}`) in org body if needed.

### Collection Creation
`organizations` collection auto-globs `src/content/organizations/**/*.md` (all types). Use in loops to iterate all orgs.

### Alpine.js in This Project
Alpine is minimal—used only for search/filter state management and theme toggle. No complex components. State lives in URL query params for persistence across page reloads.

## Git Workflow & Conventions

- **Branches**: Feature branches for changes
- **Commits**: Squash before merge for clean history
- **Organization files**: Each org added/edited as individual `.md` file commit
- **Python scripts**: CSV import scripts update multiple files; commit scripts separately from generated files
- `.git-status.sh` runs on `npm run dev` to warn if uncommitted changes exist (safety check)

## Deployment & CI/CD

- **Hosting**: Netlify
- **Trigger**: Push to main branch
- **Build**: `npm run build` (Tailwind minify + 11ty static generation)
- **Env**: Node 20 (specified in `netlify.toml`)
- **Output**: `_site/` directory deployed as static site

## Scripts Overview

| Script | Purpose |
|--------|---------|
| `merge_urls_into_csv.py` | Fuzzy-match URLs from `docs/urls.md` into org CSV |
| `csv_to_organizations.py` | Bulk convert CSV rows → `.md` files with type/interest heuristics |
| `update_org_descriptions.py` | Fetch descriptions from org websites (AI-assisted) |
| `add_book_interest_v2.py` | Bulk-add book club tag to organizations matching keywords |
| `validate_org_files.py` | Lint organization frontmatter for required fields |

## Adding New Features

**New Filter Type?** Update `index.njk` JSON serialization + Alpine filter logic + UI control.
**New Org Type?** Add folder `src/content/organizations/{new-type}/`, update `defaults.json` folder map, add color mapping in `organization.njk`.
**New Interest Tag?** Add tag to `interests` array, map color/icon in `organization.njk` (hardcoded).
**New Page?** Add `.md` or `.njk` file to `src/pages/` or `src/content/`, frontmatter sets layout/title.

## Accessibility & Performance Notes

- **Keyboard nav**: All interactive elements are keyboard-accessible (Alpine handles `:focus` states)
- **Dark mode**: Tested with high contrast settings; colors meet WCAG AA standards
- **PWA**: Service worker caches all assets; offline fallback included (`src/static/sw.js`)
- **Performance**: Static site = fast; no JS frameworks beyond Alpine for search (minimal bundle)
- **SEO**: Sitemap + robots.txt auto-generated; JSON-LD structured data in `organization.njk`

## Questions? Check These First

- **How do I add an organization?** → Add `.md` file to `src/content/organizations/{type}/` with frontmatter + body
- **How do I change a filter?** → Edit Alpine `directory()` logic in `src/index.njk`
- **How do I add a new color to the palette?** → Update `tailwind.config.cjs` and hardcoded RGB values in layouts
- **How do I bulk-import orgs from CSV?** → Use `merge_urls_into_csv.py` + `csv_to_organizations.py`
- **How do I deploy?** → Push to main; Netlify auto-deploys
