import datetime as dt
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from elasticsearch import Elasticsearch  # Koneksi ke Elasticsearch untuk pengiriman data
import pandas as pd
import psycopg2 as db
from sqlalchemy import create_engine


# Fungsi untuk mengambil data dari PostgreSQL dan menyimpannya ke file CSV
def import_data_from_db():
    # Membuat objek PostgresHook
    postgres_hook = PostgresHook(postgres_conn_id='ml3_mardi_kurnianto_postgres', port=5434)
    
    # Mendapatkan koneksi dari PostgresHook
    conn = postgres_hook.get_conn()
    
    # Membaca data dari tabel 'table_m3' ke dalam DataFrame
    query = "SELECT * FROM final_project"
    df = pd.read_sql(query, conn)
    
    # Menyimpan data dari DataFrame ke file CSV
    df.to_csv('/opt/airflow/dags/data.csv', index=False)

    
def data_processing():
    #Loading CSV to dataframe
    df_data = pd.read_csv('/opt/airflow/dags/data.csv')

    #### start transformation
    # Remove null values.
    median_building_area = df_data['BuildingArea'].median()
    df_data['BuildingArea'].fillna(median_building_area, inplace=True)
    mode_year_built = df_data['YearBuilt'].mode()[0]
    df_data['YearBuilt'].fillna(mode_year_built, inplace=True)
    mode_council_area = df_data['CouncilArea'].mode()[0]
    df_data['CouncilArea'].fillna(mode_council_area, inplace=True)
    df_data['Car'].fillna(0, inplace=True)
    df_data.rename(str.lower, axis='columns')
    df_data.to_csv('/opt/airflow/dags/fp_melbourne_clean_data.csv', index=False)

# Fungsi untuk mengirimkan data yang telah dibersihkan ke Kibana
def post_to_kibana():
    # Membuat objek Elasticsearch yang terhubung ke instance http://elasticsearch:9200
    es = Elasticsearch("http://elasticsearch:9200")
    
    # Membaca file CSV 'data_clean.csv' ke dalam DataFrame
    df_post = pd.read_csv('/opt/airflow/dags/fp_melbourne_clean_data.csv')
    
    # Iterasi melalui setiap baris (row) dari DataFrame untuk mengirim data ke Kibana
    for i, r in df_post.iterrows():
        # Mengubah setiap baris menjadi bentuk JSON
        doc = r.to_json()
        
        # Mengirim data ke Elasticsearch (Kibana) dengan mengindeksnya ke 'table_m3'
        res = es.index(index="fp_melbourne", id=i+1, body=doc)

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'email_on_failure': False, #Parameter ini mengontrol apakah notifikasi email akan dikirim jika task mengalami kegagalan.
    'email_on_retry': False, #Parameter ini mengontrol apakah notifikasi email akan dikirim jika task dijadwalkan ulang (retry).
    'retries': 1, #menentukan berapa kali task akan mencoba dijalankan ulang jika terjadi kegagalan.
    'retry_delay': timedelta(minutes=60), #menentukan berapa lama (dalam satuan waktu) Apache Airflow harus menunggu sebelum mencoba menjalankan ulang task jika terjadi kegagalan. Dalam kasus ini, task akan dijadwalkan ulang setiap 60 menit (1 jam) jika diperlukan
    #
}

with DAG('final_project_schedule',
         description='Final Project',
         default_args=default_args,
         schedule_interval='@daily', # mengatur frekuensi eksekusi DAG. Dalam hal ini, DAG ini dijadwalkan untuk berjalan setiap hari
         start_date=datetime(2023, 11, 8), #menunjukkan tanggal dan waktu saat DAG akan mulai dijalankan. 28 Oktober 2023
         catchup=False) as dag: #Airflow tidak akan mengejar eksekusi yang tertinggal sebelum tanggal start_date. 
        #Jika ada pekerjaan yang seharusnya dijalankan di hari-hari sebelum tanggal mulai, itu tidak akan dieksekusi secara otomatis
    
    # Task to fetch data from PostgreSQL    
    fetch_task = PythonOperator(
        task_id='import_data_from_db',
        python_callable=import_data_from_db
    )
    
    # Task yg akan di eksekusi pythonoperator
    clean_task = PythonOperator(
        task_id='cleaning_data',
        python_callable=data_processing
    )

    post_to_kibana_task = PythonOperator(
        task_id='post_to_kibana',  # ID task untuk mengirimkan data ke Kibana
        python_callable=post_to_kibana
    )

    
    # Set task dependencies
    #baris yang mencoba menentukan hubungan ketergantungan antara task `clean_task`
    #namun disini kita hanya menyertakan clean_task tanpa menentukan hubungan ketergantungan.
    # clean_task
    fetch_task >> clean_task
