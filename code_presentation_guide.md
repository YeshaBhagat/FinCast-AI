# 🎙️ FinCast AI: Code Presentation & Viva Defense Guide

Use this guide when presenting the project source code to your evaluators and professors. It gives you the exact sequence of files to show, what code lines to highlight, and word-for-word explanations.

---

## ⏱️ Recommended 10-Minute Presentation Flow

```
[ Minutes 0 - 4 ]: PowerPoint Presentation (Slides 1 to 14)
[ Minutes 4 - 6 ]: Live Streamlit Web App Demonstration (http://localhost:8501)
[ Minutes 6 - 8 ]: Source Code Walkthrough (data_loader -> indicators -> news_sentiment -> model)
[ Minutes 8 - 10 ]: Examiner Q&A Defense
```

---

## 🖥️ Part 1: Live Web App Demonstration (2 Minutes)

1. Open your browser to **`http://localhost:8501`**.
2. **Show the Sidebar:**
   * Point out the **Quick Watchlist pills** (`AAPL`, `NVDA`, `TSLA`, `MSFT`, `GOOGL`, `AMZN`).
   * Select a ticker (e.g., `AAPL` or `NVDA`) and click **"🚀 Run Prediction Pipeline"**.
3. **Highlight the Top KPI Cards:**
   * Show **Current Closing Price** vs **Tomorrow's Forecasted Price**.
   * Point to the **FinBERT Sentiment score** (e.g., `+0.15` Bullish) and the **Directional Hit Rate** (e.g., `60.0%`).
4. **Walk Through the 4 Tabs:**
   * **Tab 1 (Price & Technicals):** Hover over the Plotly candlestick chart, show SMA 10/30 crossovers and Bollinger Band volatility envelopes.
   * **Tab 2 (Backtest & Accuracy):** Emphasize that the red dashed predicted line tracks the blue actual line on **unseen out-of-sample data**.
   * **Tab 3 (Explainability):** Show the horizontal bar chart ranking feature importance (e.g., how much weight was given to RSI vs News Sentiment).
   * **Tab 4 (Live News):** Show actual breaking news headlines parsed with **BULLISH / BEARISH** badges.

---

## 💻 Part 2: Source Code Walkthrough (Exact Code to Show)

Open your editor and walk through these 4 core files in this exact sequence:

### 1. `src/data_loader.py` (Data Ingestion & Resilience)
* **What to show:** Function `fetch_stock_data()` and `_get_browser_session()`.
* **What to say:**
  > *"First, our data ingestion module uses `yfinance` to fetch historical OHLCV data. A major challenge with financial APIs is HTTP 429 rate-limiting. To solve this, we implemented browser session headers and an automatic local disk cache in the `data/` folder, ensuring the system operates reliably even during offline evaluations or network throttling."*

### 2. `src/indicators.py` (Quantitative Feature Engineering)
* **What to show:** Function `compute_technical_indicators()`.
* **What to say:**
  > *"Next, in `indicators.py`, we formulate 15 technical indicators capturing three fundamental market dynamics: Trend (SMA 10/30, EMA 12/26, MACD), Momentum (RSI 14 using Wilder's smoothing), and Volatility (Bollinger Bands and 10-day rolling return standard deviation). We also formulate our target variable: next-day return $\Delta P / P$."*

### 3. `src/news_sentiment.py` (Qualitative FinBERT NLP)
* **What to show:** Function `analyze_headline_sentiment()` and `analyze_news_sentiment()`.
* **What to say:**
  > *"In `news_sentiment.py`, we scrape live company headlines from Google News RSS and Yahoo Finance. Instead of generic sentiment tools like VADER—which fail to understand financial terms like 'bullish', 'crude', or 'liability'—we employ Hugging Face's `ProsusAI/finbert`, a BERT model trained on corporate filings. We calculate a continuous score between -1.0 (bearish) and +1.0 (bullish) using $P(\text{positive}) - P(\text{negative})$."*

### 4. `src/model.py` (Machine Learning & Explainability)
* **What to show:** Function `train_and_evaluate_model()`.
* **What to say:**
  > *"In `model.py`, we fuse our technical indicators with the sentiment score. Crucially, we enforce a strict forward chronological train/test split (80% train / 20% test). Standard random k-fold shuffling is disastrous in finance because it leaks future information into the past. We train a regularized XGBoost Regressor on stationary percentage returns, preventing tree scale-distortion, and extract feature importance to explain why the forecast was made."*

---

## 🛡️ Part 3: Top 7 Examiner Questions & Model Answers

### Q1: Why did you choose XGBoost instead of an LSTM or Recurrent Neural Network?
**Answer:**
> *"LSTMs are sequential neural networks that require massive training sets and are notoriously prone to overfitting noisy stock data—essentially memorizing historical market fluctuations without generalizing out-of-sample. XGBoost is the industry standard for tabular and multimodal feature sets; it trains in seconds, has built-in L1/L2 regularization (`reg_alpha`, `reg_lambda`), and provides direct feature attribution so decisions can be explained to stakeholders."*

### Q2: Why is random `train_test_split` wrong for financial stock prediction?
**Answer:**
> *"In time-series data, random splitting introduces 'lookahead bias' or data leakage. If the model trains on Wednesday's data and tests on Tuesday's data, it is essentially using future knowledge to predict the past. We use a strictly chronological split where the model only learns from the first 80% of days and is evaluated on the final 20% of unseen future trading days."*

### Q3: Why predict 'Percentage Return' instead of raw 'Dollar Price'?
**Answer:**
> *"Raw stock prices are non-stationary—a stock trading at $150 last year might trade at $340 today. Decision trees cannot extrapolate values outside the bounds of their training set. By training on daily percentage return $\frac{P_{t+1} - P_t}{P_t}$, the target variable becomes stationary and scale-invariant, allowing the model to generalize across any price level."*

### Q4: How is FinBERT better than VADER or TextBlob?
**Answer:**
> *"VADER and TextBlob are lexicon-based tools built for social media and movie reviews. In finance, words have contextual meanings: 'crude' refers to petroleum commodities, 'liability' is a standard balance sheet item, and 'beat' refers to earnings estimates. FinBERT is a transformer pre-trained on millions of financial words from corporate 10-K filings and earnings call transcripts, ensuring domain-specific semantic precision."*

### Q5: What does a 60% Directional Accuracy mean? Is that good?
**Answer:**
> *"Yes. A 50% hit rate is equivalent to a random coin flip. In professional quantitative finance and institutional algorithmic trading, achieving an out-of-sample directional hit rate between 55% and 62% on strictly forward-tested data represents a statistically significant predictive edge (alpha) that generates positive risk-adjusted returns."*

### Q6: How does the model explain its predictions?
**Answer:**
> *"We utilize XGBoost's feature importance metric, which measures the average gain brought by each feature across all boosted decision trees. Our dashboard plots this in Tab 3, showing whether today's prediction was driven more heavily by technical momentum (RSI) or by breaking news sentiment."*

### Q7: What are the limitations and future work?
**Answer:**
> *"Currently, the model predicts a 1-day ahead horizon. Future enhancements include multi-horizon forecasting (3-day and 7-day windows), integrating social sentiment from Reddit/StockTwits, and automated execution with paper trading APIs like Alpaca."*
