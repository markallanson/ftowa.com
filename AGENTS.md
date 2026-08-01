# AGENTS.md — ftowa.com archive

Guidance for AI coding agents working in this repository. Read this before editing
anything — the repo is a **historical archive**, not an active codebase, and most
"obvious fixes" (renaming files, rewriting paths, deleting the CGI) would damage
its value.

## TL;DR

- This is a **read-only static archive** of a 2002–2006 car-club website. The goal
  is faithful preservation, not modernization.
- **No build, test, or lint tooling exists** and none should be added.
- Run locally with any static server rooted at the repo root (see [Run](#run)).
- The interactive features (membership, profiles, contact form) were **Perl CGI**
  and **do not run** on static hosting — by design. Do not try to "fix" their 404s.
- `cgi-bin/run.cgi` is a **remote command-execution backdoor** — see [Security](#security).

---

## Build / Test / Lint / Run

| Command | Value |
| --- | --- |
| Build | **None.** Pure static site; no framework, no bundler, no `package.json`. |
| Test | **None.** No test suite, no test runner. |
| Lint | **None.** No linters configured. |
| Run | Serve the **repo root** as the web root: `python3 -m http.server 8000` (then open <http://localhost:8000/>), or `npx serve .` |

**Do not** introduce a build pipeline. The HTML must ship exactly as authored.

---

## Repository layout (one line each)

- `index.html` — Landing page; news archive (2004–2006) with links to older archives.
- `html/` — Content sections: `workshop/` (11 DIY articles), `motorsport/`, `gallery/`, `events/`, plus `links.html`, `contact.html`, `calendar.html`, `join.html`, `members.html`, member templates, and scraped-news fragments.
- `html/index-archive-*.html` — Older news (July 2002–March 2003; April–Dec 2003).
- `css/mainStyle.css` — The single stylesheet (one rule). Everything else is inline `<font>`/`bgcolor`.
- `images/` — Site graphics, logos, workshop illustrations; subdirs `Gallery/`, `motorsport/`, `video/`, `gearshifterprob/`.
- `profiles/` — 13 member profile dirs, each with photos + a static HTML profile page.
- `forum/` — Archived phpBB as ~9,100 static HTML files (PHP URLs preserved in filenames), plus `templates/subSilver/` and `images/{avatars,smiles}`.
- `docs/` — Event flyers (`.doc`), service-parts spreadsheet (`.xls`); `docs/motorsport/` holds results `.zip`s.
- `pub/Ash.zip` — Public download, ~60 MB.
- `sound/raw_crank.wav` — Audio clip.
- `cgi-bin/` — Original Perl CGI source (non-functional on static hosts; see below).
- `404.shtml`, `500.shtml` — IIS error pages (ignored by static hosts).
- `web.config` — Legacy IIS config (PHP via FastCGI, default docs). Ignored by Vercel/static hosts.
- `WS_FTP.LOG` (scattered) — Original FTP upload logs; provenance only, safe to ignore.

### cgi-bin/ internals

- `processmembership.cgi` — Join form handler; validates input and appends a member record to a flat file.
- `memberlist.cgi` — Renders the member directory from the flat file.
- `showprofile.cgi` — Renders one member's profile from the flat file into `html/memberprofiletemplate.html`.
- `profileedit.cgi` — Edits a member record (password-gated).
- `fmail.cgi` — Generic form-to-mailer (`© 2002, Mark Allanson`, GPL); mails to `marke@iinet.net.au` via sendmail.
- `newsgrabber.cgi` — Scraped `autospeed.com` + an RSS feed into `html/ASNews.html` / `html/AutoNews.html` (those two HTML files are its *output*).
- `showpage.cgi` — Incomplete stub; almost entirely commented out.
- `run.cgi` — **Dangerous.** See [Security](#security).
- `ptHTML.pm` — Template engine: `displayHTML(file, %hash)` substitutes every `~token~` in a file with the matching hash value. This is why `html/*template.html` and `join.html` contain `~field~` placeholders.
- `ptDIO.pm` — Flat-file key/value `loadFile`/`saveFile` and a sendmail wrapper.
- `cgiecho`, `access_log`, `error_log` — server artifacts.

---

## Key conventions

- **Absolute web-root paths everywhere.** Links/images use `/css/…`, `/images/…`,
  `/html/…`, `/cgi-bin/…`. A static server **must** use the repo root as the web
  root or these break. (A few files use relative paths like `css/mainStyle.css` —
  both styles coexist; don't "normalize" them.)
- **Table-based layout, circa-2002 markup.** Heavy use of `<font>`, `bgcolor`,
  nested `<table>`s, `bordercolor`. This is intentional — leave it alone.
- **Character encoding is `iso-8859-1`** (declared in `<meta>`). Don't re-save as
  UTF-8 or you'll corrupt non-ASCII bytes.
- **Template placeholders.** HTML files containing `~something~` are CGI templates
  consumed by `ptHTML::displayHTML`. The `~token~` syntax is load-bearing.
- **Perl shebangs are Windows paths** (`#!C:\Perl\bin\perl.exe`) — except `run.cgi`
  and `showpage.cgi` which use `#!/usr/bin/perl`. None execute on static hosting.
- **Filename casing is mixed** (`MarkAllanson`, `Faye`, `FTO-R`, `Rosie`, etc.).
  Preserve it exactly when touching profile/forum paths.
- **The forum's filenames are literal URLs.** e.g.
  `viewtopic.php@t=582&start=15.html` — the `@` replaces `?` and `&` is literal.
  Don't rename them; the in-page links match these names.

---

## Gotchas

- **CGI endpoints 404 by design.** Navigation links to `/cgi-bin/*.cgi` will not
  resolve on static hosting. This is expected; do not "fix" it by rewriting links
  unless explicitly asked.
- **`web.config` and `*.shtml` are inert** on static hosts. Editing them changes
  nothing about how the site is served today.
- **`html/ASNews.html` / `html/AutoNews.html`** are *generated* fragments (output of
  `newsgrabber.cgi`), included into pages. They reference long-dead external sites.
- **Mixed line endings** are likely (Windows origin). Be careful with editors that
  silently rewrite CRLF↔LF — prefer targeted edits.
- **Large/binary assets** exist (`pub/Ash.zip` ~60 MB, forum videos). Avoid
  commands that load the whole tree into memory.
- **No `.gitignore`** — the original upload included logs, temp files
  (`html/TMP*.htm`, `html/events/TMP*.htm`), and FTP logs. Leave them; they're part
  of the snapshot.

---

## Security

- ⚠️ **`cgi-bin/run.cgi` is a remote command-execution backdoor.** It reads a
  `command` parameter and runs it via Perl `system()`, printing the output. It must
  **never** be deployed or served as executable CGI. On static hosting it's inert
  (just a text file), but flag it for any reviewer and never wire it up to a CGI
  runtime.
- External/off-site resources (e.g. the old `extreme-dm.com` tracker, scraped news
  sites) are dead links — expected for an archive of this age.

---

## Do / Don't

- ✅ **Do** preserve content verbatim. Spelling, layout, and "broken" legacy links
  are intentional artifacts.
- ✅ **Do** serve from the repo root so absolute paths resolve.
- ✅ **Do** verify any path/encoding claim against the actual file before relying
  on it — the tree is large and inconsistent.
- ❌ **Don't** add a build step, bundler, framework, or test runner.
- ❌ **Don't** rewrite the table/`<font>` markup to modern HTML/CSS.
- ❌ **Don't** re-encode files as UTF-8 (charset is iso-8859-1).
- ❌ **Don't** rename forum/profile files or "normalize" their casing.
- ❌ **Don't** enable `cgi-bin/*.cgi` execution on any host without first removing
  `run.cgi`.
- ❌ **Don't** commit changes without human review — this repo's convention is that
  every change is reviewed before commit.

---

## Where important things live

- **Site entry point:** `index.html`
- **All readable content:** `html/**` (esp. `html/workshop/`, `html/events/`, `html/gallery/`)
- **Forum archive:** `forum/viewtopic.php@*.html`, `forum/viewforum.php@*.html`, `forum/memberlist.php@*.html`
- **Member photos/pages:** `profiles/<Username>/`
- **The membership logic (read-only reference):** `cgi-bin/processmembership.cgi`, `showprofile.cgi`, `memberlist.cgi`, `profileedit.cgi`
- **Template engine + DB layer:** `cgi-bin/ptHTML.pm`, `cgi-bin/ptDIO.pm`
