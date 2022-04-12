import pandas as pd
import argparse
from time import time
from sqlalchemy import create_engine

engine = create_engine('postgresql://root:root@localhost:5431/ny_taxi')
engine.connect()

df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)

df = next(df_iter)
print(len(df))

df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


df.to_sql(name = "yellow_taxi_data", con= engine, if_exists="replace")


df.head(n=0).to_sql(name = "yellow_taxi_data", con= engine, if_exists="replace")

df.to_sql(name = "yellow_taxi_data", con= engine, if_exists="append")


while True:
    t_start = time()

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.to_sql(name = "yellow_taxi_data", con= engine, if_exists="append")
    t_end = time()
    print("Inserted another chunk..., took %.3f second"%(t_end-t_start))