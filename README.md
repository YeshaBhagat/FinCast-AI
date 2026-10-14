# 📊 FinCast AI: Multimodal Stock & Sentiment Predictor

> **Combining Quantitative Technical Indicators with FinBERT Financial News NLP for Next-Day Stock Forecasting**

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.14-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io/)
[![Model](https://img.shields.io/badge/XGBoost-Gradient%20Boosting-orange.svg)](https://xgboost.readthedocs.io/)
[![NLP](https://img.shields.io/badge/HuggingFace-FinBERT-yellow.svg)](https://huggingface.co/ProsusAI/finbert)

---

## 📌 Project Overview

Traditional market prediction software relies purely on historical price figures. However, financial markets react rapidly to qualitative, real-world events such as breaking news headlines, earnings reports, and macroeconomic disclosures.

**FinCast AI** is a multimodal financial intelligence platform that merges both data streams into an ensemble machine learning pipeline:
1. **Quantitative Market Stream:** Historical daily OHLCV prices, trend indicators (SMA 10, SMA 30, EMA, MACD), momentum metrics (RSI 14), volatility indicators (Bollinger Bands), and volume momentum.
2. **Qualitative NLP Stream:** Real-time news headlines parsed through **FinBERT** (a BERT transformer explicitly pre-trained on corporate financial corpora) to compute a continuous market sentiment score $[-1.0, +1.0]$.
3. **Forecasting Engine:** An **XGBoost Regressor** trained with strict chronological out-of-sample testing (preventing lookahead bias / data leakage) to generate tomorrow's price forecast and directional movement.
4. **Interactive Dashboard:** A modern **Streamlit** web application with interactive Plotly candlestick charts, backtest overlays, feature importance rankings, and real-time news feeds with sentiment badges.

---

## 🏗️ System Architecture

```
[ yfinance Live Data ] ──► Technical Feature Engineering (SMA, RSI, MACD, BB) ──┐
                                                                                  ├──► [ XGBoost Regressor ] ──► [ Streamlit Dashboard ]
[ Live Financial News ] ─► FinBERT Deep NLP Sentiment Scoring [-1.0, +1.0] ──────┘
```

---

## 📂 Project Structure

```
ML_Project/
│
├── .venv/                   # Virtual environment
├── src/
│   ├── __init__.py          # Package initialization
│   ├── data_loader.py       # Stock price ingestion & company metadata via yfinance
│   ├── indicators.py        # Technical indicator calculations (RSI, SMA, MACD, BB)
│   ├── news_sentiment.py    # Live financial news scraping & FinBERT sentiment analysis
│   └── model.py             # XGBoost model training, chronological split & forecasting
│
├── app.py                   # Full interactive Streamlit dashboard
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

### 1. Clone or Open the Repository
```powershell
cd e:\ML_Project
```

### 2. Activate the Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Required Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Launch the Dashboard
```powershell
streamlit run app.py
```
The app will automatically open in your default web browser at `http://localhost:8501`.

---

## 🧠 Key Academic & Technical Highlights

* **No Data Leakage:** Avoids standard random cross-validation. Employs a strict forward chronological train/test split (80% past / 20% future).
* **Domain-Specific NLP:** Uses `ProsusAI/finbert` instead of naive sentiment tools (like VADER) to preserve financial semantic nuance (e.g., distinguishing between "bearish growth" vs "organic growth").
* **Transparent Explainability:** Exposes XGBoost feature importance scores to show users whether a forecast was driven primarily by price momentum or by breaking news.
