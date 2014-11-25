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
        self.__nDocuments = 401
        for i in range(len(self.__population)):
            self.__fitness.append(0)
    
    def show_fitness(self):
        print self.__fitness
    
    def show_population(self):
        for i in self.__population:
            print i
    
    def calculate_fitness(self , index):
        sumatoriaFreq = 0
        for i in self.__population[index]:
            sumatoriaFreq = sumatoriaFreq + i[1]
        value = 1 - (sumatoriaFreq/float(self.__nDocuments))
        self.__fitness[index] = value
    
    def calculate_fitness_population(self):
        threads = list()
        for i in range(len(self.__population)):
            t = threading.Thread(target=self.calculate_fitness , args=(i,)) 
            threads.append(t)
            t.start()
            t.join()
    
    def sort_population(self):
        for i in range(len(self.__fitness)):
            for k in range(len(self.__fitness)-1 , i , -1):
                if self.__fitness[k]<self.__fitness[k-1]:
                    tmp = self.__fitness[k]
                    tmp2 = self.__population[k]
                    self.__fitness[k] = self.__fitness[k-1]
                    self.__population[k] = self.__population[k-1]
                    self.__fitness[k-1] = tmp
                    self.__population[k-1] = tmp2
    
    def roulette_selection(self):
        acumulados = []
        new_fitness = []
        sum_fitness = 0
        for i in self.__fitness:
            sum_fitness = sum_fitness + i        
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
            value = uniform(0.0, 360.0)
            for j in range(len(ruleta)):
                inicio = ruleta[j][0]
                fin = ruleta[j][1]
                if value>inicio and value<=fin:
                    new_population.append(self.__population[j])
                    new_fitness.append(self.__fitness[j])
                    break
        self.__population = new_population
        self.__fitness = new_fitness
        self.sort_population()
    
    def tournament_selection(self):
        new_population = []
        new_fitness = []
        i = 0
        while i < len(self.__population)/2:
            for j in range(2):
                new_population.append(self.__population[i])
                new_fitness.append(self.__fitness[i])
            i+=1        
        self.__population = new_population
        self.__fitness = new_fitness
                             

if __name__ == '__main__':
    
    population = [[('cf', 13), ('lad', 99), ('ensegu', 28), ('negr', 87), ('perrill', 1), (u'enfatiz', 4)] ,
     [('manifest', 13), ('emocion', 11), ('not', 27), (u'automat', 29), ('basili', 1), ('covers', 1)] ,
     [('virtud', 13), ('mamifer', 14), (u'merc', 19), (u'desliz', 15), ('angiosperm', 1), (u'descendient', 6)],
     [('requier', 19), ('coch', 25), ('embarg', 120), ('lech', 38), (u'verific', 2), ('mucus', 1)],
     [('navid', 10), ('ib', 26), ('rock', 44), (u'convirt', 18), ('elder', 1), ('hipotet', 1)],
     [('asi', 270), ('gaseos', 12), (u'intern', 17), ('cons', 11), (u'envuelv', 2), ('piesy', 1)],
     [('estrell', 91), (u'cultiv', 19), (u'ole', 10), ('histori', 119), (u'monarc', 7), (u'impas', 1)],
     [('pucher', 15), (u'cuac', 12), ('encant', 12), ('especi', 78), (u'periheli', 3), ('arqueologi', 1)],
     [(u'consigui', 23), ('biom', 19), ('angusti', 14), (u'iglesi', 51), (u'pasab', 1), (u'repanting', 1)],
     [('vegetacion', 18), ('niebl', 10), ('hierr', 19), ('oi', 12), (u'rafag', 5), ('cation', 1)]]
          
    generations = 10
    pc = 0.7
    pm = 0.1
    tipo_cruce=1 
    genetic = Genetic(population, generations, pc , pm , tipo_cruce)
    genetic.calculate_fitness_population()
    genetic.show_fitness()
    genetic.show_population()
    print "ordenadoss"
    genetic.sort_population()
    genetic.show_fitness()
    genetic.show_population()
    
    print "seleccion torneo"
    genetic.tournament_selection()
    genetic.show_fitness()
    genetic.show_population()
    
    
  
