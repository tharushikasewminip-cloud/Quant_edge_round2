# Run Instructions — SAIFA Quant Edge 1.0 Final Challenge

## Final submitted setup

The repository is already in its final runnable form. **No files need to be renamed before running the project.**

The project root contains:

```text
app.py
run_all.py
README.md
requirements.txt
RUN_INSTRUCTIONS.md
data/
notebooks/
outputs/
```

`app.py` is the final Streamlit application and `run_all.py` is the notebook pipeline runner.

---

## Fastest way to open the dashboard

Open Command Prompt, PowerShell, Terminal, or another shell **inside the extracted `quant_edge_round2` project folder**.

Install dependencies once:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python -m streamlit run app.py
```

Streamlit will print a local URL, normally:

```text
http://localhost:8501
```

---

## Recommended clean setup on a new computer

### Windows Command Prompt

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

---

## Reproduce the full analytical pipeline

From the project root:

```bash
python run_all.py
```

The runner executes the nine notebooks in numerical order:

1. Data Collection & Governance
2. Returns & Statistical Diagnostics
3. CAPM & Institutional KPIs
4. Portfolio Construction & Optimization
5. VaR, ES, EVT & Monte Carlo Tail Risk
6. VaR Backtesting & Out-of-Sample Validation
7. Stress Testing & Scenario Analysis
8. Final Portfolio Selection, Risk Contribution & Recommendation
9. Copula Dependence & Tail Dependence Analysis

The notebooks intentionally use:

```python
PROJECT_ROOT = Path("..")
```

`run_all.py` therefore executes them with `notebooks/` as the working directory so the existing relative paths remain valid. The runner calls `python -m nbconvert` directly, so it does not depend on a separate `jupyter-nbconvert` executable being available on PATH.

After all nine notebooks finish, launch the dashboard again:

```bash
python -m streamlit run app.py
```

---

## Included data and offline reproducibility

The repository already contains the saved market-price data, processed data, the FRED DGS3MO risk-free-rate input, and the analysis outputs used by the submitted dashboard.

Notebook 01 will use the included `data/raw/prices_raw.csv` when it is present. If that file is deliberately removed, Notebook 01 can attempt a fresh Yahoo Finance download using `yfinance`.

---

## Expected dashboard default state

- Portfolio: **Best Risk Parity**
- Client capital: **USD 10 million**
- Confidence level: **99%**
- Primary monitoring model: **Historical VaR**

Final allocation:

- AGG: **65.45%**
- GLD: **17.79%**
- XLK: **16.76%**

---

## Troubleshooting

If the `streamlit` command is not recognized, use the module form used throughout this repository:

```bash
python -m streamlit run app.py
```

If `python` is not recognized on Windows, try:

```cmd
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

If notebook execution reports that `nbconvert` is missing, install the submitted requirements again:

```bash
python -m pip install -r requirements.txt
```

---

## Final verification commands

These commands can be used to verify the submitted code before evaluation:

```bash
python -m py_compile app.py
python -m py_compile run_all.py
python run_all.py
python -m streamlit run app.py
```

A successful `run_all.py` execution ends with:

```text
ALL 9 NOTEBOOKS COMPLETED SUCCESSFULLY
```
