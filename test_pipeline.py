import sys
from src.data_loader import fetch_stock_data
from src.indicators import compute_technical_indicators
from src.news_sentiment import analyze_news_sentiment
from src.model import prepare_multimodal_dataset, train_and_evaluate_model

def run_test():
    print("Step 1: Testing yfinance stock data fetch for AAPL...")
    df, meta = fetch_stock_data("AAPL", period="6mo")
    print(f"-> Fetched {len(df)} price rows for {meta['shortName']}. Current: ${meta['currentPrice']:.2f}")

    print("\nStep 2: Testing technical indicator engineering...")
    data_ind, features = compute_technical_indicators(df)
    print(f"-> Engineered {len(features)} technical indicators: {features[:5]}...")

    print("\nStep 3: Testing live news & sentiment scoring...")
    score, dist, articles = analyze_news_sentiment("AAPL", max_articles=5)
    print(f"-> Fetched {len(articles)} headlines. Sentiment score: {score:.3f}. Dist: {dist}")

    print("\nStep 4: Testing multimodal fusion & XGBoost training...")
    fused, all_features = prepare_multimodal_dataset(data_ind, features, score)
    results = train_and_evaluate_model(fused, all_features)
    metrics = results["metrics"]
    forecast = results["forecast"]
    print(f"-> Training complete! R2 Score: {metrics['r2_score']}, Hit Rate: {metrics['directional_accuracy_pct']}%, Forecast: ${forecast['predicted_price']:.2f} ({forecast['trend'].encode('ascii', 'ignore').decode('ascii').strip()})")
    print("\nSUCCESS: All pipeline modules are operational!")

if __name__ == "__main__":
    run_test()
