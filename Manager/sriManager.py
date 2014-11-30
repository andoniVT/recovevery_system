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
from Configuration.settings import documents , name_simple_corpus , name_processed_corpus , matrix_model , document_titles , vocabulary , query_dictionary
from Preprocesser.preprocessDocument import PreProcessor as PP
from VectorModel.vectorSpaceModel import VectorSpaceModel as VM
import cPickle
from Genetic.genetic_manager import Genetic
import codecs
from random import randint
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
        elif type==4:
            file = vocabulary
        elif type==5:
            file = query_dictionary
        
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
        
    def get_terms_and_frequency(self):
        documents = self.load_document_information(1)
        documents_pro = []
        for i in documents:
            pre = PP(i , True)
            word = pre.get_processed_document()
            word = self.removeNonAscii(word)
            documents_pro.append(word)
        
        dictionary = self.get_keywords(documents_pro)
        with open(vocabulary , 'wb') as fid:
            cPickle.dump(dictionary, fid)
        
        for i in dictionary:
            print i
    
    def remove_duplicate(self , matrix):
        return [list(t) for t in set(tuple(element) for element in matrix)]
    
    def genetic_process(self ,size_population=2000 , size_groups=6):
        terms_and_frequency = self.load_document_information(4)
        sumatoria = 0.0
        for i in terms_and_frequency:
            sumatoria = sumatoria + i[1]        
        N = len(terms_and_frequency)
        media = sumatoria/N
                
        high_frequency = []
        low_frequency = []
        for i in terms_and_frequency:
            if i[1]>= media:
                high_frequency.append(i)
            else:
                low_frequency.append(i)        
        print "high frequency"
        print len(high_frequency)        
        print "low frequency"
        print len(low_frequency)        
        population = []
                
        for i in range(size_population):
            gen = []
            for j in range(size_groups):
                index = randint(0,len(high_frequency)-1)
                gen.append(high_frequency[index])            
            population.append(gen)
                    
        ''' First evaluation'''
        genetic = Genetic(population, 15, 0.8 , 2)
        genetic.execute()        
        new_population = genetic.get_population()        
        #for i in new_population:print i                        
        mat = self.remove_duplicate(new_population)        
        #for i in mat:print i
        print "reducidos1: " + str(len(mat))
        
        '''Second evaluation'''
        genetic2 = Genetic(population,10,0.7,1)
        genetic2.execute()
        new_population2 = genetic2.get_population()
        #for i in new_population2:print i
        mat2 = self.remove_duplicate(new_population2)
        #for i in mat2:print i
        print "reducidos2: " + str(len(mat2))
        
        '''Third evaluation'''
        genetic3 = Genetic(population,18,0.8,1)
        genetic3.execute()
        new_population3 = genetic3.get_population()
        #for i in new_population2:print i
        mat3 = self.remove_duplicate(new_population3)
        #for i in mat3:print i
        print "reducidos3: " + str(len(mat3))
                
        ''' Final results'''
        result = mat + mat2 + mat3
        result = self.remove_duplicate(result)
        for i in result:print i
        print "result: " + str(len(result))
        
        with open(query_dictionary , 'wb') as fid:
            cPickle.dump(result, fid)
        
    def search_query(self, dictionary, keyword):
        for i in range(len(dictionary)):
            for j in range(6):
                if dictionary[i][j][0] == keyword:
                    return dictionary[i]
                         
    def search_optimized_query(self, keywords):
        qDictionary = self.load_document_information(5)    
        vec_keywords = keywords.split(' ')        
        querys = []
        optimized = vec_keywords    
        for i in vec_keywords:
            query = self.search_query(qDictionary, i)
            if query is not None:
                querys = querys + query        
        if len(querys)==0:
            return keywords                
        querys = list(set(querys))
        querys =  sorted(querys , key=lambda tup:tup[1], reverse=True)        
        new_querys = []
        for i in querys:
            if i[0] not in vec_keywords:
                new_querys.append(i)                
        faltan = 8 - len(vec_keywords)        
        if faltan>len(new_querys):
            for i in range(len(new_querys)):
                optimized.append(new_querys[i][0])
        else:
            for i in range(faltan):
                optimized.append(new_querys[i][0])
        return " ".join(optimized)        
                
    def make_query(self, query, relevants=20 , use_optimized_query=True):
        proccesed = PP(query)
        comment = proccesed.get_processed_document()
        print comment
        if use_optimized_query:
            comment = self.search_optimized_query(comment)
        print comment        
        titles = self.load_document_information(0)
        matrix = self.load_document_information(3)
        vector_model = VM()
        vector_model.set_data(matrix[0], matrix[1], matrix[2])
        comment_tfidf = vector_model.get_tf_idf_vector(comment)
        print comment_tfidf
        similitudes = vector_model.get_distances(comment_tfidf)
        most_relevants = []
        for i in range(relevants):
            most_relevants.append(similitudes[i])
        
        indexes = []
        for i in most_relevants:
            indexes.append(i[0])
        
        print indexes 
        for i in range(len(indexes)):
            print titles[indexes[i]][1] 
        
        
if __name__ == '__main__':
    
    manager = SRI_Manager()
    
    '''
    manager.make_query("algoritmo genetico")
    '''
    
    
    
    
    
    
    
    
    
   