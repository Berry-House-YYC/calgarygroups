# Calgary Groups - Technical Specification & Project Plan

**Project Name**: Calgary Groups  
**Domain**: calgarygroups.ca  
**Tagline/Subtitle**: Calgary Groups Directory (for clarity on main page)  
**Project Type**: Community directory wayfinder for grassroots organizations, clubs, activist groups, and community initiatives in Calgary

---

## Project Overview

### Purpose
A centralized, searchable directory to help Calgarians find grassroots organizations, clubs, activist groups, and community initiatives. Addresses the challenge of community-finding after leaving institutional settings (school/university) by consolidating scattered information into one accessible, SEO-optimized platform.

### Core Values
- **Ethical**: Open-source tools, full data ownership
- **Accessible**: WCAG 2.1 AA compliant, mobile-responsive, fast loading
- **Maintainable**: Content owner can update independently with minimal code knowledge
- **Community-focused**: Free/low-cost, volunteer-run, transparent operations

---

## Technical Architecture

### Tech Stack (Confirmed)

**Framework**: Jamstack approach
- **Static Site Generator**: 11ty
- **Content Management**: Markdown files in Git repository (GitHub/GitLab)
- **Styling**: Tailwind CSS
- **Interactivity**: Alpine.js for filtering/search
- **Hosting**: Netlify (free tier)
- **Version Control**: Git with GitHub Desktop (GUI for content owner)

**Why This Stack**:
- Zero AI in operational pipeline
- Open-source tools throughout
- Full data ownership and transparency
- Minimal environmental footprint
- Free except domain ($15-20/year)
- Content owner can update via markdown files

### Content Structure

**Organization Data Format** (Markdown files):
```markdown
---
name: "Organization Name"
type: "club" # club, activist-group, resource, grassroots-initiative
interests: ["arts", "social-impact"] # sports-rec, arts-culture, social-impact, environment, education, health-wellness, lgbtq2s, youth, seniors
age_range: "all-ages" # youth, young-adult, all-ages, seniors
identity_focused: false # true/false
meeting_format: "in-person" # in-person, online, hybrid
location_area: "northwest" # northwest, northeast, southwest, southeast, downtown, online, city-wide
status: "active" # active, inactive, seasonal
---

[2-3 sentence description of what the organization does]

**Contact Info:**
- Website: https://example.com
- Email: contact@example.com
- Social: @handlename
- Meeting Frequency: Weekly/Monthly/etc
```

**File Organization**:
```
/content
  /organizations
    /clubs
      calgary-cycle-chums.md
      reading-circle-yyc.md
    /activist-groups
      climate-action-calgary.md
    /resources
      volunteer-connector.md
  /pages
    about.md
    submit.md
    feedback.md
```

---

## MVP Features (Phase 1 - Launch)

### 1. Organization Directory
- Display all organizations as filterable cards
- Each card shows: name, type badge, 1-2 sentence excerpt, primary interest tags
- Click for full details page with complete info

### 2. Multi-Filter System
**Primary Filters**:
- **Type**: Club, Activist Group, Resource/Service, Grassroots Initiative
- **Interest**: Sports/Rec, Arts/Culture, Social Impact, Environment, Education, Health/Wellness, LGBTQ2S+, Youth, Seniors
- **Additional**: Age Range, Identity-Focused (checkbox), Meeting Format, Location Area

**Filter Behavior**:
- Combine filters (AND logic within categories, OR between some)
- Show count of results
- Clear all filters button
- Filters persist in URL for sharing

### 3. Search Functionality
- Text search across organization name and description
- Highlight search terms in results
- Search + filters work together

### 4. Core Pages
- **Home/Directory**: Main filterable listing
- **About**: Mission, founder story (brief), why this exists, how to use
- **Submit Your Organization**: Form (can use Netlify Forms or Google Forms embed)
- **Contact/Feedback**: Email prominently displayed, "Report incorrect info" option
- **Ko-fi Integration**: Donation button/link (non-intrusive, footer or about page)

### 5. SEO Optimization
- Semantic HTML5 structure
- Meta descriptions for all pages
- Organization schema markup (JSON-LD)
- Sitemap generation
- Calgary-focused keywords throughout
- Social sharing cards (Open Graph)

