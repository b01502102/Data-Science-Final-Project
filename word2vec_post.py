#coding=UTF-8
import word2vec
import stop

person = 'TsaiIngWen'
#person = 'LLChu'
dataType = 'comment'
dataSegFileName = './%s/%s_%sData_seg.txt' % (person,person,dataType)
fileName = './%s/%s_%sData_vector.bin' % (person,person,dataType)
cleanFileName = './%s/%s_%sData_clean.txt' % (person,person,dataType)

f = open(dataSegFileName,'r')
l = open(cleanFileName,'a')
count = 0
while True:
    line = f.readline()
    count += 1
    if  line == '':
        break
    if  count <= 194833:
        continue
    line = line.split()[1:]
    for term in line:
        try:
            if  stop.stop3(term.split('/')[1]):
                continue
        except:
            print count
            print 'ERROR'
            print term
            #quit()
        term = term.split('/')[0]
        l.write(term + ' ')
    l.write('\n')
f.close()
l.close()

quit()
word2vec.doc2vec(cleanFileName, fileName, cbow=0, size=50, window=10, negative=5, hs=0, sample='1e-4', threads=12, iter_=20, min_count=1, verbose=True)
word2vec.word2phrase(cleanFileName, fileName, verbose=True)
word2vec.word2clusters(cleanFileName, fileName, 100, verbose=True)

model = word2vec.load(fileName)
print model.vectors.shape

quit()
indexes, metrics = model.cosine('_*1')
model.generate_response(indexes, metrics).tolist()

'''
找出重要詞彙的相似字 把它存起來，vectorSim.json
'''