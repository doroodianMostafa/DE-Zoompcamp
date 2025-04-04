#!/usr/bin/env python
# coding: utf-8

from sqlalchemy import create_engine
from time import time
import pandas as pd
import argparse
import shutil
import gzip
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    url = params.url
    table_name = params.table_name

    
    # Define file names
    csv_gz_name = 'output.csv.gz'
    csv_name = 'output.csv'

    # Download the .csv.gz file
    os.system(f"wget {url} -O {csv_gz_name}")  

    # Decompress the .gz file
    with gzip.open(csv_gz_name, 'rb') as f_in:
        with open(csv_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator = True, chunksize = 100000 )

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(0).to_sql(name = table_name, con=engine, if_exists = 'replace')
    df.to_sql(name = 'yellow_taxi_driver', con=engine, if_exists = 'append')


    while True:
        t_start = time()
        
        df = next(df_iter)

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name = table_name, con=engine, if_exists = 'append')

        t_end = time()

        print("Another chunk was added ... took %.3f second" % (t_end - t_start))

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Ingest CSV to postgres")

    # user, password, host, port, database name, table name,
    # url of the csv 
    parser.add_argument("--user", help ='username for postgres')
    parser.add_argument("--password", help ='password for postgres')
    parser.add_argument("--host", help ='host for postgres')
    parser.add_argument("--port", help ='port for postgres')
    parser.add_argument("--db", help ='database name for postgres')
    parser.add_argument("--table_name", help ='the name of the table we will write the results to')
    parser.add_argument("--url", help ='url of the csv file')

    args = parser.parse_args()

    main(args)


