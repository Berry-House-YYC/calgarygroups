---
layout: layouts/base.njk
title: About
---

{% include "partials/breadcrumb.njk" %}

<section class="space-y-6">
  <h1 class="page-icon fa-solid fa-circle-info">About Calgary Groups</h1>

  <p>Calgary Groups is a community-driven directory to help people discover and connect with grassroots organizations, clubs, activist groups, and community initiatives across Calgary. We believe in making it easier for everyone to find their community.</p>
## Why we created this

Calgary has so much community energy—but it's scattered across Instagram, Facebook Groups, newsletters, old websites, and word-of-mouth. That fragmentation makes it harder for people to:

- discover groups that match their values and interests
- find where/when things happen
- share reliable links with friends
- keep a community resource up-to-date over time

We built Calgary Groups to be a simple, welcoming "public index" for local organizing and community life:

- **Searchable**: you can filter by type and interests.
- **Fast & accessible**: static site, minimal dependencies, readable on any device.
- **Community-editable**: listings live as plain text files in the repo.
- **Platform-independent**: not locked inside a social network or proprietary tool.

## How it works

Each organization listing is a Markdown file in this repository (under `src/content/organizations/`). The site is generated with Eleventy and styled with Tailwind CSS.

- **Directory page**: filter/search across all listings.
- **Organization pages**: one page per org, generated from its Markdown file.

## Add or update a listing

- **Submit a group**: use the form on [/submit/](/submit/).
- **Fix a listing**: open a GitHub issue or submit a pull request.

We try to keep listings factual and link to primary sources (official site, social profiles, etc.). If something looks wrong, please flag it.

## About Berry House

Calgary Groups is made by **[Berry House](https://berryhouse.ca/)**.

Berry House builds fast, accessible JAMstack websites and thoughtful, effective writing. We help independent creators, non-profits, and small teams communicate clearly and own their platform.

### What we do

- **Websites**: Eleventy/Tailwind builds, custom themes, content migrations, SEO, performance and accessibility audits.
- **Writing**: website copy, information architecture, editorial strategy, documentation.
- **Education**: workshops and 1:1 sessions on publishing workflows, accessibility, and sustainable content.

### How we work

- **Human-centered by design**: content first, technology second.
- **Own your platform**: no lock-in; plain files and simple pipelines.
- **Accessible and fast**: semantic HTML and performance baked in.
- **Calm, sustainable websites**: low overhead and easy maintenance.

Learn more at <https://berryhouse.ca/>.
