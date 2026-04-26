import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as curve_fit
import pandas as pd


def modelo(x, a, b, c, d, f):
    return a*np.abs(b+x)**(c) + np.exp(d*x) + f


def ajuste_stopping_power(data_path='data/datos_stopping_power.xlsx'):
    doc = pd.read_excel(data_path, header=0, names=['E', 'dE/dx'])
    E_data     = doc["E"].values
    dE_dx_data = doc["dE/dx"].values

    # --- Fit 1: ln-ln ---
    E_ln       = np.log(E_data)
    dE_dx_ln   = np.log(dE_dx_data)
    popt, pcov = curve_fit.curve_fit(modelo, E_ln, dE_dx_ln)
    a, b, c, d, f = popt

    # model_ln(E)  →  dE/dx  [keV/mm]
    model_ln = lambda E: np.exp(modelo(np.log(np.asarray(E, dtype=float)), *popt))

    # --- Fit 2: degree-2 polynomial on log10-log10 ---
    E_log10      = np.log10(E_data)
    dE_dx_log10  = np.log10(dE_dx_data)
    poly_coef    = np.polyfit(E_log10, dE_dx_log10, 2)
    p2, p1, p0   = poly_coef

    # model_poly(E)  →  dE/dx  [keV/mm]
    model_poly = lambda E: 10**np.polyval(poly_coef, np.log10(np.asarray(E, dtype=float)))

    # ── plotting helpers ────────────────────────────────────────────────────────
    E_log10_fit  = np.linspace(E_log10.min(), E_log10.max(), 500)
    E_fit        = 10**E_log10_fit

    y_ln_log10   = np.log10(model_ln(E_fit))
    y_poly_log10 = np.log10(model_poly(E_fit))

    res_ln   = dE_dx_log10 - np.log10(model_ln(E_data))
    res_poly = dE_dx_log10 - np.log10(model_poly(E_data))

    formula_ln = (
        r'$\mathbf{Ajuste\ ln:}$' + '\n' +
        fr'$\ln\!\left(\frac{{dE}}{{dx}}\right) = {a:.2f} \cdot \left| {b:.2f} + \ln(E) \right|^{{{c:.2f}}} + '
        fr'e^{{{d:.2f} \cdot \ln(E)}} + {f:.2f}$'
    )
    formula_poly = (
        r'$\mathbf{Ajuste\ poly\ (grado\ 2):}$' + '\n' +
        fr'$\log_{{10}}\!\left(\frac{{dE}}{{dx}}\right) = {p2:.3f}\,\log_{{10}}^2(E) {p1:+.3f}\,\log_{{10}}(E) {p0:+.3f}$'
    )

    # ── Figure 1: log10(E) vs log10(dE/dx) – linear axes ──────────────────────
    fig1, axs = plt.subplots(2, 1, figsize=(10, 8))

    axs[0].scatter(E_log10, dE_dx_log10, label='Datos experimentales', zorder=3, color='steelblue')
    axs[0].plot(E_log10_fit, y_ln_log10,   color='red',   label='Ajuste ln')
    axs[0].plot(E_log10_fit, y_poly_log10, color='green', label='Ajuste poly (grado 2)', linestyle='--')
    axs[0].set_xlabel(r'$\log_{10}(E)$')
    axs[0].set_ylabel(r'$\log_{10}(dE/dx)$')
    axs[0].text(0.03, 0.03, formula_ln,
        fontsize=9, verticalalignment='bottom', horizontalalignment='left',
        transform=axs[0].transAxes,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='red', alpha=0.85))
    axs[0].text(0.97, 0.97, formula_poly,
        fontsize=9, verticalalignment='top', horizontalalignment='right',
        transform=axs[0].transAxes,
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='green', alpha=0.85))
    axs[0].legend()
    axs[0].grid(True)

    axs[1].scatter(E_log10, res_ln,   color='red',   label='Residuos ln',   zorder=3)
    axs[1].scatter(E_log10, res_poly, color='green', label='Residuos poly', marker='s', zorder=3)
    axs[1].axhline(0, color='k', linewidth=0.8, linestyle='--')
    axs[1].set_xlabel(r'$\log_{10}(E)$')
    axs[1].set_ylabel('Residuos')
    axs[1].legend()
    axs[1].grid(True)

    # ── Figure 2: dE/dx vs E – log10 axes ──────────────────────────────────────
    E_range = np.logspace(E_log10.min(), E_log10.max(), 500)
    fig2, ax = plt.subplots(figsize=(8, 8))

    ax.scatter(E_data, dE_dx_data, label='Datos experimentales', zorder=3, color='steelblue')
    ax.plot(E_range, model_ln(E_range),   color='red',   label='Ajuste ln')
    ax.plot(E_range, model_poly(E_range), color='green', label='Ajuste poly (grado 2)', linestyle='--')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('E (MeV)')
    ax.set_ylabel('dE/dx (keV/mm)')
    ax.set_title('Stopping power – escala log-log')
    ax.legend()
    ax.grid(True, which='both', linestyle='--', alpha=0.5)


    return (fig1, fig2), (model_ln, model_poly), (popt, pcov, poly_coef)


if __name__ == '__main__':
    (fig1, fig2), (model_ln, model_poly), (popt, pcov, poly_coef) = ajuste_stopping_power()
    print("popt ln  :", popt)
    print("poly_coef:", poly_coef)
    plt.show()

"""
model_ln(E)   → dE/dx [keV/mm]   via exp(modelo(ln(E), *popt))
model_poly(E) → dE/dx [keV/mm]   via 10**polyval(poly_coef, log10(E))

Datos del ajuste:
  popt, pcov  → parametros y covarianza del fit ln
  poly_coef   → coeficientes [p2, p1, p0] del polinomio grado 2
"""
