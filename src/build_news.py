#!/usr/bin/env python3
from __future__ import annotations
import os, json, re, html, hashlib
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen
import feedparser

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ARCHIVE = DOCS / "archive"
SOURCES = ROOT / "sources.json"

def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s or "")
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()

def fetch_items():
    cfg = json.loads(SOURCES.read_text(encoding="utf-8"))
    cutoff = datetime.now(timezone.utc) - timedelta(hours=cfg.get("lookback_hours", 30))
    items, seen = [], set()
    for feed_cfg in cfg["feeds"]:
        feed = feedparser.parse(feed_cfg["url"])
        for e in feed.entries[:cfg.get("max_items_per_feed", 8)]:
            link = getattr(e, "link", "").strip()
            title = strip_tags(getattr(e, "title", ""))
            if not link or not title:
                continue
            published = None
            st = getattr(e, "published_parsed", None) or getattr(e, "updated_parsed", None)
            if st:
                try:
                    published = datetime(*st[:6], tzinfo=timezone.utc)
                except Exception:
                    published = None
            if published and published < cutoff:
                continue
            key = hashlib.sha1((title.lower() + "|" + link).encode()).hexdigest()
            if key in seen:
                continue
            seen.add(key)
            summary = strip_tags(getattr(e, "summary", "") or getattr(e, "description", ""))
            if len(summary) > 500:
                summary = summary[:497] + "..."
            items.append({
                "source": feed_cfg["name"], "title": title, "link": link,
                "summary": summary, "published": published.isoformat() if published else ""
            })
    items.sort(key=lambda x: x["published"] or "", reverse=True)
    return items[:cfg.get("max_total_items", 35)]

def call_deepseek(items):
    api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        return None
    compact = [{"source":x["source"],"title":x["title"],"url":x["link"],"summary":x["summary"]} for x in items]
    prompt = f"""Sei il curatore di una rassegna quotidiana italiana chiamata "Tech News Daily".
Usa esclusivamente le notizie fornite qui sotto.

Obiettivi:
- seleziona circa 12-18 notizie realmente rilevanti;
- privilegia AI, software, Linux/open source, sviluppo, hardware, sicurezza e nuovi strumenti;
- scrivi in italiano;
- non inventare dettagli non presenti;
- per ogni voce: titolo breve, 1-3 frasi di spiegazione, fonte e URL originale;
- apri con una sezione "In breve" di 5 punti;
- usa Markdown pulito;
- niente introduzioni generiche.

NOTIZIE:
{json.dumps(compact, ensure_ascii=False)}"""
    body = json.dumps({
        "model":"deepseek-chat",
        "messages":[
            {"role":"system","content":"Produci una rassegna tecnologica fattuale, concisa e leggibile."},
            {"role":"user","content":prompt}
        ],
        "temperature":0.25,
        "max_tokens":3500
    }).encode("utf-8")
    req = Request(
        "https://api.deepseek.com/chat/completions",
        data=body,
        headers={"Authorization":f"Bearer {api_key}","Content-Type":"application/json","User-Agent":"tech-news-daily/1.0"},
        method="POST"
    )
    try:
        with urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"].strip()
    except Exception as exc:
        print(f"DeepSeek non disponibile, uso fallback: {exc}")
        return None

def fallback_markdown(items):
    lines = ["## Notizie del giorno", ""]
    for x in items[:20]:
        lines.append(f"### [{x['title']}]({x['link']})")
        if x["summary"]:
            lines.append(x["summary"])
        lines.append(f"*Fonte: {x['source']}*")
        lines.append("")
    return "\n".join(lines)

def md_inline(s):
    s = html.escape(s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    return s

def markdown_to_html(md):
    out, in_ul = [], False
    for raw in md.splitlines():
        line = raw.strip()
        if not line:
            if in_ul:
                out.append("</ul>"); in_ul = False
            continue
        if line.startswith("### "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<h3>{md_inline(line[4:])}</h3>")
        elif line.startswith("## "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<h2>{md_inline(line[3:])}</h2>")
        elif line.startswith("# "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<h1>{md_inline(line[2:])}</h1>")
        elif re.match(r"^[-*]\s+", line):
            if not in_ul:
                out.append("<ul>"); in_ul = True
            out.append(f"<li>{md_inline(re.sub(r'^[-*]\\s+', '', line))}</li>")
        else:
            if in_ul:
                out.append("</ul>"); in_ul = False
            out.append(f"<p>{md_inline(line)}</p>")
    if in_ul:
        out.append("</ul>")
    return "\n".join(out)

def page(title, date_label, body_html, archive_links):
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<style>
:root {{ color-scheme: light dark; }}
body {{ margin:0; font:17px/1.6 system-ui,sans-serif; background:#111; color:#eee; }}
main {{ max-width:900px; margin:auto; padding:32px 20px 64px; }}
header {{ border-bottom:1px solid #444; margin-bottom:28px; }}
h1 {{ font-size:clamp(2rem,7vw,4rem); margin:.1em 0; }}
h2 {{ margin-top:2em; }}
h3 {{ margin:1.6em 0 .3em; }}
a {{ color:#7cc4ff; }}
.meta {{ color:#aaa; }}
.card {{ background:#181818; border:1px solid #333; border-radius:16px; padding:20px 24px; }}
.archive {{ margin-top:48px; border-top:1px solid #444; padding-top:24px; }}
.archive a {{ margin-right:14px; white-space:nowrap; }}
footer {{ color:#888; margin-top:48px; font-size:.9rem; }}
</style>
</head>
<body><main>
<header><div class="meta">Rassegna automatica · {html.escape(date_label)}</div>
<h1>Tech News Daily</h1>
<p>AI, Linux, open source, sviluppo, hardware, sicurezza e strumenti.</p>
</header>
<article class="card">{body_html}</article>
<section class="archive"><h2>Archivio</h2>{archive_links}</section>
<footer>Generato automaticamente da GitHub Actions. Le fonti originali restano collegate in ogni voce.</footer>
</main></body></html>"""

def main():
    DOCS.mkdir(exist_ok=True)
    ARCHIVE.mkdir(exist_ok=True)
    items = fetch_items()
    if not items:
        raise SystemExit("Nessuna notizia recuperata.")
    md = call_deepseek(items) or fallback_markdown(items)
    now = datetime.now().astimezone()
    date_slug, date_label = now.strftime("%Y-%m-%d"), now.strftime("%d/%m/%Y")
    body_html = markdown_to_html(md)
    archive_file = ARCHIVE / f"{date_slug}.html"
    archive_file.write_text(page("Tech News Daily", date_label, body_html, ""), encoding="utf-8")
    files = sorted(ARCHIVE.glob("*.html"), reverse=True)[:60]
    archive_links = " ".join(f'<a href="archive/{f.name}">{f.stem}</a>' for f in files)
    (DOCS / "index.html").write_text(page("Tech News Daily", date_label, body_html, archive_links), encoding="utf-8")
    archive_file.write_text(page("Tech News Daily", date_label, body_html, '<a href="../index.html">Ultima edizione</a>'), encoding="utf-8")
    (DOCS / "latest.json").write_text(json.dumps({
        "date":date_slug, "items_collected":len(items),
        "llm":bool(os.getenv("DEEPSEEK_API_KEY", "").strip())
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generata edizione {date_slug}: {len(items)} elementi raccolti.")

if __name__ == "__main__":
    main()
