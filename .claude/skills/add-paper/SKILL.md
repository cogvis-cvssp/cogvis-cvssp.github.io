---
name: add-paper
description: Add or update a paper on the CogVis site. Creates the project page under papers/<slug>/ and the matching entry in publications.html, or updates an existing paper (e.g. arXiv -> accepted at a venue, new code link). Use whenever someone wants to add, publish, or change a paper, project page, or publication link.
---

# Add or update a paper

The site is static HTML. `publications.html` and every paper page are hand-written,
so this skill keeps the page and the list entry in step. Never leave an `href="#"`
on a button (see "Missing links").

## 1. Gather details (ask for anything missing)

- Title, authors (mark group members in `<strong>`, as the existing entries do), venue + year
- arXiv ID; DOI or publisher URL if published; code repo URL if released
- slug for the folder, e.g. `signbind` -> `papers/signbind/`
- teaser figure (goes in `papers/<slug>/assets/`), abstract, BibTeX
- Whether the paper is also in the SignGPT sheet (see step 5)

For an update, edit the existing page and entry instead of creating new ones.

## 2. Project page: `papers/<slug>/index.html`

- Start from `papers/m3t/index.html` (complete, current style). Copy its `<head>`,
  CSS and JS unchanged, and replace the content sections with the new paper's.
  Drop sections the paper has no content for rather than leaving placeholders.
- Set `og:url` to `https://cogvis-cvssp.github.io/papers/<slug>/`
  (domain is `cogvis-cvssp.github.io`, not `cogvis.github.io`), plus `<title>`,
  `og:title`, and both descriptions.
- Button row, in this order, using the same markup as M3T:
  - **Paper**: `https://arxiv.org/pdf/<id>` (or the DOI/publisher link once published)
  - **arXiv**: `https://arxiv.org/abs/<id>`
  - **Code**: the repo URL, or `Code (Coming Soon)` with `href="#"` if unreleased
  - Add extras (Poster, Video) only if they exist.
- Put images in `papers/<slug>/assets/`, referenced relatively.

## 3. List entry in `publications.html`

- Add a `pub-item` inside the `year-block` for the paper's **venue year**
  (a paper accepted at ECCV 2026 goes under 2026, even if the arXiv preprint is older).
  Order within a year: match the neighbouring entries (venue papers before preprints).
- Copy the markup of a neighbour with a Page button (e.g. SignRefine). Fields:
  authors, `<span class="venue venue-...">VENUE YEAR</span>` (classes are in `css/style.css`),
  and `pub-links` with **Page** (`papers/<slug>/`, globe icon) then **arXiv**/**Paper**/**Code**.
- Every paper with a project page must have the Page button, and every Page button
  must point at an existing folder.
- When a paper's status changes (preprint -> accepted), update the venue tag,
  the year block, and the links in the same edit.

## 4. Verify

Run `python3 scripts/check_publications.py` and fix anything it reports for your
paper. Preview with `python3 -m http.server` and open `/publications.html` and the
new page; click every button.

## 5. SignGPT

`signgpt/publications.html` is generated from the SignGPT Google Sheet by
`scripts/update_signgpt_publications.py` (daily GitHub Action). Never edit its
generated block by hand. If the paper belongs to SignGPT, tell the user to add or
update its row in the sheet (Paper URL / arXiv URL / Code URL columns; Code URL
must be a real repo, not the project page).

## Missing links

If a link is not known, ask for it. Don't guess a URL and don't invent an arXiv ID.
Use `Code (Coming Soon)` for unreleased code; for other missing links, omit the button.

## Git

Commit locally with a clear message. Do not push to master until the user says so.
