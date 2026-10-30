# SAIFA Quant Edge 1.0 — Final Challenge

## Team
**Quant_Colombo**

## Project
**Serendib University Endowment Fund — Investment Committee Recommendation**

This repository contains the complete quantitative analysis and Streamlit decision dashboard prepared for the SAIFA Quant Edge 1.0 Final Challenge.

The client is a **USD 10 million conservative university endowment**. The objective is not simply to maximize expected return. The analysis gives greater weight to capital preservation, downside-risk control, diversification, stress resilience and the reliability of the risk model.

---

## Final Recommendation

The recommended strategic allocation is the **Best Risk Parity** portfolio:

| Asset | Weight |
|---|---:|
| AGG | 65.45% |
| GLD | 17.79% |
| XLK | 16.76% |

The recommendation is based on the full analytical pipeline rather than a single performance measure.

Key evidence:

- Out-of-sample annualized return: **6.51%**
- Out-of-sample volatility: **8.19%**
- Out-of-sample Sharpe ratio: **0.30**
- Maximum drawdown: **-17.11%**
- Overall stress rank: **#2 of 5**
- 99% Historical VaR backtesting: **Pass**
- Largest portfolio weight: **65.45%**

Equal Weight generated the strongest out-of-sample return, but ranked last under the combined stress framework. GMVP and Minimum ES were more defensive, but became highly concentrated in AGG and produced negative out-of-sample Sharpe ratios. Risk Parity provided the best overall balance for the stated mandate.

---

## Investable Universe

The analysis uses seven liquid ETFs:

- `SPY` — US large-cap equities
- `EFA` — developed international equities
- `EEM` — emerging-market equities
- `AGG` — US investment-grade bonds
- `GLD` — gold / real asset
- `XLE` — energy sector
- `XLK` — technology sector

---

## Data

The repository already includes the data required to reproduce the submitted analysis.

### Included data files

```text
data/
├── raw/
│   └── prices_raw.csv
├── processed/
│   ├── asset_drawdowns_development.csv
│   ├── log_returns.csv
│   ├── prices_common.csv
│   ├── risk_free_daily_aligned.csv
│   └── simple_returns.csv
└── external/
    └── DGS3MO.csv
```

`prices_raw.csv` contains the saved Yahoo Finance market-price data used by the pipeline.

If `data/raw/prices_raw.csv` is present, Notebook 01 loads the saved file instead of downloading market data again. If it is removed, Notebook 01 attempts to download the ETF prices from Yahoo Finance using `yfinance`.

`DGS3MO.csv` is the 3-month US Treasury yield input used in the CAPM / institutional KPI stage and is included in `data/external/`.

### Sample

- Initial market-data start request: **1 January 2000**
- Last included market date: **19 October 2026**
- Common seven-asset price sample: **18 November 2004 to 19 October 2026**
- Common observations: **5,513**
- Development period: through **31 December 2021**
- Out-of-sample period: **3 January 2022 to 19 October 2026**

The data-governance stage found:

- 0 internal missing values in the common dataset
- 0 duplicate dates
- 0 non-positive prices
- 3 large-move flags retained as genuine market observations

---

## Methodology

The project follows a nine-stage frozen notebook pipeline.

### 01 — Data Collection & Governance

`01_data_collection_governance.ipynb`

- loads or downloads the seven ETF price series;
- aligns all assets to a common date index;
- checks missing values, duplicates and non-positive prices;
- flags unusually large daily moves;
- saves governed raw and processed data.

### 02 — Return Construction & Statistical Diagnostics

`02_Return_Construction_and_Statistical_Diagnostics.ipynb`

- constructs simple and log returns;
- calculates descriptive statistics;
- tests normality using Jarque-Bera;
- tests stationarity using the Augmented Dickey-Fuller test;
- calculates correlations and rolling volatility.

Simple returns are used in the downstream portfolio and risk calculations. Log returns are retained for selected statistical diagnostics.

### 03 — CAPM Benchmarking & Institutional Performance Metrics

`03_CAPM_benchmarking_and_institutinal_performance_metrics.ipynb`

- uses SPY as the benchmark;
- uses the 3-month US Treasury yield as the risk-free-rate input;
- estimates CAPM statistics;
- calculates institutional performance measures including Sharpe, Sortino, drawdown and related KPIs.

### 04 — Portfolio Construction & Optimization

`04_portfolio_construction_and_optimization.ipynb`

Portfolio rules:

- long-only;
- fully invested;
- no leverage;
- 2 to 7 included assets;
- minimum 5% weight for each included asset.

The 5% minimum position size is a modelling assumption, not a client-imposed policy limit.

