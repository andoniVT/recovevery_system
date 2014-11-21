'''
Created on 21/11/2014

@author: andoni
'''

import sys
from gensim import corpora, models, similarities
from scipy import spatial


if __name__ == '__main__':
    
    docs = [['hola' , 'como' , 'estas'],
            ['yo', 'estoy',  'bien'] , 
            ['hola', 'me' , 'llamo' , 'Andoni'] ,
            ['bien' , 'yo' , 'me' , 'llamo' , 'Jorge'] ,
            ['esto', 'es' , 'perfecto'] ,
            ['estas' , 'te' , 'encuentas' , 'ahi']]
        
    dictionary = corpora.Dictionary(docs)
    id_words = dictionary.token2id
    
        
    corpus = [dictionary.doc2bow(text) for text in docs]    
    
        
    tfidf = models.TfidfModel(corpus)
    corpus_tf_idf = tfidf[corpus]
    
    
    comment = 'estoy muy bien Jorge Andoni Valverde'
    vec_bow = dictionary.doc2bow(comment.lower().split())
    vec_tf = tfidf[vec_bow]
    print vec_tf
    
    index = similarities.MatrixSimilarity(tfidf[corpus])
    sims = index[vec_tf]
    print sorted(enumerate(sims), key=lambda item: -item[1])
        