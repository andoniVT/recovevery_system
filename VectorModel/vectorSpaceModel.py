'''
Created on 21/11/2014

@author: andoni
'''

import sys
from gensim import corpora, models, similarities
from scipy import spatial

class VectorSpaceModel(object):
    
    def __init__(self , documents):
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
        for i in self.__corpus:
            print i            
        self.__tfidf = models.TfidfModel(self.__corpus)
        self.__corpus_tf_idf = self.__tfidf[self.__corpus]
    
    
    def get_frequency_vector(self , queries):
        vector =  []
        for i in queries:
            vec = self.__dictionary.doc2bow(i.split())
            vector.append(vec)
        return vector 
    
    def get_tf_idf_vector(self , queries):
        tf_idf_vector = []
        freq_vector = self.get_frequency_vector(queries)
        for i in freq_vector:
            vec = self.__tfidf[i]
            tf_idf_vector.append(vec)
        return tf_idf_vector
                                
    def get_vocabulary_and_freq(self):
        vocabulary = []
        for i in self.__words_and_id:
            keyword = i
            id = self.__words_and_id[i]
            print keyword
            print id
            print ""
          
    
if __name__ == '__main__':
    
    
    documents = ['hola como estas' , 'yo estoy bien' , 'hola me llamo Andoni' , 
                 'Jorge bien yo me llamo Jorge' , 'esto es perfecto' , 'estas te encuentras ahi']
    
    model = VectorSpaceModel(documents)
    model.prepare_corpus()
    vec = model.get_frequency_vector(['estoy muy bien Jorge Andoni Valverde'])    
    vec = model.get_tf_idf_vector(['estoy muy bien Jorge Andoni Valverde'])
    model.get_vocabulary_and_freq()
    
    
    
    '''
    index = similarities.MatrixSimilarity(tfidf[corpus])
    sims = index[vec_tf]
    print sorted(enumerate(sims), key=lambda item: -item[1])
    ''' 