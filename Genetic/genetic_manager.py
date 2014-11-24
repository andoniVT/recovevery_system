'''
Created on 10/11/2014
@author: andoni
'''

'''  
  cromosoma = query
  
  cromosoma = [1 0 0 0 0 0 0 0 0 0 0 0 0 0 1]
  
  generar_poblacion 
'''

import math
from random import randint , uniform , shuffle
import threading 
import time

def FitnessFunction(n, N):
    return 1 - n/float(N)
        
class Genetic(object):
    
    def __init__(self , population , generations, pc, pm , tipo_cruce):
        self.__population = population
        self.__generations = generations
        self.__prob_cr = pc
        self.__prob_mut = pm
        self.__fitness = []
        self.__tipo_cruce = tipo_cruce
        for i in range(len(self.__population)):
            self.__fitness.append(0)

             

if __name__ == '__main__':
    
    initial_query = [1,1,1,0,0]
    population = [[0,0,1,0,1] , [1,1,0,0,0] , [0,1,0,1,0] , [1,1,1,1,0] , [0,0,1,1,0] , [0,0,0,0,0]]
    generations = 10
    pc = 0.7
    pm = 0.1
    tipo_cruce=1 
    genetic = Genetic(initial_query,population, generations, pc , pm , tipo_cruce)        
     
    
  
