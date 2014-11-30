#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on 21/11/2014

@author: andoni
'''
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

import sys
from gensim import corpora, models, similarities
from scipy import spatial

class VectorSpaceModel(object):
    
    def __init__(self , documents=""):
        self.__documents = documents
        self.__dictionary = []
        self.__words_and_id = []
        self.__corpus = []
        self.__tfidf = []
        self.__corpus_tf_idf = []
        self.__vocabulary = []
                    
    def prepare_corpus(self):
        vec_documents = []
        for i in self.__documents:
            vec = i.split()
            vec_documents.append(vec)        
        self.__dictionary = corpora.Dictionary(vec_documents)
        self.__words_and_id = self.__dictionary.token2id        
        self.__corpus = [self.__dictionary.doc2bow(text) for text in vec_documents]    
        #for i in self.__corpus:
        #    print i            
        self.__tfidf = models.TfidfModel(self.__corpus)
        self.__corpus_tf_idf = self.__tfidf[self.__corpus]
        #for i in self.__corpus_tf_idf:
         #   print i            
        return [self.__dictionary, self.__tfidf, self.__corpus_tf_idf]
    
    def set_data(self, dic, tfidf, ctfidf):
        self.__dictionary = dic 
        self.__tfidf = tfidf
        self.__corpus_tf_idf = ctfidf
        
    def get_frequency_vector(self , query):
        return self.__dictionary.doc2bow(query.split())
              
    def get_tf_idf_vector(self , query):
        freq_vector = self.get_frequency_vector(query)
        return self.__tfidf[freq_vector]
                         
    def get_distances(self , vec_tf):
        index = similarities.MatrixSimilarity(self.__tfidf[self.__corpus_tf_idf])
        sims = index[vec_tf]        
        return sorted(enumerate(sims) , key=lambda item: -item[1])
    
    def get_tf_value(self , id):
        for i in self.__corpus_tf_idf:
            for j in i:
                if j[0] == id:                
                    return j[1]
                  
    def get_key(self , id):
        for i in self.__dictionary.token2id:
            id_value = self.__dictionary.token2id[i]
            key =  i
            if id == id_value:
                return key 
    
    def get_len_vocabulary(self):
        return len(self.__dictionary)
             
        
        
            
        
    
if __name__ == '__main__':
    
    
    
    documents = ['hola como estas' , 'yo estoy bien' , 'hola me llamo Andoni' , 
                 'Jorge bien yo me llamo Jorge' , 'esto es perfecto' , 'estas te encuentras ahi']
    
    model = VectorSpaceModel(documents)
    model.prepare_corpus()
    #vec = model.get_frequency_vector(['estoy muy bien Jorge Andoni Valverde'])    
    vec = model.get_tf_idf_vector('estoy muy bien Jorge Andoni Valverde')
    
    print model.get_tf_value(15)
    
    print model.get_key(9)
    
    print model.get_len_vocabulary()
    
    '''
    similitudes = model.get_distances(vec)
    for i in similitudes:
        print i
    '''
     