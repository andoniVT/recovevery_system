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
from Configuration.settings import documents
from Preprocesser.preprocessDocument import PreProcessor as PP

class SRI_Manager(object):
    
    def __init__(self):
        self.__corpus = []
        self.__preprocessed_corus = []
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
        self.__corpus = corpus
        return corpus
    
    def pre_process_corpus(self):
        corpus = self.load_corpus()
        processed_corpus = []
        for i in corpus:
            procesor = PP(i)
            proccesed = procesor.get_processed_document()
            processed_corpus.append(proccesed)
        return processed_corpus
                                             
    def organize_documents(self):
        pass
        '''
          * cargar todos los txts
          * pre procesarlos
          * convertirlos a booleanos
          * guardar los vectores en un binario
        '''
    
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
    documentos = manager.pre_process_corpus()
    for i in documentos:
        print i
   
   
    
    
    
    