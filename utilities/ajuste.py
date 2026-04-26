import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as curve_fit
import pandas as pd


def modelo(x, a, b, c, d, f):
    return a*np.abs(b+x)**(c) + np.exp(d*x) + f


def ajuste_stopping_power(data_path='data/datos_stopping_power.xlsx'):
    doc = pd.read_excel(data_path, header=0, names=['E', 'dE/dx'])
    E_data = doc["E"].values
    dE_dx_data = doc["dE/dx"].values
    E_log = np.log(E_data)
    dE_dx_log = np.log(dE_dx_data)

    popt, pcov = curve_fit.curve_fit(modelo, E_log, dE_dx_log)
    a, b, c, d, f = popt

    fig, axs = plt.subplots(2, 1, figsize=(10, 8))

    axs[0].scatter(E_log, dE_dx_log, label='Datos experimentales')
    axs[0].plot(E_log, modelo(E_log, a, b, c, d, f), label='Ajuste', color='red')
    axs[0].set_xlabel('ln(E)')
    axs[0].set_ylabel('ln(dE/dx)')
    axs[0].text(1.5, 1,
        r'$\mathbf{Ajuste\ Log-Log:}$' + '\n' +
        fr'$\ln\left(\frac{{dE}}{{dx}}\right) = {a:.2f} \cdot \left| {b:.2f} + \ln(E) \right|^{{{c:.2f}}} + ' +
        fr'e^{{{d:.2f} \cdot \ln(E)}} + {f:.2f}$',
        fontsize=10, verticalalignment="top", horizontalalignment='right',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='navy', alpha=0.8))
    axs[0].legend()
    axs[1].scatter(E_log, dE_dx_log - modelo(E_log, a, b, c, d, f), label='residuos', color='blue')
    axs[1].set_xlabel('ln(E)')
    axs[1].set_ylabel('Residuos')

    return fig, (popt, pcov)


if __name__ == '__main__':
    fig, (popt, pcov) = ajuste_stopping_power()
    print(popt)
    plt.show()

"""
Observamos que el modelo propuesto logra capturar la tendencia general de los datos experimentales,
aunque presenta algunas desviaciones que se reflejan en la gráfica de los residuos. Allí, se realizó
el ajuste con los datos en escala logarítmica para que el modelo pueda ajustar adecuadamente los datos, al darle
una relación más equitativa dada la distribución de datos original. De esta manera, obtenemos la relación:
dE/dx = exp(-0.35*|2.38 + ln(E)|^1.53 + exp(0.25*ln(E)) + 4.02)
Asimismo, se evidencia como los residuos oscilan alrededor del cero, lo que sugiere que el modelo pudo sustraer
los patrones deterministas de los datos, y la varianza restante podría deberse a ruido experimental o a factores no considerados en el modelo base.
"""