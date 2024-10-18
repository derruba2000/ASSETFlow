import dlt
import requests
import sys
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from tqdm import tqdm
import uuid

console = Console()

API_BASE_URL = 'http://localhost:8000'
limit=300
limitPaginations=5000000


def get_market_data(startdate :str, enddate :str):
    skip=0
    k=0
    while True:
        response = requests.get(f'{API_BASE_URL}/market_data/readAll?skip={skip}&limit={limit}&StartDate={startdate}&EndDate={enddate}')
        #response.raise_for_status()  # Raise an HTTPError for bad responses
        page_json = response.json()

        if response.status_code == 404:
            break

        if page_json:
            yield page_json
            skip+=limit
        else:
            break
        
        if len(page_json)==0:
            break

        k+=1
        if k > limitPaginations:
            break

def get_trades(startdate :str, enddate :str):
    skip=0
    k=0
    while True:
        response = requests.get(f'{API_BASE_URL}/trades/getAll?skip={skip}&limit={limit}&StartDate={startdate}&EndDate={enddate}')
        #response.raise_for_status()  # Raise an HTTPError for bad responses
        page_json = response.json()

        if response.status_code == 404:
            break
        if page_json:
            yield page_json
            skip+=limit
        else:
            break
   

        k+=1
        if k > limitPaginations:
            break



def process_time_interval(start, end):


    console.print(f"--->Processing from {start} to {end}", style="purple")

    

    assetflow_pipeline = dlt.pipeline(
        pipeline_name=f"AssetFlow-{str(uuid.uuid4())}",
        destination="snowflake",
        dataset_name="staging_assetflow",
    )

    # Market Data
    info = assetflow_pipeline.run(get_market_data(start, end), table_name="stream_market_data", write_disposition="append")
    console.print(info, style="purple")
    
    info = assetflow_pipeline.run(get_trades(start, end), table_name="stream_trades", write_disposition="append" )
    console.print(info, style="purple")


    
 


if __name__ == '__main__':
    # Use the generator to iterate over pages

    # arguments Startdate and Enddate
    start=sys.argv[1]
    end=sys.argv[2]

    
    process_time_interval(start, end)
   
