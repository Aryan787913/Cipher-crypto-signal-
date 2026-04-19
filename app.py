import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Cipher · Crypto Signals",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Premium CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #000000;
    --bg-secondary: #0a0a0a;
    --bg-card: #111111;
    --bg-card-hover: #161616;
    --border: rgba(255,255,255,0.06);
    --border-bright: rgba(255,255,255,0.12);
    --accent-blue: #0A84FF;
    --accent-blue-dim: rgba(10,132,255,0.15);
    --accent-green: #30D158;
    --accent-green-dim: rgba(48,209,88,0.12);
    --accent-red: #FF453A;
    --accent-red-dim: rgba(255,69,58,0.12);
    --accent-amber: #FFD60A;
    --accent-amber-dim: rgba(255,214,10,0.12);
    --text-primary: rgba(255,255,255,0.92);
    --text-secondary: rgba(255,255,255,0.45);
    --text-tertiary: rgba(255,255,255,0.25);
    --font-main: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: var(--bg-primary) !important;
    font-family: var(--font-main) !important;
    color: var(--text-primary) !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header, .stDeployButton { display: none !important; }
.block-container { 
    padding: 0 !important; 
    max-width: 100% !important;
}
section[data-testid="stSidebar"] { display: none; }

/* ── Global typography ── */
h1,h2,h3,h4,h5,h6,p,span,div,label {
    font-family: var(--font-main) !important;
    -webkit-font-smoothing: antialiased;
}

/* ── Top nav bar ── */
.cipher-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 40px;
    height: 64px;
    border-bottom: 1px solid var(--border);
    background: rgba(0,0,0,0.8);
    backdrop-filter: blur(20px);
    position: sticky;
    top: 0;
    z-index: 100;
}
.cipher-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 18px;
    font-weight: 600;
    letter-spacing: -0.3px;
    color: var(--text-primary);
}
.cipher-logo-icon {
    width: 32px;
    height: 32px;
    background: var(--accent-blue);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
}
.cipher-nav-pill {
    display: flex;
    align-items: center;
    gap: 6px;
    background: var(--accent-green-dim);
    border: 1px solid rgba(48,209,88,0.25);
    border-radius: 20px;
    padding: 6px 14px;
    font-size: 12px;
    font-weight: 500;
    color: var(--accent-green);
}
.live-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent-green);
    animation: pulse-green 2s infinite;
}
@keyframes pulse-green {
    0%,100% { opacity:1; transform:scale(1); }
    50% { opacity:0.4; transform:scale(0.8); }
}

/* ── Page wrapper ── */
.page-wrapper {
    padding: 40px 40px 80px;
    max-width: 1400px;
    margin: 0 auto;
}

/* ── Section label ── */
.section-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--text-tertiary);
    margin-bottom: 20px;
}

/* ── Hero signal card ── */
.signal-hero {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 36px;
    position: relative;
    overflow: hidden;
    margin-bottom: 16px;
}
.signal-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(10,132,255,0.4), transparent);
}
.signal-hero-buy::before { background: linear-gradient(90deg, transparent, rgba(48,209,88,0.5), transparent); }
.signal-hero-sell::before { background: linear-gradient(90deg, transparent, rgba(255,69,58,0.5), transparent); }
.signal-hero-hold::before { background: linear-gradient(90deg, transparent, rgba(255,214,10,0.4), transparent); }

.signal-type-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 28px;
}
.signal-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border-radius: 12px;
    font-size: 22px;
    font-weight: 700;
    letter-spacing: -0.3px;
}
.signal-badge-buy   { background: var(--accent-green-dim); color: var(--accent-green); border: 1px solid rgba(48,209,88,0.3); }
.signal-badge-sell  { background: var(--accent-red-dim);   color: var(--accent-red);   border: 1px solid rgba(255,69,58,0.3); }
.signal-badge-hold  { background: var(--accent-amber-dim); color: var(--accent-amber); border: 1px solid rgba(255,214,10,0.3); }

