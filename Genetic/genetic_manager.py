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
from random import randint , uniform
import threading 
import time

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
            return round(sumxy/value , 4)
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
    
    def __init__(self , initial_query, population , generations, pc, pm):
        self.__initial_query = initial_query
        self.__population = population
        self.__generations = generations
        self.__prob_cr = pc
        self.__prob_mut = pm
        self.__fitness = []
        self.__optimized_query = initial_query
        for i in range(len(self.__population)):
            self.__fitness.append(0)
        
    
    def print_population(self):
        print self.__population
    
    def print_fitness(self):
        print self.__fitness
    
    def calculate_fitness(self , index):
        func = FitnessFunction(self.__optimized_query , self.__population[index] , 1)
        self.__fitness[index]=  func.get_fitness()
    
    def decode_population(self):
        threads = list()
        for i in range(len(self.__population)):
            t = threading.Thread(target=self.calculate_fitness , args=(i,))
            threads.append(t)
            t.start()
            t.join()
    
    def sort_population(self):
        for i in range(len(self.__fitness)):
            for k in range(len(self.__fitness)-1, i , -1):
                if(self.__fitness[k]>self.__fitness[k-1]):
                    tmp = self.__fitness[k]
                    temp2 = self.__population[k]
                    self.__fitness[k] = self.__fitness[k-1]
                    self.__population[k] = self.__population[k-1]
                    self.__fitness[k-1] = tmp
                    self.__population[k-1] = temp2
        
    
    def sumatoria(self):
        suma = 0.0
        for i in self.__fitness:
            suma = suma + i
        return suma
    
    def roulette_selection(self):
        acumulados = []
        new_fitness =[]
        sum_fitness = self.sumatoria()
        for i in self.__fitness:
            valor = (360.0*i)/sum_fitness
            acumulados.append(valor)
        acum = 0.0
        ruleta = []
        for i in acumulados:
            inicio = acum
            fin = acum + i 
            value = (inicio , fin)
            ruleta.append(value)
            acum = acum + i
        
        new_population = []
        for i in ruleta:
            value = uniform(0.0 , 360.0)
            for j in range(len(ruleta)):
                inicio = ruleta[j][0]
                fin = ruleta[j][1]
                if value>inicio and value <=fin:
                    new_population.append(self.__population[j])
                    new_fitness.append(self.__fitness[j])
                    break
        self.__population = new_population
        self.__fitness = new_fitness
                
            
        
         
        
    def crossover1point(self, index , index2):
        cadena = self.__population[index]
        cadena2 = self.__population[index2]
        hijo = []   
        hijo2 = []
        corte = randint(1 , len(cadena)-1)
        i = 0
        while i < len(cadena):
            j = 0
            while j < corte:
                hijo.append(cadena[j])
                hijo2.append(cadena2[j])
                j+=1
                i+=1 
            k = corte
            while k<len(cadena):
                hijo.append(cadena2[k])
                hijo2.append(cadena[k])
                k+=1
                i+=1
            i+=1  
        self.__population[index]= hijo
        self.__population[index2]= hijo2
    
    def crossover2points(self, index , index2):
        cadena = self.__population[index]
        cadena2 = self.__population[index2]
        hijo = []
        hijo2 = []
        corte1 = randint(1 , len(cadena)/2)
        flag = True
        while flag:
            corte2 = corte1 + randint(1 , len(cadena)-1)
            if corte2 < len(cadena):
                flag = False
        i=0
        while i < len(cadena):
            j=0
            while j < corte1:
                hijo.append(cadena[j])
                hijo2.append(cadena2[j])
                j+=1
                i+=1 
            k = corte1
            while k < corte2:
                hijo.append(cadena2[k])
                hijo2.append(cadena[k])
                k+=1
                i+=1
            l = corte2
            while l < len(cadena):
                hijo.append(cadena[l])
                hijo2.append(cadena2[l])
                l+=1
                i+=1
        self.__population[index] = hijo
        self.__population[index2] = hijo2
        
    
    def mutation(self , cadena):
        index = randint(0 , len(cadena)-1)
        if cadena[index] == 1:
            cadena[index] = 0
        else:
            cadena[index] = 1
        return cadena
    
    def evaluate(self):
        pass 
                            
    def execute(self):
        '''
        decodificar y evaluar cada miembro de la poblacion
        '''
        self.decode_population()
        total_cruces = self.__prob_cr * self.__generations
        total_mutaciones = self.__prob_mut * self.__generations
        
        for i in range(self.__generations):            
            print "Generacion " + str(i+1)
            self.sort_population()
            
            '''
               seleccionar siguiente generacion --> ruleta
               
               operar
                    --> cruce 1 punto o cruce 2 puntos
                    --> mutacion
                    
                evaluar fitness    
            '''
             


if __name__ == '__main__':
    
    #cadena1 = [1,1,1,1,0,0,1,1,1,0,0]
    #cadena2 = [1,0,1,1,0,0,0,0,1,1,1]
    initial_query = [1,1,1,0,0]
    population = [[0,0,1,0,1] , [1,1,0,0,0] , [0,1,0,1,0] , [1,1,1,1,0]]
    generations = 10
    pc = 0.8
    pm = 0.1
    genetic = Genetic(initial_query,population, generations, pc , pm)
    
    genetic.decode_population()
    genetic.sort_population()
    genetic.roulette_selection()
    
    #genetic.execute()
    
  
