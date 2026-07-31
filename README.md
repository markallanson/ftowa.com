# FTO Drivers Club — Western Australia (ftowa.com)

A **read-only static archive** of the FTO Drivers Club – Western Australia website, a
Perth-based car club for Mitsubishi FTO owners, active roughly **2002–2006**. The
site featured news, event/cruise write-ups, photo galleries, technical "workshop"
articles, motorsport results, a phpBB forum, and a member-profile system.

This repository preserves the original hand-built site exactly as it ran, and hosts
it statically (it was migrated off its original Windows/IIS host to static hosting).

> **Heads-up:** This is an archive, not a live site. See [What works vs. what is
> broken](#what-works-vs-what-is-broken) — the interactive membership/forum features
> do **not** function on static hosting.

The archive is hosted at **[https://ftowa.allanson.org](https://ftowa.allanson.org)**.

---

## What / Why

- **What:** The complete content of `www.ftowa.com` as it existed in the mid-2000s —
  every HTML page, image, gallery, the full phpBB forum dump, member profile photos,
  downloadable documents, and the original Perl CGI source that powered membership.
- **Why:** Historical preservation. The site documents a real enthusiast community,
  its events, and a body of FTO-specific technical writing that is otherwise lost.
- The repository is essentially a **single snapshot**: the git history contains one
  commit (`Move to vercel`) that relocated the files to this repository for static
  hosting. No build step is applied to the original content.

The original site was authored by **Mark Allanson** (`marke@iinet.net.au`,
`mark@ftowa.com`); the footer reads *"(c) 2002, All Rights Reserved"* and the
form-mail script `cgi-bin/fmail.cgi` is explicitly marked *"© 2002, Mark Allanson"*.

### Provenance

Leftover `WS_FTP.LOG` files across the tree record the original upload workflow —
files were authored under `C:\ftowa\…` on Windows and pushed via FTP to the
`/public_html/` web root. The `web.config` confirms hosting on **Microsoft IIS**
with **PHP 5 via FastCGI** and the **Perl CGI** scripts run from `cgi-bin/`. This
Windows origin explains the `C:\Perl\bin\perl.exe` shebangs in the CGI files.

---

## What works vs. what is broken

This is the single most important thing to know about the archive.

| Area | Status on static hosting | Notes |
| --- | --- | --- |
| Static HTML pages, CSS, images | ✅ **Works** | The bulk of the site content. |
| Photo galleries, workshop articles | ✅ **Works** | |
| Event write-ups, links, calendar | ✅ **Works** | |
| Archived phpBB forum (`forum/`) | ✅ **Works (read-only)** | ~9,100 pre-rendered topic pages. Links between topics resolve, but you cannot log in or post. |
| Member profile pages (`profiles/`) | ✅ **Works** | Each is a static HTML page + photos. |
| Downloads (`docs/`, `pub/`, `sound/`) | ✅ **Works** | Word/Excel docs, zips, video, audio. |
| **Join** (`/cgi-bin/processmembership.cgi`) | ❌ **Broken** | No CGI runtime on static hosts → 404. |
| **Member list** (`/cgi-bin/memberlist.cgi`) | ❌ **Broken** | Same. |
| **View/edit profile** (`/cgi-bin/showprofile.cgi`, `profileedit.cgi`) | ❌ **Broken** | Same. |
| **Contact form** (`/cgi-bin/fmail.cgi`) | ❌ **Broken** | Same. |
| **News scraper** (`cgi-bin/newsgrabber.cgi`) | ❌ **Broken / obsolete** | Scraped live third-party sites that no longer exist. |
| Any `web.config` / IIS behaviour | ⛔ **Ignored** | Windows/IIS-only; irrelevant to static hosts. |

Navigation links pointing at `/cgi-bin/*.cgi` will return 404 on static hosting.
The affected buttons are: *Join*, *Members* (the CGI one), and the in-page *edit
profile* links. This is expected for an archive.

---

## Repository layout

```
.
├── index.html              # Landing page + news archive (2004–2006), links to older archives
├── 404.shtml, 500.shtml    # IIS custom error pages (ignored on static hosts)
├── web.config              # Legacy IIS config (Windows hosting) — not used by static hosts
├── css/mainStyle.css       # The (one-line) site stylesheet
├── html/                   # Content sections
│   ├── workshop/           # 11 technical "Workshop" articles (DIY, cambelt, dyno, etc.)
│   ├── motorsport/         # Motorsport / Wanneroo track content
│   ├── gallery/            # Gallery index pages (Auto Salon 2002, JoJo's 2003, Calendar 2004)
│   ├── events/             # Event write-ups (Dwellingup, Yanchep, Swan Valley, MCM cruises…)
│   ├── gallery.html, workshop.html, links.html, contact.html, calendar.html
│   ├── join.html, joinThanks.html, members.html, messageboard.html, feature.html
│   ├── memberlisttemplate.html, memberprofiletemplate.html, memberdetailsedit.html
│   ├── index-archive-*.html# Older news (July 2002–March 2003, April–Dec 2003)
│   └── ASNews.html, AutoNews.html  # Scraped news fragments written by newsgrabber.cgi
├── images/                 # Site graphics, logos, gallery images, workshop illustrations
│   ├── Gallery/            # Photo galleries (AutoSalon2002, Cal2004, Jojo2003, MC28062003…)
│   ├── motorsport/, video/ # Track photos + video (mcmotorsport1.avi, PA190147.MOV)
│   └── gearshifterprob/    # Gallery tied to a workshop article
├── profiles/               # 13 member profile dirs (photos + a static HTML page each)
├── forum/                  # Archived phpBB forum as ~9,100 static HTML files
│   ├── viewforum.php@*.html, viewtopic.php@*.html, memberlist.php@*.html, …
│   ├── templates/subSilver # Original phpBB template
│   └── images/{avatars,smiles}
├── docs/                   # Club documents: event flyers (.doc), service-parts spreadsheet (.xls)
│   └── motorsport/         # MC motorsport results as .zip archives (2004–2005)
├── pub/Ash.zip             # Public download (large: ~60 MB)
├── sound/raw_crank.wav     # Engine-crank audio clip
└── cgi-bin/                # Original Perl CGI (see below) — does NOT run on static hosts
    ├── processmembership.cgi, memberlist.cgi, showprofile.cgi, profileedit.cgi
    ├── fmail.cgi           # Generic form-mailer (© 2002 Mark Allanson, GPL)
    ├── newsgrabber.cgi     # Scraped autospeed.com / autosinfo.com news feeds
    ├── showpage.cgi        # Incomplete stub (mostly commented out)
    ├── run.cgi             # ⚠️ Dangerous remote command-execution script (see AGENTS.md)
    ├── ptHTML.pm           # Tiny template engine: replaces ~token~ placeholders in HTML
    ├── ptDIO.pm            # Flat-file load/save + sendmail wrapper
    ├── members             # Flat-file member "database" (see below)
    ├── cgiecho             # Third-party CGI echo utility
    └── access_log, error_log  # Original server logs
```

### About `cgi-bin/`

The interactive features of the original site were plain Perl CGI. The source is
kept here for completeness, but it **cannot run on static hosting** (Vercel and
similar have no Perl/CGI runtime), and the scripts use Windows Perl shebangs
(`#!C:\Perl\bin\perl.exe`) that wouldn't execute on Unix even if a runtime existed.

### The `members` flat-file "database"

`cgi-bin/members` is a plain-text key/value store (`key=value`, one per line). A
member record is keyed by nickname, with fields stored as suffixed keys, e.g.
`MarkAllansonname=…`, `MarkAllansonemail=…`, `MarkAllansmods=…` (newlines within a
multi-line field are encoded as `~`). The presence of an entry `nickname=1` marks a
valid member.

> ⚠️ **Be aware:** This file is heavily polluted with **spam sign-ups** (thousands
> of "Adult Webcam" entries) and historically stored **plaintext passwords** and
> **email addresses**. Treat it as sensitive historical data — do not assume the
> contact details in it are legitimate or that passwords were ever secured.

---

## Previewing locally

There is no build step — the site is plain static files. Serve the repository root
as the web root so the absolute paths (`/css/…`, `/images/…`, `/html/…`) resolve:

```bash
# Option A — Python (no install needed on most systems)
python3 -m http.server 8000

# Option B — Node
npx serve .

# Option C — any static file server, pointed at this directory
```

Then open <http://localhost:8000/>.

> Note: links that hit `/cgi-bin/*.cgi` will still 404 locally — this matches the
> behaviour described above and is expected.

## Deploying

The intended target is **static hosting** (the `Move to vercel` commit targeted
Vercel). Because the site is a flat set of files with no framework:

1. Set the **publish/output directory** to the **repository root** (not a `dist/`
   or `public/` subfolder).
2. No build command is required — every file ships as-is.
3. (Optional) If you want clean URLs or redirects for the legacy `/cgi-bin/*`
   links, add a `vercel.json` / host equivalent. None is included here.

---

## License & attribution

- The site content is marked **"(c) 2002, All Rights Reserved"** by the original
  author, Mark Allanson. It is preserved here as a historical archive; no new
  copyright claim is made over the original material.
- `cgi-bin/fmail.cgi` is released by its author under the **GPL** (per its header).
- The forum was powered by **phpBB** (GPL) using the **subSilver** template; both
  are preserved as static archives.
- No `LICENSE` file is present in the repository.
