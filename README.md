<p align="center">
   <img src="src/static/favicon/android-chrome-512x512.png" alt="Calgary Groups" width="128" height="128" />
 </p>

# Calgary Groups

**Search and filter grassroots organizations, clubs, activist groups, and community initiatives in Calgary.**

Calgary Groups is a centralized, searchable directory designed to help Calgarians discover and connect with local organizations that match their interests. Whether you're looking for activist groups, social clubs, nonprofits, or community initiatives, this directory makes it easy to find organizations working on the issues you care about.

![Calgary Groups Screenshot](src/screenshot.png)

## Features

- 🔍 **Advanced search & filtering** - Search by name, description, organization type, interests, meeting format, and location
- 🏷️ **Rich taxonomy** - Organizations categorized by type (Nonprofit, Grassroots, Social Club, Chapter, Cooperative, Small Business) and interests (Environment, Social Impact, LGBTQ2S+, Anti-Racism, Tech, Urban Issues, and more)
- 🎨 **Beautiful UI** - Clean, modern interface with dark mode support
- 📱 **Fully responsive** - Works seamlessly on desktop, tablet, and mobile
- ⚡ **Fast & lightweight** - Static site with no database or backend required
- 🌐 **Open source** - Full transparency and community contributions welcome

## About This Repository

This repo contains:

- A static website built with **11ty + Tailwind CSS + Alpine.js**
- Organization listings stored as **markdown files in Git** (full data ownership)
- Helper scripts for importing data from the CSVs in `docs/`

## Tech stack

- **Static site generator:** 11ty (Eleventy)
- **Styling:** Tailwind CSS
- **Interactivity:** Alpine.js
- **Hosting:** Netlify

## Local development

### Prerequisites

- Node.js **20** (see `.nvmrc`)
- npm

### Install

```bash
npm install
```

### Run dev server

```bash
npm run dev
```

Then open:

- `http://localhost:8080/`

### Production build

```bash
npm run build
```

Output is written to:

- `_site/`

## Content editing

Organization files live here:

- `src/content/organizations/`

Each organization is a markdown file with front matter.

Example:

```md
---
name: "Organization Name"
type: "Nonprofit" # Nonprofit, Grassroots, Social Club, Chapter, Cooperative, Small Business
interests: ["environment", "social-impact", "tech"]
age_range: "all-ages" # youth, young-adult, all-ages, seniors
identity_focused: false
meeting_format: "in-person" # in-person, online, hybrid
location_area: "city-wide" # northwest, northeast, southwest, southeast, downtown, online, city-wide
status: "active" # active, inactive, seasonal
---

Short description here.

**Contact Info:**
- Website: https://example.com
- Email: contact@example.com
```

### Organization Types

- **Nonprofit** - Registered nonprofits and charitable organizations
- **Grassroots** - Community-driven initiatives and grassroots movements
- **Social Club** - Social groups and book clubs
- **Chapter** - Local chapters of national/international organizations
- **Cooperative** - Member-owned cooperatives
- **Small Business** - Community-oriented small businesses

### Interests/Tags

Organizations can be tagged with multiple interests including:
- Anti-racism, Arts & culture, Disability/Neurodivergent, Education, Environment
- Health & wellness, Indigenous, LGBTQ2S+, Low-income, Seniors
- Social impact, Sports & rec, Tech, Urban Issues, Women+, Youth

### Folder conventions

Organizations are organized by type:

- `src/content/organizations/nonprofit/`
- `src/content/organizations/grassroots/`
- `src/content/organizations/social-club/`
- `src/content/organizations/chapter/`
- `src/content/organizations/cooperative/`
- `src/content/organizations/small-business/`

File naming convention:

- lowercase
- hyphen-separated
- no spaces

## Import workflow (CSV -> markdown)

The `docs/` folder contains CSVs used for bulk import/maintenance.

### 1) Merge URLs from `docs/urls.md` into the Organizations CSV

This generates a new CSV with a `Website` column:

```bash
python3 scripts/merge_urls_into_csv.py --fuzzy
```

Default output:

- `docs/Mass Organization CRM - Organizations.with_urls.csv`

### 2) Convert CSV rows into organization markdown files

```bash
python3 scripts/csv_to_organizations.py \
  --csv "docs/Mass Organization CRM - Organizations.with_urls.csv" \
  --only-site-flag Y
```

Notes:

- The script uses conservative defaults for fields we don’t have yet (e.g. `location_area`, `meeting_format`).
- Type and interest mappings are heuristics that you can refine over time in `scripts/csv_to_organizations.py`.

## Deployment (Netlify)

This repo includes `netlify.toml`.

- **Build command:** `npm run build`
- **Publish directory:** `_site`
- **Node version:** 20

## Repo hygiene

- `TODO.md` tracks planned work.
- `CHANGELOG.md` tracks notable changes.

## License

This repository is dual-licensed:

- **Code** (site source, scripts, configuration): **MIT** (see `LICENSE`)
- **Content/data** (organization listings and related data): **CC BY 4.0** (see `LICENSE-CONTENT`)
