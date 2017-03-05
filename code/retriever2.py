# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 09:56:32 2017

@author: User
"""

'''
Step 1: Select Reviews from DB, Pre-process data
'''

import sqlite3
import random
import nltk 
import re
from nltk.tokenize import word_tokenize

stop_list = nltk.corpus.stopwords.words('english')
stemmer = nltk.stem.porter.PorterStemmer()
    
db_path = 'jiakbot.db'
        
        
conn = sqlite3.connect(db_path)
c = conn.cursor()
        
t = ('kailash-parbat-singapore',)
        
        
c.execute("SELECT review_id, description FROM reviews WHERE biz_id=?",t)
results = c.fetchall()

        
docs1=[]
for i in results:
    doc = word_tokenize(i[1])
    docs1.append(doc)
    print("\n")
    #lowercase only    
    docs2 = [[w.lower() for w in doc] for doc in docs1]
    docs3 = [[w for w in doc if re.search('^[a-z]+$', w)] for doc in docs2]
    docs4 = [[w for w in doc if w not in stop_list] for doc in docs3]
    docs5 = [[stemmer.stem(w) for w in doc] for doc in docs4]
    for j in i:
            print (j)
                        
#print(docs5[0])
#print(docs5[1])

'''
Step 2: Select most similar review based on query
'''

import gensim
from gensim import corpora
reviews = corpora.Dictionary(docs5)
print(reviews)
            
import gensim
from gensim import models
r_vecs = [reviews.doc2bow(doc) for doc in docs5]
r_tfidf = models.TfidfModel(r_vecs)
r_vecs_with_tfidf = [r_tfidf[vec] for vec in r_vecs]
print(r_vecs[1][0:10])

from gensim import similarities
r_index = similarities.SparseMatrixSimilarity(r_vecs_with_tfidf, 96)

print(len(docs5))

query = [stemmer.stem('Food'),stemmer.stem('awful')]
query_vec = reviews.doc2bow(query)
query_vec_tfidf = r_tfidf[query_vec]
q_sims = r_index[query_vec_tfidf]
q_sorted_sims = sorted(enumerate(q_sims), key=lambda item: -item[1])

print("\n")
print("The most similar")
print(q_sorted_sims[0:10])



