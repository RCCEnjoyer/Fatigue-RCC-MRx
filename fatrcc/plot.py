# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 12:41:00 2024

@author: Luis
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def plot_SN_graph (N_vec, eps_vec, eps, Nmax):
    
    plt.plot(N_vec, eps_vec)
    
    #Horizontal line for EPS
    plt.plot([0, Nmax], [eps, eps], color="r", )
                      
    #Vertical line for Nmax
    plt.plot([Nmax, Nmax], [0, eps], color="r", )
    
    plt.xlabel("Number of cycles (N)")
    plt.ylabel("Strain range (%)")
    
    ax=plt.gca()
    
    plt.yscale("log")
    plt.xscale("log")
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    
    plt.show()