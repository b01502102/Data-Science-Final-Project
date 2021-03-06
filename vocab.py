#coding=UTF8
import stop

vocab = {}
#person = 'TsaiIngWen'
person = 'LLChu'
bigram = False

dataType = 'post'
fileName = './%s/%s_%sData_seg.txt' % (person,person,dataType)
termFileName = ''
if  bigram:
    termFileName = './%s/%s_%sData_term_bigram.txt' % (person,person,dataType)
else:
    termFileName = './%s/%s_%sData_term_unigram.txt' % (person,person,dataType)
    
def comp(x,y):
    return vocab[y] - vocab[x]

def addVocab(term):
    if  not vocab.has_key(term):
        vocab[term] = 0
        return False
    else:
        return True


f = open(fileName,'r')
count = 0
while True:
    line = f.readline()
    count += 1
    if  line == '':
        break
    line = line.split('\t')
    
    try:
        sentence = line[1].split()
    except:
        print count,sentence
        quit()
       
    for i in range(len(sentence)):
        termAttr = sentence[i].split('/')[-1]
        if  stop.stop3(termAttr):
            continue
        bigram = ''
        if  i is len(sentence)-1:
            word = sentence[i].split('/')[0]
            addVocab(word)
            vocab[word] += 1
        else:
            word = sentence[i].split('/')[0]
            
            try:
                if  bigram and i+1 != len(sentence) and not stop.stop3(sentence[i+1].split('/')[1]):
                    bigram = word + sentence[i+1].split('/')[0]
                    addVocab(bigram)
                    vocab[bigram] += 1
            except:
                print count
            
            addVocab(word)
            vocab[word] += 1
            
f.close()

sorted_vocab = vocab.keys()
sorted_vocab.sort(comp)

l = open(termFileName,'w')
for term in sorted_vocab:
    l.write(term+'\t'+str(vocab[term])+'\n')
l.close()
