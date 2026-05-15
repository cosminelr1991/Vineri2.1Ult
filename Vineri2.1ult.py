import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
import numpy as np
from datetime import datetime
import io

# ==========================================
# 1. CONFIGURAȚIA PAGINII
# ==========================================
st.set_page_config(page_title="Portfolio Terminal", page_icon="📈", layout="wide")
# ==========================================
# 2. PROTOCOL DE SECURITATE
# ==========================================
def check_password():
    try:
        PAROLA_SECRETA = st.secrets["APP_PASSWORD"]
    except (KeyError, FileNotFoundError):
        st.error("⚠️ Secretul APP_PASSWORD nu este configurat. Adaugă-l în Settings → Secrets pe Streamlit Cloud.")
        st.stop()

    def password_entered():
        if st.session_state.get("password_input") == PAROLA_SECRETA:
            st.session_state["authenticated"] = True
        else:
            st.session_state["authenticated"] = False

    if st.session_state.get("authenticated"):
        return True

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align: center; font-family: Georgia, serif; color: #E8C468; letter-spacing: 2px;'>"
        "AUTENTIFICARE NECESARĂ</h1>",
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input(
            "Cheie de acces:",
            type="password",
            on_change=password_entered,
            key="password_input"
        )
        if "authenticated" in st.session_state and not st.session_state["authenticated"]:
            st.error("Cod incorect. Acces refuzat.")
    return False

if not check_password():
    st.stop()



