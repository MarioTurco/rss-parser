# rss-parser (actually a scraper)

This is a work in progress 

## Phase 1 - MVP

- [x] Scrape an rss link (min requirements: link, title, description, pub date)
- [x] Save all the scraped info into a relationa database (Postgresql)
- [ ] View the scraped links from a streamlit dashboard
- [ ] Automatic trigger every 60 min with airflow

## Phase 2 - MVP+

- [ ] Use streamlit dashboard to add/remove link 
- [ ] Scrape multiple links at the time
- [ ] Also save images related to links into the database 
- [ ] Add ability to like / dislike items
- [ ] On demand trigger from streamlit 


## Phase 3

- [ ] Scrape content of the article itself and/or load the webpage inside of streamlit
- [ ] Scrape also rss feeds that require login (actually i don know if these exists)/and or webpages that require login
- [ ] Also keep track of Authors/Sources creating dedicated pages on steamlit where you can look at some stats (publications per month)
- [ ] Some kind of automatic article classification? (News, Tech, ....)
- [ ] ???