#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on 09/11/2014

@author: andoni
'''

import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

class BooleanModel(object):
    
    def __init__(self , documents):
        self.__documents = documents
        self.__vocabulary = []
        self.__matrix = []
    
    def find_word(self , word , vector):
        if word in vector:
            return True
        else:
            return False
    
    def get_vocabulary(self):
        words = []        
        for i in self.__documents:
            vec = i.split(' ')
            for j in vec:
                if not self.find_word(j, words):
                    words.append(j)
        return words
    
    def generate_matrix_model(self):
        vocabulary = self.get_vocabulary()
        print len(vocabulary)
        matrix = []
        val = 1
        for i in self.__documents:
            vector = []
            words = i.split(' ')
            for j in vocabulary:
                if self.find_word(j, words):
                    vector.append(1)
                else:
                    vector.append(0)
            print "numero: " + str(val) + " len vec: " + str(len(vector))
            val+=1
            matrix.append(vector)
        return matrix
    
    def get_the_vocabulary(self):
        return self.__vocabulary

                                                                     
if __name__ == '__main__':
    
    docs = ['hola como estas' ,'yo estoy bien' ,'hola me llamo Andoni' ,'bien yo me llamo Jorge' ,'esto es perfecto' ,'estas te encuentas ahi' ]
    
    model = BooleanModel(docs)
    
    matrix = model.generate_matrix_model()
    for i in matrix:
        print i
    
    