# ==========================================
# 3. TEMA DARK FINANCE PROFESIONALĂ
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&family=Playfair+Display:wght@400;600&display=swap');

    /* ── Base ─────────────────────────────────── */
    .stApp {
        background-color: #0D1117;
        color: #C9D1D9;
        font-family: 'DM Sans', sans-serif;
    }
    html, body, [class*="css"], .stMarkdown, .stText, p, span, label {
        color: #C9D1D9 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Typography ───────────────────────────── */
    h1 {
        font-family: 'Playfair Display', Georgia, serif !important;
        color: #E8C468 !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        text-align: center;
        font-size: 2rem !important;
        margin-bottom: 0.2rem !important;
        text-shadow: none !important;
    }
    h2, h3 {
        font-family: 'DM Sans', sans-serif !important;
        color: #E0E6F0 !important;
        font-weight: 500 !important;
        letter-spacing: 0.3px !important;
        text-shadow: none !important;
    }
    h4, h5 {
        font-family: 'DM Sans', sans-serif !important;
        color: #8B949E !important;
        font-weight: 400 !important;
        text-transform: uppercase;
        font-size: 0.75rem !important;
        letter-spacing: 1.5px !important;
        text-shadow: none !important;
    }

    /* ── Metric Cards ─────────────────────────── */
    [data-testid="stMetric"] {
        background-color: #161B22;
        padding: 20px 24px;
        border-radius: 8px;
        border: 1px solid #21262D;
        border-top: 2px solid #E8C468;
        transition: border-color 0.2s ease;
    }
    [data-testid="stMetric"]:hover {
        border-top-color: #F0D080;
        background-color: #1C2128;
    }
    [data-testid="stMetricValue"] {
        color: #E0E6F0 !important;
        font-family: 'DM Mono', monospace !important;
        font-weight: 500 !important;
        font-size: 1.4rem !important;
        text-shadow: none !important;
    }
    [data-testid="stMetricLabel"] p {
        color: #8B949E !important;
        font-size: 0.72rem !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }
    [data-testid="stMetricDelta"] {
        font-family: 'DM Mono', monospace !important;
        font-size: 0.85rem !important;
    }

    /* ── Tabs ─────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: transparent;
        border-bottom: 1px solid #21262D;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        border-radius: 0;
        padding: 10px 20px;
        color: #8B949E !important;
        font-size: 0.82rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        transition: all 0.2s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #E0E6F0 !important;
        border-bottom-color: #4A9EFF;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: transparent;
        border-bottom: 2px solid #E8C468;
        color: #E8C468 !important;
        text-shadow: none;
    }

    /* ── DataFrames ───────────────────────────── */
    .stDataFrame {
        border: 1px solid #21262D;
        border-radius: 8px;
        overflow: hidden;
    }
    .stDataFrame thead tr th {
        background-color: #161B22 !important;
        color: #8B949E !important;
        font-size: 0.72rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 1px solid #21262D !important;
    }
    .stDataFrame tbody tr:nth-child(even) {
        background-color: rgba(255,255,255,0.015) !important;
    }

    /* ── Inputs ───────────────────────────────── */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: #161B22 !important;
        color: #C9D1D9 !important;
        border: 1px solid #30363D !important;
        border-radius: 6px !important;
        font-family: 'DM Mono', monospace !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #E8C468 !important;
        box-shadow: 0 0 0 2px rgba(232, 196, 104, 0.12) !important;
    }

    /* ── Sidebar ──────────────────────────────── */
    .stSidebar {
        background-color: #0D1117;
        border-right: 1px solid #21262D;
    }

    /* ── Buttons ──────────────────────────────── */
    .stButton > button {
        background-color: transparent;
        color: #E8C468;
        border: 1px solid #E8C468;
        border-radius: 6px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.82rem;
        font-weight: 500;
        letter-spacing: 0.5px;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        background-color: rgba(232, 196, 104, 0.08);
        border-color: #F0D080;
        color: #F0D080;
    }

    /* ── Divider ──────────────────────────────── */
    hr {
        border-color: #21262D !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Custom Components ────────────────────── */
    .fin-card {
        background: #161B22;
        border: 1px solid #21262D;
        border-radius: 8px;
        padding: 18px 20px;
    }
    .fin-card-accent {
        border-left: 3px solid #E8C468;
    }
    .fin-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.70rem;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        color: #8B949E;
        margin-bottom: 4px;
    }
    .fin-value {
        font-family: 'DM Mono', monospace;
        font-size: 1.2rem;
        color: #E0E6F0;
        font-weight: 500;
    }
    .fin-value-gold {
        color: #E8C468;
    }
    .fin-value-green {
        color: #2ECC71;
    }
    .fin-value-red {
        color: #E74C3C;
    }
    .page-subtitle {
        text-align: center;
        color: #8B949E;
        font-size: 0.78rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-top: -8px;
        margin-bottom: 24px;
    }
    .section-header {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.70rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #8B949E;
        border-bottom: 1px solid #21262D;
        padding-bottom: 8px;
        margin-bottom: 16px;
    }
    .alert-box {
        border-left: 3px solid;
        padding: 12px 16px;
        margin-bottom: 8px;
        border-radius: 0 6px 6px 0;
        background-color: rgba(255,255,255,0.03);
        font-family: 'DM Sans', sans-serif;
        font-size: 0.88rem;
    }
    .alert-buy { border-color: #2ECC71; }
    .alert-sell { border-color: #E74C3C; }
    .cache-info {
        background: rgba(255,255,255,0.02);
        border: 1px solid #21262D;
        border-radius: 6px;
        padding: 8px 12px;
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        color: #8B949E !important;
    }
    .evo-box {
        background: #161B22;
        border: 1px solid #21262D;
        border-radius: 8px;
        padding: 24px;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .scorecard-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 0;
        border-bottom: 1px solid #21262D;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.88rem;
    }
    .scorecard-row:last-child { border-bottom: none; }
    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .badge-green { background: rgba(46,204,113,0.15); color: #2ECC71; }
    .badge-red { background: rgba(231,76,60,0.15); color: #E74C3C; }
    .badge-yellow { background: rgba(232,196,104,0.15); color: #E8C468; }
    .badge-gray { background: rgba(139,148,158,0.15); color: #8B949E; }
</style>
""", unsafe_allow_html=True)

# ── Paleta de culori pentru grafice ────────────
C = {
    'bg':       '#0D1117',
    'surface':  '#161B22',
    'border':   '#21262D',
    'text':     '#C9D1D9',
    'text_dim': '#8B949E',
    'gold':     '#E8C468',
    'blue':     '#4A9EFF',
    'green':    '#2ECC71',
    'red':      '#E74C3C',
    'grid':     'rgba(255,255,255,0.05)',
}

PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=C['text'], family="DM Sans, sans-serif", size=12),
)

# Ax defaults reutilizabile — folosite explicit per grafic
AX = dict(gridcolor=C['grid'], linecolor=C['border'], tickfont=dict(color=C['text_dim'], size=11))

# ==========================================
# 4. PARSER GOOGLE SHEETS
# ==========================================
def get_google_sheet_data(sheet_url):
    try:
        csv_url = sheet_url.replace('/edit?gid=', '/export?format=csv&gid=')
        if '/edit' in csv_url and '&gid=' not in csv_url:
            csv_url = sheet_url.replace('/edit', '/export?format=csv')
        df_raw = pd.read_csv(csv_url)
        df_raw.columns = [str(c).strip() for c in df_raw.columns]
        mapping = {}
        found_simbol = found_actiuni = found_pret = False
        for col in df_raw.columns:
            c_low = col.lower()
            if not found_simbol and any(k in c_low for k in ['symbol', 'ticker', 'simbol']):
                mapping[col] = 'Simbol'; found_simbol = True
            elif not found_actiuni and any(k in c_low for k in ['quantity', 'actiuni', 'cantitate', 'qty', 'buc']):
                mapping[col] = 'Actiuni'; found_actiuni = True
            elif not found_pret and any(k in c_low for k in ['mediu', 'cost', 'achizitie', 'avg']):
                mapping[col] = 'Pret_Mediu_Achizitie_US$'; found_pret = True
        if not found_pret:
            for col in df_raw.columns:
                c_low = col.lower()
                if any(k in c_low for k in ['price', 'pret']) and not any(k in c_low for k in ['curent', 'actual', 'live']):
                    mapping[col] = 'Pret_Mediu_Achizitie_US$'; break
        if len(mapping) < 3:
            st.error(f"Nu am găsit toate coloanele necesare. Identificate: {list(mapping.values())}")
            return None
        df_cleaned = df_raw[list(mapping.keys())].rename(columns=mapping)
        df_cleaned = df_cleaned.dropna(subset=['Simbol', 'Actiuni'])
        def clean_number(val):
            if pd.isna(val): return 0.0
            val_str = str(val).replace('$','').replace('€','').replace('£','').replace(' ','').replace(',','')
            try: return float(val_str)
            except: return 0.0
        df_cleaned['Actiuni'] = df_cleaned['Actiuni'].apply(clean_number)
        df_cleaned['Pret_Mediu_Achizitie_US$'] = df_cleaned['Pret_Mediu_Achizitie_US$'].apply(clean_number)
        df_cleaned['Simbol'] = df_cleaned['Simbol'].astype(str).str.upper().str.strip()
        return df_cleaned[df_cleaned['Actiuni'] > 0].copy()
    except Exception as e:
        st.error(f"Eroare la citirea Google Sheet: {e}")
        return None

# ==========================================
# 5. FUNCȚII DATE LIVE
# ==========================================
def fetch_live_data(tickers, cache_key):
    live_data = {}
    progress = st.progress(0, text="Se preiau date live...")
    total = len(tickers)
    for idx, ticker in enumerate(tickers):
        progress.progress((idx + 1) / total, text=f"Preiau date pentru {ticker}...")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            pret_curent = info.get("currentPrice") or info.get("regularMarketPrice") or 0
            pret_anterior = info.get("regularMarketPreviousClose") or pret_curent
            div_rate = info.get("dividendRate") or 0
            div_yield_calculat = (div_rate / pret_curent * 100) if pret_curent > 0 and div_rate else 0
            pay_div_ts = info.get("dividendDate") or info.get("exDividendDate")
            pay_div_date = datetime.fromtimestamp(pay_div_ts).strftime('%Y-%m-%d') if pay_div_ts else "N/A"
            earnings_date = "N/A"
            try:
                cal = stock.calendar
                if cal is not None and 'Earnings Date' in cal:
                    ed = cal['Earnings Date']
                    if isinstance(ed, list) and len(ed) > 0:
                        earnings_date = ed[0].strftime('%Y-%m-%d')
            except: pass
            live_data[ticker] = {
                "Pret_Actual_Live": pret_curent, "Pret_Anterior_Live": pret_anterior,
                "PE_Ratio": info.get("trailingPE") or 0, "Sector_Live": info.get("sector") or "N/A",
                "Nume_Companie": info.get("shortName") or ticker, "Div_Yield": div_yield_calculat,
                "Div_Rate": div_rate, "Payment_Date": pay_div_date, "Earnings_Date": earnings_date,
                "Descriere": info.get("longBusinessSummary") or "Nicio descriere disponibilă.",
                "Market_Cap": info.get("marketCap") or 0, "Profit_Margin": info.get("profitMargins") or 0,
                "ROE": info.get("returnOnEquity") or 0, "Beta": info.get("beta") or 1,
                "Current_Ratio": info.get("currentRatio") or 0, "Debt_Equity": info.get("debtToEquity") or 0,
                "Payout_Ratio": (info.get("payoutRatio") or 0) * 100,
                "sharesOutstanding": info.get("sharesOutstanding") or 1,
                "Trailing_EPS": info.get("trailingEps") or 0, "Forward_EPS": info.get("forwardEps") or 0,
                "52W_High": info.get("fiftyTwoWeekHigh") or 0, "52W_Low": info.get("fiftyTwoWeekLow") or 0,
                "Avg_Volume": info.get("averageVolume") or 0,
            }
        except Exception as e:
            st.warning(f"Nu am putut prelua date pentru {ticker}: {e}")
            live_data[ticker] = {
                "Pret_Actual_Live": 0, "Pret_Anterior_Live": 0, "PE_Ratio": 0, "Sector_Live": "N/A",
                "Nume_Companie": ticker, "Div_Yield": 0, "Div_Rate": 0, "Payment_Date": "N/A",
                "Earnings_Date": "N/A", "Descriere": "Eroare la preluarea datelor.", "Market_Cap": 0,
                "Profit_Margin": 0, "ROE": 0, "Beta": 1, "Current_Ratio": 0, "Debt_Equity": 0,
                "Payout_Ratio": 0, "sharesOutstanding": 1, "Trailing_EPS": 0, "Forward_EPS": 0,
                "52W_High": 0, "52W_Low": 0, "Avg_Volume": 0,
            }
    progress.empty()
    return live_data

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_live_data_cached(tickers_tuple, cache_key):
    return fetch_live_data(list(tickers_tuple), cache_key)

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_dividend_history(tickers_tuple, cache_key):
    """
    Returnează pentru fiecare ticker plățile lunare estimate pentru viitor,
    bazate pe istoricul din ultimul an calendaristic complet.

    Logică:
    - Luăm istoricul de dividende din ultimele 13 luni.
    - Grupăm plățile pe luna calendaristică (0=Ian, 11=Dec).
    - SUMĂM toate plățile per share din aceeași lună (unele companii plătesc
      de 2 ori sau au dividende speciale — nu suprascrie, ci adunăm).
    - Dacă aceeași lună apare atât în 2024 cât și în 2025, păstrăm DOAR
      cea mai recentă apariție (un singur ciclu anual per lună).

    Rezultat: { ticker: { month_idx(0-11): div_per_share_total_luna } }
    """
    result = {}
    for ticker in tickers_tuple:
        try:
            hist = yf.Ticker(ticker).dividends
            if hist is None or hist.empty:
                result[ticker] = {}
                continue

            # Fereastra: ultimele 13 luni (puțin mai mult pentru a prinde ciclul complet)
            cutoff = pd.Timestamp.now(tz='UTC') - pd.DateOffset(months=13)
            recent = hist[hist.index >= cutoff].copy()
            if recent.empty:
                # Fallback: ultimele max 12 plăți istorice
                recent = hist.tail(12).copy()

            # Construim: (year, month) -> sum of dividends per share
            # Grupăm pe (an, lună) ca să sumăm plăți multiple din aceeași lună
            payments = {}  # (year, month_0indexed) -> total_div_per_share
            for dt, val in recent.items():
                key = (dt.year, dt.month - 1)  # month 0-indexed
                payments[key] = payments.get(key, 0.0) + float(val)

            # Acum colapsăm pe lună calendaristică:
            # Dacă Ian 2024 și Ian 2025 există ambele, păstrăm cea mai recentă (2025).
            month_map = {}  # month_idx -> div_per_share
            for (year, month_idx), total_div in sorted(payments.items()):
                # sorted asc → iterăm cronologic, deci ultimul scrie (cel mai recent)
                month_map[month_idx] = total_div

            result[ticker] = month_map
        except:
            result[ticker] = {}
    return result

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_benchmarks(cache_key):
    try:
        result = {}
        for sym in ["SPY", "QQQ", "DIA"]:
            t = yf.Ticker(sym)
            data = t.history(period="1y")['Close'].dropna()
            result[sym] = (data / data.iloc[0]) * 100
        return pd.DataFrame(result)
    except:
        return pd.DataFrame()

# ==========================================
# 6. SIDEBAR
# ==========================================
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Nk41AxVryPWOk9Bt9kSWF3k0WtYZqe4Phpi4uEqKUWo/edit?gid=0#gid=0"

st.sidebar.markdown(
    "<p style='font-family: DM Mono, monospace; font-size: 0.75rem; color: #8B949E; "
    "letter-spacing: 2px; text-transform: uppercase; margin-bottom: 16px;'>Portfolio Terminal</p>",
    unsafe_allow_html=True
)
st.sidebar.markdown("<div class='cache-info'>Sursă: Google Sheets — Sync Automat</div>", unsafe_allow_html=True)
st.sidebar.write("")

if "refresh_key" not in st.session_state:
    st.session_state["refresh_key"] = 0

if st.sidebar.button("↻  Refresh Date Live", use_container_width=True):
    st.session_state["refresh_key"] += 1
    st.cache_data.clear()
    st.rerun()

last_refresh = st.session_state.get("last_refresh_time", "—")
st.sidebar.markdown(
    f"<div class='cache-info' style='margin-top: 8px;'>Cache: ~60 min &nbsp;|&nbsp; Ultimul: {last_refresh}</div>",
    unsafe_allow_html=True
)
st.session_state["last_refresh_time"] = datetime.now().strftime("%H:%M:%S")

# ==========================================
# 7. DATE & CALCULE
# ==========================================
df_base = get_google_sheet_data(SHEET_URL)
if df_base is None or df_base.empty:
    st.warning("Așteptare date sau format incorect.")
    st.stop()

cache_key = st.session_state["refresh_key"]
tickers_tuple = tuple(df_base["Simbol"].tolist())

with st.spinner("Se preiau date de piață..."):
    live_info = fetch_live_data_cached(tickers_tuple, cache_key)
    benchmarks = fetch_benchmarks(cache_key)
    div_history = fetch_dividend_history(tickers_tuple, cache_key)

df = df_base.copy()
df["Pret_Actual_US$"]    = df["Simbol"].map(lambda x: live_info[x]["Pret_Actual_Live"])
df["Pret_Anterior_US$"]  = df["Simbol"].map(lambda x: live_info[x]["Pret_Anterior_Live"])
df["Companie"]           = df["Simbol"].map(lambda x: live_info[x]["Nume_Companie"])
df["Sector"]             = df["Simbol"].map(lambda x: live_info[x]["Sector_Live"])
df["PE_Ratio"]           = df["Simbol"].map(lambda x: live_info[x]["PE_Ratio"])
df["Venit_Anual_Div_US$"]= df.apply(lambda r: live_info[r["Simbol"]]["Div_Rate"] * r["Actiuni"], axis=1)
df["Payment_Date"]       = df["Simbol"].map(lambda x: live_info[x]["Payment_Date"])
df["Earnings_Date"]      = df["Simbol"].map(lambda x: live_info[x]["Earnings_Date"])
df["Logo"]               = df["Simbol"].map(lambda x: f"https://financialmodelingprep.com/image-stock/{x}.png")
df["Valoare_Actuala"]    = df["Actiuni"] * df["Pret_Actual_US$"]
df["Valoare_Anterioara"] = df["Actiuni"] * df["Pret_Anterior_US$"]
df["Valoare_Investita"]  = df["Actiuni"] * df["Pret_Mediu_Achizitie_US$"]
df["Profit_Net"]         = df["Valoare_Actuala"] - df["Valoare_Investita"]
df["Profit_%"]           = (df["Profit_Net"] / df["Valoare_Investita"].replace(0, np.nan)) * 100
df["Yield_on_Cost_%"]    = (df["Venit_Anual_Div_US$"] / df["Valoare_Investita"].replace(0, np.nan)) * 100
df["Pondere_%"]          = (df["Valoare_Actuala"] / df["Valoare_Actuala"].sum()) * 100
df["Daily_Change_%"]     = np.where(
    df["Pret_Anterior_US$"] > 0,
    ((df["Pret_Actual_US$"] - df["Pret_Anterior_US$"]) / df["Pret_Anterior_US$"]) * 100, 0
)
df["Payout_Ratio"]  = df["Simbol"].map(lambda x: live_info[x]["Payout_Ratio"])
df["Current_Ratio"] = df["Simbol"].map(lambda x: live_info[x]["Current_Ratio"])
df["Profit_Margin"] = df["Simbol"].map(lambda x: live_info[x]["Profit_Margin"])
df["Beta"]          = df["Simbol"].map(lambda x: live_info[x]["Beta"])

total_value      = df["Valoare_Actuala"].sum()
total_value_prev = df["Valoare_Anterioara"].sum()
total_invested   = df["Valoare_Investita"].sum()
total_profit     = df["Profit_Net"].sum()
total_dividends  = df["Venit_Anual_Div_US$"].sum()
daily_change_usd = total_value - total_value_prev
daily_change_pct = (daily_change_usd / total_value_prev * 100) if total_value_prev > 0 else 0

if 'price_alerts' not in st.session_state:
    st.session_state['price_alerts'] = {t: {'buy': 0.0, 'sell': 0.0} for t in tickers_tuple}
else:
    for t in tickers_tuple:
        if t not in st.session_state['price_alerts']:
            st.session_state['price_alerts'][t] = {'buy': 0.0, 'sell': 0.0}

# ==========================================
# ==========================================
# 8. HEADER PRINCIPAL (5 METRICE - EVOLUȚIA ZILNICĂ MUTATĂ SUS)
# ==========================================
st.markdown("<h1>PORTFOLIO TERMINAL</h1>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Market Intelligence Dashboard</p>", unsafe_allow_html=True)

# Definim 5 coloane
c1, c2, c3, c4, c5 = st.columns(5)
pct_total = (total_profit / total_invested * 100) if total_invested else 0

c1.metric("VALOARE TOTALĂ", f"${total_value:,.2f}")
c2.metric("PROFIT NEREALIZAT", f"${total_profit:,.2f}", f"{pct_total:.2f}%")
# Coloana 3: Evoluția Zilnică (acum este vizibilă aici)
c3.metric("EVOLUȚIE ZILNICĂ", f"${daily_change_usd:,.2f}", f"{daily_change_pct:+.2f}%")
c4.metric("FLUX ANUAL DIVIDENDE", f"${total_dividends:,.2f}")
c5.metric("RANDAMENT YoC", f"{(total_dividends/total_invested*100) if total_invested else 0:.2f}%")

st.write("")
# ==========================================
# 9. TABS
# ==========================================
tab1, tab_ai, tab2, tab3, tab4, tab_alerts = st.tabs([
    "Matricea Portofoliului",
    "Diagnoză AI",
    "Fluxuri & Evenimente",
    "Rebalansare",
    "Deep Dive",
    "Alerte Preț"
])

# ==========================================
# TAB 1: MATRICEA PORTOFOLIULUI
# ==========================================
with tab1:
    def style_val(val):
        if isinstance(val, (int, float)):
            if val > 0: return f'color: {C["green"]}; font-weight: 500;'
            elif val < 0: return f'color: {C["red"]}; font-weight: 500;'
        return ''

    st.markdown("<p class='section-header'>MIȘCĂRILE ZILEI — TOP 5</p>", unsafe_allow_html=True)
    c_top1, c_top2 = st.columns(2)
    top_5_gainers = df.nlargest(5, 'Daily_Change_%')[['Logo','Simbol','Companie','Daily_Change_%']]
    top_5_losers  = df.nsmallest(5, 'Daily_Change_%')[['Logo','Simbol','Companie','Daily_Change_%']]

    with c_top1:
        st.markdown(f"<p style='color: {C['green']}; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase;'>▲ Creșteri</p>", unsafe_allow_html=True)
        st.dataframe(
            top_5_gainers.style.format({'Daily_Change_%': '{:+.2f}%'}).map(style_val, subset=['Daily_Change_%']),
            column_config={"Logo": st.column_config.ImageColumn(""), "Daily_Change_%": "Variație (%)"},
            hide_index=True, use_container_width=True
        )
    with c_top2:
        st.markdown(f"<p style='color: {C['red']}; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase;'>▼ Scăderi</p>", unsafe_allow_html=True)
        st.dataframe(
            top_5_losers.style.format({'Daily_Change_%': '{:+.2f}%'}).map(style_val, subset=['Daily_Change_%']),
            column_config={"Logo": st.column_config.ImageColumn(""), "Daily_Change_%": "Variație (%)"},
            hide_index=True, use_container_width=True
        )

    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        # ── Grafic 1: Alocare vs Performanță (Sunburst-ul tău clasic) ──
        fig_sunburst = px.sunburst(
            df, path=['Sector', 'Simbol'], values='Valoare_Actuala',
            color='Profit_%',
            color_continuous_scale=[[0, C['red']], [0.5, '#2A2A3A'], [1, C['green']]],
            color_continuous_midpoint=0,
            title="Harta Profitabilității"
        )
        fig_sunburst.update_traces(
            textinfo="label+percent parent",
            insidetextorientation='radial',
            marker=dict(line=dict(color=C['bg'], width=1.5))
        )
        fig_sunburst.update_layout(
            **PLOTLY_BASE,
            title_font=dict(color=C['text_dim'], size=13, family="DM Sans"),
            height=520,
            margin=dict(t=40, b=20, l=10, r=10),
        )
        st.plotly_chart(fig_sunburst, use_container_width=True)

    with col_b:
        # ── Grafic 2: Evoluție vs Preț Mediu (Randament %) ──
        # Pregătim textul pentru a afișa Profit % direct pe grafic
        df_plot = df.copy()
        df_plot['Label_Profit'] = df_plot['Profit_%'].apply(lambda x: f"{x:+.1f}%")

        fig_perf = px.sunburst(
            df_plot, 
            path=['Sector', 'Simbol'], 
            values='Valoare_Actuala',
            color='Profit_%', # Colorăm în funcție de performanță
            color_continuous_scale=[[0, C['red']], [0.5, '#1E2329'], [1, C['green']]],
            color_continuous_midpoint=0,
            title="Evoluție vs Preț Mediu (%)"
        )
        
        fig_perf.update_traces(
            # Configurăm să afișeze Ticker-ul și Profitul Procentual (ex: CSCO +116.2%)
            textinfo="label+text",
            text=df_plot['Label_Profit'],
            insidetextorientation='horizontal',
            marker=dict(line=dict(color=C['bg'], width=1.5)),
            hovertemplate="<b>%{label}</b><br>Profit: %{text}<br>Valoare: $%{value:,.0f}<extra></extra>"
        )

        fig_perf.update_layout(
            **PLOTLY_BASE,
            title_font=dict(color=C['text_dim'], size=13, family="DM Sans"),
            height=520,
            margin=dict(t=40, b=20, l=10, r=10),
            coloraxis_showscale=False 
        )
        
        # Adăugăm totalul în centru pentru design-ul de gogoașă
        total_pct = (total_profit / total_invested * 100) if total_invested else 0
        center_color = C['green'] if total_pct >= 0 else C['red']
        
        fig_perf.add_annotation(
            text=f"<b style='font-size:18px'>{"+" if total_pct >= 0 else ""}{total_pct:.1f}%</b><br>"
                 f"<span style='font-size:11px;color:{C['text_dim']}'>Portofoliu</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(color=center_color, family="DM Mono, monospace")
        )

        st.plotly_chart(fig_perf, use_container_width=True)

    st.divider()
    
    # Benchmark pe toată lățimea
    st.markdown("<p class='section-header'>BENCHMARK COMPARATIV — 1 AN</p>", unsafe_allow_html=True)
    if not benchmarks.empty:
        bench_colors = [C['gold'], C['blue'], C['text_dim']]
        fig_bench = go.Figure()
        for i, col_name in enumerate(benchmarks.columns):
            fig_bench.add_trace(go.Scatter(
                x=benchmarks.index, y=benchmarks[col_name], name=col_name,
                line=dict(color=bench_colors[i % len(bench_colors)], width=2)
            ))
        fig_bench.update_layout(
            **PLOTLY_BASE,
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(color=C['text_dim'], size=11)
            ),
            xaxis=dict(**AX),
            yaxis=dict(title="Valoare Normalizată (Baza 100)", **AX),
            height=400
        )
        st.plotly_chart(fig_bench, use_container_width=True)
# ==========================================
# TAB AI: DIAGNOZĂ
# ==========================================
with tab_ai:
    st.markdown("<p class='section-header'>RAPORT DE SĂNĂTATE A PORTOFOLIULUI</p>", unsafe_allow_html=True)

    # ── Claude AI Narrative Analysis ──────────────
    st.markdown(f"""
    <div style='background: #161B22; border: 1px solid #21262D; border-left: 3px solid #E8C468;
                border-radius: 8px; padding: 16px 20px; margin-bottom: 20px;'>
        <p style='font-size: 0.70rem; text-transform: uppercase; letter-spacing: 2px;
                  color: #8B949E; margin: 0 0 8px 0;'>DIAGNOZĂ NARATIVĂ — CLAUDE AI</p>
    """, unsafe_allow_html=True)

    if st.button("🧠 Generează Analiză AI a Portofoliului", use_container_width=False):
        # Construim contextul pentru Claude
        portfolio_summary = []
        for _, row in df.iterrows():
            sym = row['Simbol']
            li = live_info[sym]
            portfolio_summary.append(
                f"- {sym} ({li['Nume_Companie']}): "
                f"P/E={li['PE_Ratio']:.1f}, "
                f"Beta={li['Beta']:.2f}, "
                f"Profit%={row['Profit_%']:.1f}%, "
                f"Pondere%={row['Pondere_%']:.1f}%, "
                f"DivYield={li['Div_Yield']:.2f}%, "
                f"PayoutRatio={li['Payout_Ratio']:.0f}%, "
                f"ProfitMargin={li['Profit_Margin']*100:.1f}%, "
                f"ROE={li['ROE']*100:.1f}%, "
                f"CurrentRatio={li['Current_Ratio']:.2f}, "
                f"DebtEquity={li['Debt_Equity']:.2f}, "
                f"Sector={li['Sector_Live']}"
            )

        prompt = f"""Ești un analist financiar senior specializat în portofolii de acțiuni individuale.
Analizează acest portofoliu și oferă un comentariu narativ profesionist, specific și acționabil în română.

DATE PORTOFOLIU:
Valoare totală: ${total_value:,.0f}
Profit nerealizat: ${total_profit:,.0f} ({pct_total:.1f}%)
Flux dividende anual: ${total_dividends:,.0f}
Schimbare zilnică: ${daily_change_usd:+,.0f} ({daily_change_pct:+.2f}%)

POZIȚII:
{chr(10).join(portfolio_summary)}

Structurează răspunsul astfel (fără markdown excesiv, ton profesionist):

1. REZUMAT EXECUTIV (2-3 fraze despre starea generală)
2. PUNCTE FORTE (max 3 aspecte pozitive specifice)  
3. RISCURI IDENTIFICATE (max 3 riscuri concrete, cu ticker-ele specifice)
4. RECOMANDĂRI (max 3 acțiuni concrete pe termen scurt)

Fii specific — menționează ticker-ele, valorile, și comparații cu benchmark-uri standard."""

        with st.spinner("Claude analizează portofoliul..."):
            try:
                import requests
                response = requests.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={"Content-Type": "application/json"},
                    json={
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": 1000,
                        "messages": [{"role": "user", "content": prompt}]
                    }
                )
                data = response.json()
                ai_text = data["content"][0]["text"] if data.get("content") else "Eroare la generarea analizei."

                # Salvăm în session state
                st.session_state["ai_narrative"] = ai_text

            except Exception as e:
                st.session_state["ai_narrative"] = f"Eroare conexiune API: {e}"

    # Afișăm analiza dacă există
    if "ai_narrative" in st.session_state and st.session_state["ai_narrative"]:
        narrative = st.session_state["ai_narrative"]
        # Formatăm paragrafele
        paragraphs = narrative.strip().split('\n')
        formatted = ""
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
            if any(p.startswith(prefix) for prefix in ["1.", "2.", "3.", "4.", "REZUMAT", "PUNCTE", "RISCURI", "RECOMAND"]):
                formatted += f"<p style='color: #E8C468; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; margin: 14px 0 6px 0;'>{p}</p>"
            else:
                formatted += f"<p style='color: #C9D1D9; font-size: 0.88rem; line-height: 1.7; margin: 0 0 6px 0;'>{p}</p>"
        st.markdown(formatted, unsafe_allow_html=True)
    else:
        st.markdown(
            "<p style='color: #8B949E; font-size: 0.85rem; font-style: italic;'>"
            "Apasă butonul pentru a genera o analiză narativă a portofoliului tău.</p>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.divider()

    # ── Tabelele de diagnoză ───────────────────────
    c_ai1, c_ai2 = st.columns(2)

    def ai_table(df_in, fmt_col, fmt_str, label_col):
        if not df_in.empty:
            st.dataframe(
                df_in.style.format({fmt_col: fmt_str}),
                column_config={"Logo": st.column_config.ImageColumn("")},
                hide_index=True, use_container_width=True
            )
        else:
            st.success("✓ Nicio problemă detectată.")

    with c_ai1:
        st.markdown(f"<p style='color: {C['gold']}; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; margin-top: 12px;'>Evaluare Excesivă (P/E > 35)</p>", unsafe_allow_html=True)
        ai_table(df[(df['PE_Ratio']>35)&(df['PE_Ratio']<500)][['Logo','Simbol','Companie','PE_Ratio']].sort_values('PE_Ratio', ascending=False), 'PE_Ratio', '{:.2f}', 'PE_Ratio')

        st.markdown(f"<p style='color: {C['red']}; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; margin-top: 16px;'>Lichiditate Scăzută (Current Ratio < 1)</p>", unsafe_allow_html=True)
        ai_table(df[(df['Current_Ratio']>0)&(df['Current_Ratio']<1)&(df['Sector']!='Financial Services')][['Logo','Simbol','Companie','Current_Ratio']].sort_values('Current_Ratio'), 'Current_Ratio', '{:.2f}', 'Current_Ratio')

        st.markdown(f"<p style='color: {C['red']}; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; margin-top: 16px;'>Marjă Profit Negativă</p>", unsafe_allow_html=True)
        ai_table(df[df['Profit_Margin']<0][['Logo','Simbol','Companie','Profit_Margin']].sort_values('Profit_Margin'), 'Profit_Margin', '{:.2%}', 'Profit_Margin')

    with c_ai2:
        st.markdown(f"<p style='color: {C['gold']}; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; margin-top: 12px;'>Risc Tăiere Dividend (Payout > 80%)</p>", unsafe_allow_html=True)
        ai_table(df[(df['Payout_Ratio']>80)&(df['Venit_Anual_Div_US$']>0)&(df['Sector']!='Real Estate')][['Logo','Simbol','Companie','Payout_Ratio']].sort_values('Payout_Ratio', ascending=False), 'Payout_Ratio', '{:.1f}%', 'Payout_Ratio')

        st.markdown(f"<p style='color: {C['blue']}; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; margin-top: 16px;'>Volatilitate Ridicată (Beta > 1.5)</p>", unsafe_allow_html=True)
        ai_table(df[df['Beta']>1.5][['Logo','Simbol','Companie','Beta']].sort_values('Beta', ascending=False), 'Beta', '{:.2f}', 'Beta')

        st.markdown(f"<p style='color: {C['red']}; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; margin-top: 16px;'>Concentrare Excesivă (> 15%)</p>", unsafe_allow_html=True)
        ai_table(df[df['Pondere_%']>15][['Logo','Simbol','Companie','Pondere_%']].sort_values('Pondere_%', ascending=False), 'Pondere_%', '{:.2f}%', 'Pondere_%')

# ==========================================
# ==========================================
# TAB 3: FLUXURI & EVENIMENTE
# ==========================================
with tab2:
    st.markdown("<p class='section-header'>DISTRIBUȚIE NOMINALĂ DIVIDENDE</p>", unsafe_allow_html=True)
    
    # 1. Creăm o funcție de rezervă pentru când yfinance nu returnează "dividendRate"
    df_div = df.copy()
    def recalc_div(row):
        venit = row["Venit_Anual_Div_US$"]
        # Dacă API-ul a dat 0$, dar știm că există un randament (Yield > 0), recalculăm matematic
        if (venit == 0 or pd.isna(venit)):
            yield_pct = live_info[row['Simbol']].get('Div_Yield', 0)
            if yield_pct > 0:
                venit = row['Pret_Actual_US$'] * (yield_pct / 100) * row['Actiuni']
        return venit
        
    df_div['Venit_Anual_Corectat'] = df_div.apply(recalc_div, axis=1)
    
    # Păstrăm doar companiile care au un venit > 0 DUPĂ corecție
    df_div_nom = df_div[df_div["Venit_Anual_Corectat"] > 0].sort_values("Venit_Anual_Corectat", ascending=True)

    if df_div_nom.empty:
        st.info("Nicio acțiune plătitoare de dividende în portofoliu.")
    else:
        fig_div_nom = px.bar(
            df_div_nom, x='Simbol', y='Venit_Anual_Corectat',
            text='Venit_Anual_Corectat', height=450,
            category_orders={'Simbol': df_div_nom['Simbol'].tolist()}
        )
        fig_div_nom.update_traces(
            texttemplate='$%{text:,.2f}', textposition='outside',
            marker_color=C['gold'], textfont=dict(color=C['text_dim'], size=11)
        )
        fig_div_nom.update_layout(
            **PLOTLY_BASE,
            margin=dict(l=10, r=20, t=40, b=60),
            xaxis=dict(**AX, title="Companie", tickangle=-45),
            yaxis=dict(**AX, title="Suma Anuală Estimată ($)", rangemode='tozero')
        )
        st.plotly_chart(fig_div_nom, use_container_width=True)

    st.divider()
    col_mock, col_real = st.columns([1, 1.3])
    
    with col_mock:
        st.markdown("<p class='section-header'>PROIECȚIE FLUX LUNAR DIVIDENDE</p>", unsafe_allow_html=True)
        luni_label = ["Ian","Feb","Mar","Apr","Mai","Iun","Iul","Aug","Sep","Oct","Nov","Dec"]
        calendar_data = {i: 0.0 for i in range(12)}
        calendar_detail = {i: [] for i in range(12)}

        if not df_div_nom.empty:
            for _, row in df_div_nom.iterrows():
                sym = row["Simbol"]
                actiuni = row["Actiuni"]
                venit_anual = row["Venit_Anual_Corectat"]
                month_map = div_history.get(sym, {})

                if month_map:
                    # Avem date reale din istoric yfinance.
                    # month_map: { month_idx(0-11): div_per_share_total_pentru_luna }
                    # Suma lunară primită = div_per_share * număr acțiuni deținute
                    # Scalăm plățile istorice proporțional cu dividendRate curent,
                    # ca să reflectăm dividendul actual (nu cel de acum 12 luni).
                    total_din_istoric = sum(month_map.values())  # total anual din istoric (per share)
                    div_rate_curent = live_info[sym].get("Div_Rate", 0)

                    # Factor de scalare: dacă avem un dividendRate curent valid, ajustăm
                    if div_rate_curent > 0 and total_din_istoric > 0:
                        scale = div_rate_curent / total_din_istoric
                    else:
                        scale = 1.0  # folosim istoricul ca atare

                    for month_idx, div_ps_istoric in month_map.items():
                        div_ps_actual = div_ps_istoric * scale
                        suma = div_ps_actual * actiuni
                        calendar_data[month_idx] += suma
                        calendar_detail[month_idx].append(f"{sym}: ${suma:.2f}")
                else:
                    # Fallback pentru companii fără istoric în yfinance:
                    # distribuim venitul anual estimat pe lunile tipice de plată.
                    div_rate = live_info[sym].get("Div_Rate", 0)
                    if div_rate > 0 and venit_anual > 0:
                        # Determinăm frecvența din dividendRate vs venit anual
                        # Majoritatea companiilor US plătesc trimestrial
                        plata_per_ocazie = (div_rate / 4) * actiuni
                        for m in [2, 5, 8, 11]:  # Mar, Iun, Sep, Dec — luni tipice
                            calendar_data[m] += plata_per_ocazie
                            calendar_detail[m].append(f"{sym}: ${plata_per_ocazie:.2f} (est.)")

        df_cal = pd.DataFrame([
            {
                "Luna": luni_label[i],
                "Venit ($)": calendar_data[i],
                "Nr. Companii": len(calendar_detail[i]),
                "Detalii": "<br>".join(calendar_detail[i]) if calendar_detail[i] else "—"
            }
            for i in range(12)
        ])

        fig_cal = go.Figure()
        fig_cal.add_trace(go.Bar(
            x=df_cal["Luna"],
            y=df_cal["Venit ($)"],
            text=df_cal["Venit ($)"].apply(lambda v: f"${v:,.2f}" if v > 0 else ""),
            textposition="outside",
            textfont=dict(color=C['text_dim'], size=11),
            marker_color=[C['gold'] if v > 0 else C['surface'] for v in df_cal["Venit ($)"]],
            hovertemplate="<b>%{x}</b><br>Total: $%{y:,.2f}<br><br>%{customdata}<extra></extra>",
            customdata=df_cal["Detalii"],
        ))
        fig_cal.update_layout(
            **PLOTLY_BASE,
            margin=dict(t=40, b=20, l=10, r=20),
            xaxis=dict(**AX, title=""),
            yaxis=dict(**AX, title="Venit ($)", rangemode='tozero'),
            bargap=0.3,
        )
        st.plotly_chart(fig_cal, use_container_width=True)

        # Tabel detaliat pe luni cu suma și companiile plătitoare
        st.markdown("<p class='section-header'>DETALIU LUNAR — COMPANII PLĂTITOARE</p>", unsafe_allow_html=True)
        rows_tabel = []
        for i in range(12):
            if calendar_data[i] > 0:
                companii_lista = ", ".join(
                    [d.split(":")[0].strip() for d in calendar_detail[i]]
                )
                rows_tabel.append({
                    "Luna": luni_label[i],
                    "Total ($)": round(calendar_data[i], 2),
                    "Nr. Companii": len(calendar_detail[i]),
                    "Companii": companii_lista,
                })
        if rows_tabel:
            df_tabel_lunar = pd.DataFrame(rows_tabel)
            st.dataframe(
                df_tabel_lunar.style.format({"Total ($)": "${:,.2f}"}),
                column_config={
                    "Luna": st.column_config.TextColumn("Lună"),
                    "Total ($)": st.column_config.NumberColumn("Total Dividende ($)", format="$%.2f"),
                    "Nr. Companii": st.column_config.NumberColumn("Companii", format="%d"),
                    "Companii": st.column_config.TextColumn("Tickers Plătitori"),
                },
                hide_index=True,
                use_container_width=True,
            )
            total_anual_cal = sum(calendar_data.values())
            st.markdown(
                f"<p style='font-family: DM Mono, monospace; font-size: 0.85rem; "
                f"color: {C['gold']}; text-align: right; margin-top: 8px;'>"
                f"Total anual estimat: <b>${total_anual_cal:,.2f}</b></p>",
                unsafe_allow_html=True
            )

    with col_real:
        st.markdown("<p class='section-header'>RADAR EVENIMENTE FINANCIARE</p>", unsafe_allow_html=True)
        events_df = df[['Logo','Simbol','Companie','Payment_Date','Earnings_Date']].copy()
        st.dataframe(
            events_df.sort_values("Earnings_Date"),
            column_config={
                "Logo": st.column_config.ImageColumn(""),
                "Payment_Date": st.column_config.TextColumn("Plată Dividend"),
                "Earnings_Date": st.column_config.TextColumn("Raportare Earnings")
            },
            hide_index=True, use_container_width=True, height=450
        )

# ==========================================
# TAB 4: REBALANSARE
# ==========================================
with tab3:
    st.markdown("<p class='section-header'>ALGORITM DE OPTIMIZARE PERSONALIZAT</p>", unsafe_allow_html=True)
    col_cap1, col_cap2 = st.columns([1, 2])
    with col_cap1:
        capital_nou = st.number_input("Capital Nou (DCA) [$]:", min_value=0.0, value=0.0, step=100.0)

    df_reb = df[['Logo','Simbol','Companie','Pret_Actual_US$','Pondere_%','Valoare_Actuala']].copy()
    tinte = df_reb['Pondere_%'].round(2)
    diff = 100.0 - tinte.sum()
    if abs(diff) > 0.001:
        tinte.iloc[0] = round(tinte.iloc[0] + diff, 2)
    df_reb['Tinta_%_Dorita'] = tinte

    edited_df = st.data_editor(df_reb, column_config={
        "Logo": st.column_config.ImageColumn(""),
        "Tinta_%_Dorita": st.column_config.NumberColumn("Țintă (%)", min_value=0.0, max_value=100.0, step=0.5),
        "Pondere_%": st.column_config.NumberColumn("Pondere Act.", format="%.2f%%"),
        "Pret_Actual_US$": st.column_config.NumberColumn("Preț Live", format="$%.2f")
    }, disabled=["Logo","Simbol","Companie","Pret_Actual_US$","Pondere_%","Valoare_Actuala"],
    hide_index=True, use_container_width=True)

    suma_tinte = edited_df['Tinta_%_Dorita'].sum()
    valoare_tinta_totala = total_value + capital_nou
    st.divider()
    st.markdown(f"<p style='text-align: center; font-family: DM Mono, monospace; color: {C['text_dim']};'>Total alocat: {suma_tinte:.2f}% / 100.00%</p>", unsafe_allow_html=True)

    if abs(suma_tinte - 100.0) <= 0.1:
        st.success("Calibrat perfect — 100%")
        edited_df['Diferenta_$'] = ((edited_df['Tinta_%_Dorita'] / 100.0) * valoare_tinta_totala) - edited_df['Valoare_Actuala']
        edited_df['Actiuni_Achizitie'] = np.floor(edited_df['Diferenta_$'] / edited_df['Pret_Actual_US$'].replace(0, np.nan))
        edited_df['Cost_Efectiv_$'] = edited_df['Actiuni_Achizitie'] * edited_df['Pret_Actual_US$']
        buy_df = edited_df[edited_df['Actiuni_Achizitie'] >= 1.0].sort_values("Actiuni_Achizitie", ascending=False)
        if not buy_df.empty:
            st.markdown("<p class='section-header' style='margin-top: 16px;'>VECTORI DE ACHIZIȚIE</p>", unsafe_allow_html=True)
            st.dataframe(
                buy_df[['Logo','Simbol','Companie','Cost_Efectiv_$','Actiuni_Achizitie']],
                column_config={
                    "Logo": st.column_config.ImageColumn(""),
                    "Cost_Efectiv_$": st.column_config.NumberColumn("Cost ($)", format="$%.2f"),
                    "Actiuni_Achizitie": st.column_config.NumberColumn("Cantitate", format="%d")
                },
                hide_index=True, use_container_width=True
            )
        else:
            st.info("Adaugă capital nou pentru sugestii de achiziție.")
    elif suma_tinte > 100.1:
        st.error(f"Supra-alocare cu {suma_tinte-100:.2f}%. Ajustează țintele.")
    else:
        st.warning(f"Sub-alocare cu {100-suma_tinte:.2f}%. Distribuie restul.")

# ==========================================
# TAB 5: DEEP DIVE — COMPLET RESCRIS
# ==========================================
with tab4:
    st.markdown("<p class='section-header'>ANALIZĂ DETALIATĂ PER ACTIV</p>", unsafe_allow_html=True)
    selected_ticker = st.selectbox("Selectează ticker:", sorted(df["Simbol"].unique()), label_visibility="collapsed")
    stock_data = live_info[selected_ticker]

    try:
        stock_eval = yf.Ticker(selected_ticker)
    except Exception as e:
        st.error(f"Nu pot inițializa ticker-ul {selected_ticker}: {e}")
        st.stop()

    # ── Header companie ──────────────────────────
    col_logo, col_name, col_metrics = st.columns([1, 2, 3])
    with col_logo:
        st.image(f"https://financialmodelingprep.com/image-stock/{selected_ticker}.png", width=80)
    with col_name:
        st.markdown(f"""
        <p style='font-family: Playfair Display, Georgia, serif; font-size: 1.4rem;
                  color: #E0E6F0; margin: 0; font-weight: 600;'>
            {stock_data['Nume_Companie']}
        </p>
        <p style='font-family: DM Mono, monospace; font-size: 0.85rem; color: {C['gold']};
                  margin: 4px 0 0 0;'>{selected_ticker} · {stock_data['Sector_Live']}</p>
        """, unsafe_allow_html=True)
    with col_metrics:
        price_color = C['green'] if stock_data['Pret_Actual_Live'] >= stock_data['Pret_Anterior_Live'] else C['red']
        st.markdown(f"""
        <div style='display: flex; gap: 24px; align-items: center; height: 100%;'>
            <div>
                <p class='fin-label'>PREȚ LIVE</p>
                <p class='fin-value' style='color: {price_color};'>${stock_data['Pret_Actual_Live']:.2f}</p>
            </div>
            <div>
                <p class='fin-label'>P/E RATIO</p>
                <p class='fin-value'>{stock_data['PE_Ratio']:.1f}</p>
            </div>
            <div>
                <p class='fin-label'>MARKET CAP</p>
                <p class='fin-value'>${stock_data['Market_Cap']/1e9:.2f}B</p>
            </div>
            <div>
                <p class='fin-label'>DIV. YIELD</p>
                <p class='fin-value'>{stock_data['Div_Yield']:.2f}%</p>
            </div>
            <div>
                <p class='fin-label'>BETA</p>
                <p class='fin-value'>{stock_data.get('Beta', 1):.2f}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ══════════════════════════════════════════════
    # GRAFIC 1: ANALIZĂ TEHNICĂ (Preț + BB + RSI + MACD)
    # ══════════════════════════════════════════════
    st.markdown("<p class='section-header'>ANALIZĂ TEHNICĂ</p>", unsafe_allow_html=True)
    try:
        hist = stock_eval.history(period="1y").copy()
        if not hist.empty and len(hist) >= 26:
            close = hist['Close']
            volume = hist['Volume']

            # Bollinger Bands
            sma20 = close.rolling(20).mean()
            std20 = close.rolling(20).std()
            bb_upper = sma20 + 2 * std20
            bb_lower = sma20 - 2 * std20

            # RSI
            delta = close.diff()
            gain = delta.clip(lower=0).rolling(14).mean()
            loss = (-delta.clip(upper=0)).rolling(14).mean()
            rs = gain / loss.replace(0, np.nan)
            rsi = 100 - (100 / (1 + rs))

            # MACD
            ema12 = close.ewm(span=12, adjust=False).mean()
            ema26 = close.ewm(span=26, adjust=False).mean()
            macd_line = ema12 - ema26
            signal_line = macd_line.ewm(span=9, adjust=False).mean()
            macd_hist = macd_line - signal_line

            # Layout: 4 panouri (preț+BB, volum, RSI, MACD)
            fig_tech = make_subplots(
                rows=4, cols=1,
                shared_xaxes=True,
                row_heights=[0.5, 0.15, 0.18, 0.17],
                vertical_spacing=0.03,
                subplot_titles=("Preț + Bollinger Bands", "Volum", "RSI (14)", "MACD (12/26/9)")
            )

            # Preț
            avg_buy = df[df['Simbol'] == selected_ticker]['Pret_Mediu_Achizitie_US$'].values
            fig_tech.add_trace(go.Scatter(x=hist.index, y=close, name="Close",
                line=dict(color=C['blue'], width=2)), row=1, col=1)
            fig_tech.add_trace(go.Scatter(x=hist.index, y=sma20, name="SMA 20",
                line=dict(color=C['gold'], width=1.5, dash='dot')), row=1, col=1)
            fig_tech.add_trace(go.Scatter(x=hist.index, y=bb_upper, name="BB+",
                line=dict(color=C['text_dim'], width=1, dash='dash'), showlegend=False), row=1, col=1)
            fig_tech.add_trace(go.Scatter(x=hist.index, y=bb_lower, name="BB−",
                fill='tonexty', fillcolor='rgba(74,158,255,0.06)',
                line=dict(color=C['text_dim'], width=1, dash='dash'), showlegend=False), row=1, col=1)
            if len(avg_buy) > 0 and avg_buy[0] > 0:
                fig_tech.add_hline(y=avg_buy[0], line_dash="dash", line_color=C['gold'],
                                   annotation_text=f" Cost mediu: ${avg_buy[0]:.2f}",
                                   annotation_font=dict(color=C['gold'], size=11), row=1, col=1)

            # Volum
            vol_colors = [C['green'] if c >= o else C['red']
                          for c, o in zip(hist['Close'], hist['Open'])]
            fig_tech.add_trace(go.Bar(x=hist.index, y=volume, name="Volum",
                marker_color=vol_colors, opacity=0.7, showlegend=False), row=2, col=1)

            # RSI
            fig_tech.add_trace(go.Scatter(x=hist.index, y=rsi, name="RSI",
                line=dict(color=C['gold'], width=1.8), showlegend=False), row=3, col=1)
            fig_tech.add_hline(y=70, line_dash="dot", line_color=C['red'],
                               line_width=1, row=3, col=1)
            fig_tech.add_hline(y=30, line_dash="dot", line_color=C['green'],
                               line_width=1, row=3, col=1)
            fig_tech.add_hrect(y0=70, y1=100, fillcolor=C['red'],
                               opacity=0.05, row=3, col=1)
            fig_tech.add_hrect(y0=0, y1=30, fillcolor=C['green'],
                               opacity=0.05, row=3, col=1)

            # MACD
            macd_bar_colors = [C['green'] if v >= 0 else C['red'] for v in macd_hist]
            fig_tech.add_trace(go.Bar(x=hist.index, y=macd_hist, name="MACD Hist",
                marker_color=macd_bar_colors, opacity=0.8, showlegend=False), row=4, col=1)
            fig_tech.add_trace(go.Scatter(x=hist.index, y=macd_line, name="MACD",
                line=dict(color=C['blue'], width=1.5), showlegend=False), row=4, col=1)
            fig_tech.add_trace(go.Scatter(x=hist.index, y=signal_line, name="Signal",
                line=dict(color=C['gold'], width=1.5), showlegend=False), row=4, col=1)

            fig_tech.update_layout(
                **PLOTLY_BASE,
                height=680,
                margin=dict(t=30, b=20, l=10, r=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1,
                            font=dict(color=C['text_dim'], size=11)),
                hovermode="x unified",
            )
            for i in range(1, 5):
                fig_tech.update_yaxes(
                    gridcolor=C['grid'], linecolor=C['border'],
                    tickfont=dict(color=C['text_dim'], size=10), row=i, col=1
                )
                fig_tech.update_xaxes(gridcolor=C['grid'], linecolor=C['border'],
                                      tickfont=dict(color=C['text_dim'], size=10), row=i, col=1)
            for ann in fig_tech.layout.annotations:
                ann.font.color = C['text_dim']
                ann.font.size = 11

            st.plotly_chart(fig_tech, use_container_width=True)
        else:
            st.info("Date insuficiente pentru analiza tehnică (minim 26 zile necesar).")
    except Exception as e:
        st.warning(f"Eroare la analiza tehnică: {e}")

    st.divider()

    # ══════════════════════════════════════════════
    # GRAFIC 2: SCORECARD FINANCIAR COMPLET
    # ══════════════════════════════════════════════
    st.markdown("<p class='section-header'>SCORECARD FINANCIAR</p>", unsafe_allow_html=True)

    def badge(val, thresholds, labels=None, higher_is_better=True):
        """Returnează un badge colorat în funcție de valoare."""
        if labels is None:
            if higher_is_better:
                if val >= thresholds[1]: return f"<span class='badge badge-green'>EXCELENT</span>"
                elif val >= thresholds[0]: return f"<span class='badge badge-yellow'>MEDIU</span>"
                else: return f"<span class='badge badge-red'>SLAB</span>"
            else:
                if val <= thresholds[0]: return f"<span class='badge badge-green'>SĂNĂTOS</span>"
                elif val <= thresholds[1]: return f"<span class='badge badge-yellow'>MODERAT</span>"
                else: return f"<span class='badge badge-red'>RIDICAT</span>"
        return f"<span class='badge badge-gray'>N/A</span>"

    try:
        fin = stock_eval.financials
        cf_stmt = stock_eval.cash_flow
        bs = stock_eval.balance_sheet

        scorecard_rows = []

        # Revenue Growth YoY
        try:
            rev_idx = [i for i in fin.index if 'Total Revenue' in i]
            if rev_idx and len(fin.loc[rev_idx[0]]) >= 2:
                rev = fin.loc[rev_idx[0]].sort_index(ascending=False)
                rev_growth = ((rev.iloc[0] - rev.iloc[1]) / abs(rev.iloc[1])) * 100
                scorecard_rows.append({
                    "Indicator": "Revenue Growth YoY",
                    "Valoare": f"{rev_growth:+.1f}%",
                    "Status": badge(rev_growth, [5, 15]),
                    "Note": "Creștere venituri față de anul anterior"
                })
        except: pass

        # Gross Margin
        try:
            gp_idx = [i for i in fin.index if 'Gross Profit' in i]
            rev_idx = [i for i in fin.index if 'Total Revenue' in i]
            if gp_idx and rev_idx:
                gm = (fin.loc[gp_idx[0]].iloc[0] / fin.loc[rev_idx[0]].iloc[0]) * 100
                scorecard_rows.append({
                    "Indicator": "Gross Margin",
                    "Valoare": f"{gm:.1f}%",
                    "Status": badge(gm, [30, 50]),
                    "Note": "Marjă brută — eficiența producției"
                })
        except: pass

        # Net Margin
        nm = stock_data['Profit_Margin'] * 100 if stock_data['Profit_Margin'] else 0
        scorecard_rows.append({
            "Indicator": "Net Profit Margin",
            "Valoare": f"{nm:.1f}%",
            "Status": badge(nm, [10, 20]),
            "Note": "Profitabilitate netă"
        })

        # FCF Yield
        try:
            fcf_row = cf_stmt.loc["Free Cash Flow"] if "Free Cash Flow" in cf_stmt.index else None
            if fcf_row is not None:
                mc = stock_data['Market_Cap']
                fcf_yield = (fcf_row.iloc[0] / mc) * 100 if mc > 0 else 0
                scorecard_rows.append({
                    "Indicator": "FCF Yield",
                    "Valoare": f"{fcf_yield:.2f}%",
                    "Status": badge(fcf_yield, [3, 7]),
                    "Note": "Randamentul fluxului de numerar liber"
                })
        except: pass

        # ROE
        roe = stock_data['ROE']
        roe_pct = roe * 100 if roe < 2 else roe
        scorecard_rows.append({
            "Indicator": "Return on Equity (ROE)",
            "Valoare": f"{roe_pct:.1f}%",
            "Status": badge(roe_pct, [10, 20]),
            "Note": "Eficiența utilizării capitalului propriu"
        })

        # Debt/Equity
        de = stock_data['Debt_Equity']
        scorecard_rows.append({
            "Indicator": "Debt / Equity",
            "Valoare": f"{de:.2f}x",
            "Status": badge(de, [1.0, 2.0], higher_is_better=False),
            "Note": "Levierul financiar"
        })

        # Current Ratio
        cr = stock_data['Current_Ratio']
        scorecard_rows.append({
            "Indicator": "Current Ratio",
            "Valoare": f"{cr:.2f}x",
            "Status": badge(cr, [1.5, 2.5]),
            "Note": "Capacitatea de plată pe termen scurt"
        })

        # Payout Ratio
        pr = stock_data['Payout_Ratio']
        scorecard_rows.append({
            "Indicator": "Payout Ratio",
            "Valoare": f"{pr:.1f}%",
            "Status": badge(pr, [60, 80], higher_is_better=False),
            "Note": "Sustenabilitatea dividendului"
        })

        # EPS Growth
        t_eps = stock_data['Trailing_EPS']
        f_eps = stock_data['Forward_EPS']
        if t_eps and f_eps and t_eps != 0:
            eps_growth = ((f_eps - t_eps) / abs(t_eps)) * 100
            scorecard_rows.append({
                "Indicator": "EPS Growth (Est.)",
                "Valoare": f"{eps_growth:+.1f}%",
                "Status": badge(eps_growth, [5, 15]),
                "Note": "Creștere estimată a profitului per acțiune"
            })

        # Afișare scorecard
        sc_col1, sc_col2 = st.columns(2)
        half = len(scorecard_rows) // 2 + len(scorecard_rows) % 2

        for col_idx, col_obj in enumerate([sc_col1, sc_col2]):
            with col_obj:
                rows_subset = scorecard_rows[:half] if col_idx == 0 else scorecard_rows[half:]
                html_rows = ""
                for r in rows_subset:
                    html_rows += f"""
                    <div class='scorecard-row'>
                        <div>
                            <p style='margin:0; font-size: 0.88rem; color: {C["text"]};'>{r['Indicator']}</p>
                            <p style='margin:0; font-size: 0.72rem; color: {C["text_dim"]};'>{r['Note']}</p>
                        </div>
                        <div style='text-align: right;'>
                            <p style='margin:0 0 4px 0; font-family: DM Mono, monospace;
                                      font-size: 0.95rem; color: {C["gold"]};'>{r['Valoare']}</p>
                            {r['Status']}
                        </div>
                    </div>
                    """
                st.markdown(f"<div class='fin-card'>{html_rows}</div>", unsafe_allow_html=True)

        # Radar Chart vizual
        st.write("")
        pm_s  = min(max(stock_data['Profit_Margin'] * 200, 0), 100)
        roe_s = min(max(roe_pct, 0), 100)
        div_s = min(max(stock_data['Div_Yield'] * 12, 0), 100)
        pe_v  = stock_data['PE_Ratio']
        pe_s  = 100 - min(max((pe_v - 10) * 2.5, 0), 100) if pe_v > 0 else 50
        beta_s = 100 - min(max((stock_data['Beta'] - 0.5) * 66, 0), 100)
        cats = ['Marjă Profit', 'Eficiență (ROE)', 'Siguranță (Beta)', 'Evaluare (P/E)', 'Randament Div.', 'Marjă Profit']
        vals = [pm_s, roe_s, beta_s, pe_s, div_s, pm_s]
        fig_radar = go.Figure(go.Scatterpolar(
            r=vals, theta=cats, fill='toself',
            fillcolor=f'rgba(232,196,104,0.12)',
            line=dict(color=C['gold'], width=2)
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, range=[0,100], color=C['text_dim'], gridcolor=C['grid'], tickfont=dict(size=9)),
                angularaxis=dict(color=C['text_dim'], gridcolor=C['grid'], tickfont=dict(size=11))
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color=C['text'], family="DM Sans"),
            height=340, margin=dict(t=30, b=20)
        )
        _, rad_col, _ = st.columns([1, 2, 1])
        with rad_col:
            st.plotly_chart(fig_radar, use_container_width=True)

    except Exception as e:
        st.warning(f"Date insuficiente pentru scorecard: {e}")

    st.divider()

    # ══════════════════════════════════════════════
    # GRAFIC 3: CALENDAR HEATMAP RANDAMENTE ZILNICE
    # ══════════════════════════════════════════════
    st.markdown("<p class='section-header'>CALENDAR RANDAMENTE ZILNICE — 12 LUNI</p>", unsafe_allow_html=True)
    try:
        hist_heat = stock_eval.history(period="1y").copy()
        if not hist_heat.empty:
            returns = hist_heat['Close'].pct_change().dropna() * 100
            returns_df = returns.reset_index()
            returns_df.columns = ['Date', 'Return']
            returns_df['Date'] = pd.to_datetime(returns_df['Date']).dt.tz_localize(None)
            returns_df['Week'] = returns_df['Date'].dt.isocalendar().week.astype(int)
            returns_df['DayOfWeek'] = returns_df['Date'].dt.dayofweek  # 0=Mon, 4=Fri
            returns_df['Month'] = returns_df['Date'].dt.month
            returns_df['Year'] = returns_df['Date'].dt.year

            # Construim un pivot pentru heatmap: rânduri = zi săptămână, coloane = săptămână
            returns_df['YearWeek'] = returns_df['Date'].dt.strftime('%Y-W%U')
            pivot = returns_df.pivot_table(index='DayOfWeek', columns='YearWeek', values='Return', aggfunc='first')
            pivot = pivot.sort_index()

            # Etichetele lunilor pe axa X
            week_labels = pivot.columns.tolist()
            month_ticks = {}
            for wl in week_labels:
                try:
                    dt = pd.to_datetime(wl + '-1', format='%Y-W%U-%w')
                    mo = dt.strftime('%b %Y')
                    if mo not in month_ticks:
                        month_ticks[mo] = week_labels.index(wl)
                except: pass

            day_labels = ['Lun', 'Mar', 'Mie', 'Joi', 'Vin']

            fig_heat = go.Figure(go.Heatmap(
                z=pivot.values,
                x=pivot.columns,
                y=day_labels[:len(pivot.index)],
                colorscale=[
                    [0.0, C['red']],
                    [0.45, '#1A1A2E'],
                    [0.55, '#1A1A2E'],
                    [1.0, C['green']]
                ],
                zmid=0,
                zmin=-3, zmax=3,
                colorbar=dict(
                    title=dict(text="Return %", font=dict(color=C['text_dim'], size=11)),
                    tickfont=dict(color=C['text_dim'], size=10),
                    thickness=12,
                    len=0.8
                ),
                hoverongaps=False,
                hovertemplate="<b>%{x}</b><br>%{y}: %{z:.2f}%<extra></extra>",
                xgap=2, ygap=2
            ))

            # Adăugăm etichete luni
            for mo_label, x_pos in list(month_ticks.items())[::2]:
                fig_heat.add_annotation(
                    x=week_labels[x_pos], y=4.7,
                    text=mo_label.split()[0],
                    showarrow=False,
                    font=dict(color=C['text_dim'], size=10),
                    yref="y"
                )

            fig_heat.update_layout(
                **PLOTLY_BASE,
                height=200,
                xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color=C['text_dim'], size=11)),
                margin=dict(t=30, b=10, l=50, r=60)
            )
            st.plotly_chart(fig_heat, use_container_width=True)
    except Exception as e:
        st.warning(f"Eroare la heatmap: {e}")

    st.divider()

    # ══════════════════════════════════════════════
    # GRAFIC 4: DISTRIBUȚIE RANDAMENTE + VaR
    # ══════════════════════════════════════════════
    st.markdown("<p class='section-header'>DISTRIBUȚIE RANDAMENTE ZILNICE & RISK METRICS</p>", unsafe_allow_html=True)
    try:
        hist_var = stock_eval.history(period="1y").copy()
        if not hist_var.empty and len(hist_var) > 30:
            ret = hist_var['Close'].pct_change().dropna() * 100

            var_95 = np.percentile(ret, 5)
            var_99 = np.percentile(ret, 1)
            mean_r = ret.mean()
            std_r = ret.std()
            skew_r = float(ret.skew())
            kurt_r = float(ret.kurt())
            sharpe = (mean_r * 252) / (std_r * np.sqrt(252)) if std_r > 0 else 0
            max_dd_val = ret.min()
            positive_days = (ret > 0).sum()
            win_rate = positive_days / len(ret) * 100

            col_hist, col_risk = st.columns([2, 1])
            with col_hist:
                fig_dist = go.Figure()
                fig_dist.add_trace(go.Histogram(
                    x=ret, nbinsx=60, name="Distribuție Zilnică",
                    marker_color=C['blue'], opacity=0.75,
                    marker_line=dict(color=C['surface'], width=0.5)
                ))
                # Linie normală teoretică
                x_range = np.linspace(ret.min(), ret.max(), 200)
                from scipy import stats as scipy_stats
                normal_curve = scipy_stats.norm.pdf(x_range, mean_r, std_r)
                normal_curve_scaled = normal_curve * len(ret) * (ret.max() - ret.min()) / 60
                fig_dist.add_trace(go.Scatter(
                    x=x_range, y=normal_curve_scaled, name="Distribuție Normală",
                    line=dict(color=C['gold'], width=2, dash='dot')
                ))
                # VaR lines
                fig_dist.add_vline(x=var_95, line_dash="dash", line_color=C['gold'],
                                   annotation_text=f" VaR 95%: {var_95:.2f}%",
                                   annotation_font=dict(color=C['gold'], size=11))
                fig_dist.add_vline(x=var_99, line_dash="dash", line_color=C['red'],
                                   annotation_text=f" VaR 99%: {var_99:.2f}%",
                                   annotation_font=dict(color=C['red'], size=11))
                fig_dist.add_vline(x=mean_r, line_dash="solid", line_color=C['green'],
                                   line_width=1.5,
                                   annotation_text=f" Medie: {mean_r:.2f}%",
                                   annotation_font=dict(color=C['green'], size=11))

                fig_dist.update_layout(
                    **PLOTLY_BASE,
                    height=320,
                    legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1,
                                font=dict(color=C['text_dim'], size=11)),
                    xaxis=dict(title="Randament Zilnic (%)", gridcolor=C['grid'], linecolor=C['border'], tickfont=dict(color=C['text_dim'], size=11)),
                    yaxis=dict(title="Frecvență", gridcolor=C['grid'], linecolor=C['border'], tickfont=dict(color=C['text_dim'], size=11)),
                    bargap=0.05
                )
                st.plotly_chart(fig_dist, use_container_width=True)

            with col_risk:
                st.markdown("<br>", unsafe_allow_html=True)
                risk_metrics = [
                    ("VaR 95% (zilnic)", f"{var_95:.2f}%", var_95 > -2),
                    ("VaR 99% (zilnic)", f"{var_99:.2f}%", var_99 > -4),
                    ("Sharpe Ratio (1Y)", f"{sharpe:.2f}", sharpe > 1),
                    ("Win Rate", f"{win_rate:.1f}%", win_rate > 52),
                    ("Volatilitate Anuală", f"{std_r * np.sqrt(252):.1f}%", std_r * np.sqrt(252) < 25),
                    ("Skewness", f"{skew_r:.2f}", skew_r > -0.5),
                    ("Kurtosis", f"{kurt_r:.2f}", kurt_r < 3),
                    ("Cel mai rău Drawdown", f"{max_dd_val:.2f}%", max_dd_val > -5),
                ]
                html_risk = ""
                for label, value, is_good in risk_metrics:
                    badge_color = C['green'] if is_good else C['red']
                    dot = f"<span style='color:{badge_color}; font-size: 0.6rem;'>●</span>"
                    html_risk += f"""
                    <div style='display: flex; justify-content: space-between; align-items: center;
                                padding: 8px 0; border-bottom: 1px solid {C['border']};'>
                        <span style='font-size: 0.80rem; color: {C['text_dim']};'>{dot} {label}</span>
                        <span style='font-family: DM Mono, monospace; font-size: 0.88rem;
                                     color: {C["text"]};'>{value}</span>
                    </div>
                    """
                st.markdown(f"<div class='fin-card fin-card-accent'>{html_risk}</div>", unsafe_allow_html=True)

    except Exception as e:
        st.warning(f"Date insuficiente pentru distribuția randamentelor: {e}")

    st.divider()

    # ── Grafice existente (FCF, Revenue, EPS Surprise etc.) ──
    col_chart2, col_fcf = st.columns(2)
    with col_chart2:
        st.markdown("<p class='section-header'>ISTORICUL PREȚULUI (365 ZILE)</p>", unsafe_allow_html=True)
        try:
            hist2 = stock_eval.history(period="1y")
            if not hist2.empty:
                fig_hist2 = px.line(hist2, y="Close")
                fig_hist2.update_traces(line=dict(color=C['blue'], width=2))
                try:
                    avg_p = df[df['Simbol'] == selected_ticker]['Pret_Mediu_Achizitie_US$'].values[0]
                    if avg_p > 0:
                        fig_hist2.add_hline(y=avg_p, line_dash="dash", line_color=C['gold'],
                                            annotation_text=f" Cost mediu: ${avg_p:.2f}",
                                            annotation_font=dict(color=C['gold'], size=11))
                except: pass
                fig_hist2.update_layout(**PLOTLY_BASE, height=280,
                    margin=dict(t=30, b=20, l=10, r=10),
                    xaxis=dict(gridcolor=C['grid'], linecolor=C['border'], tickfont=dict(color=C['text_dim'], size=11)),
                    yaxis=dict(title="Preț ($)", gridcolor=C['grid'], linecolor=C['border'], tickfont=dict(color=C['text_dim'], size=11)))
                st.plotly_chart(fig_hist2, use_container_width=True)
        except Exception as e:
            st.warning(f"Eroare: {e}")

    with col_fcf:
        st.markdown("<p class='section-header'>CANAL FCF vs DIVIDEND / SHARE</p>", unsafe_allow_html=True)
        try:
            cf2 = stock_eval.cash_flow
            if cf2 is not None and not cf2.empty:
                fcf_r = cf2.loc["Free Cash Flow"] if "Free Cash Flow" in cf2.index else None
                div_r = abs(cf2.loc["Cash Dividends Paid"]) if "Cash Dividends Paid" in cf2.index else None
                if fcf_r is not None and div_r is not None:
                    sh = stock_data.get("sharesOutstanding", 1)
                    df_cf2 = pd.DataFrame({"FCF/Share": fcf_r / sh, "Div/Share": div_r / sh})
                    df_cf2.index = pd.to_datetime(df_cf2.index).year
                    df_cf2 = df_cf2.sort_index().dropna(how='all')
                    fig_fcf2 = go.Figure()
                    fig_fcf2.add_trace(go.Scatter(x=df_cf2.index, y=df_cf2["Div/Share"], name='Div/Share',
                        line=dict(color=C['gold'], width=2.5)))
                    fig_fcf2.add_trace(go.Scatter(x=df_cf2.index, y=df_cf2["FCF/Share"], name='FCF/Share',
                        fill='tonexty', fillcolor='rgba(46,204,113,0.08)',
                        line=dict(color=C['green'], width=2)))
                    fig_fcf2.update_layout(**PLOTLY_BASE, height=280,
                        margin=dict(t=30, b=20, l=10, r=10),
                        legend=dict(orientation="h", y=1.02, x=1, xanchor="right",
                                    font=dict(color=C['text_dim'], size=11)),
                        xaxis=dict(dtick=1, gridcolor=C['grid'], linecolor=C['border'], tickfont=dict(color=C['text_dim'], size=11)),
                        yaxis=dict(gridcolor=C['grid'], linecolor=C['border'], rangemode='tozero', tickfont=dict(color=C['text_dim'], size=11)))
                    st.plotly_chart(fig_fcf2, use_container_width=True)
                else:
                    st.info("Date FCF insuficiente.")
        except Exception as e:
            st.warning(f"Eroare FCF: {e}")

    st.divider()

    # EPS Surprise + P/E Evolution
    col_ei1, col_ei2, col_ei3 = st.columns([1, 1, 2])
    with col_ei1:
        st.markdown("<p class='section-header'>COUNTDOWN EARNINGS</p>", unsafe_allow_html=True)
        e_date_str = stock_data.get('Earnings_Date', 'N/A')
        if e_date_str != 'N/A':
            try:
                e_date = datetime.strptime(e_date_str, '%Y-%m-%d')
                days_left = (e_date - datetime.now()).days
                color_cd = C['gold'] if days_left >= 0 else C['text_dim']
                label_cd = f"{days_left} zile" if days_left >= 0 else "Raportat Recent"
                st.markdown(f"""
                <div class='fin-card fin-card-accent'>
                    <p class='fin-label'>Data</p>
                    <p style='font-family: DM Mono, monospace; font-size: 0.85rem; color: {C['text_dim']}; margin: 0;'>{e_date_str}</p>
                    <p class='fin-label' style='margin-top: 12px;'>Rămase</p>
                    <p style='font-family: DM Mono, monospace; font-size: 1.8rem; color: {color_cd}; margin: 0;'>{label_cd}</p>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.info("Dată indisponibilă.")
        else:
            st.info("Dată neanunțată.")

    with col_ei2:
        st.markdown("<p class='section-header'>PROIECȚIE EPS</p>", unsafe_allow_html=True)
        t_eps2 = stock_data.get('Trailing_EPS', 0)
        f_eps2 = stock_data.get('Forward_EPS', 0)
        eps_color2 = C['green'] if f_eps2 > t_eps2 else C['red']
        eps_arrow2 = "▲" if f_eps2 > t_eps2 else "▼"
        st.markdown(f"""
        <div class='fin-card fin-card-accent'>
            <p class='fin-label'>EPS Istoric (TTM)</p>
            <p style='font-family: DM Mono, monospace; font-size: 1rem; color: {C['text']}; margin: 0;'>${t_eps2:.2f}</p>
            <hr style='margin: 10px 0; border-color: {C['border']};'>
            <p class='fin-label'>Consens Estimat (Fwd)</p>
            <p style='font-family: DM Mono, monospace; font-size: 1.4rem; color: {eps_color2}; margin: 0;'>
                {eps_arrow2} ${f_eps2:.2f}
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col_ei3:
        st.markdown("<p class='section-header'>SURPRIZE EPS ISTORICE</p>", unsafe_allow_html=True)
        try:
            ed_hist = stock_eval.earnings_dates
            if ed_hist is not None and not ed_hist.empty:
                ed_past = ed_hist.dropna(subset=['Reported EPS', 'EPS Estimate']).head(4).sort_index(ascending=True)
                if not ed_past.empty:
                    ed_past.index = ed_past.index.strftime('%Y-%m')
                    fig_surp = go.Figure()
                    fig_surp.add_trace(go.Bar(x=ed_past.index, y=ed_past['EPS Estimate'],
                        name='Estimat', marker_color=f'rgba(74,158,255,0.5)'))
                    fig_surp.add_trace(go.Bar(x=ed_past.index, y=ed_past['Reported EPS'],
                        name='Raportat', marker_color=C['gold']))
                    fig_surp.update_layout(**PLOTLY_BASE, barmode='group', height=200,
                        margin=dict(t=30, b=20, l=10, r=10),
                        legend=dict(orientation="h", y=1.02, x=1, xanchor="right",
                                    font=dict(color=C['text_dim'], size=11)),
                        xaxis=dict(gridcolor=C['grid'], linecolor=C['border'], tickfont=dict(color=C['text_dim'], size=11)),
                        yaxis=dict(gridcolor=C['grid'], linecolor=C['border'], rangemode='tozero', title='EPS ($)', tickfont=dict(color=C['text_dim'], size=11)))
                    st.plotly_chart(fig_surp, use_container_width=True)
        except:
            st.info("Date EPS indisponibile.")

    st.divider()

    # Revenue + Buyback
    c_rev2, c_bb2 = st.columns(2)
    with c_rev2:
        st.markdown("<p class='section-header'>EVOLUȚIE VENITURI</p>", unsafe_allow_html=True)
        try:
            fin2 = stock_eval.financials
            rev_idx2 = [i for i in fin2.index if 'Total Revenue' in i]
            if rev_idx2:
                rev2 = fin2.loc[rev_idx2[0]].sort_index()
                rev2.index = pd.to_datetime(rev2.index).year
                fig_rev2 = px.line(x=rev2.index, y=rev2.values / 1e9, markers=True)
                fig_rev2.update_traces(line=dict(color=C['blue'], width=2.5),
                                       marker=dict(color=C['gold'], size=8))
                fig_rev2.update_layout(**PLOTLY_BASE, height=260,
                    margin=dict(t=30, b=20, l=10, r=10),
                    xaxis=dict(dtick=1, gridcolor=C['grid'], linecolor=C['border'], title="Anul", tickfont=dict(color=C['text_dim'], size=11)),
                    yaxis=dict(gridcolor=C['grid'], linecolor=C['border'], rangemode='tozero', title="Miliarde $", tickfont=dict(color=C['text_dim'], size=11)))
                st.plotly_chart(fig_rev2, use_container_width=True)
        except: pass

    with c_bb2:
        st.markdown("<p class='section-header'>MONITORIZARE BUYBACK</p>", unsafe_allow_html=True)
        try:
            bs2 = stock_eval.balance_sheet
            sh_idx2 = [i for i in bs2.index if 'Ordinary Shares Number' in i or 'Share Issuance' in i]
            if sh_idx2:
                sh2 = bs2.loc[sh_idx2[0]].sort_index()
                sh2.index = pd.to_datetime(sh2.index).year
                sh2_colors = [C['green'] if v < sh2.iloc[i-1] else C['red']
                              for i, v in enumerate(sh2) if i > 0]
                sh2_colors = [C['text_dim']] + sh2_colors
                fig_sh2 = px.bar(x=sh2.index, y=sh2.values / 1e6)
                fig_sh2.update_traces(marker_color=sh2_colors)
                fig_sh2.update_layout(**PLOTLY_BASE, height=260,
                    margin=dict(t=30, b=20, l=10, r=10),
                    xaxis=dict(dtick=1, gridcolor=C['grid'], linecolor=C['border'], title="Anul", tickfont=dict(color=C['text_dim'], size=11)),
                    yaxis=dict(gridcolor=C['grid'], linecolor=C['border'], rangemode='tozero', title="Milioane Acțiuni", tickfont=dict(color=C['text_dim'], size=11)))
                st.plotly_chart(fig_sh2, use_container_width=True)
        except: pass

    st.divider()

    # Tabel financiar complet
    st.markdown("<p class='section-header'>SUMAR DATE FINANCIARE</p>", unsafe_allow_html=True)
    try:
        raw_data2 = stock_eval.financials.copy()
        raw_data2.columns = [col.year if hasattr(col, 'year') else col for col in raw_data2.columns]
        def fmt_large(val):
            if pd.isna(val) or val == "-": return "-"
            try:
                v = float(val)
                av = abs(v)
                if av >= 1e12: return f"${v/1e12:.2f}T"
                elif av >= 1e9: return f"${v/1e9:.2f}B"
                elif av >= 1e6: return f"${v/1e6:.2f}M"
                else: return f"${v:,.2f}"
            except: return val
        st.dataframe(raw_data2.style.format(fmt_large), use_container_width=True)
    except:
        st.info("Date brute indisponibile.")

# ==========================================
# TAB 6: ALERTE PREȚ
# ==========================================
with tab_alerts:
    st.markdown("<p class='section-header'>SISTEM ALERTE PREȚ</p>", unsafe_allow_html=True)
    st.info("Setează prețuri țintă de cumpărare (DCA) sau vânzare. Lasă 0.0 pentru a dezactiva. Alertele se verifică la fiecare refresh.")

    alert_data = []
    for _, row in df.iterrows():
        sym = row['Simbol']
        live_p = row['Pret_Actual_US$']
        buy_p = st.session_state['price_alerts'].get(sym, {}).get('buy', 0.0)
        sell_p = st.session_state['price_alerts'].get(sym, {}).get('sell', 0.0)
        status = "— Inactiv"
        if buy_p > 0 and live_p <= buy_p: status = "▲ DECLANȘAT (BUY)"
        elif sell_p > 0 and live_p >= sell_p: status = "▼ DECLANȘAT (SELL)"
        elif buy_p > 0 or sell_p > 0: status = "◉ Armat"
        alert_data.append({"Logo": row["Logo"], "Simbol": sym, "Pret_Live_$": live_p,
                           "Cumpără_Sub_$": buy_p, "Vinde_Peste_$": sell_p, "Status": status})

    df_alerts_display = pd.DataFrame(alert_data)
    edited_alerts = st.data_editor(
        df_alerts_display,
        column_config={
            "Logo": st.column_config.ImageColumn(""),
            "Simbol": st.column_config.TextColumn("Ticker", disabled=True),
            "Pret_Live_$": st.column_config.NumberColumn("Preț Live ($)", format="%.2f", disabled=True),
            "Cumpără_Sub_$": st.column_config.NumberColumn("Cumpără Sub ($)", min_value=0.0, step=1.0, format="%.2f"),
            "Vinde_Peste_$": st.column_config.NumberColumn("Vinde Peste ($)", min_value=0.0, step=1.0, format="%.2f"),
            "Status": st.column_config.TextColumn("Status", disabled=True)
        },
        hide_index=True, use_container_width=True
    )
    for _, row in edited_alerts.iterrows():
        sym = row['Simbol']
        st.session_state['price_alerts'][sym]['buy'] = row['Cumpără_Sub_$']
        st.session_state['price_alerts'][sym]['sell'] = row['Vinde_Peste_$']

# ==========================================
# 10. REGISTRUL CENTRAL
# ==========================================
st.divider()
st.markdown("<p class='section-header'>REGISTRUL CENTRAL DE DATE</p>", unsafe_allow_html=True)
search_query = st.text_input("Caută ticker sau companie:", "", placeholder="Ex: AAPL, Microsoft...")
filtered_df = df[
    df['Simbol'].str.contains(search_query, case=False, na=False) |
    df['Companie'].str.contains(search_query, case=False, na=False)
] if search_query else df

def color_pnl(val):
    if isinstance(val, (int, float)):
        if val < 0: return f'color: {C["red"]}; font-weight: 500;'
        elif val > 0: return f'color: {C["green"]}; font-weight: 500;'
    return ''

cols_show = ['Logo','Simbol','Sector','Actiuni','Pret_Actual_US$','PE_Ratio','Profit_Net','Profit_%','Yield_on_Cost_%','Pondere_%']
st.dataframe(
    filtered_df[cols_show].style.map(color_pnl, subset=['Profit_Net','Profit_%']),
    column_config={
        "Logo": st.column_config.ImageColumn(""),
        "Actiuni": st.column_config.NumberColumn("Bucăți", format="%d"),
        "Pret_Actual_US$": st.column_config.NumberColumn("Preț Live", format="$%.2f"),
        "PE_Ratio": st.column_config.NumberColumn("P/E", format="%.2f"),
        "Profit_Net": st.column_config.NumberColumn("Profit ($)", format="$%.2f"),
        "Profit_%": st.column_config.NumberColumn("Profit %", format="%.2f%%"),
        "Yield_on_Cost_%": st.column_config.NumberColumn("YoC", format="%.2f%%"),
        "Pondere_%": st.column_config.NumberColumn("Pondere", format="%.2f%%"),
    },
    use_container_width=True, hide_index=True, height=600
)
