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
START_DATE = '2000-01-01'
END_DATE = '2024-10-10'
NUM_INVESTORS = 300
MAX_PORTFOLIOS = 450
MAX_TRADES = 200
NUM_ASSETS = 300
MIN_ACCOUNT_BALANCE = 1000
MAX_ACCOUNT_BALANCE = 1000000
MAX_PRICE=4000
MAX_RECORDS_BULK=160
MIN_VOLUME = 1000
MAX_VOLUME = 100000
PRICE_RANGE=20

# Asset Types and Portfolio Types
ASSET_TYPES = ['crypto', 'stocks', 'etfs', 'derivatives', 'bonds', 'commodities']
PORTFOLIO_TYPES = ['Conservative', 'Balanced', 'Aggressive Growth', 'Income-Focused', 
                   'Socially Responsible Investment', 'All-Weather Portfolio']


#-------------------------------------------------------------------------------

START_DATE = datetime.strptime(START_DATE, '%Y-%m-%d')
END_DATE = datetime.strptime(END_DATE, '%Y-%m-%d')


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



def create_portfolio(NumInvestors : int):
    """Simulate the creation of a portfolio for an investor."""
    response = requests.get(f'{API_BASE_URL}/portfolios/portfoliocount')
    ExistingPortfolios=response.json()
    PortfolioList=[]
    for portfolioNum in range(MAX_PORTFOLIOS-ExistingPortfolios):
        # Create a portfolio for the investor
        portfolio_data = {
            "InvestorID": random.choice(range(NumInvestors)),
            "PortfolioName": fake.bs().title(),
            "PortfolioType": random.choice(PORTFOLIO_TYPES),
            "CreationDate": fake.date_between(start_date=START_DATE, end_date=END_DATE).strftime('%Y-%m-%d'),
            "TotalValue": random.uniform(50000, 1000000)
        }
        PortfolioList.append(portfolio_data)
    if len(PortfolioList)>0:
        portfolioListFinal={
            "portfolios" : PortfolioList
        }
        response = requests.post(f'{API_BASE_URL}/portfolios/bulk', json=portfolioListFinal)
        response = requests.get(f'{API_BASE_URL}/portfolios/portfoliocount')
        ExistingPortfolios=response.json()

    return ExistingPortfolios

def create_asset(NumAssets : int):
    """Simulate the creation of assets."""
    # read the existing nuumber of assets from the database
    response = requests.get(f'{API_BASE_URL}/assets/assetcount/')
    ExistingAssets=response.json()
    AssetList=[]
    for assetNum in range(NumAssets-ExistingAssets):
        asset_data = {
            "AssetName": fake.company(),
            "AssetType": random.choice(ASSET_TYPES),
            "TickerSymbol": fake.lexify('????').upper(),
            "CurrentPrice": random_price()
        }
        AssetList.append(asset_data)
    if len(AssetList) > 0 :
        assetListFinal={
            "assets" : AssetList
        }
        # Uploads assets
        response = requests.post(f'{API_BASE_URL}/assets/bulk', json=assetListFinal)
        # Reads updated number of assets
        response = requests.get(f'{API_BASE_URL}/assets/assetcount/')
        ExistingAssets=response.json()

    return   ExistingAssets

def create_investor(NumInvestors : int):
    """Simulate the creation of investors."""
    response = requests.get(f'{API_BASE_URL}/investors/investorcount')
    ExistingInvestors=response.json()
    InvestorsList=[]
    for investNum in range(NumInvestors-ExistingInvestors):
        # Create an investor
        investor_data = {
            "Name": fake.name(),
            "InvestorType": random.choice(['Individual', 'Institutional']),
            "ContactInfo": fake.email(),
            "RiskTolerance": random.choice(['Conservative', 'Moderate', 'Aggressive']),
            "AccountBalance": random.uniform(MIN_ACCOUNT_BALANCE, MAX_ACCOUNT_BALANCE)
        }
        InvestorsList.append(investor_data)
    if len(InvestorsList)>0:
        investorListFinal={
            "investors" : InvestorsList
        }
        response = requests.post(f'{API_BASE_URL}/investors/bulk', json=investorListFinal)
        response = requests.get(f'{API_BASE_URL}/investors/')
        ExistingInvestors=response.json()

    return ExistingInvestors


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
    start_date = START_DATE #datetime.strptime(START_DATE, '%Y-%m-%d')
    end_date = END_DATE #datetime.strptime(END_DATE, '%Y-%m-%d')
    delta = timedelta(days=1)
    
    # Create assets
    print("Creating assets...")
    assets=create_asset(NUM_ASSETS)


       
    # Create investors and portfolios
    print("Creating investors...")
    investors = create_investor(NUM_INVESTORS) 
    print("Creating portfolios...")
    portfolios = create_portfolio(MAX_PORTFOLIOS) 
    
    # Simulate each day between start and end date
    current_date = start_date
    #Number of days between start and end date
    num_days = (end_date - start_date).days + 1
    pbar = tqdm(total=num_days, unit='day')
    pbar.set_description("Simulating...")
    pbar.update(0)
    for _ in range(num_days):
        pbar.update(1)
        pbar.set_description(f"> Simulating day {current_date}...")

        print(f"Simulating for {current_date.strftime('%Y-%m-%d')}")
        
        
        # Simulate market data for each asset       
        for asset_id in range(1, assets, MAX_RECORDS_BULK):
            MarketDataList = []
            for asset_idx in range(asset_id,asset_id+MAX_RECORDS_BULK):
                market_data = generate_market_data(asset_idx, current_date.strftime('%Y-%m-%d'))
                MarketDataList.append(market_data)
            response=requests.post(f'{API_BASE_URL}/market_data/bulk', json={"marketdata":MarketDataList})
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
               
        
        # Simulate all the trades for that day
        numTrades=random.randint(1, MAX_TRADES)
        for trade_id in range(1, numTrades, MAX_RECORDS_BULK):
            TradesList=[]
            for trade_idx in range(trade_id, trade_id+MAX_RECORDS_BULK):
                portfolio_id = random.choice(range(portfolios))
                asset_id = random.choice(range(assets))
                trade_data = create_trade(portfolio_id, asset_id, current_date.strftime('%Y-%m-%d'))
                TradesList.append(trade_data)
            requests.post(f'{API_BASE_URL}/trades/bulk', json={"trades":TradesList})  
          
        
        # Move to the next day
        current_date += delta

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
        run_simulator()
    else:
        print("API is not running. Please start the API first. Ending execution")
