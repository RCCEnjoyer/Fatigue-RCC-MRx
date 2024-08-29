# -*- coding: utf-8 -*-
"""

@author: lafernandez
"""
import sys
sys.path.append('../')
 
# importing

from fatrcc import calculation as cl

cl.elastic_fatigue_worst("stress_end_test.txt", "stress_start_test.txt", 270 , "X2CrNiMo17", 1)
cl.elastoplastic_fatigue_worst("strain_end_test.txt", "strain_start_test.txt", 300.0 , "X2CrNiMo17",1)

####################

#cl.write_mesh_range("stress_end_test.txt", "stress_start_test.txt", "Stress", "StressRange.csv")
#cl.write_mesh_range("strain_end_test.txt", "strain_start_test.txt", "Strain", "StrainRange.csv")


