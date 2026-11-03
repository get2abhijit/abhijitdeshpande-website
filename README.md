# Abhijit Deshpande — personal site

A personal technology lab and independent engineering journal. Plain HTML, CSS and vanilla JavaScript: no build step, package manager, backend, tracking or third-party requests.

## Structure

```
index.html        Home — introduction, selected projects, recent notes
projects.html     Projects and experiments, with status
notes.html        Field notes index (newest first)
notes/*.html      One page per note
notes/_template.html  Copy this to start a new note (not linked, not indexed)
now.html          Current focus (update the date when you edit it)
about.html        Background, links and contact
404.html          Shown by GitHub Pages for unknown addresses
assets/site.css   Shared design system and responsive styles
assets/site.js    Mobile menu and footer year
assets/fonts/     Self-hosted fonts + their SIL Open Font Licences
assets/favicon.svg, assets/apple-touch-icon.png
.nojekyll         Tells GitHub Pages to serve files as they are
```

Header, navigation and footer are repeated in every page. If you change one, change every page the same way. Pages inside `notes/` use `../` in front of every link and asset path.

## Preview locally

From this folder:

```bash
python -m http.server 8001
```

Then open http://localhost:8001. Stop the server with `Ctrl + C`.
Note: Python's server does not use `404.html` for missing pages; open http://localhost:8001/404.html directly to check it.

## Publish with GitHub Pages

1. Create a public repository named `abhijitdeshpande-site`.
2. Upload the *contents* of this folder (not the folder itself), including `.nojekyll`.
3. **Settings → Pages → Build and deployment → Deploy from a branch**, select `main` and `/ (root)`, Save.
4. After a minute or two the site is at `https://get2abhijit.github.io/abhijitdeshpande-site/`.

All links are relative, so the same files also work on a custom domain later.

## Fonts and privacy

DM Sans, DM Mono and Playfair Display are served from `assets/fonts/` (subset to Latin, WOFF2). The site makes no requests to Google or any other third party, which avoids the GDPR issue with remotely loaded Google Fonts. System fonts are used as fallbacks.

## Updating the Now page

Edit the four items in `now.html` and change the `LAST UPDATED` line, including the `datetime` attribute (e.g. `2027-02`).

## Adding a field note

1. Copy `notes/_template.html` to `notes/<short-name>.html` and follow the comment at the top of the file.
2. Add a row for it at the top of the list in `notes.html` (copy an existing `<li class="note-row">`).
3. Optionally add the same row to "Recent writing" on `index.html`, which shows the three newest entries.

Essays published on Substack can be listed the same way, linking to the Substack URL instead of a local page.

## Updating a project

Each project in `projects.html` has the same parts: status label, one-sentence summary, a short list of facts (Why / How / Where it stands …), technologies and links. Status labels:

- `status-live` — public and working
- `status-draft` with the text Prototype, In progress or Writing topic
