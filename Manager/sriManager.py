#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 22/11/2014

@author: andoni
'''
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

import glob
from Configuration.settings import documents , name_simple_corpus , name_processed_corpus , matrix_model , document_titles , vocabulary
from Preprocesser.preprocessDocument import PreProcessor as PP
from VectorModel.vectorSpaceModel import VectorSpaceModel as VM
import cPickle
from Genetic.genetic_manager import FitnessFunction as FF
from Genetic.genetic_manager import Genetic
import codecs
class SRI_Manager(object):
    
    def __init__(self):
        self.__titles = []
        self.__corpus = []
        self.__preprocessed_corpus = []
        self.__matrix_model = []
    
    def removeNonAscii(self , s): return "".join(i for i in s if ord(i)<128)
    
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
            words = self.removeNonAscii(words)                
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
        aux = 1
        for i in corpus:
            print aux
            procesor = PP(i)
            proccesed = procesor.get_processed_document()
            processed_corpus.append(proccesed)
            aux+=1                     
        with open(name_processed_corpus , 'wb') as fid:
            cPickle.dump(processed_corpus , fid)
        return processed_corpus
            
    def organize_documents(self):
        documents = self.load_document_information(2)
        model = VM(documents)
        matrix = model.prepare_corpus()
        with open(matrix_model , 'wb') as fid:
            cPickle.dump(matrix, fid)        
        #return [self.__dictionary, self.__tfidf, self.__corpus_tf_idf]
                 
    def load_document_information(self , type):
        if type == 0:
            file = document_titles 
        elif type==1:
            file = name_simple_corpus
        elif type==2: 
            file = name_processed_corpus
        
        elif type==3:
            file = matrix_model
        '''        
        elif type==4:
            file = vocabulary
        '''  
                                           
        with open(file , 'rb') as fid:
                clf_load = cPickle.load(fid)                            
        return clf_load
    
    def find(self, vector, word):
        index = 0
        for i in vector:
            if i == word:
                return index
            else:
                index+=1
        return -1
                
    def get_keywords(self , documents):
        words = []
        counts = []
        for i in documents:
            vec = i.split()
            for j in vec:
                if not j in words:
                    words.append(j)
                    counts.append(1)
                else:
                    index = self.find(words, j)
                    counts[index]+=1
        dictionary = []
        for i in range(len(words)):
            value = (words[i] , counts[i])
            dictionary.append(value)        
        return dictionary
    
    def make_query(self, query, relevants=10):
        proccesed = PP(query)
        comment = proccesed.get_processed_document()
        print comment
        
    
    
    
if __name__ == '__main__':
    
    manager = SRI_Manager()
    manager.make_query("ciencia de la computacion")
    

    
    

