#coding=UTF-8
import numpy as np
from sklearn.manifold import TSNE
import json


person = 'LLChu'
#person = 'LLChu'
dataType = 'post'
oldFileName = './%s/%s_%sData_dimRe.txt' % (person,person,dataType)
dimReFileName = './%s/%s_%sData_dimRe.txt' % (person,person,dataType)

vectorOld = json.load(open(oldFileName,'r'))

termVectors = []
for term in vectorOld:
    #print term
    termVectors.append(term)

X = np.array(termVectors)
model = TSNE(n_components=2, random_state=0)
np.set_printoptions(suppress=True)
print 'TSNE start'
X_new = model.fit_transform(X)
X_new = X_new.tolist()

vectorNew = []
i = 0
for term in vectorOld:
    vectorNew.append(X_new[i])
    i += 1
    
json.dump(vectorNew,open(dimReFileName,'w'))

print 'LLChu Done'
'''
#######################################################
person = 'TsaiIngWen'
#person = 'LLChu'
dataType = 'post'
oldFileName = './%s/%s_%sData_dimRe.txt' % (person,person,dataType)
dimReFileName = './%s/%s_%sData_dimRe.txt' % (person,person,dataType)

vectorOld = json.load(open(oldFileName,'r'))

termVectors = []
for term in vectorOld:
    #print term
    termVectors.append(term)

X = np.array(termVectors)
model = TSNE(n_components=2, random_state=0)
np.set_printoptions(suppress=True)
print 'TSNE start'
X_new = model.fit_transform(X)
X_new = X_new.tolist()

vectorNew = []
i = 0
for term in vectorOld:
    vectorNew.append(X_new[i])
    i += 1
    
json.dump(vectorNew,open(dimReFileName,'w'))

print 'TsaiIngWen Done'
'''