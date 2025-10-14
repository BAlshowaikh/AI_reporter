from config.settings import load_settings
import feedparser

# Load the settings
settings = load_settings()

# Handle the parsed URL
def fetch_feed():
    feed_url = settings.feed_urls

    # Download and parse the XML automatically
    for x in feed_url:
        feed = feedparser.parse(x)
        feed_title = getattr(feed.feed, "title", None)
        return feed_title

print(fetch_feed())