### 6. Accessibility
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader friendly
- High color contrast
- Alt text for any images
- Focus indicators
- Skip to content link

### 7. Design Requirements
- Modern, clean aesthetic
- Mobile-first responsive design
- Fast loading (< 2 seconds)
- Print-friendly organization pages

---

## Phase 2 Features (Near Future - 3-6 Months Post-Launch)

### 1. Enhanced Submission Process
- **Auto-submission workflow**: 
  - Form submission creates draft markdown file
  - Email notification to content owner
  - Review and publish process (edit file, commit)
  - No manual approval before appearing (low barrier to entry)

### 2. Event Calendar (Simplified)
**Approach**: Link aggregation rather than event management
- Monthly "Upcoming Events" section on homepage
- Links to organizations' own calendars/event pages
- Optional: Embed one shared Google Calendar for hand-picked events
- Manual curation by content owner (5-10 events/month max)

**What to Avoid**: Full event submission system (too much overhead)

### 3. Newsletter/Blog
- Monthly roundup of new organizations
- "Spotlight" feature on 1-2 groups per month
- Community news and opportunities
- Built into site (markdown blog posts)
- Optional email signup (Mailchimp free tier or similar)

### 4. Enhanced Organization Profiles
- Volunteer opportunity indicator/link
- Accessibility information (wheelchair accessible, ASL offered, etc.)
- Languages offered
- Cost information (free, sliding scale, membership fee)

---

## Future Considerations (Phase 3 - Shelved for Now)

### Ideas to Revisit After 6-12 Months
- **Arts Markets Directory**: Separate subdomain with vendor costs, application deadlines, host orgs
- **Reviews/Ratings System**: Requires complex moderation, potential for drama
- **Discord/Slack Community**: Needs significant community management time
- **Buddy System/Event Matching**: Technically complex, privacy concerns
- **Influencer/Blog Content**: Time-intensive, different skill set required
- **Sponsored Listings**: Mission creep, ethical considerations
- **Integration with Larger Nonprofits**: Case-by-case basis, don't dilute grassroots focus

---

## Content Owner Learning Requirements

### Skills to Learn (estimated 2-4 hours total)

**1. Markdown Basics** (30 minutes)
- Headings, lists, links
- Front matter (the `---` section at top of file)
- Practice file: https://www.markdownguide.org/basic-syntax/

