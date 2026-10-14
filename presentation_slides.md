# 📑 FinCast AI: 14-Slide Presentation Content & Speaker Notes

This document contains the exact slide content and spoken script matching the generated [FinCast_AI_Presentation.pptx](file:///e:/ML_Project/FinCast_AI_Presentation.pptx).

---

### Slide 1: Title Slide
* **Title:** FinCast AI: Multimodal Stock & Sentiment Predictor
* **Subtitle:** Combining Quantitative Technical Indicators with FinBERT Financial News NLP for Next-Day Stock Forecasting
* **Details:** Presented by Project Candidate | Department of Computer Science & Engineering
* **Spoken Script:**
  > *"Good morning respected evaluators and panel members. Today, I am presenting 'FinCast AI', a multimodal market intelligence system designed to forecast stock price movements by synthesizing quantitative technical charts and real-time qualitative financial news sentiment."*

---

### Slide 2: Introduction & Market Motivation
* **Key Points:**
  * Financial markets react to both numbers and real-world events.
  * Quantitative technical analysis (SMA, RSI) provides historical trend structure.
  * Qualitative catalysts (breaking news, earnings reports) trigger immediate market reactions.
  * Pure numerical models lag behind breaking news.
* **Spoken Script:**
  > *"Traditional stock predictors fail because they analyze past prices in isolation. But in reality, when a CEO resigns or earnings beat expectations, stock prices move immediately. A human trader looks at both charts and news; our project equips machine learning to do both simultaneously."*

---

### Slide 3: Problem Statement
* **Key Points:**
  1. Single-Stream Blindness: Ignoring news leaves models vulnerable to sudden shocks.
  2. Human Information Overload: Thousands of global headlines published hourly.
  3. Generic NLP Inadequacy: Off-the-shelf tools (like VADER) fail on financial terminology.
  4. Deep Learning Overfitting: Sequential models (LSTMs) memorize historical noise and lack explainability.
* **Spoken Script:**
  > *"Our research addresses four core bottlenecks: standard algorithms are blind to unstructured news; traders cannot manually process the overwhelming flood of financial press; generic sentiment dictionaries misclassify financial words; and complex deep neural networks like LSTMs overfit heavily on market noise."*

---

### Slide 4: Explicit Project Objectives
* **Key Points:**
  * Objective 1: Build an automated, resilient market data ingestion pipeline with caching.
  * Objective 2: Engineer 15 trend, momentum, and volatility indicators.
  * Objective 3: Implement FinBERT NLP to calculate normalized continuous sentiment in $[-1.0, +1.0]$.
  * Objective 4: Train a regularized XGBoost model using forward chronological splitting and deploy an interactive Streamlit UI.
* **Spoken Script:**
  > *"To solve this, we defined four specific objectives: automated live data ingestion; 15 mathematical technical indicators; an NLP pipeline utilizing FinBERT; and an ensemble XGBoost model deployed as an interactive web dashboard."*

---

### Slide 5: Literature Survey & Technical Comparison
* **Comparison Table:**
  * ARIMA: Quantitative only, zero NLP, linear.
  * LSTMs: High complexity, high overfitting, black-box.
  * VADER + Random Forest: Naive lexicon, weak financial nuance.
  * FinCast AI: Multimodal, FinBERT Transformer, regularized XGBoost, high explainability.
* **Spoken Script:**
  > *"Comparing our architecture with existing academic literature: ARIMA is strictly linear and lacks textual input; LSTMs suffer from severe out-of-sample degradation and opacity; whereas our multimodal pipeline achieves domain-specific semantic understanding and transparent feature attribution."*

---

### Slide 6: System Architecture
* **Flowchart Steps:**
  1. Data Ingestion (yfinance + Google RSS)
  2. Quantitative Indicator Engine (15 features)
  3. FinBERT NLP Brain (Softmax probabilities)
  4. XGBoost Regularized Regressor (Stationary return target)
  5. Streamlit Interactive Dashboard
* **Spoken Script:**
  > *"Here is the complete system architecture. Market data flows through our indicator engine, while live news flows through the FinBERT transformer. Both streams converge into a unified multimodal feature matrix fed into an XGBoost Regressor."*

---

### Slide 7: Quantitative Feature Engineering
* **Key Indicators:**
  * Trend: SMA 10, SMA 30, EMA 12/26, MACD, SMA Ratio.
  * Momentum: 14-period RSI (Wilder's smoothing).
  * Volatility: Bollinger Bands (20-day, $2\sigma$), Rolling standard deviation.
  * Volume: Volume Ratio normalized against 10-day moving average.
* **Spoken Script:**
  > *"Our quantitative engine calculates 15 features covering trend direction, momentum exhaustion via RSI, volatility bands, and volume momentum. Importantly, we formulate our target as stationary percentage returns $\Delta P / P$ to prevent scale distortion."*

---

### Slide 8: Qualitative NLP: FinBERT Deep Sentiment Engine
* **Key Points:**
  * FinBERT is pre-trained on corporate 10-Ks, earnings transcripts, and analyst research.
  * Distinguishes contextual words: 'crude' (oil), 'liability' (balance sheet item), 'bullish'.
  * Scoring formula: $\text{Score} = P(\text{Positive}) - P(\text{Negative}) \in [-1.0, +1.0]$.
* **Spoken Script:**
  > *"Why FinBERT? General sentiment models misinterpret financial vocabulary. FinBERT produces calibrated probabilities for Positive, Negative, and Neutral. We take the difference between positive and negative probabilities to generate a continuous score from minus one to plus one."*

---

### Slide 9: Machine Learning Methodology & Training Protocol
* **Key Points:**
  * Strict Chronological Split: 80% past train / 20% future test (No random shuffling).
  * Stationary Return Target: Predicts $\Delta P / P$, then scales to tomorrow's dollar price.
  * Regularized XGBoost: `max_depth=3`, `learning_rate=0.03`, L1 (`reg_alpha=0.5`), L2 (`reg_lambda=2.0`).
* **Spoken Script:**
  > *"A critical methodological contribution of our project is avoiding lookahead bias. We strictly preserve time order with an 80/20 chronological split. Furthermore, training on percentage returns ensures our tree models remain scale-invariant across any price range."*

---

### Slide 10: Experimental Results & Performance Evaluation
* **Results Achieved:**
  * $R^2$ Goodness of Fit: **0.8816**
  * Directional Hit Rate: **60.0%+**
  * Mean Absolute Error: **$4.09**
  * Root Mean Squared Error: **$5.12**
* **Spoken Script:**
  > *"On out-of-sample unseen testing data, our model achieved an $R^2$ of 0.88 and a directional hit rate of 60%. In quantitative trading, any hit rate above 55% represents a statistically meaningful predictive edge."*

---

### Slide 11: Transparent AI: Feature Importance Analysis
* **Key Points:**
  * Measures XGBoost feature gain across all decision tree splits.
  * Multimodal synergy: Sentiment acts as a breakout trigger, while RSI and moving averages act as trend anchors.
* **Spoken Script:**
  > *"Our system is completely explainable. Through XGBoost's feature gain metrics, we can prove to stakeholders whether a forecast was driven by technical momentum or by breaking market sentiment."*

---

### Slide 12: Interactive Dashboard Deployment (`app.py`)
* **Key Features:**
  * Quick asset watchlist pills (`AAPL`, `NVDA`, `TSLA`, `MSFT`, `GOOGL`, `AMZN`).
  * Live KPI forecast metrics and sentiment distribution cards.
  * Plotly candlestick charts, backtest overlays, and parsed news headlines.
* **Spoken Script:**
  > *"We packaged the entire pipeline into an interactive web application built with Streamlit and Plotly, allowing users to switch tickers and view real-time forecasts, backtest curves, and news sentiment cards."*

---

### Slide 13: Future Scope & Extensions
* **Extensions:**
  * Multi-horizon forecasting (3-day, 7-day windows).
  * Social sentiment from Reddit (r/wallstreetbets) and StockTwits.
  * Automated paper trading execution with Alpaca API.
* **Spoken Script:**
  > *"Future work will expand the prediction horizon to multi-day forecasts and incorporate retail investor sentiment from social communities."*

---

### Slide 14: Conclusion & Q&A
* **Summary:**
  * Successfully demonstrated multimodal fusion outperforming single-mode stock predictors.
  * Delivered a complete pipeline: data ingestion, technical indicators, FinBERT NLP, XGBoost modeling, and web UI.
* **Spoken Script:**
  > *"In conclusion, FinCast AI proves that merging technical market indicators with deep financial NLP sentiment produces superior, explainable stock forecasts. Thank you for your time. I am now open to your questions."*
