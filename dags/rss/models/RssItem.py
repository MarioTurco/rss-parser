from dataclasses import dataclass, field
from typing import Optional 

@dataclass
class RssItem:

    # Required fields
    title: str
    link: str 
    pub_date: str
    source: str 
    feed_url: str
    
    # Optional fields
    description: Optional[str] = None 
    category: Optional[str] = None
    author: Optional[str] = None 
    #TODO make this a foreign key to author table?

    def to_dict(self):
        return {
            'title': self.title,
            'pub_date': self.pub_date,
            'link': self.link,
            'source': self.source, 
            'feed_url': self.feed_url, 
            'description': self.description if self.description else None,
            'category': self.category if self.category else None,
            'author': self.author if self.author else None
        }
