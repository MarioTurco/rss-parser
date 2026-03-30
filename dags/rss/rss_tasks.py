from rss.models.RssItem import RssItem
from typing import List
from airflow.providers.postgres.hooks.postgres import PostgresHook

#TODO for now let's scrape a single hard coded link 
#TODO we can later extend this to scrape multiple feeds and store the feed urls in a database table


def get_list_of_rss_feeds() -> List[str]:
    #TODO implement this function to retrieve the list of RSS feed URLs from a database table
    return [
        "https://allaboutdata.substack.com/feed",
        "https://www.theseattledataguy.com/data-science-consulting-blog/feed",
        
        ]

def scrape_rss_feed(rss_url:str) -> List[RssItem]:
    """
    Scrapes the RSS feed from the given URL and returns a list of entries.
    
    Args:
        rss_url (str): The URL of the RSS feed to scrape.
    Returns:
        list: A list of RssItem objects from the RSS feed.
    """
    import feedparser
    feed = feedparser.parse(rss_url)
    rss_items = []
    for entry in feed.entries:
        rss_item = RssItem(
            title=entry.title,
            description=entry.description if 'description' in entry else None,
            link=entry.link,
            feed_url=rss_url,
            pub_date=entry.published,
            source=feed.feed.title if 'title' in feed.feed else 'Unknown Source',
            category=entry.tags[0].label if 'tags' in entry and len(entry.tags) > 0 else None
        )
        rss_items.append(rss_item)
    
    print(f"Scraped {len(rss_items)} items from {rss_url}")
    # Restituisci lista di dict invece di oggetti per compatibilità XCom
    return [item.to_dict() for item in rss_items]

def load_rss_items_to_db(**context):
    rss_items = context['ti'].xcom_pull(task_ids='scrape_rss_feed_task')
    
    if not rss_items:
        print("Nessun item da caricare.")
        return
    
    pg_hook = PostgresHook(postgres_conn_id="rss_db")
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO rss_items (title, link, description, pub_date, source, category, feed_url, author)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (title, link) DO NOTHING
    """

    data = [
        (item['title'], item['link'], item['description'], item['pub_date'], item['source'], item['category'], item['feed_url'], item['author'])
        for item in rss_items
    ]

    cursor.executemany(insert_query, data)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inseriti {len(data)} item nel DB.")



if __name__ == "__main__":
    rss_url = "https://allaboutdata.substack.com/feed"
    items = scrape_rss_feed(rss_url)
    for item in items:
        print(item.to_dict())