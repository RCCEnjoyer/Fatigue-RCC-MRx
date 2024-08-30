# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 09:22:48 2023

@author: lafernandez
"""
#pylint: disable=E1101

import os
import math
import pandas as pd
import numpy as np
from scipy import interpolate

from . import plot



def f(x):

    try:
        return float(x)
    except:
        return x

def path_creator(filename):

    directory = os.path.dirname(__file__)
    return directory + "/materials/" + filename

def get_indexes(value, vector, magnitude, units):

    indexes = [0, 0]

    try:
        indexes[0] = next(x[0] for x in enumerate(vector[1:]) if x[1] > value)
    except:
        print("WARNING! "+ magnitude + " data out of range, curve taken for maximum" +
              " available: " + str(vector[-1]) + " " + units + " \n")
        indexes[0] = len(vector[1:-1])
        indexes[1] = indexes[0]
        return indexes

    if indexes[0] == 0:
        print("WARNING! "+ magnitude + " data out of range, curve taken for minimum" +
              " available: " + str(vector[1]) + " " + units + " \n")
        indexes = [1, 1]
    else:
        indexes[1] = indexes[0] + 1

    return indexes

def fatigue_cycles (temperature, eps, material, Jf):

    N_table = pd.read_csv(path_creator("Cycles_" + material + ".csv"))
    N_table.columns = N_table.columns.map(f)

    T_index = get_indexes(temperature, N_table.columns[:], "Temperature", "ºC")

    Temps = [N_table.columns[T_index[0]], N_table.columns[T_index[1]]]
    eps_vector = [0] * len(N_table.iloc[:, T_index[0]]-1)
    
    for i, value in enumerate(N_table.iloc[:, T_index[0]]):
        eps_temp = [value, N_table.iloc[i, T_index[1]]]
        eps_vector[i] = np.interp(temperature, Temps, eps_temp)/Jf

    if eps < min(eps_vector):
        print("Obtained strain is below the minimum strain in data \n")
        print("The maximum number of cycles is = " + str(N_table.iloc[-1,0]))
        return N_table.iloc[-1,0]

    if eps > max(eps_vector):
        print("WARNING! Obtained strain is above the maximum strain in data \n")
        print("The maximum number of cycles is = " + str(N_table.iloc[1,0]))
        return N_table.iloc[1,0]

    result = interp_log10(eps, eps_vector, N_table['Unnamed: 0'])
    plot.plot_SN_graph(N_table['Unnamed: 0'], eps_vector, eps, result)

    return result

def k_eps(temperature, stress_range, material):

    k_eps_table = pd.read_csv(path_creator("K_eps_" + material + ".csv"))
    k_eps_table.columns = k_eps_table.columns.map(f)

    stress_indexes = get_indexes(stress_range, k_eps_table.columns[:], "Pressure", "MPa")
    temp_indexes = get_indexes(temperature, [0] + k_eps_table.iloc[:,0].values.tolist(), "Temperature", "ºC")

    stress_values = [k_eps_table.columns[stress_indexes[0]], k_eps_table.columns[stress_indexes[1]]]
    temp_values = [k_eps_table.iloc[temp_indexes[0]-1, 0], k_eps_table.iloc[temp_indexes[1]-1, 0]]

    x_vec = [stress_values[0], stress_values[0], stress_values[1], stress_values[1]]
    y_vec = [temp_values[0], temp_values[1], temp_values[1], temp_values[0]]
    z_vec = [k_eps_table.iloc[temp_indexes[0]-1, stress_indexes[0]],
             k_eps_table.iloc[temp_indexes[1]-1, stress_indexes[0]] ,
             k_eps_table.iloc[temp_indexes[0]-1, stress_indexes[1]] ,
             k_eps_table.iloc[temp_indexes[1]-1, stress_indexes[1]]]

    k_eps_function = interpolate.interp2d(x_vec, y_vec, z_vec)
    k_eps_value = k_eps_function(stress_range, temperature)

    return float(k_eps_value)

def k_vol(temperature, stress_range, material):

    k_vol_table = pd.read_csv(path_creator("K_vol_" + material + ".csv"))
    k_vol_table.columns = k_vol_table.columns.map(f)

    stress_indexes = get_indexes(stress_range, k_vol_table.columns[:], "Pressure", "MPa")
    temp_indexes = get_indexes(temperature, [0] + k_vol_table.iloc[:,0].values.tolist(), "Temperature", "ºC")

    stress_values = [k_vol_table.columns[stress_indexes[0]], k_vol_table.columns[stress_indexes[1]]]
    temp_values = [k_vol_table.iloc[temp_indexes[0]-1, 0], k_vol_table.iloc[temp_indexes[1]-1, 0]]


    x_vec = [stress_values[0], stress_values[0], stress_values[1], stress_values[1]]
    y_vec = [temp_values[0], temp_values[1], temp_values[1], temp_values[0]]
    z_vec = [k_vol_table.iloc[temp_indexes[0]-1, stress_indexes[0]],
            k_vol_table.iloc[temp_indexes[1]-1, stress_indexes[0]] ,
            k_vol_table.iloc[temp_indexes[0]-1, stress_indexes[1]] ,
            k_vol_table.iloc[temp_indexes[1]-1, stress_indexes[1]]]

    k_vol_function = interpolate.interp2d(x_vec, y_vec, z_vec)
    k_vol_value = k_vol_function(stress_range, temperature)

    return float(k_vol_value)

def E_properties(material, temperature):
    
    if material=="X2CrNiMo17":
        E_module = 201660 - 84.8*temperature
        poisson = 0.3
    
    return E_module, poisson

def interp_log10(eps, datos_eps, datos_N):

    # Datos de deformación y ciclos inferior y superior en la curva interpolada para la temperatura especificada
    index_eps_lower = np.argmax(pd.Series(datos_eps)-eps < 0 )
    index_eps_upper = np.argmax(pd.Series(datos_eps)-eps < 0 ) - 1
    eps_lower = datos_eps[index_eps_lower]     # Valor justo inferior de deformación en la curva interpolada para la temperatura especificada
    eps_upper = datos_eps[index_eps_upper]     # Valor justo superior de deformación en la curva interpolada para la temperatura especificada
    N_lower = datos_N[index_eps_lower]
    N_upper = datos_N[index_eps_upper]

    # Coeficiente de la recta: a*log10(eps) + b
    a = (N_lower - N_upper) / (math.log10(eps_lower) - math.log10(eps_upper))
    b = N_lower - a*math.log10(eps_lower)

    # Resultado de ciclos para un epsilon determinado a una temperatura especificada
    result = math.floor(a*math.log10(eps) + b)

    return result
