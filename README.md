# Quantum T1 Drift Analysis

A statistical analysis project developed to explore how qubit performance can change over time.

The project focuses specifically on the **T1 relaxation time** metric.

## Project Overview

Qubit properties can change over time due to calibration updates, environmental conditions, and other sources of variability.

In this project, Qiskit's `FakeBrisbane` backend is used as the starting point. The T1 values obtained from the backend are used to create a synthetic time series consisting of 20 time steps.

Small random variations are added to the synthetic data, and different drift rates are assigned to the qubits to create different example behaviors.

 **Note:** The time-series data used in this project is synthetic. It does not represent continuous measurements collected from a real IBM Quantum processor.

## Research Question

How can temporal changes in qubit T1 performance be monitored using simple statistical and time-series methods?

The project focuses on the following questions:

- How does T1 change over time?
- Do the qubits show similar behavior?
- How large is the change between the starting and ending values?
- Which qubits show a negative trend?
- Can simple statistical indicators help identify possible drift behavior?

## Method

The analysis follows this general workflow:

FakeBrisbane  
↓  
Baseline T1 values  
↓  
Synthetic time series  
↓  
Qubit-level analysis  
↓  
Trend analysis  
↓  
Drift classification  
↓  
Visualization and reporting

### 1. FakeBrisbane

The project uses `FakeBrisbane` from Qiskit's fake backend infrastructure.

The existing T1 values of the selected qubits are first obtained and then used as the baseline values for generating the synthetic data.

### 2. Synthetic Data

Twenty time steps are generated for each qubit.

Small random variations are added to simulate measurement-like fluctuations. Different drift rates are also assigned to the qubits.

This creates several example scenarios:

- stable behavior
- mild negative drift
- stronger negative drift
- slight positive change

These values are generated for demonstration purposes and are not real hardware measurements.

### 3. Trend Analysis

The following values are calculated for each qubit:

- Mean T1
- Start T1
- End T1
- Percentage change
- Trend slope
- R²
- Status

A simple linear regression model is used to examine the overall direction of T1 over time.

**Trend slope** indicates whether the T1 value tends to increase or decrease over time.

**R²** is used as a measure of how well the linear model explains the observed data.

### 4. Drift Classification

The qubits are divided into three groups based on the percentage change between their starting and ending values:

| Status | Description |
|---|---|
| STABLE | Relatively stable behavior |
| WATCH | Mild negative change |
| DEGRADING | More noticeable negative change |

These thresholds are defined specifically for this project. They are not official hardware limits defined by IBM.

## Visualizations

### Average T1 Temporal Trend

Shows how the average T1 value of the selected qubits changes over time.

### Qubit-Level T1 Trends

Shows the T1 behavior of each qubit separately, making differences between individual qubits easier to observe.

### T1 Heatmap

Shows qubits and time steps together, making the overall changes easier to compare.

## Findings and Interpretation

The analysis of the synthetic time series shows that the qubits do not all behave in exactly the same way over time. Some qubits show negative changes, while others remain relatively stable.

### Qubit-Level Findings

- **Qubit 0:** The T1 value decreased by approximately 0.80%. The trend slope is negative, but the R² value is 0.376. This means that although the overall direction is downward, the linear trend is not particularly strong. Qubit 0 was classified as WATCH.

- **Qubit 1:** The T1 value decreased by approximately 2.58%. The trend slope is negative and the R² value is 0.574. These results indicate a downward change over time. Qubit 1 was classified as DEGRADING.

- **Qubit 2:** The most noticeable negative change was observed in Qubit 2. Its T1 value decreased by approximately 3.26%. The trend slope is negative and the R² value is 0.882. Therefore, Qubit 2 shows the strongest negative T1 trend in the synthetic dataset and was classified as DEGRADING.

- **Qubit 3:** The T1 value increased by approximately 0.10%. The trend slope is positive, but the R² value is 0.170. Since there is no strong linear trend, Qubit 3 was classified as STABLE.

- **Qubit 4:** The T1 value decreased by approximately 1.09%. The trend slope is negative and the R² value is 0.533. Therefore, Qubit 4 was classified as DEGRADING.

### Overall Assessment

Three of the five qubits were classified as DEGRADING, one as WATCH, and one as STABLE.

The overall average T1 plot shows small fluctuations over time, with the series reaching lower levels toward the end of the simulated period.

The qubit-level trend plot shows that the qubits start at different T1 levels and can change in different directions over time. The heatmap also provides a combined view of these level differences and temporal changes.

The changes may appear relatively small in the plots, but the CSV results make the direction of change easier to compare. In particular, the 3.26% change in Qubit 2, together with its negative trend slope and R² value of 0.882, indicates that it has the strongest negative trend in the synthetic dataset.

These results suggest that combining simple statistical indicators such as percentage change, trend slope, and R² can be useful when examining temporal changes rather than relying only on visual inspection of the plots.

However, these classifications are based only on the synthetic data and project-specific thresholds. A qubit classified as DEGRADING in this project should not be interpreted as physically degrading on a real quantum processor.

The main purpose of this work is to demonstrate a simple approach for tracking changes in a hardware metric such as T1 before moving to real hardware data.

## Outputs

When the program is executed, the following files are created in the `outputs/` directory:

outputs/
├── synthetic_t1_timeseries.csv
├── qubit_trend_report.csv
├── overall_t1_trend.png
├── qubit_t1_trends.png
└── t1_heatmap.png

`synthetic_t1_timeseries.csv` contains the generated time-series data.

`qubit_trend_report.csv` contains the calculated trend statistics for each qubit.

## Technologies

- Python
- Qiskit
- Qiskit IBM Runtime
- NumPy
- Pandas
- Matplotlib
- Linear Regression
- Time-Series Analysis

## Installation

Install the required packages with:

    pip install -r requirements.txt

Run the program with:

    python main.py

## Reproducibility

A fixed random seed is used when generating the synthetic data:

    RANDOM_SEED = 42

This is intended to reproduce the same synthetic dataset when the same code and environment are used.

## Limitations

This project is not a real-time quantum hardware monitoring system.

The time series is synthetic, and the `FakeBrisbane` values are used only as baseline values. Therefore, the observed trends should not be interpreted as evidence of physical degradation in a real IBM Quantum processor.

The analysis also focuses only on the T1 metric and 20 simulated time steps.

The main purpose is to demonstrate a simple analysis approach that could be used before moving to real hardware data.

## Future Work

There are several possible directions for extending the project:

- T2 coherence analysis
- Readout error analysis
- Gate error analysis
- Confidence interval calculations
- Statistical significance testing
- Change-point detection
- Anomaly detection
- Analysis of real quantum hardware calibration data

At a later stage, these metrics could be combined into a broader **Quantum Hardware Health Score** or monitoring approach.

## Conclusion

This project is a small prototype for analyzing qubit T1 relaxation time using a synthetic time series.

The goal is not to predict the physical lifetime of a quantum processor.

Instead, the project provides a starting point for monitoring changes and possible drift behavior at the qubit level using simple statistical methods.

## Author

**Quantum Computing × Statistics × Data Science**

A personal portfolio project exploring the intersection of quantum computing, statistics, and data science.