.confidence-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.conf-high   { background: rgba(10,132,255,0.12); color: var(--accent-blue); border: 1px solid rgba(10,132,255,0.25); }
.conf-medium { background: rgba(255,214,10,0.10); color: var(--accent-amber); border: 1px solid rgba(255,214,10,0.2); }
.conf-low    { background: rgba(255,255,255,0.05); color: var(--text-secondary); border: 1px solid var(--border); }

.signal-price {
    font-size: 48px;
    font-weight: 300;
    letter-spacing: -2px;
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
    font-family: var(--font-main) !important;
    margin-bottom: 6px;
}
.signal-meta {
    font-size: 13px;
    color: var(--text-secondary);
    font-family: var(--font-mono) !important;
}
.signal-reason {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 24px;
    font-size: 14px;
    line-height: 1.6;
    color: rgba(255,255,255,0.7);
}
.signal-reason strong { color: var(--text-primary); font-weight: 500; }

/* ── Metric cards ── */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 16px;
}
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 22px 24px;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: var(--border-bright); }
.metric-label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-tertiary);
    margin-bottom: 10px;
}
.metric-value {
    font-size: 28px;
    font-weight: 600;
    letter-spacing: -0.5px;
    color: var(--text-primary);
    font-variant-numeric: tabular-nums;
    line-height: 1;
}
.metric-sub {
    font-size: 12px;
    color: var(--text-secondary);
    margin-top: 6px;
}
.metric-green { color: var(--accent-green) !important; }
.metric-red   { color: var(--accent-red) !important; }
.metric-blue  { color: var(--accent-blue) !important; }

/* ── Indicator pills ── */
.indicator-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-top: 20px;
}
.indicator-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 12px;
    font-family: var(--font-mono) !important;
}
.indicator-pill .ind-label { color: var(--text-tertiary); }
.indicator-pill .ind-value { color: var(--text-primary); font-weight: 500; }
.ind-bull { border-color: rgba(48,209,88,0.2); background: rgba(48,209,88,0.05); }
.ind-bear { border-color: rgba(255,69,58,0.2); background: rgba(255,69,58,0.05); }
.ind-neutral { border-color: rgba(255,214,10,0.2); background: rgba(255,214,10,0.05); }

/* ── Upload zone ── */
.upload-zone {
    border: 1px dashed rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 40px;
    text-align: center;
    background: rgba(255,255,255,0.02);
    transition: all 0.2s;
    margin-bottom: 16px;
}
.upload-icon { font-size: 32px; margin-bottom: 12px; }
.upload-title { font-size: 16px; font-weight: 500; margin-bottom: 6px; }
.upload-sub { font-size: 13px; color: var(--text-secondary); }

/* ── Backtest card ── */
.backtest-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 16px;
}
.backtest-title {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 4px;
}
.backtest-sub {
    font-size: 12px;
    color: var(--text-secondary);
    margin-bottom: 24px;
}

/* ── Tab overrides ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
    padding: 0 !important;
    margin-bottom: 28px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-secondary) !important;
    font-family: var(--font-main) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 12px 20px !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    transition: all 0.15s !important;
}
.stTabs [aria-selected="true"] {
    color: var(--text-primary) !important;
    border-bottom: 2px solid var(--accent-blue) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ── File uploader ── */
.stFileUploader > div {
    background: rgba(255,255,255,0.02) !important;
    border: 1px dashed rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
}
.stFileUploader label { color: var(--text-secondary) !important; }

/* ── Button ── */
.stButton > button {
    background: var(--accent-blue) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: var(--font-main) !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 10px 24px !important;
    transition: all 0.15s !important;
    letter-spacing: -0.1px !important;
}
.stButton > button:hover {
    background: #0070E0 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(10,132,255,0.25) !important;
}

/* ── Spinner ── */
.stSpinner { color: var(--accent-blue) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 2px; }

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
}

