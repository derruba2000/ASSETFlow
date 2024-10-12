# AssetFlow - Asset Management Platform

AssetFlow is an open-source asset management platform designed to emulate core functionalities of portfolio management systems. It provides a robust backend API built with FastAPI and integrates a SQLite database to track portfolios, trades, investors, assets, market data, and risk metrics. The project also includes a front-end (to be developed) to create an interactive interface for portfolio and asset management.

## Features

- **Portfolio Management**: Create, view, and manage investor portfolios.
- **Investor Management**: Add and track investors, including their risk tolerance and account balances.
- **Asset Tracking**: Manage various asset types like stocks, bonds, and commodities.
- **Trades**: Record and track buy/sell transactions.
- **Market Data**: Store and retrieve historical market data (e.g., daily opening, closing prices).
- **Risk Metrics**: Calculate and track key portfolio risk metrics.

## Technology Stack

### Backend:
- **Python**: Programming language
- **FastAPI**: Web framework for building APIs
- **SQLite**: Lightweight database for local data storage
- **SQLAlchemy**: ORM for database interactions

### Frontend:
- **To Be Developed**: The frontend interface will allow users to interact with the API and manage portfolios with ease.

### Additional Tools:
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server to run the FastAPI application

## Project Setup

### Requirements

- Python 3.8+
- SQLite (included with Python)
- FastAPI
- SQLAlchemy
- Pydantic
- Uvicorn

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/assetflow.git
   cd assetflow
