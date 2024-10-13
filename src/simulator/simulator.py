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
START_DATE = '2024-10-01'
END_DATE = '2024-10-10'
NUM_INVESTORS = 5
MAX_PORTFOLIOS = 5
MAX_TRADES = 5
NUM_ASSETS = 5
MIN_ACCOUNT_BALANCE = 1000
MAX_ACCOUNT_BALANCE = 1000000

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
    return round(random.uniform(10, 500), 2)

def generate_market_data(asset_id, date):
    """Generate random market data for an asset."""
    opening_price = random_price()
    closing_price = random_price()
    high_price = max(opening_price, closing_price) + random.uniform(1, 20)
    low_price = min(opening_price, closing_price) - random.uniform(1, 20)
    volume = random.randint(1000, 100000)
    
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

def create_investor():
    """Simulate the creation of an investor."""
    investor_data = {
        "Name": fake.name(),
        "InvestorType": random.choice(['Individual', 'Institutional']),
        "ContactInfo": fake.email(),
        "RiskTolerance": random.choice(['Conservative', 'Moderate', 'Aggressive']),
        "AccountBalance": random.uniform(MIN_ACCOUNT_BALANCE, MAX_ACCOUNT_BALANCE)
    }
    response = requests.post(f'{API_BASE_URL}/investors/', json=investor_data)
    return response.json()['InvestorID']

def create_portfolio(investor_id):
    """Simulate the creation of a portfolio for an investor."""

    portfolio_data = {
        "InvestorID": investor_id,
        "PortfolioName": fake.bs().title(),
        "PortfolioType": random.choice(PORTFOLIO_TYPES),
        "CreationDate": fake.date_between(start_date=START_DATE, end_date=END_DATE).strftime('%Y-%m-%d'),
        "TotalValue": random.uniform(50000, 1000000)
    }
    response = requests.post(f'{API_BASE_URL}/portfolios/', json=portfolio_data)
    return response.json()['PortfolioID']

def create_asset():
    """Simulate the creation of an asset."""
    asset_data = {
        "AssetName": fake.company(),
        "AssetType": random.choice(ASSET_TYPES),
        "TickerSymbol": fake.lexify('????').upper(),
        "CurrentPrice": random_price()
    }
    response = requests.post(f'{API_BASE_URL}/assets/', json=asset_data)
    return response.json()['AssetID']

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
    response = requests.post(f'{API_BASE_URL}/trades/', json=trade_data)
    return response.status_code

def run_simulator():
    """Run the simulation."""
    start_date = START_DATE #datetime.strptime(START_DATE, '%Y-%m-%d')
    end_date = END_DATE #datetime.strptime(END_DATE, '%Y-%m-%d')
    delta = timedelta(days=1)
    
    # Create assets
    assets = [create_asset() for _ in range(NUM_ASSETS)]
    
    # Create investors and portfolios
    investors = [create_investor() for _ in range(NUM_INVESTORS)]
    portfolios = [create_portfolio(investor) for investor in investors]
    
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
        for asset_id in assets:
            market_data = generate_market_data(asset_id, current_date.strftime('%Y-%m-%d'))
            requests.post(f'{API_BASE_URL}/market_data/', json=market_data)
        
        # Simulate trades
        for _ in range(random.randint(1, MAX_TRADES)):
            portfolio_id = random.choice(portfolios)
            asset_id = random.choice(assets)
            create_trade(portfolio_id, asset_id, current_date.strftime('%Y-%m-%d'))
        
        # Move to the next day
        current_date += delta

if __name__ == '__main__':
    # Add a 10 second pause to ensure the API is running
    TotalSeconds=10
    pbar = tqdm(range(TotalSeconds))
    for i in pbar:
        time.sleep(1)
        pbar.set_description(f"Waiting for API to start {i} of {TotalSeconds}...")
    run_simulator()