Portfolio methods:

1. Equal Weight
2. Global Minimum Variance Portfolio
3. Maximum Sharpe
4. Risk Parity
5. Minimum Expected Shortfall

The optimization stage evaluates **600 candidate portfolios** across eligible subsets and methods.

Ledoit-Wolf covariance is used in optimization to reduce instability in the sample covariance matrix.

### 05 — VaR, Expected Shortfall, EVT & Monte Carlo

`05_VaR_&_expected_shortfall_&_EVT_montecarlo_tail_risk.ipynb`

Risk methods:

- Historical VaR / ES
- Parametric Normal VaR / ES
- Normal Monte Carlo VaR / ES
- EVT Peaks-over-Threshold / Generalized Pareto tail estimates

Confidence levels:

- 90%
- 95%
- 99%

Monte Carlo uses **100,000 simulations** with a fixed random seed.

The baseline EVT threshold is the **95th percentile**, with additional threshold-sensitivity checks.

### 06 — VaR Backtesting & Out-of-Sample Validation

`06_VaR_backtesting_and_out_of_sample_validation.ipynb`

- portfolio weights remain frozen;
- out-of-sample evaluation begins on 3 January 2022;
- rolling VaR uses a **500-trading-day estimation window**;
- each forecast uses only information available before the forecast date.

Validation includes:

- Kupiec unconditional-coverage test;
- Christoffersen independence test;
- conditional-coverage test;
- Basel traffic-light monitoring.

For the recommended Risk Parity portfolio, the saved 99% Historical VaR results are:

- forecasts: **1,203**
- exceedances: **15**
- observed exceedance rate: **1.25%**
- Kupiec p-value: **0.407**
- independence p-value: **0.178**
- conditional-coverage p-value: **0.286**
- latest Basel zone: **Green**

Historical VaR passes all three statistical tests for the recommended portfolio. Parametric Normal VaR fails the 99% coverage framework and is not the preferred monitoring model.

### 07 — Stress Testing & Scenario Analysis

`07_stress_testing_and_scenario_analysis.ipynb`

Historical crisis replays:

- Global Financial Crisis 2008
- COVID crash 2020
- Inflation / rate shock 2022

The 2008 and 2020 periods are historical replays inside the development sample and are **not** treated as independent out-of-sample validation. The 2022 period is genuinely out of sample.

Hypothetical scenarios include:

- Severe Equity Crash
- Inflation and Rate Shock
- Technology Sector Crash
- Emerging Market Crisis

Hypothetical shocks are deterministic sensitivity tests. They are not forecasts and are not assigned probabilities.

### 08 — Final Portfolio Selection, Risk Contribution & Recommendation

`08_final_portfolio_selection_risk_contribution_&_institutional_recommendation.ipynb`

This stage combines:

- out-of-sample performance;
- concentration;
- VaR validation;
- stress results;
- volatility-risk contribution;
- marginal/component VaR;
- component Expected Shortfall.

Approximate volatility-risk contributions for the recommended portfolio:

- AGG: **30.88%**
- GLD: **34.54%**
- XLK: **34.58%**

Approximate 99% component ES shares:

- AGG: **32.66%**
- GLD: **31.23%**
- XLK: **36.11%**

### 09 — Copula Dependence & Tail Dependence

`09_copula_dependence_&_tail_dependence_analysis.ipynb`

The final robustness extension compares:

- Normal Monte Carlo
- Gaussian Copula
- Student-t Copula

The Student-t model is used to test whether normal dependence understates extreme joint losses.

For the recommended portfolio:

- Student-t 99% VaR ≈ **0.963%**
- Student-t 99% ES ≈ **1.443%**
- 99% VaR uplift vs Normal Monte Carlo ≈ **13.5%**
- 99% ES uplift vs Normal Monte Carlo ≈ **47.9%**

The deeper tail estimate does not overturn the Risk Parity recommendation. It is used as an additional robustness check.

---

## Repository Structure

The repository is organised as follows. All reproducibility files shown below are already included in the project root.

```text
quant_edge_round2/
├── app.py
├── run_all.py
├── README.md
├── requirements.txt
├── RUN_INSTRUCTIONS.md
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── notebooks/
│   ├── 01_data_collection_governance.ipynb
│   ├── 02_Return_Construction_and_Statistical_Diagnostics.ipynb
│   ├── 03_CAPM_benchmarking_and_institutinal_performance_metrics.ipynb
│   ├── 04_portfolio_construction_and_optimization.ipynb
│   ├── 05_VaR_&_expected_shortfall_&_EVT_montecarlo_tail_risk.ipynb
│   ├── 06_VaR_backtesting_and_out_of_sample_validation.ipynb
│   ├── 07_stress_testing_and_scenario_analysis.ipynb
│   ├── 08_final_portfolio_selection_risk_contribution_&_institutional_recommendation.ipynb
│   └── 09_copula_dependence_&_tail_dependence_analysis.ipynb
│
└── outputs/
    ├── figures/
    └── tables/
```

