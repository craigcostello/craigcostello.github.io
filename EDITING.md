# Adding papers, talks and media

Each item lives in one JSON record. Homepage highlights and expanded archives
render that same record. There is no CMS account or separate database to maintain.

## Guided additions

Run from the project directory:

```sh
python3 manage.py add paper
python3 manage.py add talk --slides /path/to/talk.pdf
python3 manage.py add media --image /path/to/image.jpg
```

Answer the title, authors/venue or event/date, year and original URL prompts.
For media, select `article`, `podcast`, `radio` or `video`. Articles go in In print;
the other formats go in Watch and listen. An interview page with a video and
transcript belongs in Watch and listen. Do not duplicate it under In print.

Add `--feature` to a media command to include it among homepage highlights.
The first four papers and first four talks feature automatically. Change those
counts or the selected media IDs in `content/site.json`.

For a talk, the command copies your PDF, assigns a stable asset filename, and
creates its first-page image. Install Poppler (`pdftoppm`) once when generating
new previews. Building and publishing existing content does not need Poppler.
Use your own episode/article image, a publisher-supplied preview, or an existing
publisher logo. Retain original image URLs as provenance when available.

## Copy an example instead of answering prompts

Copy an object from `content/templates/`, replace its example fields and save it
outside `content/`. Then run one of:

```sh
python3 manage.py add paper --from-json entry.json
python3 manage.py add talk --from-json entry.json --slides /path/to/talk.pdf
python3 manage.py add media --from-json entry.json --image /path/to/image.jpg --feature
```

IDs are assigned automatically and do not change if entries move. For additional
links, add objects with `text` and `original_url` to the entry's `links` array.
The template URLs and dates are examples only, never published content.

## Edit directly on GitHub

After repository setup, open the appropriate file in `content/`, use Edit, copy
an existing object and insert it first. Give it a unique ID; preserve JSON commas
and quotes. Existing IDs remain unchanged. Select media highlights in `site.json`.
For new media or talk images, upload the local assets too and update `assets.json`
using the command above. If a PDF needs a thumbnail, use the guided command or
ask ChatGPT to prepare the addition rather than hand-editing the checksum manifest.

The automated check on each commit catches broken local asset links, missing
thumbnails, mixed media categories, duplicate IDs and changed asset checksums.
It does not publish. Review the `website-preview` artifact from that check, then
run the separate Publish workflow when you want the update live. The preview
artifact is a downloadable build, not a hosted staging URL.

## Finish an update

```sh
python3 build.py
python3 check.py
git add .
git commit -m "Add new research and media"
git push
```

Review desktop/mobile layout and the new links in a browser. GitHub Actions can
validate and build the source; the manual publishing workflow deploys `dist/`.
Keep `public/` as the asset source. Never edit generated `dist/` files.
