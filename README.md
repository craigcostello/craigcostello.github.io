# Craig Costello academic website

Single-page academic website. Updated 18 October 2026.

Website: https://craigcostello.com.au/
GitHub Pages serves the custom domain; `craigcostello.github.io` redirects to it.
The `www` redirect is configured, with its certificate pending DNS propagation.
Squarespace remains active as a rollback option during the transition.

## Build and check

```sh
python3 build.py
python3 check.py
```

Python 3.10+ and its standard library are sufficient. Builds make no network
requests. The output is `dist/`, which is generated rather than committed.
For local browser review, serve it with `python3 -m http.server 8000 --directory dist`.
The build also writes the standalone `Craig-Costello-Website-Preview.html` beside
this project. That copy embeds images and links to original public documents;
`dist/` serves the retained PDFs locally.

## Add content

Use the guided commands; each adds one record at the beginning of the archive:

```sh
python3 manage.py add paper
python3 manage.py add talk --slides /path/to/new-talk.pdf
python3 manage.py add media --image /path/to/thumbnail.jpg --feature
python3 build.py
python3 check.py
```

Or use `--from-json entry.json` with an object based on `content/templates/`.
See `EDITING.md` for examples and the GitHub editor route. No layout code needs
to change when adding content. The full archives and their counts update together.

## Content and layout

- `content/papers.json`, `talks.json`, `media.json`: one record per item. Array
  order is display order. Do not sort by guessed dates. The existing 42 papers
  retain the exact order verified on Craig's live papers page on 18 October.
- `content/site.json`: homepage media highlight IDs and paper/talk highlight counts.
- `content/profile.json`, `career.json`, `people.json`, `service.json`: profile,
  employment/education, supervision/interns, chairing, editorial and PC service.
- `content/tutorials.json`, `branding.json`: tutorial previews and logo provenance.
- `content/assets.json`: public file size/SHA-256 manifest. Refresh with
  `python3 manage.py assets` after manual asset changes.
- `homepage.py`, `cards.py`, `build.py`: layout, shared highlight/archive cards,
  and static build. `src/` holds responsive styles and search/hash navigation.
- `assets.py`, `manage.py`: content additions and opening-slide thumbnail generation.

Audio/video and written coverage have separate searchable thumbnail archives.
Research talks have actual opening-slide thumbnails throughout their archive.
All sections remain on one scrolling page. Old `/media/`, `/papers/`, `/talks/`,
`/tutorials/` and `/home/` routes redirect to the corresponding sections. Original
same-domain `/s/` downloads are retained. `/homepage-v2` remains unresolved for
Craig's review.

## GitHub and launch

`check.yml` validates every push/PR and retains a review build. `pages.yml` builds,
checks and publishes the website on pushes to `main`; it can also be run manually.
Pages uses GitHub Actions as its publishing source, with `craigcostello.com.au`
configured in repository Pages settings. A CNAME file is not required by this
workflow. See `MIGRATION.md` for the domain configuration and rollback.

Private CV files are not public assets. The source package includes content and
public assets, plus acquisition repair evidence, without the private CV archive.
