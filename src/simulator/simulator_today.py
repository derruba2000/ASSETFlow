import random
import requests
from datetime import datetime, timedelta
from faker import Faker
from tqdm import tqdm
import time

# Initialize Faker
fake = Faker()

# API Base URL
API_BASE_URL = 'http://localhost:8000'  # Change to your API base URL

# Simulation Parameters

NUM_INVESTORS = 300
MAX_PORTFOLIOS = 450
MAX_TRADES = 3
NUM_ASSETS = 300

MIN_ACCOUNT_BALANCE = 1000
MAX_ACCOUNT_BALANCE = 1000000
MAX_PRICE=4000
MAX_RECORDS_BULK=3
MIN_VOLUME = 1000
MAX_VOLUME = 100000
PRICE_RANGE=20

# Asset Types and Portfolio Types
ASSET_TYPES = ['crypto', 'stocks', 'etfs', 'derivatives', 'bonds', 'commodities']
PORTFOLIO_TYPES = ['Conservative', 'Balanced', 'Aggressive Growth', 'Income-Focused', 
                   'Socially Responsible Investment', 'All-Weather Portfolio']


#-------------------------------------------------------------------------------

#START_DATE = datetime.strptime(START_DATE, '%Y-%m-%d')
#END_DATE = datetime.strptime(END_DATE, '%Y-%m-%d')


# Helper functions
def random_price():
    """Generate a random price."""
    return round(random.uniform(10, MAX_PRICE), 2)

def generate_market_data(asset_id, date):
    """Generate random market data for an asset."""
    opening_price = random_price()
    closing_price = random_price()
    high_price = max(opening_price, closing_price) + random.uniform(1, PRICE_RANGE)
    low_price = min(opening_price, closing_price) - random.uniform(1, PRICE_RANGE)
    volume = random.randint(MIN_VOLUME, MAX_VOLUME)
    
    market_data = {
        "AssetID": asset_id,
        "Date": date,
        "OpeningPrice": opening_price,
        "ClosingPrice": closing_price,
        "HighPrice": high_price,
        "LowPrice": low_price,
        "Volume": volume
    }
    return market_data





def create_trade(portfolio_id, asset_id, date):
    """Simulate a trade for a portfolio."""
    trade_data = {
        "PortfolioID": portfolio_id,
        "AssetID": asset_id,
        "TradeType": random.choice(['Buy', 'Sell']),
        "TradeDate": date,
        "TradePrice": random_price(),
        "Quantity": random.randint(1, 100)
    }
    return trade_data

def run_simulator():
    """Run the simulation."""
   
    delta = timedelta(days=1)
    
    #todays date
    today = datetime.today().strftime('%Y-%m-%d')

    assets=NUM_ASSETS
    investors = NUM_INVESTORS
    portfolios = MAX_PORTFOLIOS
    
    # Simulate each day between start and end date
    current_date = today
    #Number of days between start and end date
 
    while True:
        

        print(f"Simulating for {current_date}")
        
        
        # Simulate market data for each asset       
        k=0
        assetsList=[random.choice(range(1, assets-2*MAX_RECORDS_BULK)) for x in range(1, MAX_RECORDS_BULK)]
        # just want 3 elements from the list
        assetsList=assetsList[:MAX_RECORDS_BULK]

        
        for asset_id in assetsList:
            MarketDataList = []
            for asset_idx in range(asset_id,asset_id+MAX_RECORDS_BULK):
                market_data = generate_market_data(asset_idx, current_date)
                MarketDataList.append(market_data)
            response=requests.post(f'{API_BASE_URL}/market_data/bulk', json={"marketdata":MarketDataList})
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
            k+=1
            if k > MAX_RECORDS_BULK:
                break
               
        
        # Simulate all the trades for that day
        numTrades=random.randint(1, MAX_TRADES)
        for trade_id in range(1, numTrades, MAX_RECORDS_BULK):
            TradesList=[]
            for trade_idx in range(trade_id, trade_id+MAX_RECORDS_BULK):
                portfolio_id = random.choice(range(portfolios))
                asset_id = random.choice(range(assets))
                trade_data = create_trade(portfolio_id, asset_id, current_date)
                TradesList.append(trade_data)
            requests.post(f'{API_BASE_URL}/trades/bulk', json={"trades":TradesList})  
          
        
        # pause 5 seconds
        time.sleep(5)


if __name__ == '__main__':
    # Add a 10 second pause to ensure the API is running
    # Check if the API is working 
    API_running=0
    try:
        response = requests.get(f'{API_BASE_URL}/')
        API_running=1
    except requests.exceptions.ConnectionError:
        print("API is not running. Please start the API first.")
    if API_running==0:
        print("API is not running. Please start the API first.")
        TotalSeconds=10
        pbar = tqdm(range(TotalSeconds))
        for i in pbar:
            time.sleep(1)
            pbar.set_description(f"Waiting for API to start {i} of {TotalSeconds}...")

    response = requests.get(f'{API_BASE_URL}/')    
    if response.status_code == 200:
        print("API is running. Starting simulation...")
        time.sleep(1)
        print("Simulation started.")
        # two arguments are passed to the script: the start date and the end date
        
        
        run_simulator()
    else:
        print("API is not running. Please start the API first. Ending execution")
