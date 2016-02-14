import math

#person = 'TsaiIngWen'
person = 'LLChu'
dataType = 'post'
dimReFileName = './%s/%s_%sData_dimRe.txt' % (person,person,dataType)

similarFileName = './%s/%s_%sData_similar.txt' % (person,person,dataType)
cleanFileName = './%s/%s_%sData_clean.txt' % (person,person,dataType)
D3FileName = './%s/%s_%sData_D3Scatter.html' % (person,person,dataType)
dfFileName = './%s/%s_%sData_term_unigram.txt' % (person,person,dataType)
tfIdfFileName = './%s/%s_%sData_tfIdf.txt' % (person,person,dataType)

avg_doc_length = 0.0
n_TopKeywords = 5

b = 0.75

df = {}
tmp = {}

f = open(dfFileName,'r')
while True:
    line = f.readline()
    if  line == '':
        break
    line = line.split()
    df[line[0]] = 0
f.close()

def comp(x,y):
    global tmp
    if  tmp[y] > tmp[x]:
        return 1
    else:
        return -1

def IDF(df,doc_num):
    return df/doc_num
    return math.log10( (doc_num - df + 0.5)/(df + 0.5) )

def Okapi_tf(tf,doclen):
    return float(tf / (1-b+b*doclen/avg_doc_length))

def Okapi(df,doc_num,tf,doclen):
    return tf
    return IDF(df,doc_num) * Okapi_tf(tf,doclen)

def docLen(vec):
    total = 0.0
    for num in vec:
        total += num*num
    return math.sqrt(total)

def aggregateKeywords(keywordsList):
    wordsDict = {}
    allCount = 0
    for keywords in keywordsList:
        for term in keywords:
            allCount += 1
            if  wordsDict.has_key(term):
                wordsDict[term] += 1
            else:
                wordsDict[term] = 1
    wordsList = wordsDict.keys()
    global tmp
    tmp = wordsDict
    wordsList.sort(comp)
    count = 0
    for i in range(n_TopKeywords):
        count += wordsDict[wordsList[i]]
    #print str(wordsList[:n_TopKeywords]).decode('string_escape')
    #print count,allCount
    #for term in wordsDict:
    #    print term,wordsDict[term]
    countCover = 0.0
    for keywords in keywordsList:
        for term in keywords:
            flag = False
            for i in range(n_TopKeywords):
                topKeywords = wordsList[i] 
                if  topKeywords in term or term in topKeywords:
                    countCover += 1
                    flag = True
                    break
            if  flag:
                break

    #print 'Cover Rate: %d,%d' %(countCover,len(keywordsList))
    return countCover

def clusterTfidf(rawData):
    global avg_doc_length, n_TopKeywords
    
    post = []
    for line in rawData:
        line = line.split()
        tmp_vec = {}
        for term in line:
            if  not df.has_key(term):
                continue
            avg_doc_length += 1
            if  tmp_vec.has_key(term):
                tmp_vec[term] += 1
            else:
                tmp_vec[term] = 1
        
        post.append(tmp_vec)        
        
    avg_doc_length /= len(post)
    tfIdf = []
    
    for i in range(len(post)):
        tmp_dict = {}
        for term in post[i]:
            tmp_dict[term] = Okapi(df[term], len(post), post[i][term], len(post[i].values()))
        tfIdf.append(tmp_dict)

    final_keywords = []        
    for i in range(len(tfIdf)):
        keywords = tfIdf[i].keys()
        #print keywords
        global tmp
        tmp = tfIdf[i]
        if  type(tmp) != dict:
            print 'error'
            quit()
        keywords.sort(comp)
        #print str(keywords[:n_TopKeywords]).decode('string_escape')
        final_keywords.append(keywords[:n_TopKeywords])
    
    return aggregateKeywords(final_keywords)
    
def cosineSim(v1,v2):    
    innerProd = 0.0
    v1Len = 0.0
    v2Len = 0.0
    for term in v1:
        if  v2.has_key(term):
            innerProd += v1[term]*v2[term]
        v1Len += v1[term]*v1[term]
    for term in v2:
        v2Len += v2[term]*v2[term]
    if  v2Len is 0.0 or v1Len is 0.0:
        return 0
    return innerProd/math.sqrt(v1Len*v2Len)

def clusterCosSim(rawData):
    post = []
    for line in rawData:
        line = line.split()
        tmp_vec = {}
        for term in line:
            if  not df.has_key(term):
                continue
            if  tmp_vec.has_key(term):
                tmp_vec[term] += 1
            else:
                tmp_vec[term] = 1
        
        post.append(tmp_vec)
    
    aggr = 0.0
    for i in range(len(post)):
        for j in range(i+1,len(rawData)):
            aggr += cosineSim(post[i], post[j])
    aggr /= len(rawData)*(len(rawData)-1)/2
    return aggr
    
def differenceTfidf(topicDocMatrix):
    i = j = count = 0
    for i in range(len(topicDocMatrix)):
        for j in range(i+1,len(topicDocMatrix)):
            for term1 in topicDocMatrix[i]:
                for term2 in topicDocMatrix[j]:
                    if  term1 is term2:
                        count += 1
    return count