/* ── Divider ── */
hr { border: none; border-top: 1px solid var(--border); margin: 32px 0; }

/* ── Timestamp ── */
.timestamp-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 28px;
}
.ts-text {
    font-size: 12px;
    font-family: var(--font-mono) !important;
    color: var(--text-tertiary);
}
.refresh-badge {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    color: var(--text-tertiary);
    font-weight: 500;
}

/* ── Disclaimer ── */
.disclaimer {
    background: rgba(255,214,10,0.05);
    border: 1px solid rgba(255,214,10,0.15);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 12px;
    color: rgba(255,214,10,0.7);
    margin-top: 12px;
}

/* ── Trade table ── */
.stDataFrame { background: transparent !important; }
.stDataFrame table {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    font-family: var(--font-mono) !important;
    font-size: 12px !important;
    overflow: hidden !important;
}
.stDataFrame th {
    background: rgba(255,255,255,0.03) !important;
    color: var(--text-tertiary) !important;
    border-bottom: 1px solid var(--border) !important;
    font-size: 11px !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    padding: 10px 14px !important;
}
.stDataFrame td {
    color: var(--text-primary) !important;
    border-bottom: 1px solid rgba(255,255,255,0.04) !important;
    padding: 10px 14px !important;
}

/* ── Plotly override ── */
.js-plotly-plot .plotly { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ─── Signal Engine ────────────────────────────────────────────────────────────
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))

def simple_arima_forecast(series, steps=3):
    """Lightweight ARIMA-style trend via linear regression on recent data."""
    try:
        n = min(30, len(series))
        y = series.iloc[-n:].values
        x = np.arange(n)
        coeffs = np.polyfit(x, y, 1)
        slope = coeffs[0]
        last = y[-1]
        forecast = [last + slope * (i + 1) for i in range(steps)]
        return forecast, slope
    except Exception:
        return [series.iloc[-1]] * steps, 0.0

def generate_signal(df):
    """Core signal engine — returns signal dict."""
    df = df.copy().dropna()
    if len(df) < 55:
        return None

    close = df['close'].astype(float)

    # Indicators
    ma20 = close.rolling(20).mean().iloc[-1]
    ma50 = close.rolling(50).mean().iloc[-1]
    rsi  = compute_rsi(close).iloc[-1]
    current_price = close.iloc[-1]
    prev_price    = close.iloc[-2]

    # ARIMA-style trend
    forecast, slope = simple_arima_forecast(close)
    arima_direction = "up" if slope > 0 else "down"
    arima_pct = abs(slope / (current_price + 1e-9) * 100)

    # --- Bullish signals ---
    bull_points = 0
    bull_reasons = []
    if current_price > ma20:
        bull_points += 1
        bull_reasons.append(f"Price above MA20 (${ma20:,.0f})")
    if ma20 > ma50:
        bull_points += 1
        bull_reasons.append(f"MA20 crossed above MA50 — Golden Cross")
    if 40 < rsi < 70:
        bull_points += 1
        bull_reasons.append(f"RSI {rsi:.1f} — healthy bullish momentum")
    if arima_direction == "up":
        bull_points += 1
        bull_reasons.append(f"ARIMA trend: upward ({arima_pct:.3f}% slope)")
    if current_price > prev_price:
        bull_points += 0.5
        bull_reasons.append(f"Price rising on last candle")

    # --- Bearish signals ---
    bear_points = 0
    bear_reasons = []
    if current_price < ma20:
        bear_points += 1
        bear_reasons.append(f"Price below MA20 (${ma20:,.0f})")
    if ma20 < ma50:
        bear_points += 1
        bear_reasons.append(f"MA20 below MA50 — Death Cross")
    if rsi > 70:
        bear_points += 1
        bear_reasons.append(f"RSI {rsi:.1f} — overbought territory")
    elif rsi < 30:
        bear_points += 1
        bear_reasons.append(f"RSI {rsi:.1f} — oversold (bearish pressure)")
    if arima_direction == "down":
        bear_points += 1
        bear_reasons.append(f"ARIMA trend: downward ({arima_pct:.3f}% slope)")
    if current_price < prev_price:
        bear_points += 0.5
        bear_reasons.append(f"Price declining on last candle")

    # ── Decision logic ──
    diff = bull_points - bear_points
    if diff >= 2.5:
        signal = "BUY"
        confidence = "High" if diff >= 3.5 else "Medium"
        reasons = bull_reasons
    elif diff <= -2.5:
        signal = "SELL"
        confidence = "High" if diff <= -3.5 else "Medium"
        reasons = bear_reasons
    elif abs(diff) <= 1:
        signal = "HOLD"
        confidence = "Medium"
        reasons = bull_reasons[:1] + bear_reasons[:1] if bull_reasons and bear_reasons else bull_reasons or bear_reasons
    else:
        signal = "BUY" if diff > 0 else "SELL"
        confidence = "Low"
        reasons = bull_reasons if diff > 0 else bear_reasons

    reason_text = ". ".join(reasons) + "." if reasons else "Insufficient signal alignment."

    return {
        "signal": signal,
        "confidence": confidence,
        "price": current_price,
        "ma20": ma20,
        "ma50": ma50,
        "rsi": rsi,
        "arima_direction": arima_direction,
        "arima_forecast": forecast[0],
        "reason": reason_text,
        "bull_score": bull_points,
        "bear_score": bear_points,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
    }

