"""
Financial News Ingestion and FinBERT Sentiment Analysis Module for FinCast AI
Fetches live market news and evaluates financial sentiment using Hugging Face FinBERT.
"""

from typing import List, Dict, Any, Tuple
import datetime
import urllib.parse
import xml.etree.ElementTree as ET
import requests
import yfinance as yf

# Global cache for the NLP model pipeline
_FINBERT_PIPELINE = None


def get_finbert_pipeline():
    """
    Lazy loads and caches the ProsusAI/finbert pipeline in memory.
    Falls back gracefully if transformers/torch is unavailable.
    """
    global _FINBERT_PIPELINE
    if _FINBERT_PIPELINE is not None:
        return _FINBERT_PIPELINE

    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
        model_name = "ProsusAI/finbert"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        _FINBERT_PIPELINE = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer, return_all_scores=True)
        return _FINBERT_PIPELINE
    except Exception as e:
        print(f"[FinBERT Warning] Could not load FinBERT directly ({e}). Using financial lexicon fallback.")
        return None


def fetch_company_news(ticker: str, max_articles: int = 15) -> List[Dict[str, Any]]:
    """
    Fetches real-time financial news headlines from yfinance and Google News RSS.

    Args:
        ticker: Stock symbol (e.g. 'AAPL', 'NVDA')
        max_articles: Maximum number of recent articles to return

    Returns:
        List of dictionaries with 'title', 'publisher', 'published', 'link'
    """
    clean_ticker = ticker.strip().upper()
    articles: List[Dict[str, Any]] = []
    seen_titles = set()

    # 1. Fetch from yfinance news API
    try:
        stock = yf.Ticker(clean_ticker)
        yf_news = stock.news or []
        for item in yf_news:
            title = ""
            publisher = "Financial Media"
            link = ""
            pub_date = "Recent"

            # Support both older and modern yfinance payload schemas
            if isinstance(item, dict):
                content = item.get("content", {}) if "content" in item else item
                title = content.get("title") or item.get("title", "")
                publisher = (
                    content.get("provider", {}).get("displayName")
                    or item.get("publisher")
                    or "Yahoo Finance"
                )
                link = (
                    content.get("canonicalUrl", {}).get("url")
                    or item.get("link", "")
                )
                pub_time = item.get("providerPublishTime")
                if pub_time:
                    try:
                        pub_date = datetime.datetime.fromtimestamp(pub_time).strftime("%Y-%m-%d %H:%M")
                    except Exception:
                        pub_date = "Recent"

            if title and title.lower() not in seen_titles:
                seen_titles.add(title.lower())
                articles.append({
                    "title": title.strip(),
                    "publisher": publisher,
                    "published": pub_date,
                    "link": link
                })
    except Exception as e:
        print(f"[News Ingestion] yfinance news warning: {e}")

    # 2. Fetch from Google News RSS feed for additional headlines
    try:
        query = urllib.parse.quote(f"{clean_ticker} stock financial")
        rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(rss_url, headers=headers, timeout=5)

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall("./channel/item")[:max_articles]:
                title = item.findtext("title", "").strip()
                link = item.findtext("link", "").strip()
                pub_date = item.findtext("pubDate", "Recent").strip()

                # Clean publisher from Google RSS format (Title - Source)
                publisher = "Google News"
                if " - " in title:
                    parts = title.rsplit(" - ", 1)
                    title = parts[0].strip()
                    publisher = parts[1].strip()

                if title and title.lower() not in seen_titles:
                    seen_titles.add(title.lower())
                    articles.append({
                        "title": title,
                        "publisher": publisher,
                        "published": pub_date,
                        "link": link
                    })
    except Exception as e:
        print(f"[News Ingestion] RSS news warning: {e}")

    return articles[:max_articles]


