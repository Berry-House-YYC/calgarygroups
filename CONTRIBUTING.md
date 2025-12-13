# Contributing

Thanks for contributing to Calgary Groups.

## Ways to contribute

- Fix typos or improve clarity in copy
- Add or update organization listings
- Improve accessibility and performance
- Improve filters/search and overall UX

## Development setup

```bash
npm install
npm run dev
```

Before opening a PR, make sure this passes:

```bash
npm run build
```

## Adding or updating organizations

### Preferred method (simple edits)

Edit or add markdown files in:

- `src/content/organizations/**`

Use the existing front matter fields as a guide.

### Bulk import / maintenance

If updating many organizations at once, use the scripts:

- `scripts/merge_urls_into_csv.py`
- `scripts/csv_to_organizations.py`

## Pull requests

- Keep PRs small and focused.
- Describe what changed and why.
- If you are changing taxonomy (types/interests), note the impact on existing content.

## Content standards

- Keep descriptions factual and neutral.
- Do not publish private/personal information.
- Prefer official websites over social links when possible.
- If you add an email address, ensure it is a public contact address.