**2. Git Basics with GitHub Desktop** (1-2 hours)
- Clone repository to local computer
- Edit files locally
- Commit changes (save with description)
- Push to GitHub (publish changes)
- Pull updates (sync with partner's changes)
- Recommended tutorial: GitHub Desktop documentation

**3. File Organization** (30 minutes)
- Understanding folder structure
- Naming conventions (lowercase, hyphens, no spaces)
- Where to add new organization files

**4. Content Editing Workflow** (30 minutes)
- Text editor setup (VS Code with markdown preview, or Typora)
- Finding and editing existing organizations
- Adding new organizations from template
- Preview before publishing

### Ongoing Time Commitment
- **Initial setup**: Partner handles (5-10 hours)
- **Per update session**: 5-10 minutes once familiar
- **Weekly maintenance**: 15-30 minutes (check submissions, respond to feedback)
- **Monthly updates**: 1-2 hours (add new orgs, update existing, check links)

---

## Partner Development Checklist

### Initial Setup Tasks

**Repository & Infrastructure**:
- [ ] Create GitHub repository
- [ ] Set up project with Astro/11ty
- [ ] Configure Tailwind CSS
- [ ] Set up Netlify/Vercel deployment
- [ ] Connect domain (calgarygroups.ca)

**Core Features**:
- [ ] Build homepage/directory view with card layout
- [ ] Implement multi-filter system (type, interest, age, format, location)
- [ ] Build search functionality
- [ ] Create individual organization detail pages
- [ ] Set up automatic sitemap generation
- [ ] Add schema markup for SEO

**Pages & Forms**:
- [ ] About page template
- [ ] Submit organization form (Netlify Forms or Google Forms)
- [ ] Contact/feedback page
- [ ] 404 error page

**Technical Requirements**:
- [ ] Mobile responsive breakpoints
- [ ] Accessibility features (keyboard nav, ARIA labels, focus states)
- [ ] Social sharing meta tags
- [ ] Print styles for organization pages
- [ ] Analytics setup (privacy-focused: Plausible or Fathom, optional)

**Content Templates**:
- [ ] Create markdown template for organizations
- [ ] Seed with 20-30 initial organizations
- [ ] Add sample content to all pages

**Documentation**:
- [ ] Write README for content owner with update instructions
- [ ] Create organization template file
- [ ] Document git workflow with screenshots
- [ ] List of all filter tags and their meanings

### Content Owner Onboarding
- [ ] Install GitHub Desktop on content owner's computer
- [ ] Clone repository locally
- [ ] Set up text editor (VS Code or Typora)
- [ ] Walk through: edit existing org → save → commit → push
- [ ] Walk through: add new org from template
- [ ] Practice session: 2-3 complete edits

---

## Launch Checklist

### Pre-Launch (2-4 Weeks Before)

**Content Preparation**:
- [ ] List of 20-30 initial organizations compiled
- [ ] All initial orgs added as markdown files
- [ ] About page written (mission, story, how to use)
- [ ] Ko-fi account set up and linked

**Technical QA**:
- [ ] Test all filters in combinations
- [ ] Test search functionality
- [ ] Mobile testing on multiple devices
- [ ] Accessibility audit (WAVE tool, keyboard navigation)
- [ ] SEO check (meta descriptions, titles, sitemap)
- [ ] Load speed test (PageSpeed Insights)
- [ ] Cross-browser testing (Chrome, Firefox, Safari)

**Soft Launch**:
- [ ] Share with 5-10 trusted community members for feedback
- [ ] Fix any critical bugs or UX issues
- [ ] Reach out to initial 20-30 organizations for buy-in
- [ ] Ask initial orgs to verify their listings

### Launch Day

- [ ] Publish site live
- [ ] Submit to Google Search Console
- [ ] Post in relevant Calgary Facebook groups (community, volunteer, activist)
- [ ] Reddit r/Calgary post (follow subreddit rules, be humble)
- [ ] Email initial organizations asking them to share
- [ ] Personal social media announcement

### Post-Launch (First Month)

- [ ] Respond to all feedback within 48 hours
- [ ] Process submission forms weekly
- [ ] Monitor analytics (if implemented)
- [ ] Add 5-10 new organizations
- [ ] Fix any bugs reported
- [ ] Thank people who share/promote the site

---

## Success Metrics

### 6-Month Goals
- 50+ organizations listed
- 500+ monthly website visitors
- 10+ organizations actively sharing the site
- Positive feedback from community members

### 1-Year Goals
- 100+ organizations listed
- 2,000+ monthly visitors
- Recognized resource in Calgary nonprofit/grassroots sector
- Self-sustaining submission pipeline (orgs requesting to be added)

### Track
- Website traffic (if analytics implemented)
- Feedback form submissions
- Submission requests
- Anecdotal stories of connections made
- Number of organizations that link back to the site

---

## Budget

### Year 1 Costs
- **Domain registration**: $15-20/year (calgarygroups.ca)
- **Hosting**: $0 (Netlify/Vercel free tier)
- **Tools**: $0 (all open-source)
- **Total**: $15-20

### Optional Costs
- **Custom email**: $0-6/month (can use Gmail or Zoho free tier)
- **Newsletter tool**: $0 (Mailchimp free tier for <500 subscribers)
- **Analytics**: $0-9/month (Plausible if desired, but optional)

**Funding**: Ko-fi donations, keep volunteer-run, apply for micro-grants if needed later

---

## Maintenance Plan

### Regular Tasks

**Weekly** (15-30 minutes):
- Check submission form
- Respond to feedback emails
- Quick scan for any site issues

**Monthly** (1-2 hours):
- Add 3-5 new organizations
- Update 3-5 existing listings
- Check for dead links
- Review filter tags (any new needed?)
- Pull updates from partner if they've made changes

**Quarterly** (2-3 hours):
- Comprehensive link check (all organizations)
- Review all categories/tags for relevance
- Analytics review (if implemented)
- Reach out to inactive orgs (still operating?)
- Content refresh on About page if needed

**Annually**:
- Domain renewal
- Full site audit
- Celebrate with community (anniversary post, stats)

---

## Outstanding Questions & Considerations

### Design Decisions (To Consider Later)
- [ ] Color palette (modern, accessible contrast)
- [ ] Typography choices (1-2 fonts, readability focus)
- [ ] Card design for organizations (photo/logo? icon?)
- [ ] Abstract shapes or geometric elements (how much? where?)
- [ ] Dark mode? (nice to have, not essential)
- [ ] Illustrations or keep minimal?

### Content Decisions
- [ ] Finalize exact wording of filter categories
- [ ] Decide on tone for About page (personal vs. formal)
- [ ] Icon system for types/interests? (visual or text-only badges)
- [ ] How to handle organizations that become inactive?
- [ ] Include larger nonprofits? (if so, add tag for "established nonprofit")

### Policy Questions (To Draft)
- [ ] Inclusion criteria (what makes org eligible?)
- [ ] Exclusion policy (what won't be listed?)
- [ ] Update/removal requests from organizations
- [ ] Data privacy statement (what info is collected/displayed)
- [ ] Moderation approach for submissions

### Future Considerations
- [ ] Arts Markets subdomain/separate site (revisit in 6-12 months)
- [ ] Partnership opportunities (volunteer centers, immigrant services)
- [ ] Micro-grant applications for funding (only if needed)
- [ ] Community surveys (what features do users want?)

---

## To-Do List (Priority Order)

### Immediate (This Week)
1. [ ] Register domain: calgarygroups.ca
2. [ ] Partner: Create GitHub repository and basic Astro setup
3. [ ] Content owner: Start compiling list of initial 20-30 organizations
4. [ ] Content owner: Draft About page content
5. [ ] Both: Agree on final filter categories/tags

### Short-Term (Next 2-4 Weeks)
6. [ ] Partner: Build core directory functionality
7. [ ] Partner: Implement filtering and search
8. [ ] Content owner: Add initial organizations as markdown files
9. [ ] Partner: Create submission form
10. [ ] Both: Design review and adjustments
11. [ ] Content owner: Set up Ko-fi
12. [ ] Partner: Set up GitHub Desktop on content owner's computer
13. [ ] Content owner: Learn markdown and git basics

### Pre-Launch (4-6 Weeks)
14. [ ] Partner: Complete all accessibility features
15. [ ] Partner: SEO optimization (meta tags, sitemap, schema)
16. [ ] Both: Full QA testing
17. [ ] Content owner: Reach out to initial organizations for accuracy check
18. [ ] Content owner: Draft launch announcement posts
19. [ ] Both: Soft launch to small group for feedback

### Launch (Week 6-8)
20. [ ] Go live!
21. [ ] Content owner: Launch promotion (social, Reddit, email)
22. [ ] Both: Monitor for bugs and feedback
23. [ ] Content owner: Begin regular maintenance routine

---

## Notes for Content Owner

### Your Role
You are the community connector and curator. Your passion for community engagement is what makes this work. You'll:
- Know which organizations to include
- Write welcoming, clear descriptions
- Respond to community feedback
- Share the site with relevant networks
- Keep information current

### Your Partner's Role
They handle the technical infrastructure and teach you the tools. They'll:
- Build the initial website
- Set up the workflow for you
- Fix bugs and add features
- Be available for technical questions
- Make updates you can't (rare, as needed)

### Staying True to Values
- This site is AI-free in operation
- It's built with open-source tools
- You own all the data
- It's transparent and community-focused
- It respects the privacy and values of leftist/activist groups

### When in Doubt
- Start small, grow gradually
- Quality over quantity
- Community feedback guides decisions
- It's okay to say no to feature creep
- Your voice and curation is the value-add

---

## Contact & Feedback During Development
- Use GitHub Issues for technical bugs/requests
- Regular check-ins between content owner and partner
- Community feedback via email (to be set up)
- Ko-fi for donations (optional support)