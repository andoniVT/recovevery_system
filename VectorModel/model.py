'''
Created on 09/11/2014

@author: andoni
'''

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
        print vocabulary
        matrix = []
        for i in self.__documents:
            vector = []
            words = i.split(' ')
            for j in vocabulary:
                if self.find_word(j, words):
                    vector.append(1)
                else:
                    vector.append(0)
            matrix.append(vector)
        return matrix
                
                    
                                 
if __name__ == '__main__':
    
    docs = ['hola como estas' ,'yo estoy bien' ,'hola me llamo Andoni' ,'bien yo me llamo Jorge' ,'esto es perfecto' ,'estas te encuentas ahi' ]
    
    model = BooleanModel(docs)
    
    matrix = model.generate_matrix_model()
    for i in matrix:
        print i
    
    