# ─── Backtest Engine ──────────────────────────────────────────────────────────
def run_backtest(df):
    df = df.copy().dropna()
    close = df['close'].astype(float)
    ma20 = close.rolling(20).mean()
    ma50 = close.rolling(50).mean()
    rsi_series = compute_rsi(close)

    trades = []
    in_trade = False
    entry_price = 0.0
    equity = 10000.0
    peak = 10000.0
    max_dd = 0.0

    for i in range(55, len(df)):
        p     = close.iloc[i]
        r     = rsi_series.iloc[i]
        m20   = ma20.iloc[i]
        m50   = ma50.iloc[i]

        bull = (p > m20) and (m20 > m50) and (40 < r < 70)
        bear = (p < m20) and (m20 < m50) and (r > 65 or r < 35)

        if bull and not in_trade:
            entry_price = p
            in_trade = True
            entry_idx = i

        elif bear and in_trade:
            pnl_pct = (p - entry_price) / entry_price * 100
            equity  *= (1 + pnl_pct / 100)
            peak     = max(peak, equity)
            dd       = (peak - equity) / peak * 100
            max_dd   = max(max_dd, dd)
            trades.append({
                "Entry": f"${entry_price:,.2f}",
                "Exit": f"${p:,.2f}",
                "P&L %": f"{pnl_pct:+.2f}%",
                "Result": "✅ Win" if pnl_pct > 0 else "❌ Loss",
            })
            in_trade = False

    total  = len(trades)
    wins   = sum(1 for t in trades if "Win" in t["Result"])
    wr     = (wins / total * 100) if total else 0
    profit = (equity - 10000) / 100

    return {
        "total_trades": total,
        "win_rate": wr,
        "profit_pct": profit,
        "max_drawdown": max_dd,
        "equity_final": equity,
        "trades": trades[-10:],
    }

# ─── Data Fetchers ────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def fetch_binance(symbol="BTCUSDT", interval="15m", limit=200):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        if not isinstance(data, list):
            return None
        df = pd.DataFrame(data, columns=[
            'timestamp','open','high','low','close','volume',
            'ct','qav','n','tbbv','tbqv','ignore'
        ])
        df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
        for c in ['open','high','low','close','volume']:
            df[c] = pd.to_numeric(df[c])
        return df[['datetime','open','high','low','close','volume']]
    except Exception as e:
        return None

