---
layout: layouts/page.njk
title: Submit an Organization
permalink: false
---

## Submit a listing

If you know a Calgary-based community group that should be in the directory (or you want to correct an existing listing), you can submit it here.

## Guidelines

- **Keep it factual**: a short description + contact info is best.
- **Include a primary link**: website is ideal; otherwise a social profile.
- **Pick one type**: choose the closest match.
- **Pick 1–3 interests**: use the existing interest tags where possible.
- **Don’t share private info**: only public contact details.

Need help understanding the types and interests? See our [Types & Interests guide](/info/).

### Types

- `Nonprofit` - Registered organizations (societies, charities)
- `Club` - Social or interest-based groups
- `Grassroots` - Activist or advocacy-focused groups
- `Chapter` - Local branch of a larger organization
- `Cooperative` - Collective run by multiple organizations
- `Small Business` - For-profit businesses serving community needs

### Interests

- `anti-racism`
- `arts`
- `book` - Book clubs
- `culture and heritage`
- `disability/neurodivergent`
- `education`
- `environment`
- `general`
- `health-wellness`
- `indigenous`
- `international-solidarity`
- `justice`
- `2slgbtq+`
- `low-income`
- `seniors`
- `sports-rec`
- `tech`
- `urban-issues`
- `women+`
- `youth`

## Submission form

<form name="submit-organization" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/submit/success/" class="mt-6 space-y-6">
  <input type="hidden" name="form-name" value="submit-organization" />
  <p class="hidden">
    <label>Don’t fill this out if you’re human: <input name="bot-field" /></label>
  </p>

  <div class="grid gap-4 md:grid-cols-2">
    <div class="space-y-1">
      <label class="text-sm font-medium text-slate-900" for="org_name">Organization name</label>
      <input id="org_name" name="org_name" type="text" required class="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200" />
    </div>

    <div class="space-y-1">
      <label class="text-sm font-medium text-slate-900" for="website">Website (or primary link)</label>
      <input id="website" name="website" type="url" placeholder="https://…" class="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200" />
    </div>

    <div class="space-y-1">
      <label class="text-sm font-medium text-slate-900" for="email">Public contact email (optional)</label>
      <input id="email" name="email" type="email" placeholder="hello@…" class="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200" />
    </div>

    <div class="space-y-1">
      <label class="text-sm font-medium text-slate-900" for="submitter_email">Your email (optional)</label>
      <input id="submitter_email" name="submitter_email" type="email" placeholder="so we can follow up" class="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200" />
    </div>

    <div class="space-y-1">
      <label class="text-sm font-medium text-slate-900" for="type">Type</label>
      <select id="type" name="type" required class="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200">
        <option value="">Select…</option>
        <option value="Nonprofit">Nonprofit</option>
        <option value="Club">Club</option>
        <option value="Grassroots">Grassroots</option>
        <option value="Chapter">Chapter</option>
        <option value="Cooperative">Cooperative</option>
        <option value="Small Business">Small Business</option>
      </select>
    </div>

    <div class="space-y-1">
      <label class="text-sm font-medium text-slate-900" for="meeting_format">Meeting format (optional)</label>
      <select id="meeting_format" name="meeting_format" class="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200">
        <option value="">Any / unknown</option>
        <option value="in-person">in-person</option>
        <option value="hybrid">hybrid</option>
      </select>
    </div>

    <div class="space-y-1">
      <label class="text-sm font-medium text-slate-900" for="age_range">Age range (optional)</label>
      <select id="age_range" name="age_range" class="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200">
        <option value="">Any / unknown</option>
        <option value="all-ages">all-ages</option>
        <option value="youth">youth</option>
        <option value="seniors">seniors</option>
      </select>
    </div>

    <div class="space-y-1">
      <label class="text-sm font-medium text-slate-900" for="location_area">Location area (optional)</label>
      <input id="location_area" name="location_area" type="text" placeholder="e.g., city-wide, downtown, NW" class="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200" />
    </div>

    <div class="space-y-1">
      <label class="text-sm font-medium text-slate-900" for="status">Status (optional)</label>
      <select id="status" name="status" class="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200">
        <option value="">Unknown</option>
        <option value="active">active</option>
        <option value="inactive">inactive</option>
        <option value="unknown">unknown</option>
      </select>
    </div>

    <div class="flex items-center gap-2 pt-6">
      <input id="identity_focused" name="identity_focused" type="checkbox" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" />
      <label class="text-sm font-medium text-slate-900" for="identity_focused">Identity-focused</label>
    </div>
  </div>

  <fieldset class="space-y-2">
    <legend class="text-sm font-medium text-slate-900">Interests (pick up to 3)</legend>
    <div class="grid grid-cols-1 gap-2 text-sm sm:grid-cols-2 lg:grid-cols-3">
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="anti-racism" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> anti-racism</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="arts" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> arts</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="book" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> book clubs</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="disability/neurodivergent" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> disability/neurodivergent</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="education" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> education</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="environment" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> environment</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="general" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> general</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="health-wellness" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> health and wellness</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="indigenous" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> indigenous</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="international-solidarity" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> international solidarity</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="justice" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> justice</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="low-income" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> low-income</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="seniors" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> seniors</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="sports-rec" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> sports and rec</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="tech" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> tech</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="urban-issues" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> urban issues</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="women+" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> women+</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="youth" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> youth</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="culture and heritage" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> culture and heritage</label>
      <label class="flex items-center gap-2"><input type="checkbox" name="interests" value="2slgbtq+" class="h-4 w-4 rounded border-slate-300 text-slate-900 focus:ring-slate-400" /> 2slgbtq+</label>
    </div>
  </fieldset>

  <div class="space-y-1">
    <label class="text-sm font-medium text-slate-900" for="description">Short description</label>
    <textarea id="description" name="description" rows="5" required class="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200" placeholder="What does this organization do? Who is it for? What should someone know before reaching out?"></textarea>
  </div>

  <div class="space-y-1">
    <label class="text-sm font-medium text-slate-900" for="notes">Notes (optional)</label>
    <textarea id="notes" name="notes" rows="4" class="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-slate-400 focus:outline-none focus:ring-2 focus:ring-slate-200" placeholder="Anything else we should know?"></textarea>
  </div>

  <div class="space-y-2">
    <button type="submit" class="inline-flex items-center justify-center rounded-md bg-slate-900 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-400">Submit</button>
    <p class="text-sm text-slate-600">Prefer email? Send details to <a class="font-medium text-slate-900 hover:underline focus:outline-none focus:ring-2 focus:ring-slate-400" href="mailto:calgary@berryhouse.ca">calgary@berryhouse.ca</a>.</p>
  </div>
</form>

## If you want to contribute via GitHub

If you’d rather add the listing directly, you can create a new Markdown file in `src/content/organizations/`.

Template:

```md
---
layout: layouts/organization.njk
name: "Organization Name"
type: "Club" # Nonprofit, Club, Grassroots, Chapter, Cooperative, Small Business
interests: ["arts", "education"] # Choose from the list on /info/
age_range: "all-ages" # all-ages, youth, adults, seniors
identity_focused: false
meeting_format: "in-person" # in-person, online, hybrid
location_area: "city-wide"
status: "active" # active, inactive, unknown
permalink: "/organizations/{{ page.fileSlug }}/"
---

One-paragraph description.

**Contact Info:**
- Website: https://example.com
- Email: contact@example.com
```
