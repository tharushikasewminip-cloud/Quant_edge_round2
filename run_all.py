from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"

NOTEBOOKS = [
    "01_data_collection_governance.ipynb",
    "02_Return_Construction_and_Statistical_Diagnostics.ipynb",
    "03_CAPM_benchmarking_and_institutinal_performance_metrics.ipynb",
    "04_portfolio_construction_and_optimization.ipynb",
    "05_VaR_&_expected_shortfall_&_EVT_montecarlo_tail_risk.ipynb",
    "06_VaR_backtesting_and_out_of_sample_validation.ipynb",
    "07_stress_testing_and_scenario_analysis.ipynb",
    "08_final_portfolio_selection_risk_contribution_&_institutional_recommendation.ipynb",
    "09_copula_dependence_&_tail_dependence_analysis.ipynb",
]

if not NOTEBOOK_DIR.exists():
    raise FileNotFoundError(
        f"Notebook directory not found: {NOTEBOOK_DIR}"
    )

missing = [
    name
    for name in NOTEBOOKS
    if not (NOTEBOOK_DIR / name).exists()
]

if missing:
    raise FileNotFoundError(
        "Missing notebook(s):\n- "
        + "\n- ".join(missing)
    )

print("=" * 60)
print("SAIFA Quant Edge 1.0 - Final Challenge")
print("Running notebook pipeline 01-09")
print("=" * 60)

for index, name in enumerate(NOTEBOOKS, start=1):

    print()
    print(f"[{index}/9] Running {name}")

    command = [
        sys.executable,
        "-m",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--inplace",
        "--ExecutePreprocessor.timeout=-1",
        name,
    ]

    result = subprocess.run(
        command,
        cwd=NOTEBOOK_DIR,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Pipeline stopped because {name} failed."
        )

    print(f"[{index}/9] Completed {name}")

print()
print("=" * 60)
print("ALL 9 NOTEBOOKS COMPLETED SUCCESSFULLY")
print("=" * 60)

print()
print("Start the dashboard with:")
print(f"{sys.executable} -m streamlit run app.py")
