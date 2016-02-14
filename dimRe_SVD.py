#coding=UTF-8
from sklearn.decomposition import TruncatedSVD
import json

termFreqLowBound = 2

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
    w.close()

def initDocTermMatrix(docTermMatrix,cleanFileName,vocabFileName):
    word_dict = {}
    initWordDict(word_dict,vocabFileName)
    
    f = open(cleanFileName,'r')
    count = 0    
    
    while True:
        line = f.readline()
        if  line == '':
            break
        count += 1
        print count
            
        #ID = line.split()[0]
        line = line.split()[1:]  
        resetWordDict(word_dict)
        for term in line:
            if  word_dict.has_key(term):
                word_dict[term] += 1
        
        docTermMatrix.append(word_dict.values())
        
    f.close()

#person = 'TsaiIngWen'
person = 'LLChu'
dataType = 'post'
cleanFileName = './%s/%s_%sData_clean.txt' % (person,person,dataType)
vocabFileName = './%s/%s_%sData_term_unigram.txt' % (person,person,dataType)
dimReFileName = './%s/%s_%sData_dimRe.txt' % (person,person,dataType)

X = []
initDocTermMatrix(X,cleanFileName,vocabFileName)

svd = TruncatedSVD(n_components=50, random_state=42)
print 'SVD Start'
X_new = svd.fit_transform(X) 
print(svd.explained_variance_ratio_) 
print(svd.explained_variance_ratio_.sum())
    
json.dump(X_new.tolist(),open(dimReFileName,'w'))
print 'LLChu Done'