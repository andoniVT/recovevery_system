'''
Created on 10/11/2014
@author: andoni
'''
import math
from random import randint , uniform , shuffle
import threading 
import time
from __builtin__ import list

class Genetic(object):
    
    def __init__(self , population , generations, pc , tipo_cruce):
        self.__population = population
        self.__generations = generations
        self.__prob_cr = pc
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
    
    def get_population(self):
        return self.__population
    
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
        posiciones = []
        for i in range(len(self.__population)):
            posiciones.append(i)        
        shuffle(posiciones)        
        i=0
        k=0
        while i<len(self.__population)/2:
            for j in range(2):
                index = posiciones[k]
                index2 = posiciones[k+1]
                if self.__fitness[index] < self.__fitness[index2]:
                    new_population.append(self.__population[index])
                    new_fitness.append(self.__fitness[index])
                else:
                    new_population.append(self.__population[index2])
                    new_fitness.append(self.__fitness[index2])
            k+=2 
            i+=1 
        self.__population = new_population
        self.__fitness = new_fitness
    
    def crossover1point(self , index, index2):
        cadena = self.__population[index]
        cadena2 = self.__population[index2]
        hijo = []
        hijo2 = []
        corte = randint(1 , len(cadena)-1)
        i=0
        while i<len(cadena):
            j = 0
            while j < corte:
                hijo.append(cadena[j])
                hijo2.append(cadena2[j])
                j+=1
                i+=1
            k = corte
            while k < len(cadena):
                hijo.append(cadena2[k])
                hijo2.append(cadena[k])
                k+=1
                i+=1
            i+=1
        self.__population[index] = hijo
        self.__population[index2] = hijo2
    
    def crossover2points(self , index, index2):
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
    
    def cruce_1punto_paralelo(self):
        posiciones = []
        for i in range(len(self.__population)):
            posiciones.append(i)
        shuffle(posiciones)
        threads = list()
        i = 0
        while i < len(posiciones):
            t = threading.Thread(target=self.crossover1point, args=(posiciones[i], posiciones[i+1],))
            threads.append(t)
            t.start()
            t.join()
            i+=2
    
    def cruce_2punto_paralelo(self):
        posiciones = []
        for i in range(len(self.__population)):
            posiciones.append(i)
        shuffle(posiciones)
        threads = list()
        i = 0
        while i < len(posiciones):
            t = threading.Thread(target=self.crossover2points, args=(posiciones[i], posiciones[i+1],))
            threads.append(t) 
            t.start()
            t.join()                     
            i+=2
    
    def realizar_cruce(self , tipo):
        if tipo == 1:
            self.cruce_1punto_paralelo()
        elif tipo == 2:
            self.cruce_2punto_paralelo()
    
    def execute(self):
        self.calculate_fitness_population()
        total_cruces = self.__prob_cr * self.__generations
        self.sort_population()
        for i in range(self.__generations):
            print "Generacion " + str(i+1)
            self.tournament_selection()
            if total_cruces>=1:
                hacer_cruce = randint(0,1)
                faltan = (self.__generations-i)-total_cruces
                if hacer_cruce == 1 and faltan>=0:
                    self.realizar_cruce(self.__tipo_cruce)
                    total_cruces-=1
                if hacer_cruce==0 and faltan<=0:
                    self.realizar_cruce(self.__tipo_cruce)
            self.calculate_fitness_population()
            self.sort_population()
            print "ok"
                             
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
    tipo_cruce=1 
    genetic = Genetic(population, generations, pc , tipo_cruce)
    genetic.execute()
    
  
