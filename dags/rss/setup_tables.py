#TODO move all the queries into separate .sql file 
# and load them in the functions instead of hardcoding them 

def createRssTable():
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS rss_items (
        title TEXT NOT NULL,
        link TEXT NOT NULL,
        description TEXT,
        pub_date TIMESTAMP NOT NULL,
        source TEXT,
        category TEXT,
        feed_url TEXT NOT NULL,
        author TEXT, 
        scrape_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        primary key (link, title)
    );
    """
    return create_table_query