def _lexicon_sentiment_fallback(text: str) -> Dict[str, float]:
    """
    Lightweight financial lexicon fallback if FinBERT weights are still downloading.
    """
    lower = text.lower()
    positive_words = {
        'surge', 'jump', 'gain', 'growth', 'bullish', 'profit', 'beat', 'record',
        'upgrade', 'soar', 'strong', 'rally', 'positive', 'breakthrough', 'dividend', 'outperform'
    }
    negative_words = {
        'plunge', 'drop', 'fall', 'loss', 'bearish', 'miss', 'down', 'lawsuit',
        'downgrade', 'slump', 'weak', 'risk', 'negative', 'decline', 'crash', 'underperform'
    }

    pos_count = sum(1 for w in positive_words if w in lower)
    neg_count = sum(1 for w in negative_words if w in lower)

    total = pos_count + neg_count
    if total == 0:
        return {"positive": 0.2, "neutral": 0.6, "negative": 0.2, "score": 0.0, "label": "neutral"}

    pos_prob = pos_count / (total + 1.0)
    neg_prob = neg_count / (total + 1.0)
    neu_prob = 1.0 - (pos_prob + neg_prob)
    score = pos_prob - neg_prob

    if score > 0.05:
        label = "positive"
    elif score < -0.05:
        label = "negative"
    else:
        label = "neutral"

    return {"positive": pos_prob, "neutral": max(0.0, neu_prob), "negative": neg_prob, "score": score, "label": label}


def analyze_headline_sentiment(text: str) -> Dict[str, Any]:
    """
    Analyzes a single news headline using FinBERT or financial lexicon fallback.

    Returns:
        Dictionary with probabilities for positive, negative, neutral, and compound score.
    """
    pipe = get_finbert_pipeline()

    if pipe is not None:
        try:
            # FinBERT outputs: [{'label': 'positive', 'score': 0.8}, {'label': 'negative', ...}, ...]
            results = pipe(text[:512])[0]
            scores_by_label = {item['label'].lower(): float(item['score']) for item in results}
            pos = scores_by_label.get('positive', 0.0)
            neg = scores_by_label.get('negative', 0.0)
            neu = scores_by_label.get('neutral', 0.0)

            # Continuous sentiment score between -1.0 (bearish) and +1.0 (bullish)
            compound_score = pos - neg
            dominant_label = max(scores_by_label, key=scores_by_label.get)

            return {
                "positive": pos,
                "negative": neg,
                "neutral": neu,
                "score": compound_score,
                "label": dominant_label
            }
        except Exception as e:
            print(f"[FinBERT Inference Error] {e}")

    # Fallback if FinBERT pipeline is not yet loaded
    return _lexicon_sentiment_fallback(text)


def analyze_news_sentiment(ticker: str, max_articles: int = 12) -> Tuple[float, Dict[str, float], List[Dict[str, Any]]]:
    """
    Gathers news for a ticker and calculates aggregate sentiment metrics.

    Returns:
        Tuple of:
            - aggregate_score: float in [-1.0, 1.0]
            - sentiment_distribution: {'positive_pct': %, 'neutral_pct': %, 'negative_pct': %}
            - articles_with_sentiment: List of article dicts annotated with scores
    """
    articles = fetch_company_news(ticker, max_articles=max_articles)
    if not articles:
        return 0.0, {"positive_pct": 0.0, "neutral_pct": 100.0, "negative_pct": 0.0}, []

    annotated_articles = []
    scores = []
    labels_count = {"positive": 0, "neutral": 0, "negative": 0}

    for art in articles:
        sentiment = analyze_headline_sentiment(art["title"])
        art_info = dict(art)
        art_info.update(sentiment)
        annotated_articles.append(art_info)

        scores.append(sentiment["score"])
        lbl = sentiment["label"]
        if lbl in labels_count:
            labels_count[lbl] += 1

    total_articles = len(annotated_articles)
    aggregate_score = float(sum(scores) / total_articles) if total_articles > 0 else 0.0

    distribution = {
        "positive_pct": round((labels_count["positive"] / total_articles) * 100, 1),
        "neutral_pct": round((labels_count["neutral"] / total_articles) * 100, 1),
        "negative_pct": round((labels_count["negative"] / total_articles) * 100, 1),
    }

    return aggregate_score, distribution, annotated_articles
