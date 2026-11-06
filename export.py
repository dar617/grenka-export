import json, re, urllib.request, datetime

CHANNEL = "Grenka_Sans_Love"
url = f"https://t.me/s/{CHANNEL}"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")

posts = []
blocks = re.findall(r'<div class="tgme_widget_message[^"]"[^>]data-post="[^"]+".?(?=<div class="tgme_widget_message |</section>)', html, re.S)
for b in blocks:
m = re.search(r'<div class="tgme_widget_message_text[^"]*"[^>]>(.*?)</div>', b, re.S)
text = re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""
text = re.sub(r"\s+", " ", text).strip()
date = re.search(r'datetime="([^"]+)"', b)
views = re.search(r'tgme_widget_message_views">([^<]+)<', b)
reactions = re.search(r'tgme_reaction_count">([^<]+)<', b)
link = re.search(r'data-post="([^"]+)"', b)
posts.append({
"date": date.group(1) if date else None,
"text": text,
"views": views.group(1).strip() if views else None,
"reactions": reactions.group(1).strip() if reactions else None,
"link": link.group(1) if link else None,
})

out = {
"channel": CHANNEL,
"updated": datetime.datetime.utcnow().isoformat() + "Z",
"posts": posts,
}
open("posts.json", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=2))
print("saved", len(posts), "posts")
