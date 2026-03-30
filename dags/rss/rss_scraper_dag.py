from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta
from rss.rss_tasks import scrape_rss_feed, load_rss_items_to_db
from rss.setup_tables import createRssTable


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retry_delay': timedelta(minutes=5),
    'retries': 3,
    'email_on_failure': True, #TODO check how to set up email notifications
}


dag = DAG(
    dag_id='rss_scraping',
    description='An ELT pipeline for extracting RSS data and loading it into an iceberg table in a postgres database',
    start_date=datetime(2023, 1, 1),
    schedule="*/60 * * * *",  # Every 60 minutes
    default_args=default_args
)


create_table_task = SQLExecuteQueryOperator(
    task_id='create_rss_table',
    sql=createRssTable(),
    dag=dag,
    conn_id='rss_db'
)

scrape_rss_feed_task = PythonOperator(
    task_id='scrape_rss_feed_task',
    dag=dag,
    python_callable=scrape_rss_feed,
    op_kwargs={
        'rss_url': 'https://allaboutdata.substack.com/feed'
    },
    #TODO do i need a pre-step that loads all the feed urls from a database table 
    # and then dynamically creates tasks for each feed url? 
)

load_rss_data_to_db_task = PythonOperator(
    task_id='load_rss_data_to_db',
    dag=dag,
    python_callable=load_rss_items_to_db
)


create_table_task >> scrape_rss_feed_task >> load_rss_data_to_db_task