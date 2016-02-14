#coding=UTF-8
import json
#import word2vec
import sys
reload(sys)

#person = 'TsaiIngWen'
person = 'LLChu'
dataType = 'post'
dimReFileName = './%s/%s_%sData_dimRe.txt' % (person,person,dataType)
vocabFileName = './%s/%s_%sData_term_unigram.txt' % (person,person,dataType)

count = 0
wordsSelected = {}
f = open(vocabFileName,'r')
while True:
    line = f.readline()
    if  len(wordsSelected) is 100:
        break
    line = line.split()
    wordsSelected[line[0]] = True  
f.close()
model = json.load(open(dimReFileName,'r'))
arffFileName = './%s/%s_%sData_D3.arff' % (person,person,dataType)
l = open(arffFileName,'w')

l.write('@relation DBSCAN\n')
l.write('\n')
l.write('@attribute x real\n')
l.write('@attribute y real\n')
l.write('\n')
l.write('@data\n')
'''
for word in wordsSelected:
    l.write(str(model[word.decode('utf8')][0]) +','+ str(model[word.decode('utf8')][1]) + '\n')
'''
count = 0
for term in model:
    l.write(str(term[0]) +','+ str(term[1]) + '\n')
    
l.close()
