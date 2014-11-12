'''
Created on 10/11/2014

@author: andoni
'''

'''
numero de individuos   : 
numero de generaciones :
numero experimentos    :
numero de variables    :
tipo de cruce          :
probabilidad de cruce  :
probabilidad  mutacion :
aplicar elitismo       :
precision              :
limite superior        :
limite inferior        :
funcion de evaluacion  : 

'''

'''  
  cromosoma = query
  
  cromosoma = [1 0 0 0 0 0 0 0 0 0 0 0 0 0 1]
  
  generar_poblacion 
'''

import math

class FitnessFunction(object):
    
    def __init__(self , vector , vector2 , option):
        self.__vector = vector
        self.__vector2 = vector2
        self.__option = option
        self.__fitness = self.calculate_fitness()
    
    def get_fitness(self):
        return self.__fitness
    
    def calculate_fitness(self):
        if self.__option == 1:
            return self.cosine_similarity()
        if self.__option == 2:
            return self.dice_similarity()
        if self.__option == 3:
            return self.jaccard_similarity() 
            
    def cosine_similarity(self):
        sumxx , sumxy , sumyy = 0 , 0 , 0
        for i in range(len(self.__vector)):
            x = self.__vector[i]
            y = self.__vector2[i]
            sumxx+=x*x
            sumyy+=y*y
            sumxy+=x*y
        value = math.sqrt(sumxx*sumyy)
        if value!=0:
            return sumxy/value
        else: 
            return 0
    
    def dice_similarity(self):
        a = set(self.__vector)
        b = set(self.__vector2)
        overlap = len(a & b)
        return overlap * 2.0/(len(a)+len(b)) 
    
    def jaccard_similarity(self):
       set1 , set2 , shared = 0 , 0 , 0
       for i in range(len(self.__vector)):
           if self.__vector[i]!=0:
               set1+=1
           if self.__vector2[i]!=0:
               set2+=1
           if self.__vector[i]!=0 and self.__vector2[i]!=0:
               shared+=1
       val = set1+set2-shared
       if val!=0:
           return 1.0 - (float(shared)/val)
       else:
           return 0   
    

class Genetic(object):
    
    def __init__(self , population):
        self.__population = population


if __name__ == '__main__':
    
    func = FitnessFunction([1,0,0,1] , [0,1,1,0] , 1)
    print func.get_fitness()
    
    func2 = FitnessFunction([1,0,0,1] , [0,1,1,0] , 2)
    print func2.get_fitness()
    
    func3 = FitnessFunction([1,0,0,1] , [0,1,1,0] , 3)
    print func3.get_fitness()


