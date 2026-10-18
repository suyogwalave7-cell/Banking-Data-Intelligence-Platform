
# Banking Data Intelligence Platform

## Project Overview
An end-to-end banking transaction analysis project built using Python and Pandas to explore financial transaction patterns and identify potential fraudulent activities.

## Dataset
- **Dataset:** PaySim Financial Transactions
- **Total Transactions:** 6,362,620
- **Total Columns:** 11
- **Fraud Transactions:** 8,213
- **Overall Fraud Rate:** 0.1291%

The dataset CSV is not included in this repository because of its large size. Add the official dataset source link here after verifying the source.

## Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Jupyter Notebook
- Git and GitHub

## Key Business Insights
- Fraud transactions were identified in CASH_OUT and TRANSFER transaction types.
- Average fraud transaction amount: approximately 1,467,967.30.
- Average non-fraud transaction amount: approximately 178,197.04.
- Overall fraud rate: approximately 0.1291%.

## Project Structure
```text
Banking_Data_Intelligence_Platform/
├── data/
├── notebooks/
│   └── 01_paysim_data_exploration.ipynb
├── outputs/
│   ├── charts/
│   └── reports/
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup Instructions

1. Clone this repository:
   `git clone https://github.com/suyogwalave7-cell/Banking-Data-Intelligence-Platform.git`

2. Open the project folder:
   `cd Banking-Data-Intelligence-Platform`

3. Install the required libraries:
   `pip install -r requirements.txt`

4. Download the PaySim dataset from its verified source and place the CSV file inside the `data/` folder.

5. Open `notebooks/01_paysim_data_exploration.ipynb` in Jupyter Notebook or VS Code and run the cells in order.

## Project Status
Exploratory data analysis completed. Further development and validation will be documented as the project progresses.

## Disclaimer
This project uses a simulated financial transaction dataset for educational and analytical purposes. Findings from this dataset should not be treated as proof of fraud in real banking transactions.
