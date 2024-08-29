# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 09:34:36 2023

@author: lafernandez
"""

import linecache
import numpy as np

############################### FUNCTIONS ################################

def read_file(File):



    num_lines =  len(open(File).read().splitlines())
    print ('Reading file: ',File, ' ---> Number of lines:',num_lines)

    data_matrix = np.zeros([num_lines-1,11])

    for i in range(num_lines-1):

        data = linecache.getline(File,2+i)
        values=data.split()

        data_matrix[i][0]=float(values[0]) # Node
        data_matrix[i][1]=float(values[1]) # X
        data_matrix[i][2]=float(values[2]) # Y
        data_matrix[i][3]=float(values[3]) # Z
        data_matrix[i][4]=float(values[4]) # SX
        data_matrix[i][5]=float(values[5]) # SY
        data_matrix[i][6]=float(values[6]) # SZ
        data_matrix[i][7]=float(values[7]) # SXY
        data_matrix[i][8]=float(values[8]) # SXZ
        data_matrix[i][9]=float(values[9]) # SYZ

    return data_matrix,num_lines-2


def get_tensor_range(vector2, vector1):

    vector_range = [0] * len(vector2)

    vector_range[0]=vector2[0]
    vector_range[1]=vector2[1]
    vector_range[2]=vector2[2]
    vector_range[3]=vector2[3]
    vector_range[4]=vector2[4]-vector1[4]
    vector_range[5]=vector2[5]-vector1[5]
    vector_range[6]=vector2[6]-vector1[6]
    vector_range[7]=vector2[7]-vector1[7]
    vector_range[8]=vector2[8]-vector1[8]
    vector_range[9]=vector2[9]-vector1[9]

    return vector_range


def get_Von_Mises(vector, tensortype):

    if tensortype == "Stress":

        vonmises = (vector[4]-vector[5])**2+(vector[5]-vector[6])**2+(vector[4]-vector[6])**2
        vonmises = vonmises + 6*(vector[7]**2+vector[8]**2+vector[9]**2)
        vonmises = np.sqrt(1/2)*np.sqrt(vonmises)

    elif tensortype == "Strain":

        vonmises = (vector[4]-vector[5])**2+(vector[5]-vector[6])**2+(vector[4]-vector[6])**2
        vonmises = vonmises + 3/2*(vector[7]**2+vector[8]**2+vector[9]**2)
        vonmises = np.sqrt(2)/3*np.sqrt(vonmises)

    return vonmises


def get_mesh_tensor_range(file_end, file_start, keyword):

    File_1, n_elements = read_file(file_start)
    File_2, n_elements = read_file(file_end)

    total_range=np.zeros([n_elements,11])

    for i in range(n_elements):
        total_range[i][0:10] = get_tensor_range(File_2[i][0:10], File_1[i][0:10])
        total_range[i][10]= get_Von_Mises(total_range[i][0:10], keyword)

    return total_range, n_elements


def max_vonMises_range(mesh_range, n_elements):

    max_vonMises_range=0
    max_location = 0

    for i in range(n_elements):
        if  max_vonMises_range<mesh_range[i][10]:
            max_vonMises_range=mesh_range[i][10]
            max_location = i

    return float(max_vonMises_range), max_location
