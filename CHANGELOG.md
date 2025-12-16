# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2025-12-16

### Design & Branding
- Added custom brand color palette (Pumpkin Spice, Seashell, Petal Pink, Coffee Bean, Dark Cyan)
- Integrated brand colors throughout site for both light and dark modes
- Updated theme colors: cream backgrounds (light mode), coffee backgrounds (dark mode)
- Added brand accent colors: orange (light mode), cyan (dark mode)

### User Interface Enhancements
- Redesigned navigation bar: floating, rounded, 90% width with sticky positioning (desktop only)
- Enhanced navigation with subtle shadow, backdrop blur, and semi-transparent background
- Redesigned organization cards with rounded corners and better spacing
- Updated organization detail pages with prominent type badges and colorful interest tags
- Made organization titles clickable (link to external website)
- Added filter icons with dark mode color variants for better visibility
- Fixed mobile viewport overflow issues on organization cards

### User Experience Improvements
- Implemented collapsible filters for Type and Interests sections
- Responsive filter defaults: open on desktop, closed on mobile
- Enhanced filter buttons on mobile with clear visual indicators
- Removed sticky navigation on mobile to save screen space
- Added "Back to Directory" link on organization detail pages

### Dark Mode Optimization
- Improved dark mode color variation across components
- Changed card backgrounds from slate-900 to slate-800 for better depth
- Brightened link colors (Learn More, titles) from dark cyan to bright cyan-400
- Increased border opacity for better element definition
- Enhanced results counter and metadata box contrast

### Progressive Web App (PWA)
- Created comprehensive web manifest with proper PWA configuration
- Implemented service worker with caching strategy (static + dynamic cache)
- Added offline support for cached pages
- Enabled app installation on mobile and desktop
- Configured maskable icons for better Android display
- Added app screenshot for install prompts

### Documentation
- Updated README with detailed feature breakdown (core functionality, design/UX, PWA)
- Updated TODO.md to reflect completed MVP items and Phase 2 plans
- Documented all new features and improvements

### Bug Fixes
- Fixed empty organization cards caused by duplicate files in old folder structure
- Removed old organization folders (activist-groups, grassroots-initiatives, resources, clubs)
- Fixed mobile card width overflow issues

## [0.1.0] - 2025-12-13

- Initial project scaffolding (11ty + Tailwind)
- Added baseline site pages and organization content structure
- Added scripts to:
  - Merge URLs from `docs/urls.md` into the Organizations CSV (`scripts/merge_urls_into_csv.py`)
  - Generate organization markdown files from the CSV (`scripts/csv_to_organizations.py`)
- Fixed directory Alpine initialization by avoiding raw JSON inside the `x-data` attribute
- Added repo documentation and hygiene files (`README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `.editorconfig`, `.nvmrc`)
- Added dual licensing (MIT for code, CC BY 4.0 for content)
