# Abhijit Deshpande — personal site

A personal technology lab and journal. Plain HTML, CSS and vanilla JavaScript: no build step, package manager, backend, cookies, tracking or third-party requests.

Live at: https://get2abhijit.github.io/abhijitdeshpande-website/

## Structure

```
index.html            Home
projects.html         Projects, each with status, why/how/where it stands
household-finance-tracker.html
                      Project page for the Household Finance Tracker (linked from projects.html)
notes.html            Field notes index (newest first)
notes/*.html          One page per note
notes/_template.html  Copy this to start a new note (unlisted, noindex)
notes/norway-denmark-2026.html, notes/statue-of-unity.html
                      Travel drafts (unlisted, noindex) — see "Publishing a draft"
now.html              Current focus — update the date when you edit it
about.html            Bio, photos, links, contact
404.html              Shown by GitHub Pages for unknown addresses
feed.xml              RSS feed of field notes
sitemap.xml           List of public pages for search engines
robots.txt            Points crawlers to the sitemap
assets/site.css       Shared design system and responsive styles
assets/site.js        Mobile menu and footer year
preview.py            Local preview that also shows draft notes (not needed on the public site)
assets/fonts/         Self-hosted fonts + SIL Open Font Licences
assets/images/        Photos (resized, metadata removed)
.nojekyll             Tells GitHub Pages to serve files as they are
```

Header, navigation and footer are repeated in every page. If you change one, change every page the same way. Pages inside `notes/` use `../` in front of every link and asset path.

## Preview locally

```bash
python -m http.server 8001
```

Open http://localhost:8001 and stop with `Ctrl + C`.

### Preview with drafts

```bash
python preview.py
```

Same idea, but drafts (any page in `notes/` with `<meta name="robots" content="noindex">`, such as the two travel pages) are added to the Field notes list and to "Recent writing" on the home page, and a small "Local preview" label appears in the corner. Nothing on disk changes, so the public site still hides them. It tries the next port if 8001 is busy and prints the address. `preview.py` is only for your computer; you don't need to upload it. To keep a draft off the public site entirely, don't upload its file. Python's server doesn't use `404.html` automatically; open `/404.html` directly to check it.

## Publish an update

Upload the changed files to the `main` branch of `get2abhijit/abhijitdeshpande-website` (or `git push`). GitHub Pages redeploys within a minute or two; the run is visible under the repository's **Actions** tab as "pages build and deployment".

## Adding a field note

1. Copy `notes/_template.html` to `notes/<short-name>.html` and follow the comment at the top.
2. Add a row at the top of the list in `notes.html` (copy an existing `<li class="note-row">`).
3. Add the same row to "Recent writing" on `index.html` (it shows the three newest).
4. Add an `<item>` at the top of `feed.xml` and a `<url>` line to `sitemap.xml`.

Substack essays are listed the same way, linking to the Substack URL instead of a local page (no sitemap entry needed).

## Publishing a travel draft

The two travel pages are layouts waiting for words and photos. They are not linked anywhere and carry `<meta name="robots" content="noindex">`.

1. Put photos in `assets/images/` (resized to about 1200 px wide, location data removed — exporting a copy from your photo app usually does both).
2. Replace each dashed box with a photo:
   `<figure class="photo"><img src="../assets/images/bergen-harbour.jpg" width="1200" height="900" alt="Describe the photo" loading="lazy"><figcaption>Caption</figcaption></figure>`
3. Replace highlighted text (`<mark>…</mark>`) and the italic prompts (`<p class="todo">…</p>`) with real text.
4. Delete the `<p class="draft-banner">…</p>` line and the robots `noindex` line.
5. Add the canonical/og:url lines (copy from another note and change the file name), then list it as in "Adding a field note".

## Updating a project

Each project in `projects.html` has: status label, one-sentence summary, a list of facts (Why / How / Where it stands …), technologies and links. Status labels: `status-live` (public and working) or `status-draft` with the text Prototype, In progress or Writing topic.

## Photos

To swap a photo, keep the file name or update `src`, `width` and `height`. Remove location metadata before adding new photos.

## Fonts and privacy

DM Sans, DM Mono and Playfair Display are served from `assets/fonts/` (Latin subset, WOFF2). No requests go to Google or any other third party.

## When the custom domain is bought (abhijitdeshpande.in)

1. Search and replace `https://get2abhijit.github.io/abhijitdeshpande-website/` with `https://abhijitdeshpande.in/` in every `.html` file, `feed.xml`, `sitemap.xml`, `robots.txt` and this README.
2. In the repository: **Settings → Pages → Custom domain**, enter `abhijitdeshpande.in` and save (GitHub adds a `CNAME` file).
3. At the registrar's DNS settings, add:
   - `A` records for `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `CNAME` record for `www` → `get2abhijit.github.io`
4. Wait for the DNS check to pass, then tick **Enforce HTTPS**.
5. Optional: set up an email address on the domain and add it to `about.html`.

`robots.txt` only takes effect at the root of a domain, so it starts working once the custom domain is live. Until then, the sitemap can be submitted directly in Google Search Console.
