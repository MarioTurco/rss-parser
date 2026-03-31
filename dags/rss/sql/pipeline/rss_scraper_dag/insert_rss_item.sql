INSERT INTO rss_items (title, link, description, pub_date, source, category, feed_url, author)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (title, link) DO NOTHING;