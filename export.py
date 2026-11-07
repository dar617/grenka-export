import json, re, urllib.request, datetime
CHANNEL = "Grenka_Sans_Love"
req = urllib.request.Request("https://t.me/s/" + CHANNEL, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
chunks = [c for c in re.split(r'data-post="', html, flags=re.I)[1:] if c.split("/")[0].lower() == CHANNEL.lower()]
posts = [{"id": c.split('"')[0], "date": (g.group(1) if (g := re.search(r'datetime="([^"]+)"', c)) else None), "text": (re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", (t.group(1) if (t := re.search(r'tgme_widget_message_text[^"]*"[^>]*>([\s\S]*?)</div>', c)) else ""))).strip()), "views": (v.group(1).strip() if (v := re.search(r'tgme_widget_message_views">([^<]+)<', c)) else None), "reactions": (r.group(1).strip() if (r := re.search(r'tgme_reaction_count">([^<]+)<', c)) else None), "link": "https://t.me/" + CHANNEL + "/" + c.split('"')[0]} for c in chunks]
out = {"channel": CHANNEL, "updated": datetime.datetime.now(datetime.timezone.utc).isoformat(), "posts": posts}
open("posts.json", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=2))
print("saved", len(posts), "posts")
