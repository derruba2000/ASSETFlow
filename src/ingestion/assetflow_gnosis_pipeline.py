import dlt
import requests
import sys

API_BASE_URL = 'http://localhost:8000'
limit=100

limitPaginations=5


def get_assets():
    skip=0
    while True:
        response = requests.get(f'{API_BASE_URL}/assets?skip={skip}&limit={limit}')
        response.raise_for_status()  # Raise an HTTPError for bad responses
        page_json = response.json()
        if page_json:
            yield page_json
            skip+=limit
        else:
            break

def get_investors():
    skip=0
    while True:
        response = requests.get(f'{API_BASE_URL}/investors?skip={skip}&limit={limit}')
        response.raise_for_status()  # Raise an HTTPError for bad responses
        page_json = response.json()
        if page_json:
            yield page_json
            skip+=limit
        else:
            break
        
def get_portfolios():
    skip=0
    while True:
        response = requests.get(f'{API_BASE_URL}/portfolios?skip={skip}&limit={limit}')
        response.raise_for_status()  # Raise an HTTPError for bad responses
        page_json = response.json()
        if page_json:
            yield page_json
            skip+=limit
        else:
            break


def get_market_data(startdate :str, enddate :str):
    skip=0
    k=0
    while True:
        response = requests.get(f'{API_BASE_URL}/market_data/readAll?skip={skip}&limit={limit}&StartDate={startdate}&EndDate={enddate}')
        #response.raise_for_status()  # Raise an HTTPError for bad responses
        page_json = response.json()
        if page_json:
            yield page_json
            skip+=limit
        else:
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
        if page_json:
            yield page_json
            skip+=limit
        else:
            break
        k+=1
        if k > limitPaginations:
            break
        

if __name__ == '__main__':
    # Use the generator to iterate over pages
    assetflow_pipeline = dlt.pipeline(
        pipeline_name="AssetFlow",
        destination="snowflake",
        dataset_name="staging_assetflow",
    )

    # arguments Startdate and Enddate
    startdate=sys.argv[1]
    enddate=sys.argv[2]

    # Market Data
    info = assetflow_pipeline.run(get_market_data(startdate, enddate), table_name="stream_market_data", write_disposition="append" )
    print(info)

    info = assetflow_pipeline.run(get_trades(startdate, enddate), table_name="stream_trades", write_disposition="append" )
    print(info)


    # Fullload
    # Assets
    info = assetflow_pipeline.run(get_assets(),table_name="stream_assets",write_disposition="replace")
    print(info)

    # Investors
    info = assetflow_pipeline.run(get_investors(), table_name="stream_investors", write_disposition="replace")
    print(info)

    # Portfolio
    info = assetflow_pipeline.run(get_portfolios(), table_name="stream_portfolios", write_disposition="replace")
    print(info)
    
    

