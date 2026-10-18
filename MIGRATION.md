# GitHub Pages launch plan

Updated 18 October 2026. Source is imported into
`craigcostello/craigcostello.github.io`. GitHub Pages builds the independent preview
at https://craigcostello.github.io/ from `main`. Squarespace, custom-domain DNS,
and subscriptions remain unchanged. There is no CNAME file or Pages custom domain.

## Repository and transfer

The public repository already exists under `craigcostello`. Source and retained
public assets were extracted from the source archive and transferred using Git,
preserving the repository's initial commit. The archive itself and generated
`dist/` are not committed. Do not place the private CV, credentials or uploads in it.

## Import and validate

The ZIP contains the project source and retained public assets, without generated
`dist/` or local git history. Import all source files, including `.github/` and
`.gitignore`. For an empty repository, a local checkout can use:

```sh
git init -b main
git add .
git commit -m "Prepare Craig Costello academic website"
git remote add origin https://github.com/craigcostello/craigcostello.github.io.git
git push -u origin main
```

If importing from this existing local checkout, skip `git init` and the initial
commit; add the remote and push the prepared `main` branch. Once the connected
repository is visible, ChatGPT can perform the source import with the available
repository tools. Authentication should use GitHub's normal UI/credential flow,
not credentials pasted into chat.

`Check website changes` builds and validates pushes/PRs and retains a downloadable
review artifact. `Publish website preview to GitHub Pages` builds the exact
committed source, checks it, and deploys `dist/` on pushes to `main` or manual runs.
Pages uses GitHub Actions as the publishing source. Review https://craigcostello.github.io/
before the domain switch. Confirm mobile/desktop layout, search, section expansion,
the headshot and all local downloads, including legacy `/s/` links.

## Current public DNS snapshot

The read-only snapshot in `content/dns-before-migration.json` was fetched on
18 October 2026. Re-query immediately before any cutover; these are observations,
not a complete authenticated DNS-zone export.

| Name | Type | Observed value |
| --- | --- | --- |
| `@` | A | `198.185.159.145`, `198.49.23.145`, `198.49.23.144`, `198.185.159.144` |
| `www` | CNAME | `ext-cust.squarespace.com.` |
| domain | NS | `ns1.netregistry.net.`, `ns2.netregistry.net.`, `ns3.netregistry.net.` |
| `@` | AAAA, MX, TXT | No answer in this resolver snapshot |

The nameservers indicate Netregistry DNS delegation. They do not establish who
currently bills the domain or which account administers it. Confirm registrar,
DNS-login access, renewal and any email/subdomain dependencies. No public MX/TXT
answer is not proof that no related service exists; preserve the authenticated zone.

## Proposed domain switch — prepared, not applied

Use `www.craigcostello.com.au` as the preferred name, retaining the existing domain.
A registrar transfer is optional; changing website hosting does not require one.

1. Save the full DNS-zone export and verify domain renewal will continue.
2. Verify domain ownership in GitHub using the TXT record GitHub supplies. Its
   account-specific token cannot be prepared without the account UI.
3. Add `www.craigcostello.com.au` in repository Settings → Pages before changing
   its traffic-routing DNS. With a custom Actions publishing workflow, GitHub
   does not require a repository CNAME file.
4. Replace only the apex website A records and `www` CNAME as below, following
   GitHub's current official documentation. Keep nameservers, mail, verification
   and unrelated records. Reconcile any conflicting website AAAA records if present.
5. Verify `www` and apex, GitHub's domain check, certificate issuance and Enforce
   HTTPS. DNS propagation/certificate readiness can take time; do not cancel
   Squarespace during this check.

| Name | Type | Proposed GitHub Pages value |
| --- | --- | --- |
| `@` | A | `185.199.108.153` |
| `@` | A | `185.199.109.153` |
| `@` | A | `185.199.110.153` |
| `@` | A | `185.199.111.153` |
| `www` | CNAME | `craigcostello.github.io.` |

These targets were checked against GitHub's documentation on 18 October 2026.
Optional IPv6 can follow GitHub's documented AAAA values if wanted; it is not
required for the initial switch. Do not copy old Squarespace website IPs alongside
GitHub's new addresses.

## Rollback and cancellation

If the new host fails, restore the website A records and `www` CNAME from the
fresh pre-cutover export, then re-check Squarespace. The table above is a dated
reference; the account export at cutover is the rollback authority.

After the new domain and downloads are working, cancel only the Squarespace
website subscription. Keep domain registration and renewal active. If the domain
is registered through Squarespace, it can remain there separately from the website.
Confirm any annual term/refund details in the actual account before cancelling.

## Link retention

The six main historical routes have redirects or content. Same-domain `/s/`
downloads remain local. Squarespace-owned `static1.squarespace.com` URLs cannot
be redirected with Craig's DNS; external bookmarks to them may eventually fail.
The new site uses the retained local copies. One old PDF was re-downloaded after
render validation found it incomplete; `content/asset-repairs.json` records both
checksums and the original incomplete bytes remain as migration evidence outside the website asset directory.

## Official references, checked 18 October 2026

- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- https://support.squarespace.com/hc/en-us/articles/205845348-What-to-do-with-your-domain-if-you-cancel-your-website