`app.py` is the final Streamlit application. `run_all.py` executes the nine analytical notebooks in order, and the README, requirements and run instructions describe the submitted repository exactly as provided.

---

## Installation

Python **3.12** is recommended.

Open a terminal in the extracted `quant_edge_round2` project root. No file renaming is required.

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Upgrade pip and install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Run the Streamlit Dashboard

From the project root:

```powershell
python -m streamlit run app.py
```

Streamlit normally opens:

```text
http://localhost:8501
```

The final dashboard reads the saved analytical results from `outputs/tables/`. It does not silently re-optimize the submitted portfolio.

---

## Reproduce the Full Notebook Pipeline

From the project root:

```powershell
python run_all.py
```

`run_all.py` executes the nine notebooks in numerical order while using `notebooks/` as the working directory.

This matters because the notebooks intentionally use:

```python
PROJECT_ROOT = Path("..")
```

The runner preserves that directory convention.

After all nine notebooks finish, run:

```powershell
python -m streamlit run app.py
```

---

## Main Dashboard Outputs

The dashboard uses saved files in `outputs/tables/`, including:

- `recommended_portfolio_allocation.csv`
- `portfolio_shortlist.csv`
- `oos_portfolio_returns.csv`
- `oos_performance_summary.csv`
- `historical_var_es_development.csv`
- `parametric_var_es_development.csv`
- `monte_carlo_var_es_development.csv`
- `evt_risk_development.csv`
- `rolling_var_backtests.csv`
- `var_validation_99_summary.csv`
- `basel_rolling_traffic_light.csv`
- `historical_stress_results.csv`
- `hypothetical_stress_results.csv`
- `stress_resilience_rankings.csv`
- `recommended_portfolio_risk_contributions.csv`
- `recommended_tail_risk_budgeting_summary.csv`
- `institutional_decision_gates.csv`
- `copula_tail_dependence.csv`
- `copula_model_comparison.csv`
- `normal_mc_vs_copula_risk_comparison.csv`

The repository also includes the additional tables and figures generated throughout Notebooks 01–09.

---

## Important Assumptions and Limitations

- Historical relationships may not persist into future market regimes.
- Historical VaR depends on the empirical return distribution.
- Parametric Normal VaR may understate heavy-tail risk.
- Normal Monte Carlo captures mean/covariance structure but not skewness, excess kurtosis or nonlinear tail dependence.
- EVT estimates depend on threshold selection.
- Copula tail-dependence estimates are model-dependent.
- The 5% minimum included position is a modelling assumption rather than a client policy.
- Stress scenarios are sensitivity tests rather than probability forecasts.
- Transaction costs, taxes, liquidity frictions, rebalancing costs and market impact are not explicitly modelled.
- Risk is estimated from daily observations and may differ at longer horizons.
- A passing VaR backtest does not imply that losses cannot exceed VaR.
- The recommended allocation is a quantitative strategic recommendation and would still require governance and ongoing monitoring before real-world implementation.

The Streamlit application contains a dedicated **Assumptions and Limitations** page.

---

## Reproducibility

The project is designed so that submitted numerical results can be traced to the notebook pipeline and saved outputs.

Key controls:

- saved market and risk-free data are included;
- development and out-of-sample periods are separated;
- portfolio weights remain frozen during out-of-sample evaluation;
- rolling backtests use only information available before each forecast;
- randomized simulation stages use fixed seeds;
- the Streamlit app reads saved outputs rather than recomputing a different portfolio.

---

## AI-Tool Disclosure

AI tools were used as assistance for learning, debugging, code review, wording refinement and presentation/dashboard development.

The team remains responsible for:

- every modelling choice;
- every assumption;
- all calculations;
- the final code;
- all reported results;
- the investment recommendation.

The team reviewed the submitted implementation and should be able to explain, modify and reproduce the final work.

---

## Final Investment View

For the stated conservative endowment mandate, the project recommends:

**Best Risk Parity — AGG 65.45% / GLD 17.79% / XLK 16.76%**

Historical VaR and Expected Shortfall are used for regular downside-risk monitoring. EVT and Student-t copula estimates are retained as additional checks on extreme-tail risk.
