#coding=UTF-8
import numpy as np
import lda
import stop
import json
import random
from tmp import *

#person = 'TsaiIngWen'
person = 'LLChu'
dataType = 'post'
dataFileName = './%s/%s_%sData.txt' % (person,person,dataType)
dataSegFileName = './%s/%s_%sData_seg.txt' % (person,person,dataType)
vocabFileName = './%s/%s_%sData_term_unigram.txt' % (person,person,dataType)
cleanFileName = './%s/%s_%sData_clean.txt' % (person,person,dataType)
logFileName = './%s/%s_LDA2_log.txt' % (person,person)
writeJson = False
loadJson = False

### GLOBAL VARIABLE ###
termFreqLowBound = 2
LDA_iter = 500
### EXP result: 
#post:            500
#comment: 
#commentComment:
model = 0
topic_num = 6
topic_num_end = 35
topicPosts = []
id_list = []
vocab = []
idToTitle_dict = []
word_dict = {}
docTermMatrix = []

### FUNCTION FOR LDA ###
def reset_word_dict(word_dict):
    for key in word_dict:
        word_dict[key] = 0

#def STD(num,data):
#    x = np.array(data)
#    return (np.mean(x),np.std(x))

def LDA_INIT():
    global vocab,word_dict
    global model
    global id_list
    global topic_num
    global vocab
    global idToTitle_dict
    global word_dict
    global docTermMatrix
       
    ### Construct Vocabulary List
    vocab = []
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
    
    vocab = word_dict.keys()
    #############################
    ### Construct Title List
    w = open(cleanFileName,'r')
    while True:
        line = w.readline()
        if  line == '':
            break
        
        try:
            idToTitle_dict.append(line)
        except:
            continue
    w.close()
    #############################
    ### Construct Doc-Term Matrix
    f = open(dataSegFileName,'r')
    count = 0
    
    while not loadJson:
        line = f.readline()
        count += 1
        print count
        if  line == '':
            break
        
        ID = line.split()[0]
        id_list.append(ID)
        line = line.split()[1:]  
        reset_word_dict(word_dict)
        for term in line:
            termAttribute = term.split('/')[-1]
            if  stop.stop3(termAttribute):
                continue
            
            try:
                #print term
                term = term.split('/')[0]
                if  word_dict.has_key(term):
                    word_dict[term] += 1
                #else:
                    #print 'ERROR: word_dict does not have term'
            except:
                print 'ERROR: term error'
                print term
        
        vec = word_dict.values()
        docTermMatrix.append(vec)
    
    f.close()
    if  loadJson:
        jsonFileName = './%s/%s_LDA_Doc_Term_Matrix_%s.json' % (person,person,dataType)
        docTermMatrix = json.load(open(jsonFileName,'r'))
    
    if  writeJson:
        jsonFileName = './%s/%s_LDA_Doc_Term_Matrix_%s.json' % (person,person,dataType)
        json.dump(docTermMatrix, open(jsonFileName,'w'))
    #############################
    print 'LDA_INIT DONE!!!'

def LDA_MODEL():
    global docTermMatrix,model
    X = np.array(docTermMatrix)
    
    print(X.shape)
    model = lda.LDA(n_topics=topic_num, n_iter=LDA_iter, random_state=1)
    model.fit(X)

LDA_INIT()

### MAIN ###
logFd = open(logFileName,'a')
while topic_num < topic_num_end + 1:
    global model
    LDA_MODEL()

    ### TOPIC POST MATRIX ###    
    doc_topic = model.doc_topic_
    topicPosts = []
    topicPostsList = []
    #topicPostsDT = []
    for i in range(topic_num):
        topicPosts.append([])
        topicPostsList.append([])
        #topicPostsDT.append([])
    
    for i in range(len(doc_topic)):
        topicPosts[doc_topic[i].argmax()].append(i)
        topicPostsList[doc_topic[i].argmax()].append(idToTitle_dict[i])
        #topicPostsDT[doc_topic[i].argmax()].append(docTermMatrix[i])
    
    ### LDA_LOG & EVALUATION ###
    topic_word = model.topic_word_
    n_top_words = 10
    evalGrades = 0.0
    evalGrades_avg = 0.0
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {0}: {1}'.format(i, ' '.join(topic_words)))
        print len(topicPostsList[i])
        clusterGrades = clusterCosSim(topicPostsList[i])
        evalGrades += clusterGrades
        #evalGrades_avg += clusterGrades/len(topicPostsList[i])
        #print clusterGrades
        #logFd.write('Topic {0}: {1}\n'.format(i, ' '.join(topic_words)))
        #for postOrder in topicPosts[i]:
            #print postOrder
            #logFd.write(idToTitle_dict[postOrder])
    
    diffTopicPosts = []
    for topicCluster in topicPostsList:
        diffTopicPosts.append(topicCluster[random.randint(0,len(topicCluster)-1)])
    evalGrades -= clusterCosSim(diffTopicPosts)
    
    evalGrades /= topic_num
    #evalGrades_avg /= topic_num
    print 'Grades:%f, %f(avg)' % (evalGrades, evalGrades_avg)
    logFd.write('%d %f, %f(avg)\n' % (topic_num, evalGrades, evalGrades_avg))
    #for i in range(topic_num):
        #print len(topicPosts[i])
        #logFd.write(str(len(topicPosts[i])) + '\n')
    
    #logFd.write('\n')
    
    topic_num += 1
    
logFd.close()