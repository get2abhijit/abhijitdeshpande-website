# Abhijit Deshpande — personal site

A personal technology lab and journal. Plain HTML, CSS and vanilla JavaScript: no build step, package manager, backend, cookies, tracking or third-party requests.

Live at: https://get2abhijit.github.io/abhijitdeshpande-website/

## Structure

```
index.html                Home
projects.html             Projects list (status, one-line summary)
projects/*.html           One page per project: why / how / where it stands
household-finance-tracker.html
                          Project page for the Household Finance Tracker (kept at its original address)
notes.html                Notes list, grouped: Travel, Cricket and family, Engineering
notes/*.html              One page per note
notes/_template.html      Copy this to start a new note (unlisted, noindex)
notes/norway-denmark-2026.html, notes/statue-of-unity.html
                          Travel drafts (unlisted, noindex): see "Publishing a draft"
now.html                  Current focus: update the date when you edit it
about.html                Bio, photos, links, contact
404.html                  Shown by GitHub Pages for unknown addresses (works at any depth)
feed.xml                  RSS feed of notes
sitemap.xml               Public pages for search engines
robots.txt                Points crawlers to the sitemap
assets/site.css           Design system: colours, layout, light and dark theme
assets/site.js            Mobile menu, sidebar sub-menu, "On this page", previous/next, back link
assets/site-map.js        THE list of projects and notes used for navigation (see below)
assets/favicon.svg        Logo ("ad" with a bat as the d); favicon-32.png and apple-touch-icon.png are exports of it
assets/fonts/             Self-hosted fonts + SIL Open Font Licences
assets/images/            Photos (resized, metadata removed); travel/ holds the trip photos
preview.py                Local preview that also shows drafts (not needed on the public site)
tools/check_site.py       Checks links, images, navigation and placeholders before you upload
.nojekyll                 Tells GitHub Pages to serve files as they are
```

### How navigation works

Every page has the same sidebar (photo, Home / Projects / Notes / Now / About, links) written directly in its HTML, plus a breadcrumb and, on phones, a menu button that opens the sidebar as a drawer. Those parts work without JavaScript.

Three things are added by `assets/site.js` from the one list in `assets/site-map.js`: the sidebar sub-menu under Projects or Notes, the "Previous / Next" links at the end of a page, and the "← Back to …" label. Articles with three or more `<h2>` headings also get an "On this page" menu automatically. So adding a note or project means adding one line to `site-map.js` (and a row to the list page), not editing every page.

If you change the sidebar markup itself (for example a new top-level page), change it identically in every page; `tools/check_site.py` tells you if one differs.

## Preview locally

```bash
python -m http.server 8001
```

Open http://localhost:8001 and stop with `Ctrl + C`.

### Preview with drafts

```bash
python preview.py
```

Same idea, but drafts (any page in `notes/` with `<meta name="robots" content="noindex">`, such as the two travel pages) are added to the Notes list, to "Recent writing" on the home page, to the sidebar and to previous/next links, and a small "Local preview" label appears in the corner. Nothing on disk changes, so the public site still hides them. It tries the next port if 8001 is busy and prints the address. To keep a draft off the public site entirely, don't upload its file. Python's plain server doesn't use `404.html`; open `/404.html` directly to check it.

## Check before you upload

```bash
python tools/check_site.py
```

It reports broken links and anchors, missing images or alt text, pages without a title, description or single heading, a sidebar that differs between pages, notes or projects missing from `site-map.js`, the list pages or `sitemap.xml`, drafts that leaked into public lists, and leftover placeholders such as highlighted text. Fix every `ERROR` before uploading.

## Publish an update

Upload the changed files to the `main` branch of `get2abhijit/abhijitdeshpande-website` (or `git push`). GitHub Pages redeploys within a minute or two; the run is visible under the repository's **Actions** tab as "pages build and deployment".

## Adding a field note

