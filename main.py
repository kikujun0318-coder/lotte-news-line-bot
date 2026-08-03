import os
import requests
import feedparser

LINE_TOKEN = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

FEEDS = [
    'https://news.yahoo.co.jp/rss/topics/baseball.xml',
    'https://www.marines.co.jp/news/rss.xml'
]

KEYWORDS = ['ロッテ', 'マリーンズ', '千葉ロッテ']

def send_line(text):
    headers = {
        'Authorization': f'Bearer {LINE_TOKEN}',
        'Content-Type': 'application/json'
    }
    requests.post(
        'https://api.line.me/v2/bot/message/broadcast',
        headers=headers,
        json={'messages': [{'type': 'text', 'text': text}]}
    )

seen_file = 'seen.txt'
if os.path.exists(seen_file):
    with open(seen_file, 'r', encoding='utf-8') as f:
        seen = set(f.read().splitlines())
else:
    seen = set()

new_seen = set(seen)

for feed in FEEDS:
    d = feedparser.parse(feed)
    for entry in d.entries[:10]:
        title = entry.title
        link = entry.link
        uid = link
        if uid in seen:
            continue
        if any(k in title for k in KEYWORDS):
            send_line(f'【ロッテ速報】\n{title}\n{link}')
        new_seen.add(uid)

with open(seen_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(new_seen))
send_line("テスト通知です！ロッテBot動作確認")
