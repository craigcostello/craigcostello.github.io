# Review notes — 18 October 2026

## This revision

- Removed the extra cryptography/quantum/mathematics tagline. The research sentence
  now uses exactly the same role paragraph style as the QUT/MathQuEST introduction.
- LinkedIn replaces GitHub among the profile links, using Craig's verified QUT profile.
- Separated audio/video from written coverage, with independent searchable archives.
  The Public Sector Network interview includes both video and transcript; it is
  classified with video, not duplicated under written coverage.
- Expanded media and research-talk archives use the same thumbnail-card renderers
  as their highlights. Featured written coverage retains its compact publisher-logo
  treatment; other written items use original article previews or venue artwork.
- Restored all 42 papers to the exact sequence verified on Craig's live papers page.
  Removed year sorting entirely. Previously updated journal metadata from the CV
  remains, without moving those entries.
- Added QUT PhD 2008–2012, Mathematics Honours (First class) 2007 and Bachelor of
  Applied Science (Mathematics) 2005–2006 to Experience.
- Corrected IACR Communications in Cryptology to Editorial board member, 2026–ongoing.
  It is separate from the 20 program-committee entries and CANS 2026 chairing.
- Consolidated duplicate featured media records into the master media file; selected
  highlight IDs now live in `site.json`. Guided content commands and examples let
  future additions update the archive and highlights without layout edits.
- Added automatic validation and a downloadable review artifact for GitHub pushes/PRs.
  Publishing remains a separate manual workflow. Generated output is no longer a
  duplicate committed source tree.
- Tightened responsive grids, fluid heading sizes, narrow-screen wrapping and mobile
  tap targets; kept the profile role and research sentence styles identical.
- Recorded current public DNS and prepared the proposed cutover/rollback values.
  No external repository, hosting, DNS or subscription changes have been made.

## Preserved decisions

Karpathy-inspired compact typography, small tiles, no top navigation tabs, supplied
657B1299 headshot, QUT/MathQuEST role order and logos, teaching and supervision,
the CV's ten Microsoft intern names, service, and research-opportunities section
remain. The application text can be filled in later with Craig.

Supervision follows Craig's explicit spelling and roles, including Yintong Luo.
The older CV says Liu; that has not replaced Craig's instruction. Unverified
student homepages remain unlinked. No private research or full CV is public.

## Asset provenance and limits

Every research-talk entry now has a first-page thumbnail from its retained slide
PDF (72 entries, 71 distinct decks). Render validation discovered that the retained
2012 EiPSI deck was incomplete. A fresh public download is valid with 28 pages;
the repair log records both hashes and the incomplete bytes remain outside `public/`.
Original PDFs are not rewritten to create previews.

Featured written media uses downloaded outlet logos. Remaining articles use their
original preview images where available. Provider access failures are retained in
media metadata even where an alternative source succeeded. FIVEAA uses verified
series artwork from Apple Podcasts. The Microsoft webinar uses its actual opening
slide because YouTube's image endpoint did not return an image.

The Australian article is dated 18 August 2015 in the CV and remains the first
featured written piece. Its publisher blocks automated full-text access; the
original link remains. TED links to TED.com; its 2.3M+ plays label is a 13 October
snapshot, not a live counter.

The pairings tutorial uses the actual first page. The isogeny tutorial PDF on
ePrint returned HTTP 403, so its preview is the labelled opening slide of the
companion webinar, with the original ePrint link retained. SIDH's historical
security note remains.

The asset manifest covers local public files with sizes and SHA-256 checksums.
External destination availability is not guaranteed by a successful local build.

## Validation and remaining launch checks

Local build/content validation checks section order, unique anchors, local links,
all media categories/thumbnails, complete paper ordering, talk previews, profile,
education/service details and every public asset checksum. JavaScript syntax and
content-addition commands were checked in an isolated copy: new paper, featured
written media, a talk with slides, and rollback after a corrupt PDF. All passed.
All 71 public slide PDFs also passed PDF parser validation.

Browser visual QA remains outstanding: this managed environment has no supported
control-browser capability. No alternate browser was installed or used. Review
desktop/mobile layout and search/expansion before publication.

The repository is not yet accessible through the GitHub connection. See
`MIGRATION.md` for the single account setup step, staging publication and later
domain changes. Do not cancel Squarespace until replacement hosting and local
downloads have been reviewed on the actual domain.

## Browser review matrix

These are the remaining visual/interaction checks, not claimed device test results.

| Viewport | Expected layout | Review |
| --- | --- | --- |
| 320–360 px | Stacked profile; one talk/video tile per row; stacked timeline | Pending |
| 375–600 px | Two media tiles per row; one print item per row; stacked timeline | Pending |
| 768 px | Two media tiles per row; compact profile; two print columns | Pending |
| 1024–1440 px | Four media tiles per row; restrained content width | Pending |
| 200% zoom / keyboard | Readable wrapping; visible focus; working search and expansion | Pending |

Also check iOS Safari and Android Chrome, orientation changes, direct section
hash links, opening/closing each archive and searching for an empty result.
