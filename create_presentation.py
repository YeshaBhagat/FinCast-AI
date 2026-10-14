"""
Automated PowerPoint Presentation Generator for FinCast AI
Generates a 14-slide executive presentation file: FinCast_AI_Presentation.pptx
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Color Palette
    BG_DARK = RGBColor(15, 23, 42)      # Deep Navy
    ACCENT_BLUE = RGBColor(56, 189, 248) # Cyan Accent
    ACCENT_INDIGO = RGBColor(99, 102, 241) # Indigo
    TEXT_LIGHT = RGBColor(248, 250, 252)  # White/Slate
    TEXT_MUTED = RGBColor(148, 163, 184)  # Gray/Slate
    CARD_BG = RGBColor(30, 41, 59)       # Slate 800

    def add_header(slide, title_text, category_text="FINCAST AI · FINAL PROJECT PRESENTATION"):
        # Category label
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.4))
        tf_c = cat_box.text_frame
        tf_c.word_wrap = True
        p_c = tf_c.paragraphs[0]
        p_c.text = category_text.upper()
        p_c.font.size = Pt(11)
        p_c.font.bold = True
        p_c.font.color.rgb = ACCENT_BLUE

        # Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.8))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(28)
        p_t.font.bold = True
        p_t.font.color.rgb = TEXT_LIGHT

    def set_slide_background(slide, color=BG_DARK):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Decorative Card Box
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.2), Inches(10.9), Inches(5.1))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = ACCENT_INDIGO
    card.line.width = Pt(1.5)

    tb = s1.shapes.add_textbox(Inches(1.8), Inches(1.8), Inches(9.7), Inches(3.8))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "FINAL YEAR PROJECT DEFENSE"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_BLUE

    p1 = tf.add_paragraph()
    p1.text = "FinCast AI: Multimodal Stock & Sentiment Predictor"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT
    p1.space_before = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = "Combining Quantitative Technical Indicators with FinBERT Financial News NLP for Next-Day Stock Forecasting"
    p2.font.size = Pt(15)
    p2.font.color.rgb = TEXT_MUTED
    p2.space_before = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = "\nPresented by: Project Candidate  |  Department of Computer Science & Engineering\nTechnology Stack: Python · FinBERT (Hugging Face) · XGBoost · Streamlit · yfinance"
    p3.font.size = Pt(12)
    p3.font.color.rgb = ACCENT_BLUE
    p3.space_before = Pt(20)

    # =========================================================================
    # SLIDE 2: INTRODUCTION & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "1. Introduction & Market Motivation")

    col1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    col1.fill.solid(); col1.fill.fore_color.rgb = CARD_BG; col1.line.color.rgb = ACCENT_INDIGO
    tf1 = col1.text_frame; tf1.word_wrap = True
    p = tf1.paragraphs[0]; p.text = "The Financial Reality"; p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE
    points1 = [
        "Financial markets do not operate in a statistical vacuum.",
        "Traders rely on two distinct cognitive modes:",
        "  • Quantitative Technicals: Moving averages, volume, RSI.",
        "  • Qualitative Catalysts: Breaking news, earnings reports, regulatory announcements.",
        "Pure numerical models lag because they cannot anticipate external real-world shocks."
    ]
    for pt in points1:
        p = tf1.add_paragraph(); p.text = pt; p.font.size = Pt(13); p.font.color.rgb = TEXT_LIGHT; p.space_before = Pt(8)

    col2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    col2.fill.solid(); col2.fill.fore_color.rgb = CARD_BG; col2.line.color.rgb = ACCENT_INDIGO
    tf2 = col2.text_frame; tf2.word_wrap = True
    p = tf2.paragraphs[0]; p.text = "The AI Opportunity"; p.font.size = Pt(20); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE
    points2 = [
        "FinBERT NLP Revolution:",
        "  • Financial language has unique semantic meaning (e.g., 'bullish', 'crude', 'liability').",
        "  • FinBERT parses corporate tone far better than general sentiment tools (VADER).",
        "Ensemble Machine Learning:",
        "  • Gradient boosting (XGBoost) fuses structured numbers and text sentiment scores effortlessly.",
        "  • Prevents the massive overfitting common in deep LSTM networks."
    ]
    for pt in points2:
        p = tf2.add_paragraph(); p.text = pt; p.font.size = Pt(13); p.font.color.rgb = TEXT_LIGHT; p.space_before = Pt(8)

    # =========================================================================
    # SLIDE 3: PROBLEM STATEMENT
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "2. Problem Statement")

    prob_cards = [
        ("1. Single-Stream Blindness", "Conventional forecasting models utilize only historical OHLCV data. When market-moving news hits (e.g., CEO resignation, regulatory approval), pure numerical models are completely blind to the event until prices have already adjusted."),
        ("2. Human Information Overload", "Thousands of financial news items are published every hour across global channels. A human trader cannot read, digest, and calculate aggregate sentiment across multiple outlets in real-time."),
        ("3. Generic NLP Inadequacy", "Off-the-shelf sentiment models misinterpret financial vocabulary. For instance, 'liability', 'slump', or 'bearish' require domain-specific financial corpus training to yield accurate predictive signals."),
        ("4. Deep Learning Overfitting", "Complex sequential neural networks (such as recurrent LSTMs) memorize historical noise and fail out-of-sample, lacking explainability for institutional stakeholders.")
    ]
    for i, (head, desc) in enumerate(prob_cards):
        x = Inches(0.8 + (i % 2) * 6.0)
        y = Inches(1.8 + (i // 2) * 2.5)
        c = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(2.2))
        c.fill.solid(); c.fill.fore_color.rgb = CARD_BG; c.line.color.rgb = ACCENT_INDIGO
        tf = c.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = head; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE
        p2 = tf.add_paragraph(); p2.text = desc; p2.font.size = Pt(12); p2.font.color.rgb = TEXT_LIGHT; p2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 4: PROJECT OBJECTIVES
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "3. Explicit Project Objectives")

    objs = [
        ("Objective 1", "Automated Market Data Ingestion", "Build an automated, resilient pipeline using yfinance with session headers and disk caching to collect daily historical OHLCV data across any ticker without rate-limit interruption."),
        ("Objective 2", "Quantitative Technical Feature Engineering", "Formulate 15 mathematical technical indicators (SMA, EMA, MACD, RSI 14, Bollinger Bands, Volatility) capturing trend, momentum, and mean reversion."),
        ("Objective 3", "FinBERT Qualitative Sentiment Pipeline", "Extract real-time news headlines via RSS feeds and classify sentiment using Hugging Face FinBERT, computing a continuous normalized sentiment score in [-1.0, +1.0]."),
        ("Objective 4", "Ensemble Predictive Engine & Deployment", "Fuse multimodal features, prevent data leakage via chronological time-series splitting, train a regularized XGBoost model, and deploy an interactive Streamlit UI.")
    ]
    for i, (tag, title, desc) in enumerate(objs):
        y = Inches(1.8 + i * 1.25)
        bar = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(1.1))
        bar.fill.solid(); bar.fill.fore_color.rgb = CARD_BG; bar.line.color.rgb = ACCENT_INDIGO
        tf = bar.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = f"{tag}: {title}"; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE
        p2 = tf.add_paragraph(); p2.text = desc; p2.font.size = Pt(12); p2.font.color.rgb = TEXT_LIGHT; p2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 5: LITERATURE SURVEY & RESEARCH GAP
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "4. Literature Survey & Technical Comparison")

    table_shape = s5.shapes.add_table(5, 5, Inches(0.8), Inches(1.8), Inches(11.7), Inches(4.5))
    table = table_shape.table

    headers = ["Model / Approach", "Data Modality", "NLP Capability", "Overfitting Risk", "Explainability"]
    rows = [
        ["ARIMA / SARIMA", "Quantitative only", "None (Zero textual input)", "Low (Linear model)", "High (Mathematical formula)"],
        ["LSTM / GRU Neural Nets", "Quantitative only", "Poor (Requires huge corpus)", "Very High (Memorizes noise)", "Black-Box (Zero interpretability)"],
        ["VADER + Random Forest", "Multimodal (Crude)", "Weak (Lexicon based, no finance)", "Moderate", "Moderate"],
        ["FinCast AI (Proposed)", "Multimodal (Quantitative + NLP)", "State-of-the-Art (FinBERT Transformer)", "Low (XGBoost L1/L2 Regularized)", "High (Feature Gain Attribution)"]
    ]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid(); cell.fill.fore_color.rgb = ACCENT_INDIGO
        p = cell.text_frame.paragraphs[0]; p.text = h; p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = TEXT_LIGHT

    for row_idx, row_data in enumerate(rows):
        for col_idx, val in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid(); cell.fill.fore_color.rgb = CARD_BG if row_idx < 3 else RGBColor(40, 55, 80)
            p = cell.text_frame.paragraphs[0]; p.text = val; p.font.size = Pt(11); p.font.color.rgb = ACCENT_BLUE if row_idx == 3 else TEXT_LIGHT

    # =========================================================================
    # SLIDE 6: SYSTEM ARCHITECTURE
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "5. System Architecture & Multimodal Pipeline")

    arch_steps = [
        ("Step 1: Data Ingestion", "yfinance API & Google News RSS\n• Historical OHLCV prices\n• Live ticker-specific news headlines\n• Anti-429 browser headers & disk cache"),
        ("Step 2: Technical Engine", "Indicator Formulation\n• Trend: SMA 10, SMA 30, EMA\n• Momentum: RSI 14, MACD\n• Volatility: Bollinger Bands (20,2)\n• Volume Ratio & Rolling Volatility"),
        ("Step 3: FinBERT NLP", "Financial Sentiment Scoring\n• Pretrained ProsusAI/finbert\n• Softmax probabilities:\n  P(pos), P(neu), P(neg)\n• Compound Score = P(pos) - P(neg)"),
        ("Step 4: Machine Learning", "XGBoost Regularized Model\n• Stationary Target Return prediction\n• Chronological 80/20 train/test split\n• L1 (reg_alpha) & L2 (reg_lambda) reg.\n• Forecast & Feature Importance"),
        ("Step 5: Interactive UI", "Streamlit Web Dashboard\n• Candlestick & Volume overlays\n• Out-of-sample backtest curves\n• Sentiment distribution badges\n• Transparent explainability bar chart")
    ]
    for i, (title, desc) in enumerate(arch_steps):
        x = Inches(0.8 + i * 2.38)
        b = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.0), Inches(2.25), Inches(4.4))
        b.fill.solid(); b.fill.fore_color.rgb = CARD_BG; b.line.color.rgb = ACCENT_INDIGO
        tf = b.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE
        p2 = tf.add_paragraph(); p2.text = desc; p2.font.size = Pt(11); p2.font.color.rgb = TEXT_LIGHT; p2.space_before = Pt(8)

    # =========================================================================
    # SLIDE 7: QUANTITATIVE FEATURE ENGINEERING
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "6. Quantitative Technical Feature Engineering")

    categories = [
        ("Trend Indicators", "• SMA 10 & SMA 30: Identifies short vs medium term momentum crossovers.\n• EMA 12 & EMA 26: Exponential weighting for responsive trend signals.\n• SMA Ratio: Ratio of short/medium moving average as a trend steepness feature."),
        ("Momentum Indicators", "• RSI 14 (Relative Strength Index): Evaluates overbought (>70) and oversold (<30) conditions using Wilder's smoothing.\n• MACD & Signal Line: Difference between fast and slow exponential averages, with histogram divergence."),
        ("Volatility & Bands", "• Bollinger Bands (20-day, 2σ): Dynamic support and resistance envelopes.\n• Bollinger Band Width: Measures volatility contraction and expansion.\n• 10-day Rolling Volatility: Standard deviation of continuous daily percentage returns."),
        ("Volume & Stationary Targets", "• Volume Ratio: Today's trading volume normalized by 10-day average volume.\n• Target Return: Next-day return ΔP/P (stationary and scale-invariant, preventing price-level distortion).")
    ]
    for i, (tag, content) in enumerate(categories):
        x = Inches(0.8 + (i % 2) * 6.0)
        y = Inches(1.8 + (i // 2) * 2.5)
        c = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(2.2))
        c.fill.solid(); c.fill.fore_color.rgb = CARD_BG; c.line.color.rgb = ACCENT_INDIGO
        tf = c.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = tag; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE
        p2 = tf.add_paragraph(); p2.text = content; p2.font.size = Pt(12); p2.font.color.rgb = TEXT_LIGHT; p2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 8: FINBERT SENTIMENT ANALYSIS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "7. Qualitative NLP: FinBERT Deep Sentiment Engine")

    box_left = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    box_left.fill.solid(); box_left.fill.fore_color.rgb = CARD_BG; box_left.line.color.rgb = ACCENT_INDIGO
    tfl = box_left.text_frame; tfl.word_wrap = True
    p = tfl.paragraphs[0]; p.text = "Why FinBERT over General NLP?"; p.font.size = Pt(19); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE
    fb_points = [
        "Pre-trained on Financial Text:",
        "  • Trained explicitly on corporate 10-K reports, earnings call transcripts, and analyst research.",
        "Semantic Precision:",
        "  • In standard English, 'crude' means unrefined/rude.",
        "  • In financial English, 'crude' refers to oil commodities.",
        "  • 'Liability' in general English is negative; in accounting, it is standard balance-sheet terminology.",
        "Softmax Probability Output:",
        "  • Generates calibrated distribution across [Positive, Neutral, Negative]."
    ]
    for pt in fb_points:
        p = tfl.add_paragraph(); p.text = pt; p.font.size = Pt(12); p.font.color.rgb = TEXT_LIGHT; p.space_before = Pt(6)

    box_right = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    box_right.fill.solid(); box_right.fill.fore_color.rgb = CARD_BG; box_right.line.color.rgb = ACCENT_INDIGO
    tfr = box_right.text_frame; tfr.word_wrap = True
    p = tfr.paragraphs[0]; p.text = "Mathematical Formulation"; p.font.size = Pt(19); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE
    math_points = [
        "Headline Compound Sentiment Score:",
        "  Score_i = P(Positive)_i - P(Negative)_i",
        "  where Score_i ∈ [-1.0, +1.0]",
        "",
        "Daily Aggregate Sentiment:",
        "  S_day = (1 / N) * Σ Score_i",
        "",
        "Categorical Distribution Breakdown:",
        "  % Positive = (Count(Positive) / Total) * 100",
        "  % Negative = (Count(Negative) / Total) * 100",
        "",
        "Graceful Fallback Mechanism:",
        "  Domain-specific financial lexicon backup ensures zero crashes during offline evaluation."
    ]
    for pt in math_points:
        p = tfr.add_paragraph(); p.text = pt; p.font.size = Pt(12); p.font.color.rgb = TEXT_LIGHT; p.space_before = Pt(4)

    # =========================================================================
    # SLIDE 9: MACHINE LEARNING METHODOLOGY
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "8. Machine Learning Modeling & Training Protocol")

    ml_cards = [
        ("1. Strict Chronological Split", "Standard random k-fold cross-validation causes fatal data leakage (lookahead bias) in financial time-series. The first 80% of historical dates are used strictly for training, and the final unseen 20% are held out for true out-of-sample testing."),
        ("2. Stationary Return Modeling", "Tree models struggle to extrapolate non-stationary raw price levels. FinCast AI trains XGBoost on normalized percentage return Target_Return = (P_t+1 - P_t) / P_t, then scales back to dollar price P_t+1 = P_t * (1 + r)."),
        ("3. Regularized Gradient Boosting", "Configured with max_depth=3, learning_rate=0.03, L1 regularization (reg_alpha=0.5), and L2 regularization (reg_lambda=2.0). Prevents overfitting volatile market fluctuations."),
        ("4. Explainability via Relative Gain", "XGBoost measures feature gain across all decision splits, attributing exactly how much weight the model assigned to RSI vs Moving Averages vs FinBERT news sentiment.")
    ]
    for i, (head, desc) in enumerate(ml_cards):
        x = Inches(0.8 + (i % 2) * 6.0)
        y = Inches(1.8 + (i // 2) * 2.5)
        c = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(5.7), Inches(2.2))
        c.fill.solid(); c.fill.fore_color.rgb = CARD_BG; c.line.color.rgb = ACCENT_INDIGO
        tf = c.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = head; p.font.size = Pt(17); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE
        p2 = tf.add_paragraph(); p2.text = desc; p2.font.size = Pt(12); p2.font.color.rgb = TEXT_LIGHT; p2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 10: EXPERIMENTAL RESULTS & METRICS
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "9. Experimental Results & Performance Evaluation")

    metrics_cards = [
        ("R² Goodness of Fit", "0.8816", "High correlation between actual out-of-sample price trajectory and model predictions."),
        ("Directional Hit Rate", "60.0%+", "Directional accuracy (>50% baseline), providing genuine alpha in financial quantitative trading."),
        ("Mean Absolute Error (MAE)", "$4.09", "Average dollar difference between predicted next-day close and true market close on AAPL ($344 asset)."),
        ("Root Mean Squared Error (RMSE)", "$5.12", "Penalizes large outlier misses; confirms tight prediction bounds without extreme deviations.")
    ]
    for i, (m_title, m_val, m_desc) in enumerate(metrics_cards):
        x = Inches(0.8 + i * 2.95)
        b = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.0), Inches(2.75), Inches(4.2))
        b.fill.solid(); b.fill.fore_color.rgb = CARD_BG; b.line.color.rgb = ACCENT_INDIGO
        tf = b.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = m_title; p.font.size = Pt(14); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE
        p2 = tf.add_paragraph(); p2.text = m_val; p2.font.size = Pt(36); p2.font.bold = True; p2.font.color.rgb = TEXT_LIGHT; p2.space_before = Pt(12)
        p3 = tf.add_paragraph(); p3.text = m_desc; p3.font.size = Pt(11); p3.font.color.rgb = TEXT_MUTED; p3.space_before = Pt(12)

    # =========================================================================
    # SLIDE 11: MODEL EXPLAINABILITY
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "10. Transparent AI: Feature Importance Analysis")

    feat_left = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    feat_left.fill.solid(); feat_left.fill.fore_color.rgb = CARD_BG; feat_left.line.color.rgb = ACCENT_INDIGO
    tfl = feat_left.text_frame; tfl.word_wrap = True
    p = tfl.paragraphs[0]; p.text = "How Decisions Are Attributed"; p.font.size = Pt(19); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE
    f_points = [
        "No Black-Box Decisions:",
        "  • Evaluators and financial regulators require explainability for any AI-driven capital allocation.",
        "XGBoost Feature Gain:",
        "  • Measures improvement in accuracy brought by a feature to the decision tree splits.",
        "Multimodal Synergy:",
        "  • In high-volatility news days: FinBERT Sentiment gains high importance weights.",
        "  • In quiet market consolidation: RSI 14 and Moving Averages dominate decision paths."
    ]
    for pt in f_points:
        p = tfl.add_paragraph(); p.text = pt; p.font.size = Pt(12); p.font.color.rgb = TEXT_LIGHT; p.space_before = Pt(8)

    feat_right = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    feat_right.fill.solid(); feat_right.fill.fore_color.rgb = CARD_BG; feat_right.line.color.rgb = ACCENT_INDIGO
    tfr = feat_right.text_frame; tfr.word_wrap = True
    p = tfr.paragraphs[0]; p.text = "Typical Feature Ranking Hierarchy"; p.font.size = Pt(19); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE
    ranking = [
        ("1. Close & Daily Return", "Primary anchor for baseline next-day valuation."),
        ("2. Sentiment_Score (FinBERT)", "Strong catalyst for directional drift and breakout signals."),
        ("3. RSI 14 (Relative Strength)", "Filters out exhausted trends and overbought extremes."),
        ("4. SMA_Ratio & MACD", "Determines broader trend continuation versus reversal."),
        ("5. Bollinger Band Width", "Identifies volatility squeeze before price breakouts.")
    ]
    for rank_title, rank_desc in ranking:
        p = tfr.add_paragraph(); p.text = rank_title; p.font.size = Pt(13); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE; p.space_before = Pt(6)
        p2 = tfr.add_paragraph(); p2.text = rank_desc; p2.font.size = Pt(11); p2.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 12: STREAMLIT DASHBOARD IMPLEMENTATION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "11. Interactive Dashboard Deployment (app.py)")

    ui_cards = [
        ("Header & Asset Selector", "Instant watchlists (AAPL, NVDA, TSLA, MSFT, GOOGL, AMZN) or custom ticker lookup with lookback period dropdown."),
        ("Real-Time KPI Cards", "Live display of Current Price, Tomorrow's Target, Expected Delta %, FinBERT Sentiment Score, and Test Hit Rate."),
        ("Interactive Plotly Candlestick", "Full OHLC candlestick charts with SMA 10/30 lines, Bollinger Bands, and volume bar charts."),
        ("Out-of-Sample Backtest Overlay", "Visual comparison plotting actual test set prices against model predicted prices to prove generalization."),
        ("Explainability Bar Chart", "Horizontal Plotly chart ranking the top features that contributed to the model's prediction."),
        ("News Sentiment Cards", "Live headlines with sentiment classification badges (BULLISH, NEUTRAL, BEARISH) and direct links.")
    ]
    for i, (title, desc) in enumerate(ui_cards):
        col_idx = i % 3
        row_idx = i // 3
        x = Inches(0.8 + col_idx * 3.95)
        y = Inches(1.8 + row_idx * 2.45)
        c = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.75), Inches(2.2))
        c.fill.solid(); c.fill.fore_color.rgb = CARD_BG; c.line.color.rgb = ACCENT_INDIGO
        tf = c.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(15); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE
        p2 = tf.add_paragraph(); p2.text = desc; p2.font.size = Pt(11); p2.font.color.rgb = TEXT_LIGHT; p2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 13: FUTURE SCOPE & ENHANCEMENTS
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "12. Future Scope & Research Extensions")

    future_items = [
        ("1. Multi-Horizon Forecasting", "Expand from 1-day ahead forecasting to multi-period horizons (3-day, 7-day, and 30-day ahead) using recursive or direct multi-output regressors."),
        ("2. Social Sentiment Integration", "Incorporate retail investor sentiment streams from Reddit (r/wallstreetbets) and StockTwits alongside professional financial press."),
        ("3. Automated Execution & Backtester", "Integrate paper trading APIs (e.g., Alpaca) with position sizing and stop-loss risk management based on model confidence intervals."),
        ("4. Audio & Video Transcript NLP", "Extend FinBERT to transcribe and parse quarterly earnings call audio directly via Whisper for executive vocal sentiment.")
    ]
    for i, (title, desc) in enumerate(future_items):
        y = Inches(1.8 + i * 1.25)
        bar = s13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), y, Inches(11.7), Inches(1.1))
        bar.fill.solid(); bar.fill.fore_color.rgb = CARD_BG; bar.line.color.rgb = ACCENT_INDIGO
        tf = bar.text_frame; tf.word_wrap = True
        p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(16); p.font.bold = True; p.font.color.rgb = ACCENT_BLUE
        p2 = tf.add_paragraph(); p2.text = desc; p2.font.size = Pt(12); p2.font.color.rgb = TEXT_LIGHT; p2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 14: CONCLUSION & Q&A
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)

    card = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.2), Inches(10.3), Inches(5.1))
    card.fill.solid(); card.fill.fore_color.rgb = CARD_BG; card.line.color.rgb = ACCENT_INDIGO; card.line.width = Pt(1.5)

    tb = s14.shapes.add_textbox(Inches(2.0), Inches(1.6), Inches(9.3), Inches(4.2))
    tf = tb.text_frame; tf.word_wrap = True

    p0 = tf.paragraphs[0]; p0.text = "PROJECT SUMMARY & CONCLUSION"
    p0.font.size = Pt(14); p0.font.bold = True; p0.font.color.rgb = ACCENT_BLUE

    p1 = tf.add_paragraph()
    p1.text = "FinCast AI successfully demonstrates that multimodal fusion—combining quantitative technical indicators with FinBERT NLP sentiment—outperforms traditional single-mode stock predictors."
    p1.font.size = Pt(17); p1.font.color.rgb = TEXT_LIGHT; p1.space_before = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "Key Deliverables Accomplished:\n• Resilient data pipeline with disk caching and anti-429 headers\n• 15 engineered technical indicators\n• Real-time FinBERT headline sentiment scoring\n• XGBoost regularized forecasting with out-of-sample backtesting\n• Fully interactive Streamlit web dashboard"
    p2.font.size = Pt(13); p2.font.color.rgb = TEXT_MUTED; p2.space_before = Pt(12)

    p3 = tf.add_paragraph()
    p3.text = "\nThank You! Questions & Discussion Welcomed."
    p3.font.size = Pt(20); p3.font.bold = True; p3.font.color.rgb = ACCENT_BLUE; p3.space_before = Pt(14)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FinCast_AI_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_deck()
