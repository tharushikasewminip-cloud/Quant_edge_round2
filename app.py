
from pathlib import Path
import ast

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Serendib Endowment | Investment Committee",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROJECT_ROOT = Path(__file__).resolve().parent
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"

RECOMMENDED_PORTFOLIO = "Best Risk Parity"
DEFAULT_CAPITAL = 10_000_000


# ============================================================
# PROFESSIONAL UI
# ============================================================
st.markdown(
    """
    <style>
    .stApp {
        background: #0b0f17;
    }

    [data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    .block-container {
        padding-top: 1.7rem;
        padding-bottom: 4rem;
        max-width: 1450px;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    .verdict {
        display: inline-block;
        padding: 0.38rem 0.7rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.82rem;
        margin-right: 0.35rem;
        margin-top: 0.6rem;
    }

    .pass {
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.35);
        color: #86efac;
    }

    .watch {
        background: rgba(245,158,11,0.12);
        border: 1px solid rgba(245,158,11,0.35);
        color: #fcd34d;
    }

    .neutral {
        background: rgba(96,165,250,0.12);
        border: 1px solid rgba(96,165,250,0.35);
        color: #93c5fd;
    }

    .evidence-card {
        padding: 1rem 1.05rem;
        border: 1px solid rgba(255,255,255,0.09);
        background: rgba(15,23,42,0.65);
        border-radius: 14px;
        min-height: 165px;
    }

    .evidence-card h4 {
        margin: 0 0 0.55rem 0;
        font-size: 1rem;
    }

    .evidence-card p,
    .evidence-card li {
        color: #cbd5e1;
        font-size: 0.90rem;
        line-height: 1.45;
    }

    .section-note {
        color: #94a3b8;
        font-size: 0.88rem;
        margin-top: -0.45rem;
        margin-bottom: 0.8rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(15,23,42,0.55);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 0.85rem 0.95rem;
        border-radius: 12px;
    }

    div[data-testid="stMetricLabel"] {
        color: #cbd5e1;
    }

    .small-muted {
        color: #94a3b8;
        font-size: 0.82rem;
    }

    .decision-strip {
        padding: 0.9rem 1rem;
        border-radius: 12px;
        background: rgba(37,99,235,0.10);
        border: 1px solid rgba(96,165,250,0.28);
        color: #dbeafe;
        margin-bottom: 1rem;
    }

    .warning-strip {
        padding: 0.9rem 1rem;
        border-radius: 12px;
        background: rgba(245,158,11,0.08);
        border: 1px solid rgba(245,158,11,0.25);
        color: #fde68a;
    }

    .footer-note {
        margin-top: 2rem;
        color: #64748b;
        font-size: 0.78rem;
    }
    
/* Quant-style hero: subtle, presentation-safe and independent of external files */
.quant-hero {
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(120, 160, 255, 0.18);
    border-radius: 18px;
    padding: 28px 30px 26px 30px;
    margin-bottom: 18px;
    background:
        radial-gradient(circle at 82% 22%, rgba(64, 123, 255, 0.16), transparent 28%),
        radial-gradient(circle at 18% 82%, rgba(54, 211, 153, 0.08), transparent 30%),
        linear-gradient(135deg, rgba(9, 16, 31, 0.98), rgba(14, 27, 50, 0.94));
    box-shadow: 0 12px 35px rgba(0,0,0,0.18);
}

.quant-hero::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(126, 164, 255, 0.055) 1px, transparent 1px),
        linear-gradient(90deg, rgba(126, 164, 255, 0.055) 1px, transparent 1px);
    background-size: 32px 32px;
    mask-image: linear-gradient(to right, rgba(0,0,0,.25), rgba(0,0,0,.8));
    pointer-events: none;
}

.quant-hero::after {
    content: "";
    position: absolute;
    width: 440px;
    height: 180px;
    right: -45px;
    bottom: -95px;
    border: 1px solid rgba(118, 155, 255, 0.15);
    border-radius: 50%;
    transform: rotate(-8deg);
    box-shadow:
        -55px -32px 0 -54px rgba(118,155,255,.18),
        -110px -55px 0 -108px rgba(118,155,255,.14);
    pointer-events: none;
}

.quant-hero > * {
    position: relative;
    z-index: 1;
}

.quant-hero .eyebrow {
    font-size: .78rem;
    letter-spacing: .13em;
    text-transform: uppercase;
    opacity: .72;
    margin-bottom: 7px;
}

.quant-hero h1 {
    margin: 0 0 8px 0;
    font-size: 2.0rem;
    line-height: 1.1;
}

.quant-hero p {
    margin: 0;
    max-width: 860px;
    opacity: .82;
    line-height: 1.5;
}

</style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================
@st.cache_data(show_spinner=False)
def load_csv(filename, index_col=None, parse_dates=None, required=True):
    path = TABLE_DIR / filename

    if not path.exists():
        if required:
            st.error(
                f"Required dashboard source is missing:\n\n{path}"
            )
            st.stop()
        return None

    return pd.read_csv(
        path,
        index_col=index_col,
        parse_dates=parse_dates,
    )


def optional_csv(filename, index_col=None, parse_dates=None):
    return load_csv(
        filename,
        index_col=index_col,
        parse_dates=parse_dates,
        required=False,
    )


def pct(x, digits=2):
    if x is None or pd.isna(x):
        return "N/A"
    return f"{float(x) * 100:.{digits}f}%"


def pp(x, digits=2):
    if x is None or pd.isna(x):
        return "N/A"
    return f"{float(x) * 100:.{digits}f} pp"


def money(x):
    if x is None or pd.isna(x):
        return "N/A"
    sign = "-" if float(x) < 0 else ""
    return f"{sign}${abs(float(x)):,.0f}"


def parse_weights(value):
    if isinstance(value, (list, np.ndarray)):
        return np.asarray(value, dtype=float)

    text = str(value).strip()

    try:
        parsed = ast.literal_eval(text)
        if isinstance(parsed, (list, tuple)):
            return np.asarray(parsed, dtype=float)
    except Exception:
        pass

    text = (
        text.replace("[", "")
        .replace("]", "")
        .replace(",", " ")
        .replace(";", " ")
    )

    return np.asarray(
        [float(x) for x in text.split()],
        dtype=float,
    )


def parse_assets(value):
    return [
        x.strip()
        for x in str(value).split(",")
        if x.strip()
    ]


def first_existing(df, candidates, default=np.nan):
    if df is None:
        return default

    for col in candidates:
        if col in df.columns:
            return col

    return default


def risk_point(
    df,
    portfolio,
    confidence,
    var_col,
    es_col,
):
    if df is None:
        return np.nan, np.nan

    required = {"Portfolio", "Confidence", var_col, es_col}

    if not required.issubset(df.columns):
        return np.nan, np.nan

    subset = df[
        (df["Portfolio"] == portfolio)
        & np.isclose(
            df["Confidence"].astype(float),
            confidence,
        )
    ]

    if subset.empty:
        return np.nan, np.nan

    row = subset.iloc[0]

    return (
        float(row[var_col]),
        float(row[es_col]),
    )


def section(title, subtitle=None):
    st.subheader(title)

    if subtitle:
        st.markdown(
            f'<div class="section-note">{subtitle}</div>',
            unsafe_allow_html=True,
        )


def card(title, body, kind="neutral"):
    icon_class = {
        "pass": "pass",
        "watch": "watch",
        "neutral": "neutral",
    }.get(kind, "neutral")

    st.markdown(
        f"""
        <div class="evidence-card">
            <span class="verdict {icon_class}">{title}</span>
            <p style="margin-top:0.8rem;">{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def find_portfolio_row(df, portfolio):
    if df is None:
        return None

    possible_cols = [
        "Portfolio Label",
        "Portfolio",
    ]

    for col in possible_cols:
        if col in df.columns:
            subset = df[df[col] == portfolio]
            if not subset.empty:
                return subset.iloc[0]

    if portfolio in df.index:
        return df.loc[portfolio]

    return None


def get_stress_rank(stress_df, portfolio):
    if stress_df is None:
        return np.nan

    if portfolio in stress_df.index:
        row = stress_df.loc[portfolio]

        for col in [
            "Overall Stress Rank",
            "Stress Rank",
            "Overall Rank",
        ]:
            if col in stress_df.columns:
                return float(row[col])

    for pcol in ["Portfolio", "Portfolio Label"]:
        if pcol in stress_df.columns:
            subset = stress_df[stress_df[pcol] == portfolio]
            if not subset.empty:
                row = subset.iloc[0]
                for col in [
                    "Overall Stress Rank",
                    "Stress Rank",
                    "Overall Rank",
                ]:
                    if col in subset.columns:
                        return float(row[col])

    return np.nan


def historical_validation_pass(validation_df, portfolio):
    if validation_df is None:
        return None

    subset = validation_df[
        validation_df["Portfolio"] == portfolio
    ]

    if "Model" in subset.columns:
        subset = subset[
            subset["Model"]
            .astype(str)
            .str.contains("Historical", case=False, na=False)
        ]

    if subset.empty:
        return None

    row = subset.iloc[0]

    pass_cols = [
        c
        for c in [
            "Kupiec Pass",
            "Independence Pass",
            "Conditional Coverage Pass",
        ]
        if c in row.index
    ]

    if pass_cols:
        return all(bool(row[c]) for c in pass_cols)

    if "Overall Validation Pass" in row.index:
        return bool(row["Overall Validation Pass"])

    return None


def traffic_zone(
    basel_df,
    portfolio,
    model_name="Historical",
):
    if basel_df is None:
        return None

    subset = basel_df.copy()

    if "Portfolio" in subset.columns:
        subset = subset[
            subset["Portfolio"] == portfolio
        ]

    if "Model" in subset.columns:
        subset = subset[
            subset["Model"]
            .astype(str)
            .str.contains(model_name, case=False, na=False)
        ]

    if subset.empty:
        return None

    for col in [
        "Zone",
        "Basel Zone",
        "Traffic Light",
    ]:
        if col in subset.columns:
            return str(subset.iloc[-1][col])

    return None


def get_allocation_for_portfolio(portfolio):
    if portfolio == RECOMMENDED_PORTFOLIO:
        alloc = recommended_allocation.copy()

        if {"Asset", "Weight"}.issubset(alloc.columns):
            return alloc[["Asset", "Weight"]].copy()

    row = find_portfolio_row(
        portfolio_shortlist,
        portfolio,
    )

    if row is None:
        return pd.DataFrame(
            columns=["Asset", "Weight"]
        )

    assets = parse_assets(row["Subset"])
    weights = parse_weights(row["Weights"])

    return pd.DataFrame(
        {
            "Asset": assets,
            "Weight": weights,
        }
    )


# ============================================================
# LOAD FROZEN NOTEBOOK OUTPUTS
# ============================================================
recommended_allocation = load_csv(
    "recommended_portfolio_allocation.csv"
)

portfolio_shortlist = load_csv(
    "portfolio_shortlist.csv"
)

oos_returns = load_csv(
    "oos_portfolio_returns.csv",
    index_col=0,
    parse_dates=True,
)

oos_performance = load_csv(
    "oos_performance_summary.csv",
    index_col=0,
)

historical_risk = load_csv(
    "historical_var_es_development.csv"
)

parametric_risk = load_csv(
    "parametric_var_es_development.csv"
)

mc_risk = load_csv(
    "monte_carlo_var_es_development.csv"
)

evt_risk = load_csv(
    "evt_risk_development.csv"
)

rolling_backtests = load_csv(
    "rolling_var_backtests.csv",
    parse_dates=["Date"],
)

validation_99 = load_csv(
    "var_validation_99_summary.csv"
)

basel_results = load_csv(
    "basel_rolling_traffic_light.csv"
)

historical_stress = load_csv(
    "historical_stress_results.csv"
)

hypothetical_stress = load_csv(
    "hypothetical_stress_results.csv"
)

stress_rankings = load_csv(
    "stress_resilience_rankings.csv",
    index_col=0,
)

risk_contrib = load_csv(
    "recommended_portfolio_risk_contributions.csv"
)

tail_budget = load_csv(
    "recommended_tail_risk_budgeting_summary.csv"
)

decision_gates = optional_csv(
    "institutional_decision_gates.csv",
    index_col=0,
)

copula_tail_dep = load_csv(
    "copula_tail_dependence.csv"
)

copula_model_fit = load_csv(
    "copula_model_comparison.csv"
)

three_model = load_csv(
    "normal_mc_vs_copula_risk_comparison.csv"
)


# ============================================================
# SIDEBAR — PRESENTATION CONTROLS
# ============================================================
st.sidebar.markdown("## QuantEdge Final")
st.sidebar.caption(
    "Investment Committee Evidence Console"
)

portfolio_options = list(oos_returns.columns)

capital_base = st.sidebar.number_input(
    "Capital base (USD)",
    min_value=100_000,
    value=DEFAULT_CAPITAL,
    step=100_000,
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Evidence",
    [
        "1 · Recommendation",
        "2 · Portfolio Performance",
        "3 · Tail Risk",
        "4 · VaR Backtesting",
        "5 · Stress Tests",
        "6 · Where the risk comes from",
        "7 · Tail Dependence Check",
        "8 · Assumptions and Limitations",
    ],
)

# Portfolio switching is available only where the saved outputs support
# every shortlisted portfolio. Recommendation, risk-contribution and copula
# pages are tied to the submitted Best Risk Parity allocation.
interactive_portfolio_pages = {
    "2 · Portfolio Performance",
    "3 · Tail Risk",
    "4 · VaR Backtesting",
    "5 · Stress Tests",
}

if page in interactive_portfolio_pages:
    portfolio_default_index = (
        portfolio_options.index(RECOMMENDED_PORTFOLIO)
        if RECOMMENDED_PORTFOLIO in portfolio_options
        else 0
    )

    selected_portfolio = st.sidebar.selectbox(
        "View portfolio",
        portfolio_options,
        index=portfolio_default_index,
    )
else:
    selected_portfolio = RECOMMENDED_PORTFOLIO

    if page in {
        "1 · Recommendation",
        "6 · Where the risk comes from",
        "7 · Tail Dependence Check",
    }:
        st.sidebar.markdown(
            """
            🔒 **Best Risk Parity — Final Recommendation**
            """
        )

risk_pages = {
    "1 · Recommendation",
    "3 · Tail Risk",
    "4 · VaR Backtesting",
}

if page in risk_pages:
    confidence_pct = st.sidebar.selectbox(
        "Confidence level",
        [90, 95, 99],
        index=2,
    )
else:
    confidence_pct = 99

confidence = confidence_pct / 100

if page == "1 · Recommendation":
    risk_method = st.sidebar.selectbox(
        "Risk model",
        [
            "Historical",
            "Parametric Normal",
            "Monte Carlo Normal",
        ],
    )
else:
    risk_method = "Historical"

if page == "4 · VaR Backtesting":
    backtest_model = st.sidebar.selectbox(
        "VaR methodology",
        [
            "Historical",
            "Parametric Normal",
        ],
    )

    min_date = rolling_backtests["Date"].min().date()
    max_date = rolling_backtests["Date"].max().date()

    backtest_range = st.sidebar.date_input(
        "Backtest period",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
else:
    backtest_range = None

st.sidebar.divider()

st.sidebar.markdown(
    """
    **Default presentation state**

    Portfolio: **Best Risk Parity**  
    Confidence: **99%**  
    Client capital: **USD 10 million**
    """
)


# ============================================================
# SELECTED METRICS
# ============================================================
hist_var, hist_es = risk_point(
    historical_risk,
    selected_portfolio,
    confidence,
    "Historical VaR",
    "Historical ES",
)

param_var, param_es = risk_point(
    parametric_risk,
    selected_portfolio,
    confidence,
    "Parametric VaR",
    "Parametric ES",
)

mc_var, mc_es = risk_point(
    mc_risk,
    selected_portfolio,
    confidence,
    "Monte Carlo VaR",
    "Monte Carlo ES",
)

evt_var, evt_es = risk_point(
    evt_risk,
    selected_portfolio,
    confidence,
    "EVT VaR",
    "EVT ES",
)

method_lookup = {
    "Historical": (hist_var, hist_es),
    "Parametric Normal": (param_var, param_es),
    "Monte Carlo Normal": (mc_var, mc_es),
}

selected_var, selected_es = method_lookup[
    risk_method
]

perf_row = oos_performance.loc[
    selected_portfolio
]

allocation = get_allocation_for_portfolio(
    selected_portfolio
)

stress_rank = get_stress_rank(
    stress_rankings,
    selected_portfolio,
)

validation_pass = historical_validation_pass(
    validation_99,
    selected_portfolio,
)

largest_weight = (
    float(allocation["Weight"].max())
    if not allocation.empty
    else np.nan
)


# ============================================================
# GLOBAL HEADER
# ============================================================
st.markdown(
    """
    <div class="quant-hero">
        <div class="eyebrow">
            SAIFA Quant Edge 1.0 · Final Challenge
        </div>
        <h1>Serendib University Endowment Fund</h1>
        <p>
            Portfolio recommendation, downside-risk analysis and stress testing
            for a USD 10 million conservative endowment.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PAGE 1 — RECOMMENDATION
# ============================================================
if page == "1 · Recommendation":

    st.markdown(
        """
        <div class="decision-strip">
            <b>Recommendation:</b> Adopt the <b>Best Risk Parity</b> portfolio
            as the strategic allocation for the Serendib University Endowment Fund.
            We chose it because it gives a better balance between return and downside protection:
            positive out-of-sample risk-adjusted performance, stress rank #2,
            lower concentration than the defensive alternatives,
            and validated 99% Historical VaR.
        </div>
        """,
        unsafe_allow_html=True,
    )

    section(
        "Why this portfolio fits",
        "We compare the portfolio against the client's main priorities: downside protection, diversification and stable long-term performance.",
    )

    st.caption(
        "PASS / WATCH labels are internal decision screens used to compare the shortlisted portfolios; "
        "they are not client-imposed limits."
    )

    f1, f2, f3, f4 = st.columns(4)

    with f1:
        passed = float(perf_row["Sharpe Ratio"]) > 0
        card(
            "OOS Sharpe · PASS" if passed else "OOS Sharpe · WATCH",
            f"Sharpe ratio = <b>{float(perf_row['Sharpe Ratio']):.2f}</b>. "
            "The portfolio delivered positive risk-adjusted performance in the out-of-sample period.",
            "pass" if passed else "watch",
        )

    with f2:
        rank_text = (
            f"#{int(stress_rank)} of 5"
            if not pd.isna(stress_rank)
            else "N/A"
        )
        top3 = (
            not pd.isna(stress_rank)
            and stress_rank <= 3
        )
        card(
            "Stress Tests · PASS" if top3 else "Stress Tests · WATCH",
            f"Overall stress rank = <b>{rank_text}</b>. "
            "The portfolio ranked second overall across the historical and hypothetical stress tests.",
            "pass" if top3 else "watch",
        )

    with f3:
        card(
            "99% Historical VaR · PASS" if validation_pass else "99% Historical VaR · WATCH",
            "The 99% Historical VaR model passed the Kupiec, independence and conditional-coverage tests."
            if validation_pass
            else "The Historical VaR model needs review because at least one backtest condition was not satisfied.",
            "pass" if validation_pass else "watch",
        )

    with f4:
        acceptable_concentration = (
            not pd.isna(largest_weight)
            and largest_weight < 0.80
        )
        card(
            "Concentration screen · PASS" if acceptable_concentration else "Concentration screen · WATCH",
            f"Largest position = <b>{pct(largest_weight)}</b>. "
            "Our comparison screen flags portfolios above 80%; this is also less concentrated than the GMVP and Minimum-ES alternatives.",
            "pass" if acceptable_concentration else "watch",
        )

    st.divider()

    section(
        "Recommended Allocation",
        "The portfolio combines bonds for stability, gold for diversification and technology equities for growth.",
    )

    left, right = st.columns([1, 1.45])

    with left:
        fig = px.pie(
            allocation,
            names="Asset",
            values="Weight",
            hole=0.58,
        )
        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
        )
        fig.update_layout(
            margin=dict(l=5, r=5, t=10, b=5),
            showlegend=False,
            height=390,
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with right:
        roles = {
            "AGG": "Defensive fixed-income anchor",
            "GLD": "Real-asset / crisis hedge",
            "XLK": "Growth and upside participation",
            "SPY": "Broad US equity exposure",
            "EFA": "Developed international equity",
            "EEM": "Emerging-market equity",
            "XLE": "Energy / real-economy exposure",
        }

        alloc_table = allocation.copy()
        alloc_table["Weight (%)"] = (
            alloc_table["Weight"] * 100
        )
        alloc_table["Portfolio Role"] = (
            alloc_table["Asset"]
            .map(roles)
            .fillna("Diversifying exposure")
        )

        st.dataframe(
            alloc_table[
                [
                    "Asset",
                    "Weight (%)",
                    "Portfolio Role",
                ]
            ].round(2),
            hide_index=True,
            use_container_width=True,
        )

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "OOS return",
            pct(
                perf_row["Annualized Return"]
            ),
        )

        m2.metric(
            "OOS volatility",
            pct(
                perf_row["Volatility"]
            ),
        )

        m3.metric(
            "Max drawdown",
            pct(
                perf_row["Maximum Drawdown"]
            ),
        )

        m4, m5, m6 = st.columns(3)

        m4.metric(
            "Sharpe",
            f"{float(perf_row['Sharpe Ratio']):.2f}",
        )

        m5.metric(
            "Stress rank",
            (
                f"#{int(stress_rank)} / 5"
                if not pd.isna(stress_rank)
                else "N/A"
            ),
        )

        m6.metric(
            "Largest weight",
            pct(largest_weight),
        )

    st.divider()

    section(
        "Capital at Risk",
        "Change the confidence level or risk model in the sidebar to see how the estimated one-day loss changes.",
    )

    r1, r2, r3, r4 = st.columns(4)

    r1.metric(
        f"{confidence_pct}% {risk_method} VaR",
        pct(selected_var),
        money(selected_var * capital_base),
        delta_color="off",
    )

    r2.metric(
        f"{confidence_pct}% {risk_method} ES",
        pct(selected_es),
        money(selected_es * capital_base),
        delta_color="off",
    )

    r3.metric(
        f"{confidence_pct}% EVT ES",
        pct(evt_es),
        money(evt_es * capital_base),
        delta_color="off",
    )

    tail_premium = (
        evt_es - selected_es
        if (
            not pd.isna(evt_es)
            and not pd.isna(selected_es)
        )
        else np.nan
    )

    r4.metric(
        "EVT gap vs selected ES",
        pp(tail_premium),
        (
            money(
                tail_premium
                * capital_base
            )
            if not pd.isna(tail_premium)
            else "N/A"
        ),
        delta_color="off",
        help=(
            "Difference between EVT Expected Shortfall and the selected conventional Expected Shortfall. Positive values indicate a more severe EVT tail estimate; negative values indicate a slightly lower EVT estimate."
        ),
    )

    st.divider()

    section(
        "Why we chose this portfolio",
        "No portfolio wins on every measure, so we compare return, risk, stress performance and concentration together.",
    )

    alt = oos_performance.copy()

    alt["Stress Rank"] = [
        get_stress_rank(
            stress_rankings,
            p,
        )
        for p in alt.index
    ]

    largest_weights = []

    for p in alt.index:
        p_alloc = get_allocation_for_portfolio(
            p
        )
        largest_weights.append(
            float(
                p_alloc["Weight"].max()
            )
            if not p_alloc.empty
            else np.nan
        )

    alt["Largest Weight"] = largest_weights

    show_cols = [
        c
        for c in [
            "Annualized Return",
            "Volatility",
            "Sharpe Ratio",
            "Maximum Drawdown",
            "Stress Rank",
            "Largest Weight",
        ]
        if c in alt.columns
    ]

    alt_display = alt[show_cols].copy()

    for col in [
        "Annualized Return",
        "Volatility",
        "Maximum Drawdown",
        "Largest Weight",
    ]:
        if col in alt_display.columns:
            alt_display[col] *= 100

    st.dataframe(
        alt_display.round(2),
        use_container_width=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        card(
            "Why we recommend Risk Parity",
            "It kept a positive OOS Sharpe ratio, ranked second in the stress tests, avoided extreme concentration and spread risk more evenly across the three assets.",
            "pass",
        )

    with c2:
        card(
            "Why not Minimum ES / GMVP?",
            "They were strong on downside protection, but both became heavily concentrated in AGG and had negative OOS Sharpe ratios.",
            "watch",
        )

    with c3:
        card(
            "Why not Equal Weight?",
            "It produced the strongest OOS return, but ranked weakest under the combined stress framework. For this client, downside resilience receives greater weight than return maximization.",
            "neutral",
        )

    st.divider()

    section(
        "What Could Change the Recommendation?",
        "These are the main conditions that would make us review the current allocation.",
    )

    w1, w2, w3, w4 = st.columns(4)

    with w1:
        card(
            "Performance deterioration",
            "A persistent fall in OOS risk-adjusted performance would weaken the case for keeping the current mix.",
            "watch",
        )

    with w2:
        card(
            "Model validation failure",
            "Repeated VaR backtest failures would trigger a review of the risk model and monitoring limits.",
            "watch",
        )

    with w3:
        card(
            "Concentration drift",
            "A material rise in the largest position or risk contribution would reduce diversification and require rebalancing.",
            "watch",
        )

    with w4:
        card(
            "Tail-risk regime shift",
            "If stress losses or deep-tail estimates rise sharply, the portfolio should be reviewed and risk reduced if necessary.",
            "watch",
        )



    st.divider()

    section(
        "Final Decision",
        "Our final recommendation to the investment committee.",
    )

    st.markdown(
        """
        <div class="decision-strip">
            <b>Recommendation:</b> <b>Use the Best Risk Parity portfolio as the strategic allocation.</b><br><br>
            Use Historical VaR and ES for regular risk monitoring,
            and use EVT and the Student-t copula as extra checks for extreme losses. Review the
            allocation if out-of-sample performance, model validation, concentration, or stress
            results weaken materially.
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# PAGE 2 — PORTFOLIO EVIDENCE
# ============================================================
elif page == "2 · Portfolio Performance":

    section(
        "Out-of-Sample Performance",
        "The selected portfolio weights are held fixed and evaluated from 3 January 2022 onward.",
    )

    selected_returns = (
        oos_returns[
            selected_portfolio
        ]
        .dropna()
    )

    wealth = (
        1
        + selected_returns
    ).cumprod()

    running_peak = wealth.cummax()

    drawdown = (
        wealth
        / running_peak
        - 1
    )

    p1, p2, p3, p4 = st.columns(4)

    p1.metric(
        "Annualized return",
        pct(
            perf_row["Annualized Return"]
        ),
    )

    p2.metric(
        "Volatility",
        pct(
            perf_row["Volatility"]
        ),
    )

    p3.metric(
        "Sharpe",
        f"{float(perf_row['Sharpe Ratio']):.2f}",
    )

    p4.metric(
        "Max drawdown",
        pct(
            perf_row["Maximum Drawdown"]
        ),
    )

    if selected_portfolio == RECOMMENDED_PORTFOLIO:
        st.info(
            "Equal Weight produced the highest OOS return, but return alone is not the objective. "
            "Risk Parity kept a positive Sharpe ratio, ranked second under stress and avoided the very high "
            "bond concentration seen in the most defensive portfolios."
        )

    c1, c2 = st.columns(2)

    with c1:
        fig = px.line(
            x=wealth.index,
            y=wealth.values,
            labels={
                "x": "Date",
                "y": "Growth of $1",
            },
            title="Cumulative Wealth",
        )
        fig.update_layout(
            margin=dict(
                l=10,
                r=10,
                t=45,
                b=10,
            )
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with c2:
        fig = px.area(
            x=drawdown.index,
            y=drawdown.values * 100,
            labels={
                "x": "Date",
                "y": "Drawdown (%)",
            },
            title="Drawdown",
        )
        fig.update_layout(
            margin=dict(
                l=10,
                r=10,
                t=45,
                b=10,
            )
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    section(
        "Portfolio Weights",
        "The selected portfolio's fixed asset weights are shown alongside its out-of-sample performance.",
    )

    weights_display = allocation[["Asset", "Weight"]].copy()
    weights_display["Weight (%)"] = weights_display["Weight"] * 100

    st.dataframe(
        weights_display[["Asset", "Weight (%)"]].round(2),
        hide_index=True,
        use_container_width=True,
    )

    section(
        "Shortlist Comparison",
        "This compares the recommended portfolio with the other shortlisted construction methods.",
    )

    display_perf = oos_performance.copy()

    for col in [
        "Annualized Return",
        "CAGR",
        "Volatility",
        "Maximum Drawdown",
    ]:
        if col in display_perf.columns:
            display_perf[col] *= 100

    st.dataframe(
        display_perf.round(3),
        use_container_width=True,
    )


# ============================================================
# PAGE 3 — TAIL RISK
# ============================================================
elif page == "3 · Tail Risk":

    section(
        "How Bad Could a One-Day Loss Become?",
        "Historical, Parametric Normal, Monte Carlo Normal and EVT are compared side by side under the same portfolio and confidence setting.",
    )

    comparison = pd.DataFrame(
        {
            "Model": [
                "Historical",
                "Parametric Normal",
                "Monte Carlo Normal",
                "EVT",
            ],
            "VaR": [
                hist_var,
                param_var,
                mc_var,
                evt_var,
            ],
            "ES": [
                hist_es,
                param_es,
                mc_es,
                evt_es,
            ],
        }
    ).dropna()

    comparison["VaR (%)"] = (
        comparison["VaR"] * 100
    )

    comparison["ES (%)"] = (
        comparison["ES"] * 100
    )

    comparison["VaR Capital"] = (
        comparison["VaR"]
        * capital_base
    )

    comparison["ES Capital"] = (
        comparison["ES"]
        * capital_base
    )

    t1, t2 = st.columns([1.45, 1])

    with t1:
        fig = go.Figure()

        fig.add_bar(
            name="VaR",
            x=comparison["Model"],
            y=comparison["VaR (%)"],
        )

        fig.add_bar(
            name="Expected Shortfall",
            x=comparison["Model"],
            y=comparison["ES (%)"],
        )

        fig.update_layout(
            barmode="group",
            yaxis_title="Daily loss (%)",
            margin=dict(
                l=10,
                r=10,
                t=25,
                b=10,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with t2:
        comparison_display = comparison[
            [
                "Model",
                "VaR (%)",
                "ES (%)",
                "VaR Capital",
                "ES Capital",
            ]
        ].copy()

        comparison_display["VaR (%)"] = comparison_display["VaR (%)"].map(
            lambda x: f"{x:.3f}"
        )
        comparison_display["ES (%)"] = comparison_display["ES (%)"].map(
            lambda x: f"{x:.3f}"
        )
        comparison_display["VaR Capital"] = comparison_display["VaR Capital"].map(
            lambda x: f"${x:,.0f}"
        )
        comparison_display["ES Capital"] = comparison_display["ES Capital"].map(
            lambda x: f"${x:,.0f}"
        )

        st.dataframe(
            comparison_display,
            hide_index=True,
            use_container_width=True,
        )

    conventional = comparison[
        comparison["Model"]
        != "EVT"
    ]

    if len(conventional) >= 2:
        disagreement = (
            conventional["VaR"].max()
            - conventional["VaR"].min()
        )

       
        st.metric(
            "Conventional-model VaR disagreement",
        pp(disagreement, 3),
        money(
            disagreement
            * capital_base
        ),
        delta_color="off",
        help=(
            "This shows how much the estimated loss changes when the modelling approach changes."
        ),
    )
    if confidence_pct == 90:
        st.info(
            "The EVT model uses a 95th-percentile threshold, so a 90% EVT estimate is not shown."
        )

    st.markdown(
        """
        <div class="warning-strip">
            <b>Interpretation:</b> VaR gives the loss cutoff at the selected confidence level.
            ES shows the average loss after that cutoff is exceeded. We also check EVT because
            this client is more concerned about large downside losses than chasing the highest return.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE 4 — MODEL VALIDATION
# ============================================================
elif page == "4 · VaR Backtesting":

    section(
        "Out-of-Sample VaR Backtesting",
        "Rolling 500-day forecasts use only information available before each forecast date.",
    )

    bt = rolling_backtests[
        (
            rolling_backtests["Portfolio"]
            == selected_portfolio
        )
        & np.isclose(
            rolling_backtests[
                "Confidence"
            ].astype(float),
            confidence,
        )
    ].copy()

    if (
        isinstance(
            backtest_range,
            (tuple, list),
        )
        and len(backtest_range) == 2
    ):
        start, end = backtest_range

        bt = bt[
            (
                bt["Date"].dt.date
                >= start
            )
            & (
                bt["Date"].dt.date
                <= end
            )
        ]

    var_col = (
        "Historical VaR"
        if backtest_model == "Historical"
        else "Parametric VaR"
    )

    exc_col = (
        "Historical Exceedance"
        if backtest_model == "Historical"
        else "Parametric Exceedance"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=bt["Date"],
            y=bt["Realized Loss"] * 100,
            name="Realized loss",
            mode="lines",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=bt["Date"],
            y=bt[var_col] * 100,
            name=f"{backtest_model} VaR",
            mode="lines",
        )
    )

    exceeded = bt[
        bt[exc_col].astype(bool)
    ]

    fig.add_trace(
        go.Scatter(
            x=exceeded["Date"],
            y=(
                exceeded[
                    "Realized Loss"
                ]
                * 100
            ),
            name="Exceedance",
            mode="markers",
            marker=dict(size=7),
        )
    )

    fig.update_layout(
        yaxis_title="Daily loss (%)",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    b1, b2, b3, b4 = st.columns(4)

    b1.metric(
        "Forecasts",
        f"{len(bt):,}",
    )

    exceedances = (
        int(
            bt[exc_col].sum()
        )
        if len(bt)
        else 0
    )

    b2.metric(
        "Exceedances",
        f"{exceedances:,}",
    )

    observed_rate = (
        bt[exc_col].mean()
        if len(bt)
        else np.nan
    )

    b3.metric(
        "Observed rate",
        pct(observed_rate),
    )

    expected_rate = (
        1 - confidence
    )

    b4.metric(
        "Expected rate",
        pct(expected_rate),
    )

    if confidence_pct == 99:
        model_key = (
            "Historical"
            if backtest_model == "Historical"
            else "Parametric"
        )

        summary = validation_99[
            (
                validation_99[
                    "Portfolio"
                ]
                == selected_portfolio
            )
            & (
                validation_99[
                    "Model"
                ]
                .astype(str)
                .str.contains(
                    model_key,
                    case=False,
                    na=False,
                )
            )
        ]

        if not summary.empty:
            row = summary.iloc[0]

            section(
                "Statistical Verdict",
                "A reliable VaR model should get both the number and clustering of exceedances broadly right.",
            )

            v1, v2, v3, v4 = st.columns(4)

            v1.metric(
                "Kupiec p-value",
                f"{float(row['Kupiec p-value']):.3f}",
            )

            v2.metric(
                "Independence p-value",
                f"{float(row['Christoffersen p-value']):.3f}",
            )

            v3.metric(
                "Conditional coverage",
                f"{float(row['Conditional Coverage p-value']):.3f}",
            )

            zone = traffic_zone(
                basel_results,
                selected_portfolio,
                model_key,
            )

            v4.metric(
                "Basel zone",
                zone or "N/A",
            )

            passes = (
                bool(row["Kupiec Pass"])
                and bool(row["Independence Pass"])
                and bool(
                    row[
                        "Conditional Coverage Pass"
                    ]
                )
            )

            if passes:
                st.success(
                    "Result: this 99% VaR model passes the coverage, independence and conditional-coverage tests."
                )
                if backtest_model == "Historical":
                    st.markdown(
                        """
                        <div class="decision-strip">
                            <b>Model choice:</b> Historical VaR is our preferred monitoring model because it passed all three 99% backtests.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.error(
                    "Result: this VaR model fails at least one core backtest and should not be used on its own."
                )
                if backtest_model == "Parametric Normal":
                    st.markdown(
                        """
                        <div class="warning-strip">
                            <b>Model choice:</b> We would not rely on Parametric Normal VaR for 99% monitoring. It produced too many exceptions and failed the coverage tests.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


# ============================================================
# PAGE 5 — STRESS
# ============================================================
elif page == "5 · Stress Tests":

    rank_value = get_stress_rank(
        stress_rankings,
        selected_portfolio,
    )

    s0, s1, s2 = st.columns(3)

    s0.metric(
        "Overall stress rank",
        f"#{int(rank_value)} / 5" if not pd.isna(rank_value) else "N/A",
    )

    hs_selected = historical_stress[
        historical_stress["Portfolio"] == selected_portfolio
    ].copy()

    worst_hist = (
        hs_selected["Cumulative Return"].min()
        if not hs_selected.empty
        else np.nan
    )

    s1.metric(
        "Worst historical replay",
        pct(worst_hist),
    )

    hypo_selected = hypothetical_stress[
        hypothetical_stress["Portfolio"] == selected_portfolio
    ].copy()

    worst_hypo = (
        hypo_selected["Portfolio Shock Return"].min()
        if not hypo_selected.empty
        else np.nan
    )

    s2.metric(
        "Worst hypothetical shock",
        pct(worst_hypo),
    )

    section(
        "Historical Crisis Replay",
        "2008 and 2020 are historical replays inside the development sample; 2022 is genuinely out of sample.",
    )

    hs = historical_stress[
        historical_stress[
            "Portfolio"
        ]
        == selected_portfolio
    ].copy()

    fig = px.bar(
        hs,
        x="Scenario",
        y="Cumulative Return",
        text_auto=".1%",
    )

    fig.update_layout(
        yaxis_tickformat=".1%",
        yaxis_title="Cumulative return",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    section(
        "Hypothetical Stress",
        "These are deterministic portfolio shocks, not forecasts or assigned probabilities.",
    )

    hypo = hypothetical_stress[
        hypothetical_stress[
            "Portfolio"
        ]
        == selected_portfolio
    ].copy()

    fig = px.bar(
        hypo,
        x="Scenario",
        y="Portfolio Shock Return",
        text_auto=".1%",
    )

    fig.update_layout(
        yaxis_tickformat=".1%",
        yaxis_title="Portfolio shock return",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    section(
        "How the portfolios ranked under stress",
        "Lower rank is better. Risk Parity finished second overall, giving a stronger balance than the return-focused alternatives.",
    )

    stress_compare_rows = []
    for p in oos_performance.index:
        rank = get_stress_rank(
            stress_rankings,
            p,
        )
        stress_compare_rows.append(
            {
                "Portfolio": p,
                "Stress Rank": rank,
            }
        )

    stress_compare_df = (
        pd.DataFrame(stress_compare_rows)
        .dropna()
        .sort_values("Stress Rank")
    )

    fig = px.bar(
        stress_compare_df,
        x="Portfolio",
        y="Stress Rank",
        text="Stress Rank",
    )
    fig.update_layout(
        yaxis_title="Overall stress rank",
        xaxis_title="",
        yaxis=dict(autorange="reversed"),
        margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    section(
        "Try your own stress scenario",
        "Change the asset shocks to see how the selected portfolio would react.",
    )

    row = find_portfolio_row(
        portfolio_shortlist,
        selected_portfolio,
    )

    if row is not None:
        assets = parse_assets(
            row["Subset"]
        )

        weights = parse_weights(
            row["Weights"]
        )

        slider_cols = st.columns(
            min(3, len(assets))
        )

        shocks = {}

        for i, asset in enumerate(assets):
            with slider_cols[
                i
                % len(slider_cols)
            ]:
                shocks[asset] = (
                    st.slider(
                        f"{asset} instantaneous shock",
                        -50,
                        30,
                        0,
                        1,
                        key=f"scenario_{asset}",
                    )
                    / 100
                )

        shock_vector = np.array(
            [
                shocks[a]
                for a in assets
            ]
        )

        portfolio_shock = float(
            np.dot(
                weights,
                shock_vector,
            )
        )

        s1, s2, s3 = st.columns(3)

        s1.metric(
            "Portfolio shock",
            pct(portfolio_shock),
        )

        s2.metric(
            "Capital impact",
            money(
                portfolio_shock
                * capital_base
            ),
        )

        s3.metric(
            "Remaining capital",
            money(
                capital_base
                * (
                    1
                    + portfolio_shock
                )
            ),
        )

        st.caption(
            "The custom scenario is a first-order weighted shock. "
            "It tests sensitivity but does not estimate probability."
        )


# ============================================================
# PAGE 6 — RISK BUDGET
# ============================================================
elif page == "6 · Where the risk comes from":

    section(
        "Where Does the Risk Actually Come From?",
        "Capital allocation and risk allocation are different. The final recommendation is judged on both.",
    )

    rb = risk_contrib.copy()

    if (
        "Weight (%)"
        not in rb.columns
        and "Weight"
        in rb.columns
    ):
        rb["Weight (%)"] = (
            rb["Weight"]
            * 100
        )

    if (
        "Risk Contribution (%)"
        not in rb.columns
        and "Risk Contribution"
        in rb.columns
    ):
        rb[
            "Risk Contribution (%)"
        ] = (
            rb[
                "Risk Contribution"
            ]
            * 100
        )

    chart_df = rb[
        [
            "Asset",
            "Weight (%)",
            "Risk Contribution (%)",
        ]
    ].melt(
        id_vars="Asset",
        var_name="Measure",
        value_name="Percent",
    )

    fig = px.bar(
        chart_df,
        x="Asset",
        y="Percent",
        color="Measure",
        barmode="group",
    )

    fig.update_layout(
        yaxis_title="Percent",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    section(
        "Tail Risk Contribution",
        "Component VaR and Component ES show which holdings contribute most to severe losses, not just day-to-day volatility.",
    )

    display_tail = tail_budget.copy()

    selected_cols = [
        c
        for c in [
            "Asset",
            "Weight (%)",
            "Component VaR Share (%)",
            "Component ES Share (%)",
        ]
        if c in display_tail.columns
    ]

    st.dataframe(
        display_tail[
            selected_cols
        ].round(2),
        hide_index=True,
        use_container_width=True,
    )

    st.markdown(
        """
        <div class="decision-strip">
            <b>Interpretation:</b> The portfolio is not equal-weighted in capital terms, but its volatility contribution is much more balanced. This is the main reason Risk Parity gives a better diversification profile.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE 7 — COPULA
# ============================================================
elif page == "7 · Tail Dependence Check":

    section(
        "Tail Dependence Robustness Check",
        "This checks whether extreme portfolio losses become larger when asset relationships are allowed to strengthen in the tail.",
    )

    model_display = (
        three_model
        .copy()
    )

    for col in [
        "VaR 95%",
        "VaR 99%",
        "ES 95%",
        "ES 99%",
    ]:
        if col in model_display.columns:
            model_display[
                col
            ] *= 100

    chart = model_display.melt(
        id_vars="Model",
        var_name="Risk Measure",
        value_name="Percent",
    )

    fig = px.bar(
        chart,
        x="Model",
        y="Percent",
        color="Risk Measure",
        barmode="group",
    )

    fig.update_layout(
        yaxis_title="Daily loss (%)",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    if {
        "Model",
        "VaR 99%",
        "ES 99%",
    }.issubset(
        three_model.columns
    ):
        student = three_model[
            three_model[
                "Model"
            ]
            == "Student-t Copula"
        ]

        normal = three_model[
            three_model[
                "Model"
            ]
            == "Normal Monte Carlo"
        ]

        if (
            not student.empty
            and not normal.empty
        ):
            student = student.iloc[0]
            normal = normal.iloc[0]

            v99_uplift = (
                student["VaR 99%"]
                / normal["VaR 99%"]
                - 1
            )

            es99_uplift = (
                student["ES 99%"]
                / normal["ES 99%"]
                - 1
            )

            u1, u2 = st.columns(2)

            u1.metric(
                "99% VaR uplift vs Normal MC",
                pct(v99_uplift),
            )

            u2.metric(
                "99% ES uplift vs Normal MC",
                pct(es99_uplift),
            )

            if es99_uplift > 0:
                st.warning(
                    "The Student-t model gives a larger 99% tail-loss estimate than Normal Monte Carlo. "
                    "The final portfolio choice stays the same, but the result shows that normal dependence can understate extreme losses."
                )

    c1, c2 = st.columns(2)

    with c1:
        section(
            "Pairwise Tail Dependence",
            "Student-t copula estimates for the recommended assets.",
        )

        tail_display = copula_tail_dep.copy()

        pair_cols = [
            c
            for c in [
                "Asset 1",
                "Asset 2",
                "t-Copula Correlation",
                "Student-t Tail Dependence",
            ]
            if c in tail_display.columns
        ]

        st.dataframe(
            tail_display[pair_cols].round(4),
            hide_index=True,
            use_container_width=True,
        )

        st.caption(
            "Gaussian copula asymptotic tail dependence is zero for these non-perfect correlations; "
            "the table focuses on the Student-t dependence estimates that drive the deep-tail robustness check."
        )

    with c2:
        section(
            "Dependence Model Fit",
            "Pseudo-likelihood comparison; lower pseudo-AIC is preferred within this framework.",
        )

        st.dataframe(
            copula_model_fit.round(3),
            hide_index=True,
            use_container_width=True,
        )

    st.markdown(
        """
        <div class="decision-strip">
            <b>Main finding:</b> The Student-t copula gives larger deep-tail loss estimates than the
            simpler models, but it does not change the final Risk Parity recommendation. We therefore use it
            as an extra tail-risk check rather than as a separate portfolio-selection rule.
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE 8 — LIMITATIONS
# ============================================================
elif page == "8 · Assumptions and Limitations":

    section(
        "Assumptions and Limitations",
        "These assumptions define how the analysis was built, what the risk numbers mean, and where the results may be less reliable.",
    )

    st.markdown(
        """
### Data and evaluation
- Investable universe: SPY, EFA, EEM, AGG, GLD, XLE and XLK.
- The common daily-price sample runs from 18 November 2004 to 19 October 2026.
- Portfolio development uses data through 31 December 2021; out-of-sample evaluation begins on 3 January 2022.
- SPY is the market benchmark. The 3-month US Treasury yield is used as the risk-free-rate input in the CAPM/KPI stage.
- Simple returns are used for portfolio and risk calculations; log returns are used only for selected statistical diagnostics.
- Annualization uses 252 trading days.

### Portfolio construction
- Long-only, fully invested and no leverage.
- Between 2 and 7 included assets.
- The 5% minimum position size is a modelling assumption, not a client policy.
- Historical annualized arithmetic mean returns are used as the baseline expected-return input; they are not forecasts.
- Ledoit-Wolf covariance is used in optimization to reduce sample-covariance instability.
- The shortlisted methods are Equal Weight, GMVP, Maximum Sharpe, Risk Parity and Minimum ES.
- PASS / WATCH decision screens in the dashboard are comparison heuristics, not client-imposed limits.

### Risk measurement
- Historical VaR/ES assumes past return behaviour contains useful information about future downside risk.
- Parametric Normal VaR can understate risk when returns are skewed or heavy-tailed.
- Normal Monte Carlo uses the estimated mean/covariance structure and therefore does not reproduce skewness, excess kurtosis or nonlinear tail dependence.
- Monte Carlo estimates use 100,000 simulations with a fixed seed for reproducibility.
- EVT uses a Peaks-over-Threshold / Generalized Pareto approach with a 95th-percentile baseline threshold.
- EVT results are threshold-sensitive; the notebook also checks nearby thresholds as a robustness test.
- VaR and ES shown in the dashboard are one-day loss measures unless a section explicitly states otherwise.

### Backtesting
- Portfolio weights are frozen during the out-of-sample evaluation.
- Rolling VaR forecasts use a 500-day estimation window and only information available before each forecast date.
- Kupiec, Christoffersen independence and conditional-coverage tests are used at 99% for the saved validation summary.
- Basel traffic-light results are used as an additional monitoring diagnostic.
- Passing a VaR backtest means the model was statistically credible over the tested period; it does not mean future losses cannot exceed VaR.

### Stress testing
- The 2008 and March 2020 crisis windows are historical replays within the development sample, not independent validation samples.
- The 2022 stress window is genuinely out of sample.
- Hypothetical scenarios are deterministic shocks, not forecasts and not assigned probabilities.
- The interactive scenario tool applies a first-order weighted shock and does not estimate scenario likelihood.
- Very-high-confidence historical ES can become sample-sensitive in short crisis windows.

### Tail dependence
- Gaussian and Student-t copulas are used as dependence robustness checks for the recommended portfolio.
- Empirical marginals cannot generate asset-specific returns outside observed historical support.
- Student-t degrees of freedom are selected through a grid-based pseudo-likelihood approximation rather than full joint maximum-likelihood estimation.
- Tail-dependence estimates are model-dependent and are used as robustness evidence, not as a separate portfolio-selection rule.

### Implementation limits
- Transaction costs, taxes, liquidity frictions, rebalancing costs and market impact are not explicitly modelled.
- The analysis is based on daily data; risk can differ at weekly, monthly or multi-year horizons.
- Historical correlations, volatilities and return relationships can change when market regimes change.
- The portfolio is a strategic model recommendation and would still require governance, monitoring and periodic review before real-world implementation.
        """
    )

    section(
        "Source Check",
        "This confirms that the dashboard is reading the saved outputs produced by the analysis notebooks.",
    )

    expected_outputs = [
        "recommended_portfolio_allocation.csv",
        "portfolio_shortlist.csv",
        "oos_portfolio_returns.csv",
        "oos_performance_summary.csv",
        "historical_var_es_development.csv",
        "parametric_var_es_development.csv",
        "monte_carlo_var_es_development.csv",
        "evt_risk_development.csv",
        "rolling_var_backtests.csv",
        "var_validation_99_summary.csv",
        "basel_rolling_traffic_light.csv",
        "historical_stress_results.csv",
        "hypothetical_stress_results.csv",
        "stress_resilience_rankings.csv",
        "recommended_portfolio_risk_contributions.csv",
        "recommended_tail_risk_budgeting_summary.csv",
        "copula_tail_dependence.csv",
        "copula_model_comparison.csv",
        "normal_mc_vs_copula_risk_comparison.csv",
    ]

    audit = pd.DataFrame(
        {
            "Analysis output": expected_outputs,
            "Available": [
                (
                    TABLE_DIR
                    / filename
                ).exists()
                for filename
                in expected_outputs
            ],
        }
    )

    with st.expander("Show source-file check"):
        st.dataframe(
            audit,
            hide_index=True,
            use_container_width=True,
        )

    if audit["Available"].all():
        st.success("All required analysis outputs were loaded successfully.")
    else:
        st.error("One or more required analysis outputs are missing.")

    st.markdown(
        """
        <div class="footer-note">
            Dashboard values are read from the saved analysis outputs. Interactive controls
            change the view or scenario inputs; they do not re-optimize the submitted portfolio.
        </div>
        """,
        unsafe_allow_html=True,
    )
