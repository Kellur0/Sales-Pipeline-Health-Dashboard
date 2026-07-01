# Sales Pipeline Health Dashboard

## Overview

This project is a prototype interactive Sales Pipeline Health Dashboard built using **Python** and **Streamlit**. The dashboard analyzes a public CRM sales pipeline dataset to help monitor pipeline health, identify bottlenecks, forecast revenue, and evaluate sales performance.

## Features

- Pipeline Value by Stage
- Average Deal Size
- Conversion Rates by Stage
- Weighted Revenue Forecast Based on Deal Probability
- Sales Representative Performance
- Interactive Filters
  - Date Range
  - Sales Representative
  - Product Category
- View Cleaned Sales Pipeline Data

## Dataset

This project uses the publicly available CRM Sales Pipeline dataset:

https://github.com/ikebude/CRM-Sales-Analysis

The data is automatically loaded from the public GitHub repository when the application starts.

## Technologies Used

- Python 3
- Streamlit
- Pandas
- Plotly Express

## Project Structure

```
sales-pipeline-dashboard/
│
├── app.py
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/sales-pipeline-dashboard.git
cd sales-pipeline-dashboard
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Dashboard

Start the Streamlit application:

```bash
streamlit run app.py
```

The dashboard will open automatically in your default web browser.

## Dashboard Metrics

The dashboard includes the following key metrics and visualizations:

- Total Pipeline Value
- Average Deal Size
- Weighted Revenue Forecast
- Win Rate
- Pipeline Value by Stage
- Average Deal Size by Stage
- Revenue Forecast by Stage
- Sales Representative Performance
- Conversion Rates by Stage

## Interactive Filters

Users can filter the dashboard by:

- Close Date
- Sales Representative
- Product Category

## Author

Created as part of a Sales Pipeline Dashboard prototype assignment using a public CRM sales pipeline dataset.
