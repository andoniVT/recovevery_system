#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on 09/11/2014

@author: andoni
'''
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

import glob
from Configuration.settings import documents , name_simple_corpus , name_processed_corpus , matrix_model , document_titles , vocabulary
from Preprocesser.preprocessDocument import PreProcessor as PP
from VectorModel.model import BooleanModel as BM
import cPickle
from Genetic.genetic_manager import FitnessFunction as FF
from Genetic.genetic_manager import Genetic 

class SRI_Manager(object):
    
    def __init__(self):
        self.__titles = []
        self.__corpus = []
        self.__preprocessed_corpus = []
        self.__matrix_model = []            
    
    def get_title_name(self , file):
        i = len(file)-1
        fin = i 
        while file[i] != '/':
            i-=1        
        ini = i+1
        fin-=3
        word = ''
        for k in range(ini , fin):
            word = word + file[k]
        word = word.replace('_', ' ')
        return word  
        
    def load_corpus(self):
        corpus = []
        titles = []
        files = glob.glob(documents)           
        for name in files:
            value = (name , self.get_title_name(name))
            titles.append(value)
            f = open(name , 'r')
            words = ""
            for line in f.readlines():
                line = line.rstrip('\n')
                words = words + line + " "
            corpus.append(words)  
            f.close() 
        
        with open(document_titles , 'wb') as fid:
            cPickle.dump(titles , fid)
        
        with open(name_simple_corpus , 'wb') as fid:
            cPickle.dump(corpus , fid)
        return corpus
        
    def pre_process_corpus(self):
        corpus = self.load_corpus()
        processed_corpus = []
        for i in corpus:
            procesor = PP(i)
            proccesed = procesor.get_processed_document()
            processed_corpus.append(proccesed)
        #self.__preprocessed_corpus = processed_corpus
        with open(name_processed_corpus , 'wb') as fid:
            cPickle.dump(processed_corpus , fid)
        return processed_corpus
                                             
    def organize_documents(self):
        documents = self.pre_process_corpus()
        
        model = BM(documents)        
        matrix = model.generate_matrix_model()
        with open(matrix_model , 'wb') as fid:
            cPickle.dump(matrix , fid)
        '''
          * cargar todos los txts ---
          * pre procesarlos    ----
          * convertirlos a booleanos
          * guardar los vectores en un binario
        '''            
    
    def load_document_information(self , type):
        if type == 0:
            file = document_titles 
        elif type==1:
            file = name_simple_corpus
        elif type==2: 
            file = name_processed_corpus
        elif type==3:
            file = matrix_model        
        elif type==4:
            file = vocabulary  
                                           
        with open(file , 'rb') as fid:
                clf_load = cPickle.load(fid)                            
        return clf_load 
    
    def get_menor(self , vector): 
        menor = 10000000
        index = -1        
        for i in range(len(vector)):
            if menor > vector[i]:
                menor = vector[i]
                index = i
        return index
    
    def get_relevants(self, query , matrix , relevants):
        vec_fitness = []          
        vec_indexes = []        
        lleno = 0              
        for i in range(len(matrix)):
            vec_document = matrix[i] 
            fitness = FF(query , vec_document , 1)
            value = fitness.get_fitness()            
            if lleno < relevants:
                vec_fitness.append(value)
                vec_indexes.append(i)
                lleno+=1
            else:
                index = self.get_menor(vec_fitness)
                menor = vec_fitness[index]
                if value > menor:
                    vec_fitness[index] = value                
                    vec_indexes[index] = i
            
        return vec_indexes
                                                            
    def make_query(self , query , relevants=6):
        
        processed = PP(query)
        list = processed.get_processed_document().split(' ') 
        vocabulary_list = self.load_document_information(4)
        query_bool = []
        for i in vocabulary_list:
            if i in list:
                query_bool.append(1)
            else:
                query_bool.append(0)
                
        titles = self.load_document_information(0)
        matrix = self.load_document_information(3)
        
        index_relevants = self.get_relevants(query_bool, matrix, relevants)
        population = []
        for i in range(len(index_relevants)):
            population.append(matrix[index_relevants[i]])
        
        
        initial_query = query_bool           
        generations = 10
        pc = 0.7
        pm = 0.01
        tipo_cruce = 1
        genetic = Genetic(initial_query, population , generations, pc, pm , tipo_cruce)
        genetic.execute()
        optimized_query = genetic.get_optimized_query()
        
        
        index_relevants = self.get_relevants(optimized_query, matrix, relevants)
        
        for i in range(len(index_relevants)):
            print titles[index_relevants[i]][1]
        
        
        
        '''
          * preprocesar el query ok
          * convertir a booleano  ok
          * hacer el algoritmo genetico del query pa optimizar
          * comparar el query con todas los vectores de los documentos
          * devolver los n mas relevantes
        '''
            
if __name__ == '__main__':
    prueba = 'prueba/*.txt'
    
    
    #query = "ciencia de la computacion"
    manager = SRI_Manager()
    query = "arbol binario"
    manager.make_query(query)
    
    
    
    
    '''
    query = [0 , 1, 0 , 0, 1]
    matrix = [[1 , 1, 0 , 0, 1] , [0 , 0, 0 , 0, 1],[1 , 1, 0 , 0, 1],
              [0 , 1, 1 , 1, 1],[1 , 1, 1 , 1, 1],[0 , 1, 1 , 0, 0],
              [1 , 0, 0 , 0, 0],[0 , 0, 0 , 0, 0],[1 , 1, 0 , 1, 0],
              [0 , 1, 1 , 1, 0],[0 , 1, 0 , 0, 1],[0 , 0, 1 , 1, 0]]
    
    
    relevants = manager.get_relevants(query, matrix, 2)
    for i in relevants:
        print i
    '''
    
    
    