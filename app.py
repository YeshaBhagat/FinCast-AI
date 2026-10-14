"""
FinCast AI: Multimodal Stock & Sentiment Predictor
Streamlit Web Application
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.data_loader import fetch_stock_data
from src.indicators import compute_technical_indicators
from src.news_sentiment import analyze_news_sentiment
from src.model import prepare_multimodal_dataset, train_and_evaluate_model


# ---------------------------------------------------------
# Page Configuration & Custom CSS Aesthetics
# ---------------------------------------------------------
st.set_page_config(
    page_title="FinCast AI | Multimodal Stock & Sentiment Predictor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for a sleek, modern financial dashboard
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    
    .badge-bullish {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    .badge-bearish {
        background-color: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }

    .badge-neutral {
        background-color: rgba(148, 163, 184, 0.15);
        color: #94a3b8;
        border: 1px solid rgba(148, 163, 184, 0.3);
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
    }

    .metric-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    
    .metric-title {
        color: #94a3b8;
        font-size: 0.82rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 6px;
    }
    
    .metric-val {
        font-size: 1.75rem;
        font-weight: 700;
        color: #f8fafc;
    }

    .news-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 10px;
        transition: transform 0.2s ease;
    }
    .news-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/bullish.png", width=64)
    st.title("FinCast AI")
    st.caption("Multimodal Quantitative & FinBERT Predictor")
    st.divider()

    st.subheader("⚙️ Asset Configuration")

    # Quick selection pills
    quick_tickers = ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL", "AMZN"]
    selected_quick = st.pills("Quick Watchlist", quick_tickers, default="AAPL")

    ticker_input = st.text_input("Ticker Symbol", value=selected_quick or "AAPL").upper()
    time_period = st.selectbox("Historical Lookback", options=["6mo", "1y", "2y", "5y"], index=2)

    st.divider()
    st.subheader("🧠 Model Architecture")
    st.markdown("""
    * **Market Engine:** yfinance (OHLCV)
    * **Technicals:** SMA, EMA, MACD, RSI, Bollinger Bands
    * **NLP Brain:** FinBERT (Hugging Face)
    * **ML Regressor:** XGBoost Regularized
    """)

    st.divider()
    run_btn = st.button("🚀 Run Prediction Pipeline", type="primary", width="stretch")


# ---------------------------------------------------------
# Main Application Content
# ---------------------------------------------------------

# Header Banner
st.markdown(f"""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; color: #ffffff; font-size: 2.2rem; font-weight: 800; letter-spacing: -0.02em;">
                FinCast AI <span style="font-weight: 400; font-size: 1.4rem; color: #818cf8;">| Multimodal Market Intelligence</span>
            </h1>
            <p style="margin: 8px 0 0 0; color: #94a3b8; font-size: 1rem;">
                Bridging quantitative technical indicators with deep financial NLP sentiment for next-day stock forecasting.
            </p>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(99, 102, 241, 0.2); border: 1px solid #6366f1; color: #a5b4fc; padding: 6px 14px; border-radius: 8px; font-weight: 600; font-size: 0.9rem;">
                Active Ticker: {ticker_input}
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Execute Pipeline
if run_btn or 'initialized' not in st.session_state:
    st.session_state['initialized'] = True

    with st.spinner(f"Ingesting market data & analyzing live news sentiment for {ticker_input}..."):
        try:
            # 1. Fetch Price Data & Indicators
            raw_df, meta = fetch_stock_data(ticker_input, period=time_period)
            data_with_indicators, feature_cols = compute_technical_indicators(raw_df)

            # 2. Fetch News and Calculate FinBERT Sentiment
            sentiment_score, sentiment_dist, articles = analyze_news_sentiment(ticker_input, max_articles=12)

            # 3. Fuse Dataset and Train XGBoost
            fused_df, all_features = prepare_multimodal_dataset(data_with_indicators, feature_cols, sentiment_score)
            pipeline_results = train_and_evaluate_model(fused_df, all_features)

            forecast = pipeline_results["forecast"]
            metrics = pipeline_results["metrics"]
            feature_imp = pipeline_results["feature_importance"]
            test_results = pipeline_results["test_results"]

            # Save in session state for smooth tab transitions
            st.session_state['results'] = {
                'raw_df': raw_df,
                'data_with_indicators': data_with_indicators,
                'meta': meta,
                'sentiment_score': sentiment_score,
                'sentiment_dist': sentiment_dist,
                'articles': articles,
                'forecast': forecast,
                'metrics': metrics,
                'feature_imp': feature_imp,
                'test_results': test_results
            }

        except Exception as e:
            st.error(f"⚠️ Error executing pipeline: {e}")
            st.stop()


