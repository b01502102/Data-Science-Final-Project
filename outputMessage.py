#coding=UTF-8
import os
import json


years = [2014,2015]
months = range(1,13)
person = 'LLChu'

postFd = False
commentFd = False
commentCommentFd = False

def openMessageFiles():
    global postFd,commentFd,commentCommentFd
    fileName = './%s/%s_postData.txt' % (person,person)
    postFd = open(fileName,'w')
    fileName = './%s/%s_commentData.txt' % (person,person)
    commentFd = open(fileName,'w')
    fileName = './%s/%s_commentCommentData.txt' % (person,person)
    commentCommentFd = open(fileName,'w')

def closeMessageFiles():
    if  postFd:
        postFd.close()
    if  commentFd:
        commentFd.close()
    if  commentCommentFd:
        commentCommentFd.close()

def writePostToFile(message):
    global postFd
    message = message.encode('utf8')
    if  postFd is not False:
        postFd.write(message)
    else:
        print 'ERROR: postFd is False'
    
def writeCommentToFile(message):
    global commentFd
    message = message.encode('utf8')
    if  commentFd is not False:
        commentFd.write(message)
    else:
        print 'ERROR: commentFd is False'
    
def writeCommentCommentToFile(message):
    global commentCommentFd
    message = message.encode('utf8')
    if  commentCommentFd is not False:
        commentCommentFd.write(message)
    else:
        print 'ERROR: commentCommentFd is False'
    
def cleanEndLineInMessage(message):
    string = ''
    for sentence in message.split('\n'):
        string += sentence.strip('\r\n').replace('\t',u'，') + u'。'
    return string

def outputMessageFromDataDict(dataDict,messageType):
    ID = dataDict.get('id')
    if  ID is None:
        print 'ERROR: %s ID is NONE' % messageType
        quit()
    
    message = dataDict.get('message')
    if  message:
        #print ID + '\t' + cleanEndLineInMessage(message)
        
        message = ID + '\t' + cleanEndLineInMessage(message) + '\n'
        
        if  messageType is 'post':
            writePostToFile(message)
        elif messageType is 'comment':
            writeCommentToFile(message)
        elif messageType is 'commentComment':
            writeCommentCommentToFile(message)
        else:
            print 'ERROR: UNKNOWN messageType'
        
        return True
    else:
        return False
            

post_count = 0
comment_count = 0
commentComment_count = 0
openMessageFiles()
for year in years:
    for month in months:
        print year, month
        postDataListFileName = '%s_%d_%d_postDataList.json' % (person,year,month)
        postDataListFileDic = './%s/%d/' % (person,year)
        if  not os.path.exists(postDataListFileDic):
            print 'ERROR: POST_LIST Does not exist'
            quit()
        postDataListFileAddr = postDataListFileDic + postDataListFileName
        postDataList = json.load(open(postDataListFileAddr,'r'))
        for postID in postDataList:
            postFileName = '%s/%d/%s.json' % (postDataListFileDic,month,postID)
            if  not os.path.exists(postFileName):
                print 'POST Does not exist'
                continue
            
            postDataDict = json.load(open(postFileName,'r'))
            
            if  outputMessageFromDataDict(postDataDict[postID], 'post'):
                post_count += 1
            else:
                print 'WARNING: POST No message'
                print postDataDict[postID].get('message')
            
            for comment in postDataDict[postID]['comments']:
                if  outputMessageFromDataDict(comment, 'comment'):
                    comment_count += 1
                else:
                    print 'WARNING: COMMENT No message'
                    print comment.get('message')
                
                if  comment.has_key('comments'):
                    for commentComment in comment['comments']['data']:
                        if  outputMessageFromDataDict(commentComment, 'commentComment'):
                            commentComment_count += 1
                        else:
                            print 'WARNING: COMMENT_COMMENT No message'
                            print commentComment.get('message')
            #quit()
closeMessageFiles()
print post_count
print comment_count
print commentComment_count
