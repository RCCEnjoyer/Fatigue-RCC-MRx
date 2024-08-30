# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 10:04:53 2023

@author: lafernandez
"""

import pandas as pd

from . import extract_range as er
from . import properties as pro



def elastoplastic_fatigue_worst(file_end, file_start, temperature, material, Jf, f):

    strain_range, n_elements = er.get_mesh_tensor_range(file_end, file_start, "Strain")
    eps_total, max_location = er.max_vonMises_range(strain_range, n_elements)

    max_cycles =  pro.fatigue_cycles(temperature, eps_total*100*f, material, Jf)

    print("\n Maximum equivalent strain range = " + "{:.3f}".format(eps_total*100) + "%")

    print("Point location in ANSYS units:" )
    print("X = " + "{:.3f}".format(strain_range[max_location][1]) )
    print("Y = " + "{:.3f}".format(strain_range[max_location][2]) )
    print("Z = " + "{:.3f}".format(strain_range[max_location][3]) )

    print("\n Maximum number of cycles = " + "{:.2e}".format(max_cycles))
    print("############################################## \n")


def elastic_fatigue_worst(file_end, file_start, temperature, material, Jf, f):

    stress_range, n_elements = er.get_mesh_tensor_range(file_end, file_start, "Stress")
    sigma_total, max_location = er.max_vonMises_range(stress_range, n_elements)
    sigma_total = sigma_total/1e6

    print("\n Maximum equivalent stress range = " + "{:.3f}".format(sigma_total) + " MPa")
    print("Point location in ANSYS units:" )
    print("X = " + "{:.3f}".format(stress_range[max_location][1]) )
    print("Y = " + "{:.3f}".format(stress_range[max_location][2]) )
    print("Z = " + "{:.3f}".format(stress_range[max_location][3]) )


    young_mod, poisson_rat = pro.E_properties(material, temperature)  # Elastic properties for mat

    eps_1 = (2/3)*(1+poisson_rat)*sigma_total/young_mod
    #eps_2
    eps_3 = (pro.k_eps(temperature, sigma_total, material)-1)*eps_1    # Plastic def (Keps)
    eps_4 = (pro.k_vol(temperature, sigma_total, material)-1)*eps_1    # 3D plastic (Kmu)

    eps_total = (eps_1 + eps_3 + eps_4)

    print("\n Maximum estimated strain range = " + "{:.3f}".format(eps_total*100) + "%")
    print("eps 1 = " + "{:.2f}".format(eps_1*100) + "%" )
    print("eps 3 = " + "{:.2f}".format(eps_3*100) + "%" )
    print("eps 4 = " + "{:.2f}".format(eps_4*100) + "%")
    max_cycles =  pro.fatigue_cycles(temperature, eps_total*f*100, material, Jf)
    print("\n Maximum number of cycles = " + "{:.2e}".format(max_cycles))
    print("############################################## \n")


def write_mesh_range(file_end, file_start, keyword, name ="mesh_range_output.csv"):

    mesh_range, n_elements = er.get_mesh_tensor_range(file_end, file_start, keyword)
    pd.DataFrame(mesh_range).to_csv(name)
    