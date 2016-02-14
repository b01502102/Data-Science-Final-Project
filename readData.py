#coding=UTF-8

import json
import os

'''
print os.listdir('C:/Users/LENOVO/workspace/DataScience_Final/src')
print os.path.exists('C:/Users/LENOVO/workspace/DataScience_Final/src/')
person = 'Tsai'
personDir =  os.path.curdir + '/' + person
di = {}
for term in di:
    print term
print di.has_key('123')
print personDir
'''

'''
files = os.listdir('C:/Users/LENOVO/workspace/DataScience_Final/src/TsaiIngWen/2015/11')
print files
postDataDict = {}
for filePost in files:
    json_filename = 'C:/Users/LENOVO/workspace/DataScience_Final/src/TsaiIngWen/2015/11/' + filePost
    with open(json_filename, 'r') as f:
        postDataDict.update(json.load(f))

    
oldPostDataList = json.load(open('C:/Users/LENOVO/workspace/DataScience_Final/src/postDataList.json','r'))
postDataList = []
for fileTerm in oldPostDataList:
    if  postDataDict.has_key(fileTerm['id']):
        postDataList.append(fileTerm['id'])
with open('C:/Users/LENOVO/workspace/DataScience_Final/src/2015_11_postDataList.json', 'w') as f:
        json.dump(postDataList, f)

with open('C:/Users/LENOVO/workspace/DataScience_Final/src/2015_11_postDataDict.json', 'w') as f:
        json.dump(postDataDict, f)
'''

for i in range(1,13):
    
    '''
    json_filename = filename + '.json'
    with open(json_filename, 'w') as f:
        json.dump(postDataList, f)
    '''
    json_filename = 'C:/Users/LENOVO/workspace/DataScience_Final/src/LLChu/2015/LLChu_2015_%d_postDataList.json' % i
    postDataList = []
    oldPostDataList = []
    with open(json_filename, 'r') as f:
        oldPostDataList = json.load(f)
    for postID in oldPostDataList:
        postDataList.append(postID['id'])
    if  len(postDataList) != len(oldPostDataList):
        print 'error'
        quit()
    with open(json_filename, 'w') as f:
        json.dump(postDataList, f)
    #with open(json_filename, 'r') as f:
    #    postDataList1 = json.load(f)
    continue
    filename = 'C:/Users/LENOVO/workspace/DataScience_Final/src/TsaiIngWen/2014/2014_%d_postDataDict.json' % i
    #postDataDict = pickle.load(open(filename,'r'))
    print filename
    #with open(json_filename, 'w') as f:
    #    json.dump(postDataDict, f)
    with open(json_filename, 'r') as f:
        postDataDict1 = json.load(f)
    f.close()
    del postDataDict1
    print '%d file can be read' % i
    



