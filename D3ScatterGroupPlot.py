#coding=UTF-8
import json
#import word2vec
import sys
reload(sys)

#person = 'TsaiIngWen'
person = 'LLChu'
dataType = 'post'

dimReFileName = './%s/%s_%sData_dimRe.txt' % (person,person,dataType)
clusterFileName = './%s/%s_%sData_cluster.txt' % (person,person,dataType)

similarFileName = './%s/%s_%sData_similar.txt' % (person,person,dataType)
D3FileName = './%s/%s_%sData_D3Group.html' % (person,person,dataType)
vocabFileName = './%s/%s_%sData_term_unigram.txt' % (person,person,dataType)
tfIdfFileName = './%s/%s_%sData_tfIdf.txt' % (person,person,dataType)


name = []


cluster = []
f = open(clusterFileName,'r')
while True:
    line = f.readline()
    if  line == '':
        break
    if  not '-->' in line:
        continue
    line = line.split()
    cluster.append(line[-1])
f.close()


similar = {}
size = {}
f = open(similarFileName,'r')
while True:
    line = f.readline()
    if  line == '':
        break
    line = line.split()
    similar[line[0]] = line[1]
    #print line[0],similar[line[0]]
f.close()

wordsSelected = {}
f = open(vocabFileName,'r')
while True:
    line = f.readline()
    if  len(wordsSelected) is 100:
        break
    line = line.split()
    wordsSelected[line[0]] = True  
    size[line[0]] = int(line[1])  
f.close()

model = json.load(open(dimReFileName,'r'))

l = open(D3FileName,'w')


l.write('<!doctype html>\n')
l.write('<meta charset="utf-8">\n')
l.write('<script src="http://www.d3plus.org/js/d3.js"></script>\n')
l.write('<script src="http://www.d3plus.org/js/d3plus.js"></script>\n')
l.write('<div id="viz"></div>\n')
l.write('<script>\n')
l.write('  var sample_data = [\n')
'''
count = 0
for words in wordsSelected:
    term = model[words.decode('utf-8')]
    l.write('    {"x": %f, "y": %f, "name": "%s", "size": %d, "group":"group %s"}'% (term[0],term[1],words,size[words],cluster[count]))
    
    if  count < len(wordsSelected)-1:
        l.write(',\n')
    else:
        l.write('\n')
    count += 1
'''
count = 0
for term in model:
    l.write('    {"x": %f, "y": %f, "name": "%s", "size": %d, "group":"group %s"}'% (term[0],term[1],str(count),10,cluster[count]))
    if  count < len(model)-1:
        l.write(',\n')
    else:
        l.write('\n')
    count += 1

l.write('  ]\n')
l.write('  var visualization = d3plus.viz()\n')
l.write('    .container("#viz")\n')  
l.write('    .data(sample_data)\n')  
l.write('    .type("scatter")\n')    
l.write('    .id(["group","name"])\n')         
l.write('    .x("x")\n')         
l.write('    .y("y")\n')
l.write('    .size("size")\n')
l.write('    .shape({\n')
l.write('      "rendering":"optimizeSpeed" // fine-tune SVG shape rendering\n')
l.write('    })\n')
l.write('    .draw()\n')             
l.write('</script>\n')

l.close()

import os
htmlFileName = 'C:\Users\LENOVO\workspace\DataScience_Final\src\%s\%s_%sData_D3Group.html'% (person,person,dataType)
os.system(htmlFileName)
