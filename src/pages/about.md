---
layout: layouts/base.njk
title: About
permalink: /about/
---

{% include "partials/breadcrumb.njk" %}

<section class="space-y-6">
  <header class="space-y-2">
    <h1 class="inline-flex items-center gap-3 text-3xl font-semibold tracking-tight">
      <i aria-hidden="true" class="fa-solid fa-circle-info text-slate-900 dark:text-slate-100"></i>
      <span>About Calgary Groups</span>
    </h1>
    <p class="max-w-2xl text-slate-700 dark:text-slate-300">Learn more about {{ site.name }} and our mission to connect Calgarians with community organizations.</p>
  </header>

  <div class="prose prose-slate max-w-none dark:prose-invert">
    <p>Calgary Groups is a community-driven directory to help people discover and connect with grassroots organizations, clubs, activist groups, and community initiatives across Calgary. We believe in making it easier for everyone to find their community.</p>
    
    <h2>Why we created this</h2>

    <p>Calgary has so much community energy—but it's scattered across Instagram, Facebook Groups, newsletters, old websites, and word-of-mouth. That fragmentation makes it harder for people to:</p>

    <ul>
      <li>discover groups that match their values and interests</li>
      <li>find where/when things happen</li>
      <li>share reliable links with friends</li>
      <li>keep a community resource up-to-date over time</li>
    </ul>

    <p>We built Calgary Groups to be a simple, welcoming "public index" for local organizing and community life:</p>

    <ul>
      <li><strong>Searchable</strong>: you can filter by type and interests.</li>
      <li><strong>Fast & accessible</strong>: static site, minimal dependencies, readable on any device.</li>
      <li><strong>Community-editable</strong>: listings live as plain text files in the repo.</li>
      <li><strong>Platform-independent</strong>: not locked inside a social network or proprietary tool.</li>
    </ul>

    <h2>How it works</h2>

    <p>Each organization listing is a Markdown file in this repository (under <code>src/content/organizations/</code>). The site is generated with Eleventy and styled with Tailwind CSS.</p>

    <h2>Add or update a listing</h2>

    <p><strong>Submit a group</strong>: use the form on <a href="/submit/">/submit/</a>.</p>
    <p><strong>Fix a listing</strong>: open a GitHub issue or submit a pull request.</p>

    <p>We try to keep listings factual and link to primary sources (official site, social profiles, etc.). If something looks wrong, please flag it.</p>

    <h2>About Berry House</h2>

    <p>Calgary Groups is made by <strong><a href="https://berryhouse.ca/" target="_blank" rel="noopener noreferrer">Berry House</a></strong>.</p>

    <p>Berry House builds fast, accessible JAMstack websites and thoughtful, effective writing. We help independent creators, non-profits, and small teams communicate clearly and own their platform.</p>

    <h3>What we do</h3>

    <ul>
      <li><strong>Websites</strong>: Eleventy/Tailwind builds, custom themes, content migrations, SEO, performance and accessibility audits.</li>
      <li><strong>Writing</strong>: website copy, information architecture, editorial strategy, documentation.</li>
      <li><strong>Education</strong>: workshops and 1:1 sessions on publishing workflows, accessibility, and sustainable content.</li>
    </ul>

    <p><a href="https://berryhouse.ca/" target="_blank" rel="noopener noreferrer">Visit Berry House</a> to learn more or work with us.</p>
  </div>
</section>