# picoGIGA Lab homepage

Static site (HTML/CSS/JS, no build step) for the pico-to-GIGA Multiscale Simulation Research Group, KIST.

## Files

```
index.html  research.html  people.html  publications.html  news.html  contact.html
assets/js/data.js           ← members and news (edit by hand)
assets/js/publications.js   ← generated; do not edit
assets/js/projects.js       ← research projects (edit by hand; shown on the research page)
assets/js/main.js           layout, hero animation, page rendering
assets/css/style.css
assets/img/                 photos and figures
assets/video/hero.mp4       optional; replaces the hero animation if present
tools/sync_publications.py  Google Scholar + OpenAlex + KIPRIS → publications.js
tools/sync_config.json      Scholar ID, alumni names, KIPRIS search terms
tools/publication_overrides.json   manual corrections
tools/patents.json          master patent list (KR/US/PCT, one entry per invention)
tools/pi_roles.json         PI's first/corresponding roles from the KIST profile
tools/download_images.py    pulls images from the old Google Site
```

## Publications (automatic)

`tools/sync_publications.py` rebuilds the list:

1. **Google Scholar** profile → papers, US patents, preprints (entries without a venue count as preprints)
2. **Crossref / OpenAlex** → DOI, full author list, and corresponding-author flags where available
3. `patents.json` → all patents; Scholar's US copies and KIPRIS hits with the same title merge into it
4. `pi_roles.json` → the PI's first/co-first/corresponding role per paper (overrides public metadata)
5. **KIPRIS Plus** → Korean patents not yet in `patents.json` (needs an API key, see below)
6. `publication_overrides.json` → other fixes

**Research areas** are assigned automatically: every paper or patent a member co-authors gets that member's `areas` from `data.js` (set them when a member joins), and title keywords add application areas (CO₂, biomass, plastic). Per-paper exceptions go in `publication_overrides.json` → `topics`.

Lab members are bolded in author lists, and papers get "First author" / "Corresponding" badges when a lab member holds that role. Current members come from `data.js`; add alumni to `former_members` in `sync_config.json`.

OpenAlex does not know the corresponding author of every paper. Add missing ones to `publication_overrides.json`:

```json
"corresponding": [
  { "match": "sodium solid electrolytes", "authors": ["Kyeongsu Kim"] }
]
```

### Running it

- **By hand**: double-click `tools/sync.bat` (or `python tools/sync_publications.py`). New papers are listed at the end (also in `tools/cache/new_items.json`).
- **Automatically**: on GitHub, `.github/workflows/sync-publications.yml` runs every Monday and commits the new list. Google Scholar sometimes blocks GitHub's servers; the script then keeps the old list and the run shows as failed. Run it by hand in that case.

### Korean patents (KIPRIS)

1. Apply for the KIPRIS Plus Open API "특허·실용 공개·등록공보" service (plus.kipris.or.kr or data.go.kr) and get a service key.
2. Local: `set KIPRIS_API_KEY=발급키` before running. GitHub: Settings → Secrets → Actions → `KIPRIS_API_KEY`.
3. The search uses inventor `김경수` and applicant `한국과학기술연구원` (change in `sync_config.json`). Hide someone else's patent with `hide` in the overrides file.

## Members and news

Edit `assets/js/data.js`. Photos go in `assets/img/people/` and `assets/img/news/`; without a photo, initials are shown.

## Hero animation

The hero draws a continuous zoom: electrons → molecule on a catalyst → catalyst particle → reactor → chemical plant. To use a video instead (e.g. made with an AI video tool), save it as `assets/video/hero.mp4` (square, a few MB); it replaces the drawing automatically. Add `?zoom=2.5` to the URL to freeze the drawing at any point for checking.

## Images from the old site

KIST blocks `googleusercontent.com`, so run `python tools/download_images.py` from another network.

## Deploying

GitHub Pages (Settings → Pages → main branch), Netlify or Cloudflare Pages. For the domain, add a `CNAME` file with `www.picogigalab.com` and point DNS at the host.
