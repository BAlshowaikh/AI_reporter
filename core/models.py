# Imports
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
from typing import List, Optional

# Create an Article class that truns the feed after parsing into a consistence object
@dataclass
class Article:
    id: str
    title: Optional[str] = None
    url: Optional[str] = None
    published_at: Optional[datetime] = None
    summary: Optional[str] = None
    # What below means: This field must hold a list of strings, and if no list is provided when creating an 
    # Article object, a brand new, empty list should be created for it.
    categories: List[str] = field(default_factory=list)
    source_title: Optional[str] = None

# Function to generate ids automatically
def generate_article_id(url: Optional[str], title: Optional[str], published_at: Optional[datetime]):
    """
    Generate a stable hash ID for an article.
    Priority: URL → title + published_at → fallback "missing_id"
    """
    final_hash = ""
    if (url):
        hash = hashlib.blake2b(digest_size=12)

        # Convert the url into bytes (because hash only accept byte)
        url_encode = url.encode("utf-8")

        # Pass the encoded (bytes) variable into the hashing function
        hash.update(url_encode)

        # Use the object's .hexdigest() method to get the final hash as a human-readable hex string.
        final_hash = hash.hexdigest()

        # The above code could be one line as below
        # final_hash = hashlib.blake2b(url_string.encode('utf-8')).hexdigest()

        return final_hash
    
    elif title and published_at:
            # This is done in this way because
            # When published_at is a datetime, its default string form 
            # includes spaces and timezone info that might differ between runs.
            comb = f"{title}|{published_at.isoformat()}"
            # Do the same steps for hasing
            encoder = comb.encode("utf-8")
            hash = hashlib.blake2b(digest_size=12)
            hash.update(encoder)
            final_hash = hash.hexdigest()

            return final_hash
    else:
            return "missing_url"