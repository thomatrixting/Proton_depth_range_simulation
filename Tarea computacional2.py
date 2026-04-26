# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 19:10:23 2026

@author: valez
"""

import numpy as np
import matplotlib.pyplot as plt


E_data = np.array([0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0, 30.0, 50.0, 70.0, 100.0, 150.0, 200.0])
dEdx_data = np.array([466.0, 303.0, 221.0, 144.0, 112.0, 81.5, 46.6, 35.0, 23.3, 18.2, 14.0, 8.1, 6.3, 4.6, 3.9, 3.3, 2.9, 2.5])


logE = np.log10(E_data)
logDE = np.log10(dEdx_data)
coeffs = np.polyfit(logE, logDE, 2)

def dEdx_fit(E_val):
    if E_val < 0.01: E_val = 0.01 
    lE = np.log10(E_val)
    return 10.0 ** np.polyval(coeffs, lE)


deltaX = 0.005   
E = 100.0       
X = 0.0
xs, dEs = [], []

while E > 0.005:
    dedx = dEdx_fit(E) 
    de_step = dedx * deltaX 
    
    if E - de_step <= 0:
        
        ultimo_paso = (E / dedx)
        xs.append(X + ultimo_paso)
        dEs.append(E * 1000.0)
        break
        
    E -= de_step
    X += deltaX
    xs.append(X)
    dEs.append(de_step * 1000.0)


plt.figure(figsize=(10, 6))
plt.plot(xs, dEs, color='darkred', linewidth=2, label='Depósito de energía (dE)')
plt.fill_between(xs, dEs, color='red', alpha=0.15)

alcance_final = xs[-1]
plt.axvline(alcance_final, color='black', linestyle='--', label=f'Alcance R = {round(alcance_final, 3)} mm')

plt.title('Pico de Bragg: Protones de 100 MeV en Silicio', fontsize=14)
plt.xlabel('Profundidad X (mm)', fontsize=12)
plt.ylabel('Energía depositada ΔE (keV)', fontsize=12)
plt.xlim(0, alcance_final * 1.05)
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(fontsize=11)
plt.show()

print(f"Alcance calculado: {round(alcance_final, 4)} mm")