def parse_uploaded_csv(file):
    try:
        df = pd.read_csv(file)
        df.columns = [c.strip().lower() for c in df.columns]
        if 'datetime' not in df.columns and 'date' in df.columns:
            df.rename(columns={'date': 'datetime'}, inplace=True)
        df['datetime'] = pd.to_datetime(df['datetime'])
        for c in ['open','high','low','close','volume']:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors='coerce')
        return df.sort_values('datetime').reset_index(drop=True)
    except Exception as e:
        return None

# ─── Chart Builder ────────────────────────────────────────────────────────────
def build_chart(df, sig=None):
    sub = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.72, 0.28], vertical_spacing=0.02)

    # Candles
    sub.add_trace(go.Candlestick(
        x=df['datetime'], open=df['open'], high=df['high'],
        low=df['low'], close=df['close'],
        increasing_line_color='#30D158', decreasing_line_color='#FF453A',
        increasing_fillcolor='rgba(48,209,88,0.7)',
        decreasing_fillcolor='rgba(255,69,58,0.7)',
        line_width=1, name='Price'
    ), row=1, col=1)

    close = df['close'].astype(float)
    ma20 = close.rolling(20).mean()
    ma50 = close.rolling(50).mean()

    sub.add_trace(go.Scatter(x=df['datetime'], y=ma20, name='MA20',
        line=dict(color='rgba(10,132,255,0.8)', width=1.5)), row=1, col=1)
    sub.add_trace(go.Scatter(x=df['datetime'], y=ma50, name='MA50',
        line=dict(color='rgba(255,214,10,0.7)', width=1.5, dash='dot')), row=1, col=1)

    # RSI
    rsi = compute_rsi(close)
    sub.add_trace(go.Scatter(x=df['datetime'], y=rsi, name='RSI',
        line=dict(color='rgba(10,132,255,0.6)', width=1.5),
        fill='tozeroy', fillcolor='rgba(10,132,255,0.04)'), row=2, col=1)
    for lvl, col in [(70,'rgba(255,69,58,0.3)'), (30,'rgba(48,209,88,0.3)'), (50,'rgba(255,255,255,0.1)')]:
        sub.add_hline(y=lvl, line_dash="dot", line_color=col, row=2, col=1)

    sub.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(17,17,17,0.8)',
            bordercolor='rgba(255,255,255,0.06)',
            borderwidth=1,
            font=dict(color='rgba(255,255,255,0.5)', size=11),
            x=0, y=1, xanchor='left', yanchor='top'
        ),
        xaxis=dict(
            showgrid=True, gridcolor='rgba(255,255,255,0.04)',
            zeroline=False, showspikes=True,
            spikecolor='rgba(255,255,255,0.15)', spikethickness=1,
            rangeslider=dict(visible=False),
            tickfont=dict(color='rgba(255,255,255,0.3)', size=10),
        ),
        yaxis=dict(
            showgrid=True, gridcolor='rgba(255,255,255,0.04)',
            zeroline=False, side='right',
            tickfont=dict(color='rgba(255,255,255,0.3)', size=10),
            tickprefix='$', tickformat=',.0f',
        ),
        xaxis2=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', zeroline=False,
                    tickfont=dict(color='rgba(255,255,255,0.3)', size=10)),
        yaxis2=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)',
                    zeroline=False, side='right', range=[0,100],
                    tickfont=dict(color='rgba(255,255,255,0.3)', size=10)),
        height=480,
        hovermode='x unified',
        hoverlabel=dict(bgcolor='rgba(17,17,17,0.95)', bordercolor='rgba(255,255,255,0.1)',
                        font=dict(color='white', size=12)),
    )
    return sub

