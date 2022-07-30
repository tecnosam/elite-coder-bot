import asyncio
import discord
import feedparser

from bs4 import BeautifulSoup as bs


NEWS_CHANNEL_ID = 1002215469207523358

rss_format = """
    {entry.title} by {entry.author} at {entry.published}

    {text}

    Read More: {entry.link}
"""

# TODO: skip news that was posted before the time of the last article

async def send_to_channel(client: discord.Client):
    print("Running news aggregator")
    channel = client.get_channel(NEWS_CHANNEL_ID)

    print("sending message to channel")
    for feed, server in daily_feed():
        try:

            text = bs(feed.get('summary', ''), features="html.parser").get_text()
            msg = rss_format.format(entry=feed, text=text)
            
            if len(msg) > 2000:
                continue

            # yield msg
            await channel.send(msg)
            await asyncio.sleep(300)

        except AttributeError:
            print(server)
    
    print("Done with the news")


def daily_feed():

    for server in fetch_rss_servers():
        for feed in fetch_feed(server):
            yield feed, server
    return 


def fetch_rss_servers():
    # Fetch rss servers from feedly.com
    return [
        "http://feeds.feedburner.com/TheHackersNews",
        "https://www.sitepoint.com/sitepoint.rss",
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
        "https://nakedsecurity.sophos.com/feed/",
        "https://www.youtube.com/feeds/videos.xml?channel_id=UCvjgXvBlbQiydffZU7m1_aw",
        "https://www.btcwires.com/feed/",
        "https://www.ibm.com/blogs/blockchain/feed/",
        "https://css-tricks.com/feed/",
        "http://www.thecrazyprogrammer.com/feed"
    ]


def fetch_feed(server: str) -> list:
    # Fetch feed from RSS server
    feed = feedparser.parse(server)

    return feed.entries
