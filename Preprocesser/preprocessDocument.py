#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on 09/11/2014

@author: andoni
'''
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

import re
import unicodedata
from unicodedata import normalize
import snowballstemmer
import string
from Configuration.settings import stop_words , verbs 
stopWordFile = stop_words

class PreProcessor(object):
    
    def __init__(self , comment , flag=False):
        self.__comment = comment
        self.__remove_verbs = flag
        self.__new_comment = self.process_comment(self.__comment)        
    
    def remove_accent(self , word):
        word= word.replace("á", "a")
        word= word.replace("é", "e")
        word= word.replace("í", "i") 
        word= word.replace("ó", "o")
        word= word.replace("ú", "u")
        word= word.replace("ä", "a")
        word= word.replace("ë", "e")
        word= word.replace("ï", "i")
        word= word.replace("ö", "o")
        word= word.replace("ü", "u")
        word= word.replace("Á", "a")
        word= word.replace("É", "e")
        word= word.replace("Í", "i") 
        word= word.replace("Ó", "o")
        word= word.replace("Ú", "u")
        return word 
    
    def find_symbol(self, word):
        alphabet = "abcdefghijklmnñopqrstuvwxyz"
        pos = 0
        flag = 0
        for i in word:
            if alphabet.find(i) != -1:
                pos = pos + 1
            else:
                flag = 1
                break
        return [flag , pos]
    
    def split_symbols(self,lista):
        new = []
        for i in lista:
            val = self.find_symbol(i)
            if val[0] == 0:
                new.append(i)
            else:
                pos = val[1]
                if pos == 0:
                    new.append(i)
                else:
                    param = len(i)-pos
                    uno = i[:pos]
                    dos = i[-param:]
                    new.append(uno)
                    new.append(dos)
        return new
    
    def lemmatizer(self ,word):
        stemmer = snowballstemmer.stemmer('spanish');
        return stemmer.stemWord(word)

    def lemmatized_comment(self , comment):
        lista = comment.split()
        lista = self.split_symbols(lista)
        lematizado = ""
        for i in lista:
            i = self.lemmatizer(i)
            lematizado = lematizado + i + " "
        lematizado = lematizado[:-1]
        return lematizado

    def lemmatized_words(self, comentario):
        lista = comentario.split()
        lematizado = ""
        for i in lista:
            i = self.lemmatizer(i)
            lematizado = lematizado + i + " "
        lematizado = lematizado[:-1]    
        return lematizado
    
    def remove_stop_word(self, comentario):    
        arch = open(stopWordFile , 'r')
        stops = []
        for line in arch:
            word = line.strip()
            stops.append(word)
        text_list = []
        words = re.split("\s+",comentario)        
        for word in words:
            if len(word)>1 and (not word in stops):
                text_list.append(word)
        return " ".join(text_list)
    
    def remove_verbs(self , comentario):
        arch = open(verbs , 'r')
        stops = []
        for line in arch:
            word = line.strip()
            word = self.lemmatized_comment(word)            
            stops.append(word)
        text_list = []
        words = re.split("\s+", comentario)
        for word in words:
            if len(word)>1 and (not word in stops):
                text_list.append(word)
        return " ".join(text_list)
    
    def process_comment(self , comentario):
        comentario = self.remove_accent(comentario)
        comentario = comentario.lower()
        comentario = re.sub('@[^\s]+','',comentario) 
        comentario = re.sub('[\s]+', ' ', comentario)
        comentario = comentario.strip('\'"')
        signos = ['$' , '1' , '2' , '3' , '4' , '5' , '6' , '7' ,'8', '9' , '0' , '¿' , '¡' , ',']
        for c in signos:
            comentario = comentario.replace(c , "")
        predicate = lambda x:x not in string.punctuation
        comentario  = filter(predicate, comentario)
        pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
        comentario = self.remove_stop_word(comentario)
        comentario = self.lemmatized_comment(comentario)
        if self.__remove_verbs:
            comentario = self.remove_verbs(comentario)        
        return comentario 
    
    def get_processed_document(self):
        return self.__new_comment
            
if __name__ == '__main__':
    

    
    asking = "te voy a cuidar pronto"
    asking2 = "te voy a cuido pronto"
    asking3 = "te voy a cuidare pronto"
    asking4 = "te voy a cuida pronto"
    procesor = PreProcessor(asking)
    procesor2 = PreProcessor(asking2)
    procesor3 = PreProcessor(asking3)
    procesor4 = PreProcessor(asking4)
    print procesor.get_processed_document()
    print procesor2.get_processed_document()
    print procesor3.get_processed_document()
    print procesor4.get_processed_document()
     
    
    
