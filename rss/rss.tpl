%from api.bottle import html_escape
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
 <channel>
  <title>{{title}}</title>
  <description>{{desc}}</description>
  <link>{{link}}</link>
  <language>ru</language>
%for msg in msgs:
<item>
<name>{{msg.title}}</name>
<title>{{msg.title}}</title>
%ftxt = '<br>\n'.join([html_escape(x) for x in msg.txt.splitlines()])
<description>{{ftxt}}</description>
<pubDate>{{msg.pubDate}}</pubDate>
<author>{{msg.who}}</author>
<link>{{msg.url}}</link>
<guid>{{msg.url}}</guid>
</item>
%end
</channel>
</rss>