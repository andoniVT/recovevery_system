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
from Configuration.settings import documents , name_simple_corpus , name_processed_corpus , matrix_model
from Preprocesser.preprocessDocument import PreProcessor as PP
from VectorModel.model import BooleanModel as BM
import cPickle

class SRI_Manager(object):
    
    def __init__(self):
        self.__corpus = []
        self.__preprocessed_corpus = []
        self.__matrix_model = []
    
    def load_corpus(self):
        corpus = []
        files = glob.glob(documents)           
        for name in files:
            f = open(name , 'r')
            words = ""
            for line in f.readlines():
                line = line.rstrip('\n')
                words = words + line + " "
            corpus.append(words)  
            f.close()
        #self.__corpus = corpus
        
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
        for i in matrix:
            print i
        
        with open(matrix_model , 'wb') as fid:
            cPickle.dump(matrix , fid)
        '''
          * cargar todos los txts ---
          * pre procesarlos    ----
          * convertirlos a booleanos
          * guardar los vectores en un binario
        '''            
    
    def load_document_information(self , type):
        if type==1:
            file = name_simple_corpus
        if type==2: 
            file = name_processed_corpus
        if type==3:
            file = matrix_model                                 
        with open(file , 'rb') as fid:
                clf_load = cPickle.load(fid)                            
        return clf_load                        
    
    def make_query(self , query , relevants):
        pass
        '''
          * preprocesar el query
          * convertir a booleano
          * hacer el algoritmo genetico del query pa optimizar
          * comparar el query con todas los vectores de los documentos
          * devolver los n mas relevantes
        '''
        

    
if __name__ == '__main__':
   
    manager = SRI_Manager()
    data = manager.load_document_information(3)
    for i in data:
        print i 
    
    #manager.organize_documents()
    
   
   
    
    
    
    