
# Vanguard Horizons Capital - Data Pipeline with Snowflake, dlt, dbt, and Power BI

## Overview

This repository demonstrates an end-to-end data pipeline for **Vanguard Horizons Capital**, utilizing **Snowflake**, **dlt Hub**, **dbt**, and **Power BI**. The pipeline ingests data from a **SQLite** database (`AssetFlow`), transforms it into business-ready datasets, and visualizes key metrics in Power BI dashboards.

### Key Components:

1. **Source Database**: 
   - `AssetFlow.sqlite`: The SQLite database containing raw financial data, including **assets**, **trades**, and **portfolios**.
   
2. **Ingestion Framework**: 
   - **DLT Hub**: Automates data extraction from SQLite and loads it into **Snowflake**. The process is orchestrated to ensure efficient and scalable ingestion.
   
3. **Transformation Layer**: 
   - **dbt (Data Build Tool)**: Applies transformations to the raw data in Snowflake, converting it into business-friendly tables for reporting. Business logic includes calculating portfolio values, asset performance, and daily returns.

4. **Visualization**:
   - **Power BI**: Reports and dashboards are built on the transformed data from Snowflake, providing real-time insights into **portfolio performance**, **asset allocation**, and **trade activity**.

---

## Data Pipeline Architecture

The following steps outline the architecture of the pipeline:

1. **Source Data (SQLite Database)**:
   - The `AssetFlow` SQLite database is the primary data source. It contains information on:
     - **Assets**: Stocks, bonds, cryptocurrencies, etc.
     - **Portfolios**: Investor portfolios that hold multiple assets.
     - **Trades**: Transactions executed for buying/selling assets.

2. **Data Ingestion via DLT Hub**:
   - **DLT Hub** is responsible for extracting the data from the SQLite database and loading it into **Snowflake**. The ingestion process is automated and scheduled to ensure up-to-date data is available for analysis.

3. **Snowflake Data Warehouse**:
   - The data is organized into layers within **Snowflake**:
     - **Raw Layer**: Directly loaded data from SQLite with minimal transformation.
     - **Staging Layer**: Cleaned and standardized data, ready for business transformations.
     - **Transformation Layer**: Final, business-focused datasets that are ready for reporting.

4. **Data Transformation with dbt**:
   - **dbt** is used to transform raw and staging data in Snowflake. The transformations involve:
     - **Calculating AUM (Assets Under Management)**.
     - **Calculating daily portfolio values and returns**.
     - **Summarizing trade activity**.
     - **Calculating asset performance over time**.

5. **Reporting in Power BI**:
   - Power BI connects directly to Snowflake to visualize the transformed data.
   - Key dashboards include:
     - **Portfolio Performance**: Track the value of investor portfolios over time.
     - **Asset Allocation**: Visualize the breakdown of assets held by the fund.
     - **Trade Activity**: Review all trades, including buy/sell transactions and their impact on the portfolios.
     - **AUM Tracking**: Real-time visualization of the total assets under management.

---

## Setup Instructions

### Prerequisites

Before setting up the pipeline, ensure you have the following:

- **Snowflake account**: Access to a Snowflake data warehouse.
- **DLT Hub**: Installed and configured for data orchestration.
- **dbt**: Installed locally or in your environment to run transformations.
- **Power BI**: Installed or access to Power BI online for visualization.

### Step 1: Ingest Data with DLT Hub

1. Configure DLT Hub to extract data from the `AssetFlow` SQLite database.
2. Set up Snowflake as the destination for the ingested data.
3. Schedule the ingestion pipeline to run at regular intervals.

### Step 2: Transform Data with dbt

1. Clone the repo and navigate to the dbt folder:
   ```bash
   git clone https://github.com/derruba2000/vanguard-horizons-capital.git
   cd vanguard-horizons-capital/dbt
   ```
2. Configure your **profiles.yml** to connect dbt to Snowflake.
3. Run the dbt models to transform the data:
   ```bash
   dbt run
   ```
   This will apply all the transformations and create the necessary business-ready tables in Snowflake.

4. Optional: Run dbt tests to ensure data quality:
   ```bash
   dbt test
   ```

### Step 3: Reporting with Power BI

1. Open **Power BI Desktop** or Power BI Online.
2. Connect Power BI to the Snowflake instance.
3. Load the transformed datasets (e.g., portfolio performance, trade activity) into Power BI.
4. Build the following reports:
   - **AUM Dashboard**: Displaying total assets under management.
   - **Portfolio Performance**: Tracking portfolio values over time.
   - **Trade Activity Report**: Showing all trade transactions.
5. Publish the reports for real-time monitoring.

---

## Contribution

We welcome contributions! If you'd like to improve this project or add features:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add your feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/your-feature
   ```
5. Open a pull request.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.

---

## Contact

For any questions or feedback, please reach out to:

- **Name**: João Ramos
- **Email**: correia_ramos@hotmail.com

