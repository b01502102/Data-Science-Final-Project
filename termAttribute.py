#coding=UTF8
import stop

vocab = {}
person = 'TsaiIngWen'

def comp(x,y):
    return vocab[y] - vocab[x]

def addVocab(term):
    if  not vocab.has_key(term):
        vocab[term] = 0

fileName = './%s/%s_postData_seg.txt' % (person,person)
logFileName = './%s/%s_log1.txt' % (person,person)
f = open(fileName,'r')
l = open(logFileName,'w')
termAttribute = {}

while True:
    line = f.readline()
    if  line == '':
        break
    line = line.split('\t')
    
    sentence = line[1].split()
    for i in range(len(sentence)):
        bigram = ''
        if  True:
            word = sentence[i].split('/')[0]
            attribute = sentence[i].split('/')[-1]
            if  termAttribute.has_key(attribute):
                termAttribute[attribute][word] = True
            else:
                termAttribute[attribute] = {}
                termAttribute[attribute][word] = True
        else:
            word = sentence[i].split('/')[0]
            attribute = sentence[i].split('/')[1]
            bigram = word + sentence[i+1].split('/')[0]
            addVocab(word)
            addVocab(bigram)
            vocab[word] += 1
            vocab[bigram] += 1
            if  termAttribute.has_key(attribute):
                termAttribute[attribute][word] = True
            else:
                termAttribute[attribute] = {}
                termAttribute[attribute][word] = True
f.close()


for att in termAttribute:
    print att
    l.write(att + '\n')
    for term in termAttribute[att]:
        l.write(term + ' ')
    l.write('\n')
l.close()
quit()