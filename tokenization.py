#coding=UTF-8

import ckip

person = 'LLChu'

messageFileName = './%s/%s_postData.txt' % (person,person)
segMessageFileName = './%s/%s_postData_seg.txt' % (person,person)

def ckipToken(string):
    result = ckip.seg(string)
    return result.text()


messageFd = open(messageFileName,'r')
segMessageFd = open(segMessageFileName,'a')

line_count = 0
while True:
    line = messageFd.readline()
    line_count += 1
    if  line == '':
        break
    line = line.split('\t')
    ID = line[0]
    message = line[1].strip('\n\r')
    
    errorWords = []
    cleanMessage = ''
    print message.decode('utf8')
    for c in message.decode('utf8'):
        try:
            x = c.encode('cp950')
            cleanMessage += c
        except:
            #print c
            errorWords.append(c)
    
    try:
        tokenResult = ckipToken(cleanMessage)
    except:
        print 'ERROR: %d lines: %s' % (line_count,cleanMessage)
        continue
    #continue
    segMessageFd.write(ID + '\t' + tokenResult.encode('utf8') + '\n')
    #quit()