# If results are ready, render the dashboard
if 'results' in st.session_state:
    res = st.session_state['results']
    meta = res['meta']
    forecast = res['forecast']
    metrics = res['metrics']
    sentiment_dist = res['sentiment_dist']
    sentiment_score = res['sentiment_score']
    articles = res['articles']
    raw_df = res['raw_df']
    data_with_indicators = res['data_with_indicators']
    feature_imp = res['feature_imp']
    test_results = res['test_results']

    # --- TOP ROW: KPI SUMMARY CARDS ---
    col1, col2, col3, col4, col5 = st.columns(5)

    is_bullish = forecast['expected_change'] >= 0
    change_color = "#10b981" if is_bullish else "#ef4444"
    trend_badge_class = "badge-bullish" if is_bullish else "badge-bearish"

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Current Price</div>
            <div class="metric-val">${forecast['current_price']:.2f}</div>
            <span style="color: #64748b; font-size: 0.8rem;">{meta['currency']} · {meta['shortName']}</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Tomorrow Forecast</div>
            <div class="metric-val" style="color: {change_color};">${forecast['predicted_price']:.2f}</div>
            <span class="{trend_badge_class}">{forecast['trend']}</span>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Expected Change</div>
            <div class="metric-val" style="color: {change_color};">{forecast['expected_change']:+.2f} ({forecast['expected_change_pct']:+.2f}%)</div>
            <span style="color: #64748b; font-size: 0.8rem;">Model Output Delta</span>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        sentiment_label = "BULLISH" if sentiment_score > 0.05 else ("BEARISH" if sentiment_score < -0.05 else "NEUTRAL")
        sent_color = "#10b981" if sentiment_label == "BULLISH" else ("#ef4444" if sentiment_label == "BEARISH" else "#94a3b8")
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">FinBERT Sentiment</div>
            <div class="metric-val" style="color: {sent_color};">{sentiment_score:+.2f}</div>
            <span style="color: #94a3b8; font-size: 0.8rem;">{sentiment_dist['positive_pct']}% Pos | {sentiment_dist['negative_pct']}% Neg</span>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Test Direction Accuracy</div>
            <div class="metric-val" style="color: #38bdf8;">{metrics['directional_accuracy_pct']}%</div>
            <span style="color: #64748b; font-size: 0.8rem;">R² Score: {metrics['r2_score']} | MAE: ${metrics['mae']}</span>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    # --- MAIN INTERACTIVE TABS ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Price & Technicals",
        "🎯 Backtest & Accuracy",
        "💡 Model Explainability (Feature Importance)",
        "📰 Live News & FinBERT Breakdown"
    ])

    # TAB 1: INTERACTIVE PRICE CHART WITH TECHNICALS
    with tab1:
        st.subheader(f"📈 {meta['shortName']} ({ticker_input}) Technical Price Chart")

        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.08,
            row_heights=[0.75, 0.25],
            specs=[[{"secondary_y": False}], [{"secondary_y": False}]]
        )

        # Candlestick
        fig.add_trace(go.Candlestick(
            x=data_with_indicators.index,
            open=data_with_indicators['Open'],
            high=data_with_indicators['High'],
            low=data_with_indicators['Low'],
            close=data_with_indicators['Close'],
            name='OHLC Price',
            increasing_line_color='#10b981',
            decreasing_line_color='#ef4444'
        ), row=1, col=1)

        # Moving Averages
        fig.add_trace(go.Scatter(
            x=data_with_indicators.index, y=data_with_indicators['SMA_10'],
            mode='lines', name='SMA 10 (Short)', line=dict(color='#f59e0b', width=1.5)
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=data_with_indicators.index, y=data_with_indicators['SMA_30'],
            mode='lines', name='SMA 30 (Medium)', line=dict(color='#6366f1', width=1.5)
        ), row=1, col=1)

        # Bollinger Bands
        fig.add_trace(go.Scatter(
            x=data_with_indicators.index, y=data_with_indicators['BB_Upper'],
            mode='lines', name='Upper Bollinger', line=dict(color='rgba(148, 163, 184, 0.4)', dash='dot', width=1)
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=data_with_indicators.index, y=data_with_indicators['BB_Lower'],
            mode='lines', name='Lower Bollinger', line=dict(color='rgba(148, 163, 184, 0.4)', dash='dot', width=1),
            fill='tonexty', fillcolor='rgba(99, 102, 241, 0.05)'
        ), row=1, col=1)

        # Volume Bar Chart
        colors = ['#10b981' if c >= o else '#ef4444' for c, o in zip(data_with_indicators['Close'], data_with_indicators['Open'])]
        fig.add_trace(go.Bar(
            x=data_with_indicators.index, y=data_with_indicators['Volume'],
            name='Volume', marker_color=colors, opacity=0.6
        ), row=2, col=1)

        fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(15, 23, 42, 0.4)',
            paper_bgcolor='rgba(15, 23, 42, 0.0)',
            height=580,
            xaxis_rangeslider_visible=False,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig, width="stretch")

    # TAB 2: BACKTEST & ACCURACY
    with tab2:
        st.subheader("🎯 Chronological Out-of-Sample Test Set Validation")
        st.markdown("""
        To prevent lookahead bias (data leakage), the model is trained on the first **80%** of historical data 
        and evaluated strictly on the final unseen **20%** of trading days.
        """)

        backtest_fig = go.Figure()

        backtest_fig.add_trace(go.Scatter(
            x=test_results.index,
            y=test_results['Actual_Close'],
            mode='lines',
            name='Actual Closing Price',
            line=dict(color='#38bdf8', width=2.5)
        ))

        backtest_fig.add_trace(go.Scatter(
            x=test_results.index,
            y=test_results['Predicted_Close'],
            mode='lines',
            name='XGBoost Predicted Price',
            line=dict(color='#f43f5e', width=2, dash='dash')
        ))

        backtest_fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(15, 23, 42, 0.4)',
            paper_bgcolor='rgba(15, 23, 42, 0.0)',
            height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(backtest_fig, width="stretch")

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric("R² Goodness of Fit", f"{metrics['r2_score']}")
        m_col2.metric("Root Mean Squared Error (RMSE)", f"${metrics['rmse']}")
        m_col3.metric("Mean Absolute Error (MAE)", f"${metrics['mae']}")
        m_col4.metric("Directional Hit Rate", f"{metrics['directional_accuracy_pct']}%")

    # TAB 3: FEATURE IMPORTANCE
    with tab3:
        st.subheader("💡 What Drove the AI's Forecast? (Feature Importance)")
        st.markdown("""
        XGBoost calculates the **relative gain** of each feature across all boosted decision trees, 
        illustrating how much the model relied on technical indicators vs sentiment analysis.
        """)

        top_features = feature_imp.head(10).sort_values(by='Importance', ascending=True)

        imp_fig = go.Figure(go.Bar(
            x=top_features['Importance'],
            y=top_features['Feature'],
            orientation='h',
            marker=dict(
                color=top_features['Importance'],
                colorscale='Viridis',
                showscale=False
            )
        ))

        imp_fig.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(15, 23, 42, 0.4)',
            paper_bgcolor='rgba(15, 23, 42, 0.0)',
            height=420,
            xaxis_title="Relative Feature Importance Score",
            margin=dict(l=10, r=10, t=20, b=20)
        )
        st.plotly_chart(imp_fig, width="stretch")

    # TAB 4: LIVE NEWS & FINBERT SENTIMENT
    with tab4:
        st.subheader(f"📰 Live Financial News Sentiment Analysis for {ticker_input}")

        p_col, neu_col, n_col = st.columns(3)
        p_col.metric("Bullish News %", f"{sentiment_dist['positive_pct']}%", delta="Positive")
        neu_col.metric("Neutral News %", f"{sentiment_dist['neutral_pct']}%")
        n_col.metric("Bearish News %", f"{sentiment_dist['negative_pct']}%", delta="-Negative", delta_color="inverse")

        st.divider()

        if not articles:
            st.info("No recent news headlines found for this ticker.")
        else:
            for art in articles:
                lbl = art.get('label', 'neutral').lower()
                badge_class = "badge-bullish" if lbl == 'positive' else ("badge-bearish" if lbl == 'negative' else "badge-neutral")
                score_val = art.get('score', 0.0)

                st.markdown(f"""
                <div class="news-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
                        <a href="{art.get('link', '#')}" target="_blank" style="color: #f1f5f9; text-decoration: none; font-weight: 600; font-size: 1rem; line-height: 1.4;">
                            {art.get('title')}
                        </a>
                        <span class="{badge_class}" style="margin-left: 12px; white-space: nowrap;">
                            {lbl.upper()} ({score_val:+.2f})
                        </span>
                    </div>
                    <div style="color: #64748b; font-size: 0.8rem;">
                        <span>{art.get('publisher', 'Financial Press')}</span> · <span>{art.get('published', 'Recent')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
