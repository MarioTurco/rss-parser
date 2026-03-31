from rss.common import read_query


def createRssSourceTable() -> str:
    return read_query("dags/rss/sql/tables/tb_source_rss.sql") #TODO parametrize path
 

def createRssTable() -> str:
    return read_query("dags/rss/sql/tables/rss_items.sql") #TODO parametrize path
    