1. Copy `notes/_template.html` to `notes/<short-name>.html` and follow the comment at the top. In `<head>`, delete the robots `noindex` and `note-group` lines, and add the canonical and og:url lines (copy them from another note and change the file name).
2. Add a line for it, newest first within its group, to `notes` in `assets/site-map.js`. Groups are `travel`, `cricket-family` and `engineering`.
3. Add a row at the top of its group in `notes.html` (copy an existing `<li class="row note-row">`). If a group was hidden because it was empty, remove its `hidden` attribute.
4. Add the same row to "Recent writing" on `index.html` (it shows the three newest).
5. Add an `<item>` at the top of `feed.xml` and a `<url>` line to `sitemap.xml`.
6. Run `python tools/check_site.py`.

Substack essays are listed the same way, but with `ext: '<Substack URL>'` instead of `href` in `site-map.js` and a link to the Substack URL in the row (no sitemap entry needed).

## Publishing a draft (the travel notes)

The two travel pages are real drafts: they have text and photos, but also highlighted placeholders. They are not linked anywhere and carry `<meta name="robots" content="noindex">`.

1. Replace every highlighted passage (`<mark>…</mark>`) and italic prompt (`<p class="todo">…</p>`) with real text, and check each photo caption.
2. Delete the `<p class="draft-banner">…</p>` paragraph and the robots `noindex` and `note-group` lines.
3. Add the canonical and og:url lines, then list it as in "Adding a field note". The Travel group in `notes.html` is hidden while empty: remove its `hidden` attribute.
4. Run `python tools/check_site.py`. It refuses pages that still contain highlighting.

Before publishing, also check the things the draft deliberately leaves out: booking references and links, the apartment's street address, any Strava or map link, prices and receipts.

## Adding or updating a project

A new project needs `projects/<name>.html` (copy an existing one), a line in `projects` in `assets/site-map.js`, a row in `projects.html` and a `<url>` in `sitemap.xml`. Status labels: `status-live` (public and working) or `status-draft` with the text Prototype, In progress or Writing topic. Don't describe a concept as a finished product.

Old addresses like `projects.html#cricketiq` still work: a few lines in `site.js` forward them to the new project pages.

## Photos and privacy

- Resize photos to about 1000–1200 px wide and remove location data; exporting a copy from your photo app usually does both. Keep each file under about 400 KB (the checker warns above that).
- **Your daughter's face is covered with a small smiley in every published photo.** The smiley is part of the image file, so it cannot be removed by saving the picture. Do this before adding any new photo of her.
- Keep out of public pages: booking references, street addresses, prices and receipts, other people's names or faces without their agreement, and anything confidential from your employer.

## Design

Colours, fonts and spacing are variables at the top of `assets/site.css`. The site follows the visitor's light or dark setting. The logo is `assets/favicon.svg`; to change it, replace that file and re-export `favicon-32.png` (32×32) and `apple-touch-icon.png` (180×180, full-bleed square).

## Fonts and privacy

DM Sans, DM Mono and Playfair Display are served from `assets/fonts/` (Latin subset, WOFF2). No requests go to Google or any other third party.

## When the custom domain is bought (abhijitdeshpande.in)

1. Search and replace `https://get2abhijit.github.io/abhijitdeshpande-website/` with `https://abhijitdeshpande.in/` in every `.html` file, `feed.xml`, `sitemap.xml`, `robots.txt` and this README. (`404.html` and the other pages use relative paths and need nothing else.)
2. In the repository: **Settings → Pages → Custom domain**, enter `abhijitdeshpande.in` and save (GitHub adds a `CNAME` file).
3. At the registrar's DNS settings, add:
   - `A` records for `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` record for `www` → `get2abhijit.github.io`
4. Wait for the DNS check to pass, then tick **Enforce HTTPS**.
5. Optional: set up an email address on the domain and add it to `about.html`.

`robots.txt` only takes effect at the root of a domain, so it starts working once the custom domain is live. Until then, the sitemap can be submitted directly in Google Search Console.
