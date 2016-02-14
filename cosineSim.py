#coding=UTF-8
import json
from math import sqrt

termFreqLowBound = 2
terms = []

def resetWordDict(word_dict):
    for key in word_dict:
        word_dict[key] = 0

def initWordDict(word_dict,vocabFileName):
    w = open(vocabFileName,'r')
    while True:
        line = w.readline()
        if  line == '':
            break
        
        try:
            line.split()[1]
        except:
            continue
        if  int(line.split()[1]) < termFreqLowBound:
            break
        line = line.split()[0]
        word_dict[line] = 0
    global terms
    terms = word_dict.keys()
    w.close()

def initDocTermMatrix(docTermMatrix,cleanFileName,vocabFileName):
    word_dict = {}
    initWordDict(word_dict,vocabFileName)
    
    f = open(cleanFileName,'r')
    
    while True:
        line = f.readline()
        if  line == '':
            break
            
        #ID = line.split()[0]
        line = line.split()[1:]  
        resetWordDict(word_dict)
        for term in line:
            if  word_dict.has_key(term):
                word_dict[term] += 1
        
        docTermMatrix.append(word_dict.values())
        
    f.close()

def calCosineSim(post1,post2):
    if  len(post1) != len(post2):
        print 'ERROR: Differenct length of posts!!!'
        quit()
    aggr = 0.0
    length1 = 0
    length2 = 0
    for i in range(len(post1)): 
        aggr += post1[i]*post2[i]
        length1 += post1[i]*post1[i]
        length2 += post2[i]*post2[i]
    if  length1 is 0 or length2 is 0:
        print 'Zero length post:'
        print post1
        print post2
        return 0
    aggr = sqrt(aggr*aggr/length1/length2)
    return aggr
        

def calCosineMatrix(data):
    cosineMatrix = []
    i = 0
    for i in range(len(data)):
        print i
        cosineMatrix.append([])
        j = 0
        for j in range(len(data)):
            sim = 0.0
            if  j == i:
                sim = 1.0
            elif j < i:
                sim = cosineMatrix[j][i]
            else:
                sim = calCosineSim(data[i], data[j])
            cosineMatrix[i].append(sim)
    return cosineMatrix

#person = 'TsaiIngWen'
person = 'LLChu'
dataType = 'post'
cleanFileName = './%s/%s_%sData_clean.txt' % (person,person,dataType)
vocabFileName = './%s/%s_%sData_term_unigram.txt' % (person,person,dataType)
dimReFileName = './%s/%s_%sData_dimRe.txt' % (person,person,dataType)
cosineSimFileName = './%s/%s_%sData_cosSim.json' % (person,person,dataType)

X = []
initDocTermMatrix(X,cleanFileName,vocabFileName)
cosineSimMatrix = calCosineMatrix(X)
print len(cosineSimMatrix[0])
print len(cosineSimMatrix)
json.dump(cosineSimMatrix,open(cosineSimFileName,'w'))