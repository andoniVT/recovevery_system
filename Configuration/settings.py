'''
Created on 09/11/2014

@author: andoni
'''

''' path  '''
path_cicc = '/home/ucsp/workspace/recovevery_system'
path_home = '/home/andoni/Escritorio/PythonProjets/InfRecoverySistem'
#path = path_cicc
path = path_home


''' resource '''
stop_words = path + '/Resource/stopwords_spanish.txt'
verbs = path + '/Resource/verbs.txt'


#souce_dir = "prueba/*.txt"
documents = path + '/Documents/*.txt'


''' corpus names '''
document_titles = 'document_titles.pk1'
name_simple_corpus = 'corpus.pk1' 
name_processed_corpus = 'preprocessed_corpus.pk1'
matrix_model = 'matrix_model.pk1' 
vocabulary = 'vocabulary.pk1'

