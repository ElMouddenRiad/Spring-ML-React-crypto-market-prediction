# PeakPredict

PeakPredict is a final-year academic project in #2024 that combines a crypto market dashboard, a Spring Boot backend, and a Python-based forecasting module.

The repository is organized as a publishable GitHub portfolio project: the web application is usable for a local demo, the backend provides authentication and portfolio management, and the machine learning module can be executed as a standalone BTC forecasting script.

## Overview

PeakPredict focuses on three main areas:

- real-time crypto market visualization
- authenticated portfolio operations
- exploratory price forecasting for Bitcoin

## Screenshots

Add your project screenshots here after publication:

- Home page preview
- Authentication flow
- Portfolio dashboard
- BTC prediction view
- ML output / API result

Example placeholders:

![Home page screenshot](docs/screenshots/home-page.png)
![Portfolio screenshot](docs/screenshots/portfolio.png)
![ML prediction screenshot](docs/screenshots/ml-prediction.png)

## Tech Stack

- Frontend: React, React Router, Axios, TradingView widgets, lightweight charts
- Backend: Spring Boot, Spring Security, JWT, JPA, MySQL
- Machine Learning: Python, pandas, NumPy, scikit-learn, XGBoost, yfinance, Matplotlib
- Data / Utilities: Selenium, SQL, CSV-based ETL

## Repository Structure

- `front/`: React user interface and chart pages
- `financePredict_back-end/financePredict/`: Spring Boot REST API
- `MachineLearning/`: BTC forecasting and ETL scripts
- `Twitter-Scrapper/`: separate experimental scraping module
- `Database/`: SQL scripts and data model artifacts

## Implemented Features

- user registration and login
- JWT-based authentication
- portfolio creation and crypto purchase flow
- test portfolio mode
- crypto price and chart visualization
- local frontend-to-backend proxy configuration

## Machine Learning Module

The machine learning module is functional as a standalone Python workflow:

- `MachineLearning/MLModel.py`: downloads BTC market data from Yahoo Finance, trains an XGBoost regression model, evaluates it with MAE and RMSE, and produces a next-day price direction estimate
- `MachineLearning/etl.py`: loads the local BTC CSV file into MySQL after basic transformation

This module is best described as an exploratory forecasting pipeline rather than a production-grade ML system.

## Known Limitations

This project was built as an academic prototype, so some parts still need hardening before production use:

- passwords and secrets should be externalized and hashed consistently
- the experimental scraping module is fragile and depends on third-party UI behavior
- the ML workflow is not yet exposed through a dedicated production API
- automated test coverage is still limited

## Recommended Improvements

- move all secrets to environment variables
- replace fragile scraping with official APIs where possible
- package the ML workflow behind a clean service endpoint
- add unit and integration tests for auth, portfolio, and forecasting flows
- introduce CI for build and regression checks

## Local Setup

### Prerequisites

- Node.js 18+
- Java 21
- MySQL 8+
- Python 3.10+

### Backend

From `financePredict_back-end/financePredict`:

```bash
./gradlew bootRun
```

On Windows PowerShell:

```powershell
.\gradlew.bat bootRun
```

Backend URL: `http://localhost:8080`

### Frontend

From `front`:

```bash
npm install
npm start
```

Frontend URL: `http://localhost:3000`

### Machine Learning Script

From `MachineLearning`:

```bash
python MLModel.py
```

For ETL loading:

```bash
python etl.py
```

## License

No license has been added yet. Add one before public release if the repository is intended to be open source.
