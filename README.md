# Stopping Power & Proton Range in Silicon — Computational Project

## Overview

This project fits empirical stopping power data for protons in Silicon and uses that model to numerically simulate proton energy loss through matter. The experimental data is sourced from:

> J. B. Marion and F. C. Young, *Nuclear Reaction Analysis: Graphs and Tables*, North-Holland Publishing Company, 1968.

The goal is to reproduce and validate the range predictions found in that reference using a numerical Euler integration, comparing two different regression models against the book's theoretical values.

---

## Project Structure

```
.
├── main.ipynb          # Main notebook: regression, simulation, and analysis
├── utilities/
│   └── ajuste.py       # Fitting routines and model definitions
├── data/               # Source data extracted from the book's graphs
└── environment.yml     # Conda environment
```



## Results

For an initial proton energy of **100 MeV** in Silicon:

| Model       | Range R (mm) |
|-------------|-------------|
| ln fit      | 41.93       |
| poly fit    | 41.84       |
| Book value  | ~40         |

The numerical results agree well with the Marion & Young reference (~5% relative error), with the small discrepancy explained by digitization uncertainty in the source graphs. Both models yield nearly identical ranges, confirming that the degree-2 polynomial is a valid approximation over this energy range.

