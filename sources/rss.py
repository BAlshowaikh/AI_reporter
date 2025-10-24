from config.settings import load_settings
import feedparser

# Load the settings
settings = load_settings()

# Handle the parsed URL
def fetch_feed():
    feed_url = settings.feed_urls
    feedDetails = {}

    # Download and parse the XML automatically
    for url in feed_url:
        feed = feedparser.parse(url)
        if feed.bozo:
            print("⚠️  Parsing issue detected!")
            print("Reason:", feed.bozo_exception)

        # The feedparser.parse(url) downloads and parses the XML automatically
        # returned feed object behaves like a dictionary, with keys like:

        # feed → contains metadata (title, link, description)
        # entries → list of articles/items
        # status → HTTP status (if fetched over HTTP)
        # bozo → flag indicating if parsing failed or was malformed

        # Get the attributes from the feed 
        feed_title = getattr(feed.feed, "title", None)
        if not feed_title:
            feed_title = getattr(feed.feed, "link", None)
        
        feed_desc = getattr(feed.feed, "description", "No description available")
        feed_link = getattr(feed.feed, "link", "No link available")
        feed_status = getattr(feed, "status", "No status available")

        if feed.entries: 
            first = feed.entries[0] 
            print("\nSample Entry:")
            print("Title:", getattr(first, "title", "(no title)"))
            print(" Link:", getattr(first, "link", "(no link)"))
            print("Published:", getattr(first, "published", "(no date)"))
        else:
            print("No entries found in this feed.")
        
        feedDetails = {
            "title": feed_title,
            "url": feed_link,
            "Description": feed_desc,
            "Status:": feed_status,
            "Feed entries:": feed.entries[0] if feed.entries else None
        }

    return feedDetails

if __name__ == "__main__":
    fetch_feed()
