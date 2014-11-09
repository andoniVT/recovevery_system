'''
Created on 09/11/2014

@author: andoni
'''

import cPickle

vec = [0 , 1, 1 , 1 , 0 , 0]
vec2 = [1 , 1, 0 , 1 , 1 , 0]
vec3 = [0 , 0, 0 , 1 , 1 , 0]

matrix = [vec , vec2 , vec3]

with open("file.pk1" , 'wb') as fid:
    cPickle.dump(matrix , fid)

with open("file.pk1" , 'rb') as fid:
    copia = cPickle.load(fid)
    

for i in copia:
    print i 
