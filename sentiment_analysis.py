import csv
import pandas as pd
from collections import Counter, defaultdict
from nltk import sent_tokenize,word_tokenize,porter
from nltk import PorterStemmer
from nltk.corpus import stopwords
import numpy as np
#import scipy as sp
#import scipy.stats
from itertools import chain
import operator
import re
import time
#from sklearn.feature_extraction.text import CountVectorizer
#from gensim.models import ldamodel;
#from gensim import matutils;
review = pd.read_csv('test.csv',encoding = 'ISO-8859-1')
#review_new = open('out.csv','w',encoding = 'ISO-8859-1')
#writer = csv.writer(review_new)
print(review.columns.values)

pndict = dict()


# ALl positive and negative reviews
positive=[]
negative=[]
flag = ['Overall_review']

#keys_to_ignore = ['Entry','Source','Defined']
with open('general_inquirer_dict.txt') as fin:
    reader = csv.DictReader(fin,delimiter='\t')
    for i,line in enumerate(reader):
        if line['Negativ']=='Negativ':
            if line['Entry'].find('#')==-1:
                negative.append(line['Entry'].lower())
            if line['Entry'].find('#')!=-1: #In General Inquirer, some words have multiple senses. Combine all tags for all senses.
                negative.append(line['Entry'].lower()[:line['Entry'].index('#')]) 
        if line['Positiv']=='Positiv':
            if line['Entry'].find('#')==-1:
                positive.append(line['Entry'].lower())
            if line['Entry'].find('#')!=-1: #In General Inquirer, some words have multiple senses. Combine all tags for all senses.
                positive.append(line['Entry'].lower()[:line['Entry'].index('#')])

pvocabulary=sorted(list(set(positive))) #In General Inquirer, some words have multiple senses. Combine all tags for all senses.
nvocabulary=sorted(list(set(negative))) #In General Inquirer, some words have multiple senses. Combine all tags for all senses.
print('done')

#Count positive and negative word frequency in all Chinese restaurant reviews in 2014
def positivenegative():
    pndict['Positive']=Counter()
    pndict['Negative']=Counter()
    negativesum=0
    positivesum=0
    for pword in pvocabulary:
        for ptext in vocabulary:
            if pword==ptext:
                pndict['Positive'][pword]=vocabulary[pword]
                positive500 = sorted( pndict['Positive'].items(), key=operator.itemgetter(1), reverse=True)[0:]

                lengthp = len(positive500)
                #print("lengthpostive",lengthp)
                print("Positive",positive500)
                for i in range(0,lengthp):
                    positivesum += positive500[i][1]

    for nword in nvocabulary:
        for ntext in vocabulary:
            if nword==ntext:
                pndict['Negative'][nword]=vocabulary[nword]
                negative500 = sorted( pndict['Negative'].items(), key=operator.itemgetter(1), reverse=True)[0:]
                lengthn = len(negative500)
                #print("lengthnegative",lengthn)
                print("Negative",negative500)
                for i in range(0,lengthn):
                    negativesum += negative500[i][1]
    if(positivesum > negativesum):
        flag.append("P")
       # print("Positive-negative words ratio =", 1.0*positivesum)
    elif(positivesum < negativesum):
        flag.append("N")
        #print("Positive-negative words ratio =", 1.0*positivesum/negativesum)
    else:
        flag.append("NA")
    print(type(flag))   
   
        
    


# Word frequency calculation function
def getWordCounts(texts,word_proc = lambda x : x): # lambda function
    word_counts = Counter()
    for text in texts:
        bytetext = str.encode(str(text))
        for sent in sent_tokenize(bytetext.decode('ISO-8859-1')):
            for word in word_tokenize(sent):
                word_counts[word_proc(word)] += 1
    return word_counts

reviewtext = []
i = 0
for text in review['text']:
    i += 1
    print("line number  and text is :",i,text)
    reviewtext.append(text)
    
    vocabulary=getWordCounts(reviewtext,lambda x: x.lower())
    print("get word count is ",vocabulary)
    positivenegative()
    print()
    print('<------------------------Next Line----------------------------->')
    reviewtext = []

with open('business_review.csv','r') as csvinput:
        
        with open('withreview.csv','w') as csvoutput:
            writer = csv.writer(csvoutput)
            j = 0
            print("flag",flag)
            #writer = csv.DictWriter(csvoutput, fieldnames = ['user_id','review_id','stars','date','text','type','business_id','overall_review'])
            #writer.writeheader()
            for row in csv.reader(csvinput):
                temp = flag[j]
                writer.writerow(row+[temp])
                j = j + 1 



    
