import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from qiskit_ibm_runtime.fake_provider import FakeBrisbane


# --------------------------------------------------
# Project settings
# --------------------------------------------------

RANDOM_SEED = 42
NUM_QUBITS = 5
NUM_TIME_STEPS = 20

OUTPUT_DIR = "outputs"

np.random.seed(RANDOM_SEED)


# --------------------------------------------------
# Load backend
# --------------------------------------------------

def load_backend():
    """Load IBM's FakeBrisbane backend."""

    backend = FakeBrisbane()

    print("Backend:", backend.name)
    print("Available qubits:", backend.num_qubits)

    return backend


# --------------------------------------------------
# Generate synthetic time-series data
# --------------------------------------------------

def generate_data(backend):
    """
    Generate synthetic T1 measurements over time.

    FakeBrisbane provides the baseline T1 values.
    Temporal changes are synthetically simulated.
    """

    records = []

    number_of_qubits = min(NUM_QUBITS, backend.num_qubits)

    # Synthetic drift scenarios for demonstration
    drift_rates = {
        0: 0.00000000,    # stable
        1: -0.00000015,   # mild degradation
        2: -0.00000040,   # stronger degradation
        3: 0.00000010,    # slight improvement
        4: -0.00000010    # small degradation
    }

    for qubit in range(number_of_qubits):

        properties = backend.qubit_properties(qubit)

        if properties is None or properties.t1 is None:
            continue

        base_t1 = properties.t1
        drift_rate = drift_rates.get(qubit, 0)

        for time_step in range(1, NUM_TIME_STEPS + 1):

            drift = drift_rate * time_step

            noise = np.random.normal(
                loc=0,
                scale=0.000001
            )

            simulated_t1 = base_t1 + drift + noise

            records.append({
                "Time_Step": time_step,
                "Qubit": f"Qubit_{qubit}",
                "T1": simulated_t1
            })

    return pd.DataFrame(records)


# --------------------------------------------------
# Statistical trend analysis
# --------------------------------------------------

def calculate_trends(data):
    """Calculate trend statistics for each qubit."""

    results = []

    for qubit, group in data.groupby("Qubit"):

        x = group["Time_Step"].to_numpy()
        y = group["T1"].to_numpy()

        # Linear regression
        slope, intercept = np.polyfit(x, y, 1)

        predicted = slope * x + intercept

        residuals = y - predicted

        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum(
            (y - np.mean(y)) ** 2
        )

        if ss_tot == 0:
            r_squared = 0
        else:
            r_squared = 1 - (
                ss_res / ss_tot
            )

        start_t1 = y[0]
        end_t1 = y[-1]

        percentage_change = (
            (end_t1 - start_t1)
            / start_t1
        ) * 100

        # Simple project-defined classification
        if percentage_change <= -1:
            status = "DEGRADING"

        elif percentage_change <= -0.2:
            status = "WATCH"

        else:
            status = "STABLE"

        results.append({
            "Qubit": qubit,
            "Mean_T1": np.mean(y),
            "Start_T1": start_t1,
            "End_T1": end_t1,
            "Change_Percent": percentage_change,
            "Trend_Slope": slope,
            "R_Squared": r_squared,
            "Status": status
        })

    return pd.DataFrame(results)


# --------------------------------------------------
# Print report
# --------------------------------------------------

def print_report(results):

    print("\n")
    print("=" * 80)
    print("QUANTUM HARDWARE T1 DRIFT REPORT")
    print("=" * 80)

    columns = [
        "Qubit",
        "Mean_T1",
        "Change_Percent",
        "Trend_Slope",
        "R_Squared",
        "Status"
    ]

    print(
        results[columns].to_string(
            index=False
        )
    )

    print("\nInterpretation:")

    for _, row in results.iterrows():

        if row["Status"] == "DEGRADING":

            print(
                f"- {row['Qubit']}: "
                f"negative T1 trend detected "
                f"({row['Change_Percent']:.2f}%)."
            )

        elif row["Status"] == "WATCH":

            print(
                f"- {row['Qubit']}: "
                f"mild temporal drift detected "
                f"({row['Change_Percent']:.2f}%)."
            )

        else:

            print(
                f"- {row['Qubit']}: "
                f"relatively stable T1 behavior."
            )


# --------------------------------------------------
# Plot average trend
# --------------------------------------------------

def plot_overall_trend(data):

    trend = (
        data.groupby("Time_Step")["T1"]
        .mean()
        .reset_index()
    )

    plt.figure(figsize=(10, 5))

    plt.plot(
        trend["Time_Step"],
        trend["T1"],
        marker="o",
        linewidth=2
    )

    plt.axhline(
        trend["T1"].mean(),
        linestyle="--",
        label="Overall mean"
    )

    plt.title(
        "Average T1 Temporal Trend"
    )

    plt.xlabel("Time Step")
    plt.ylabel("Average T1")

    plt.grid(
        True,
        linestyle=":",
        alpha=0.6
    )

    plt.legend()
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "overall_t1_trend.png"
        ),
        dpi=300
    )

    plt.show()


# --------------------------------------------------
# Plot individual qubit trends
# --------------------------------------------------

def plot_qubit_trends(data):

    plt.figure(figsize=(10, 6))

    for qubit, group in data.groupby("Qubit"):

        plt.plot(
            group["Time_Step"],
            group["T1"],
            marker="o",
            label=qubit
        )

    plt.title(
        "Qubit-Level T1 Performance Over Time"
    )

    plt.xlabel("Time Step")
    plt.ylabel("T1")

    plt.grid(
        True,
        linestyle=":",
        alpha=0.6
    )

    plt.legend()
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "qubit_t1_trends.png"
        ),
        dpi=300
    )

    plt.show()


# --------------------------------------------------
# T1 heatmap
# --------------------------------------------------

def plot_heatmap(data):

    matrix = data.pivot(
        index="Qubit",
        columns="Time_Step",
        values="T1"
    )

    plt.figure(figsize=(12, 4))

    plt.imshow(
        matrix,
        aspect="auto",
        interpolation="nearest"
    )

    plt.colorbar(label="T1")

    plt.title(
        "Qubit T1 Performance Heatmap"
    )

    plt.xlabel("Time Step")
    plt.ylabel("Qubit")

    plt.xticks(
        range(len(matrix.columns)),
        matrix.columns
    )

    plt.yticks(
        range(len(matrix.index)),
        matrix.index
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "t1_heatmap.png"
        ),
        dpi=300
    )

    plt.show()


# --------------------------------------------------
# Save results
# --------------------------------------------------

def save_results(data, results):

    data.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "synthetic_t1_timeseries.csv"
        ),
        index=False
    )

    results.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "qubit_trend_report.csv"
        ),
        index=False
    )


# --------------------------------------------------
# Main program
# --------------------------------------------------

def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    print(
        "Quantum T1 Drift Analysis"
    )
    print(
        "-" * 50
    )

    backend = load_backend()

    print(
        "\nGenerating synthetic temporal data..."
    )

    data = generate_data(backend)

    print(
        f"Generated {len(data)} observations."
    )

    results = calculate_trends(data)

    print_report(results)

    save_results(
        data,
        results
    )

    plot_overall_trend(data)

    plot_qubit_trends(data)

    plot_heatmap(data)

    print(
        "\nAnalysis completed."
    )

    print(
        "Results saved in the 'outputs' directory."
    )


if __name__ == "__main__":
    main()
