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



if __name__ == '__main__':
    # Use the generator to iterate over pages
    assetflow_pipeline = dlt.pipeline(
        pipeline_name="AssetFlow_static",
        destination="snowflake",
        dataset_name="staging_assetflow",
    )



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
    
    

