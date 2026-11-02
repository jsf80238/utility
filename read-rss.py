import feedparser

URL = "https://dockets.justia.com/browse/circuit-10/court-ca10/mode-rss"

d = feedparser.parse(URL)

print(d["feed"])
