# TODO

## MVP (Phase 1) - Launch Ready ✅

- [x] Implement directory filters (type, interest, age range, identity-focused, meeting format, location area) with URL persistence
- [x] Implement text search across organization name + description
- [x] Add sitemap + robots.txt
- [x] Dark mode support with optimized colors
- [x] Mobile responsive design with collapsible filters
- [x] Accessibility features (keyboard navigation, focus states, high contrast)
- [ ] Add organization schema markup (JSON-LD) to organization detail pages
- [ ] Add print-friendly styling for organization pages
- [ ] Term highlighting in search results

## Design & UX (Recently Completed)

- [x] Custom brand color palette (cream/coffee backgrounds, orange/cyan accents)
- [x] Modern UI (floating navigation, rounded cards, shadows, backdrop blur)
- [x] Enhanced organization detail pages (prominent badges, clickable titles)
- [x] Responsive collapsible filters (open on desktop, closed on mobile)
- [x] Optimized dark mode with better color variation and text contrast
- [x] PWA functionality (installable, offline support, service worker)

## Content

- [x] Import initial organization list from CSVs in `docs/`
- [x] Merge URLs from `docs/urls.md` into the Organizations CSV (see `scripts/merge_urls_into_csv.py`)
- [x] Generate organization markdown files from the CSV (see `scripts/csv_to_organizations.py`)
- [ ] Add content templates and editing workflow notes for non-technical editors
- [ ] Reach out to initial organizations for accuracy verification

## Phase 2 - Post-Launch

- [ ] Enhanced submission workflow (auto-create draft markdown from form)
- [ ] Event calendar (link aggregation)
- [ ] Newsletter/blog system (markdown posts)
- [ ] Enhanced organization profiles (volunteer opportunities, accessibility info, languages, cost)
- [ ] Analytics setup (privacy-focused: Plausible or Fathom)
