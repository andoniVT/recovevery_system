'''
Created on 09/11/2014

@author: andoni
'''

import glob
from Configuration.settings import documents

#souce_dir = "prueba/*.txt"



class SRI_Manager(object):
    
    def __init__(self):
        pass
    
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
        return corpus
                                
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
    corpus = manager.load_corpus()
    for i in corpus:
        print i
    
    print len(corpus)