# ─── UI Components ────────────────────────────────────────────────────────────
def render_signal_card(sig):
    s = sig['signal']
    c = sig['confidence']
    cls_signal = s.lower()
    cls_conf   = c.lower()
    icon = "↑" if s == "BUY" else "↓" if s == "SELL" else "→"
    conf_icon  = "⬤" if c == "High" else "◉" if c == "Medium" else "○"

    st.markdown(f"""
    <div class="signal-hero signal-hero-{cls_signal}">
        <div class="signal-type-row">
            <div class="signal-badge signal-badge-{cls_signal}">{icon} {s}</div>
            <div class="confidence-tag conf-{cls_conf}">{conf_icon} &nbsp;{c} Confidence</div>
        </div>
        <div class="signal-price">${sig['price']:,.2f}</div>
        <div class="signal-meta">BTC/USDT · 15m · {sig['timestamp']}</div>
        <div class="signal-reason"><strong>Analysis:</strong> {sig['reason']}</div>
        <div class="indicator-row">
            <div class="indicator-pill {'ind-bull' if sig['price'] > sig['ma20'] else 'ind-bear'}">
                <span class="ind-label">MA20</span>
                <span class="ind-value">${sig['ma20']:,.0f}</span>
            </div>
            <div class="indicator-pill {'ind-bull' if sig['ma20'] > sig['ma50'] else 'ind-bear'}">
                <span class="ind-label">MA50</span>
                <span class="ind-value">${sig['ma50']:,.0f}</span>
            </div>
            <div class="indicator-pill {'ind-bull' if 40 < sig['rsi'] < 70 else 'ind-bear'}">
                <span class="ind-label">RSI</span>
                <span class="ind-value">{sig['rsi']:.1f}</span>
            </div>
            <div class="indicator-pill {'ind-bull' if sig['arima_direction'] == 'up' else 'ind-bear'}">
                <span class="ind-label">ARIMA</span>
                <span class="ind-value">{sig['arima_direction'].upper()} → ${sig['arima_forecast']:,.0f}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_backtest_metrics(bt):
    wr  = bt['win_rate']
    pnl = bt['profit_pct']
    dd  = bt['max_drawdown']
    wr_class  = "metric-green" if wr >= 55 else "metric-red"
    pnl_class = "metric-green" if pnl >= 0 else "metric-red"
    dd_class  = "metric-red"

    st.markdown(f"""
    <div class="metrics-grid">
        <div class="metric-card">
            <div class="metric-label">Total Trades</div>
            <div class="metric-value metric-blue">{bt['total_trades']}</div>
            <div class="metric-sub">Simulated entries/exits</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Win Rate</div>
            <div class="metric-value {wr_class}">{wr:.1f}%</div>
            <div class="metric-sub">Profitable trades</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Net Profit</div>
            <div class="metric-value {pnl_class}">{pnl:+.2f}%</div>
            <div class="metric-sub">From $10,000 base</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Max Drawdown</div>
            <div class="metric-value {dd_class}">-{dd:.2f}%</div>
            <div class="metric-sub">Peak-to-trough decline</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Nav ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="cipher-nav">
    <div class="cipher-logo">
        <div class="cipher-logo-icon">⚡</div>
        Cipher
    </div>
    <div style="display:flex;align-items:center;gap:16px;">
        <div style="font-size:12px;color:rgba(255,255,255,0.3);font-family:'JetBrains Mono',monospace;">
            BTCUSDT · 15m
        </div>
        <div class="cipher-nav-pill">
            <div class="live-dot"></div>
            Live
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Page body ────────────────────────────────────────────────────────────────
st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["⚡  Live Signals", "📂  CSV Analysis", "📊  Backtest"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 — Live Signals
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    # Timestamp bar
    now_str = datetime.now().strftime("%A, %d %B %Y · %H:%M:%S")
    st.markdown(f"""
    <div class="timestamp-bar">
        <div class="ts-text">{now_str}</div>
        <div class="refresh-badge">🔄 Auto-refresh every 60s</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("AI analyzing market data..."):
        df_live = fetch_binance("BTCUSDT", "15m", 200)

    if df_live is None or len(df_live) < 60:
        st.markdown("""
        <div style="text-align:center;padding:60px 0;">
            <div style="font-size:32px;margin-bottom:16px;">🌐</div>
            <div style="font-size:16px;font-weight:500;margin-bottom:8px;">Connection Error</div>
            <div style="font-size:13px;color:rgba(255,255,255,0.4);">
                Unable to reach Binance API. Try uploading a CSV in the Analysis tab.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        sig = generate_signal(df_live)
        if sig:
            st.markdown('<div class="section-label">Current Signal</div>', unsafe_allow_html=True)
            render_signal_card(sig)

            st.markdown('<div class="section-label" style="margin-top:32px;">Price Chart</div>', unsafe_allow_html=True)
            chart = build_chart(df_live, sig)
            st.plotly_chart(chart, use_container_width=True, config={
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['lasso2d','select2d','autoScale2d'],
            })

            st.markdown("""
            <div class="disclaimer">
                ⚠️ For educational and informational purposes only. Not financial advice. 
                Past performance does not guarantee future results. Always do your own research.
            </div>
            """, unsafe_allow_html=True)

    # Auto-refresh every 60s
    time.sleep(0)
    st.markdown('<script>setTimeout(()=>window.location.reload(),60000)</script>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 — CSV Upload
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="section-label">Upload OHLCV Data</div>
    <div class="upload-zone">
        <div class="upload-icon">📊</div>
        <div class="upload-title">Drop your CSV file here</div>
        <div class="upload-sub">Format: datetime, open, high, low, close, volume</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("", type=["csv"], label_visibility="collapsed")

    if uploaded:
        with st.spinner("Parsing and analyzing data..."):
            df_csv = parse_uploaded_csv(uploaded)

        if df_csv is None or len(df_csv) < 60:
            st.error("Could not parse CSV. Ensure columns: datetime, open, high, low, close, volume")
        else:
            sig_csv = generate_signal(df_csv)
            if sig_csv:
                st.markdown('<div class="section-label" style="margin-top:24px;">Signal</div>', unsafe_allow_html=True)
                sig_csv['timestamp'] = f"{df_csv['datetime'].iloc[-1].strftime('%Y-%m-%d %H:%M')} (CSV)"
                sig_csv['price'] = df_csv['close'].iloc[-1]
                render_signal_card(sig_csv)

                st.markdown('<div class="section-label" style="margin-top:32px;">Chart</div>', unsafe_allow_html=True)
                chart_csv = build_chart(df_csv)
                st.plotly_chart(chart_csv, use_container_width=True, config={
                    'displayModeBar': True, 'displaylogo': False,
                    'modeBarButtonsToRemove': ['lasso2d','select2d'],
                })

                st.markdown("""
                <div class="disclaimer">
                    ⚠️ For educational and informational purposes only. Not financial advice.
                </div>
                """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="margin-top:24px;padding:32px;background:rgba(255,255,255,0.02);
             border:1px solid rgba(255,255,255,0.06);border-radius:14px;text-align:center;">
            <div style="font-size:14px;color:rgba(255,255,255,0.35);margin-bottom:10px;">
                No file uploaded yet
            </div>
            <div style="font-size:12px;color:rgba(255,255,255,0.2);">
                Download the sample CSV below to test
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Sample CSV download
        sample_dates = pd.date_range("2024-01-01", periods=200, freq="15min")
        np.random.seed(42)
        price = 42000.0
        rows = []
        for d in sample_dates:
            o = price
            c = o * (1 + np.random.normal(0, 0.003))
            h = max(o,c) * (1 + abs(np.random.normal(0, 0.002)))
            l = min(o,c) * (1 - abs(np.random.normal(0, 0.002)))
            v = np.random.randint(100, 1000)
            rows.append([d.strftime("%Y-%m-%d %H:%M:%S"), round(o,2), round(h,2), round(l,2), round(c,2), v])
            price = c
        sample_df = pd.DataFrame(rows, columns=['datetime','open','high','low','close','volume'])
        st.download_button(
            label="⬇  Download Sample CSV",
            data=sample_df.to_csv(index=False),
            file_name="cipher_sample_btc.csv",
            mime="text/csv",
        )

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 — Backtest
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-label">Backtest Engine</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="backtest-card">
        <div class="backtest-title">Strategy Simulation</div>
        <div class="backtest-sub">Entry on BUY signal (MA crossover + RSI) · Exit on SELL signal · Starting equity $10,000</div>
    </div>
    """, unsafe_allow_html=True)

    col_src, col_btn = st.columns([3, 1])
    with col_src:
        bt_source = st.selectbox("Data Source", ["Live BTCUSDT (15m)", "Uploaded CSV"], label_visibility="visible")
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        run_bt = st.button("Run Backtest →")

    if run_bt:
        if "Live" in bt_source:
            with st.spinner("Fetching data and running backtest..."):
                df_bt = fetch_binance("BTCUSDT", "15m", 500)
        else:
            df_bt = None
            if uploaded:
                df_bt = parse_uploaded_csv(uploaded)
            if df_bt is None:
                st.warning("Please upload a CSV first.")

        if df_bt is not None and len(df_bt) >= 60:
            bt = run_backtest(df_bt)
            st.markdown('<div class="section-label" style="margin-top:8px;">Performance Metrics</div>', unsafe_allow_html=True)
            render_backtest_metrics(bt)

            if bt['trades']:
                st.markdown('<div class="section-label" style="margin-top:28px;">Last 10 Trades</div>', unsafe_allow_html=True)
                trades_df = pd.DataFrame(bt['trades'])
                st.dataframe(trades_df, use_container_width=True, hide_index=True)

            # Equity curve (simple)
            close = df_bt['close'].astype(float)
            eq = [10000.0]
            ma20s = close.rolling(20).mean()
            ma50s = close.rolling(50).mean()
            rsi_s = compute_rsi(close)
            in_t, ep = False, 0.0
            eq_vals = [10000.0]
            ts_vals  = [df_bt['datetime'].iloc[55]]
            for i in range(55, len(df_bt)):
                p = close.iloc[i]; r = rsi_s.iloc[i]; m20 = ma20s.iloc[i]; m50 = ma50s.iloc[i]
                bull = (p > m20) and (m20 > m50) and (40 < r < 70)
                bear = (p < m20) and (m20 < m50) and (r > 65 or r < 35)
                if bull and not in_t: ep = p; in_t = True
                elif bear and in_t:
                    pnl = (p - ep) / ep; eq_vals[-1] *= (1 + pnl); in_t = False
                eq_vals.append(eq_vals[-1])
                ts_vals.append(df_bt['datetime'].iloc[i])

            fig_eq = go.Figure()
            fig_eq.add_trace(go.Scatter(
                x=ts_vals, y=eq_vals, name='Equity',
                line=dict(color='#0A84FF', width=2),
                fill='tozeroy', fillcolor='rgba(10,132,255,0.06)'
            ))
            fig_eq.add_hline(y=10000, line_dash="dot", line_color="rgba(255,255,255,0.1)")
            fig_eq.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=220, margin=dict(l=0,r=0,t=8,b=0),
                showlegend=False,
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', zeroline=False,
                           tickfont=dict(color='rgba(255,255,255,0.3)', size=10)),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', zeroline=False,
                           side='right', tickprefix='$', tickformat=',.0f',
                           tickfont=dict(color='rgba(255,255,255,0.3)', size=10)),
                hovermode='x unified',
                hoverlabel=dict(bgcolor='rgba(17,17,17,0.95)', font=dict(color='white', size=12)),
            )
            st.markdown('<div class="section-label" style="margin-top:28px;">Equity Curve</div>', unsafe_allow_html=True)
            st.plotly_chart(fig_eq, use_container_width=True, config={'displaylogo': False})

            st.markdown("""
            <div class="disclaimer">
                ⚠️ Backtesting is for simulation only. Past results do not indicate future returns. 
                Slippage, fees, and market impact are not modeled.
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close page-wrapper
