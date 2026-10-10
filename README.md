# Fulfillment Hub

## Overview
Fulfillment Hub is a Streamlit-based application for managing e-commerce order fulfillment and inventory operations.

## Features
- **Dashboard:** View order fulfillment metrics and identify orders that need attention.
- **Orders:** Search, filter, and update order statuses.
- **Inventory:** Review stock availability and identify inventory issues.
- **Packing & Pickup:** Verify order details before packing and view courier recommendations.
- **Action Tracking:** Record operational actions and status updates.

## Technologies Used
- Python
- Streamlit
- Pandas
- CSV files for data storage

## Project Structure
```text
fulfillment-hub/
├── app.py
├── requirements.txt
├── README.md
└── data/
    ├── orders.csv
    ├── inventory.csv
    ├── products.csv
    └── couriers.csv
```

## How to Run
1. Install Python.
2. Open a terminal in the project folder.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Start the application:

   `streamlit run app.py`

5. Open the local URL displayed in the terminal.

## Notes
The application uses CSV files in the `data` folder. Keep these files in place when running the application.
