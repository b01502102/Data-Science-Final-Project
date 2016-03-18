#coding=UTF-8
import requests
import json
import datetime
import time
import random
import os

token = ''

year = 2015
month = 11
intervalMonth = 1
sinceTime = ''
endTime = datetime.datetime(2016,1,1,0,0,0)

directory_addr = 'TsaiIngWen_'
person = 'TsaiIngWen'
personID = '46251501064'
personDir =  os.path.curdir + '/' + person
personYearDir = personDir + '/' + str(year)
personYearMonthDir = personYearDir + '/' + str(month)

limitOriginal = 1000
limitComment = 1000

postDataDict = {}
postDataList = []

def updateDir():
    global personYearDir, personYearMonthDir
    personYearDir = personDir + '/' + str(year)
    personYearMonthDir = personYearDir + '/' + str(month)

def checkAddrExist():
    if  not os.path.exists(personDir):
        os.mkdir(personDir)

    if  not os.path.exists(personYearDir):
        os.mkdir(personYearDir)
    
    if  not os.path.exists(personYearMonthDir):
        os.mkdir(personYearMonthDir)

def checkFileDown():
    fileList = os.listdir(personYearMonthDir)
    fileDict = {}
    for term in fileList:
        fileDict[term] = True
    return fileDict

def writeLog(string):
    filename = directory_addr + sinceTime + '_log'
    f = open(filename,'a')
    f.write(string)
    f.close()
    return

def getSince():
    global year,month,sinceTime
    
    sinceTime = str(year)+'_'+str(month)
    
    dt = datetime.datetime(year,month,1,0,0,0)
    since = int(time.mktime(dt.timetuple()))
    month += 1
    if  month is 13:
        month = 1
        year += 1
    return str(since)

def getUntil():
    global year,month
    dt = datetime.datetime(year,month,1,0,0,0)
    until = int(time.mktime(dt.timetuple()))
    return str(until)

def jsonDump(data,name):
    #filename = directory_addr + sinceTime + '_' + name + '.json'
    if  name is 'postDataList':
        filename = directory_addr + sinceTime + '_' + name + '.json'
    else:
        filename = personYearMonthDir + '/' + name + '.json'
        
    try:
        with open(filename, 'w') as f:
            json.dump(data, f)
    except:
        writeLog('ERROR: jsonDump %s dump fail\n' % filename)

def hasNext(data):
    if  data.has_key('paging'):
        if  data['paging'].has_key('next'):
            return True
        else:
            return False
    else:
        return False
    
def generateUrl(choose,postID):
    if  choose == 'likes':
        return 'https://graph.facebook.com/v2.5/%s/likes?limit=1000&summary=true&fields=id,name&access_token=%s'% (postID,token)
    elif choose == 'comments':
        return 'https://graph.facebook.com/v2.5/%s/comments?limit=%d&summary=true&fields=id,message,comment_count,from,created_time,like_count,comments.limit(1000)&order=chronological&access_token=%s'% (postID,limitComment,token)
    elif choose == 'posts':
        return 'https://graph.facebook.com/v2.5/%s?fields=message,shares,created_time,link,id,type&access_token=%s'% (postID,token)
    elif choose == 'post list':
        since = getSince()
        until = getUntil()
        return 'https://graph.facebook.com/v2.5/%s/posts?access_token=%s&fields=id&until=%s&since=%s&limit=100'% (postID,token,until,since)
    else:
        print 'ERROR: GENERATE_URL invalid choose'
        writeLog('ERROR: GENERATE_URL invalid choose\n')
        return 0

def reduceLimit(limitToReduce,url,choice):
    writeLog('ERROR: REDUCE %s\n' % choice)
    if  limitToReduce > 100:
        print 'ERROR: REDUCE %s %d - 100' % (choice,limitToReduce)
        old = 'limit='+str(limitToReduce)
        limitToReduce -= 100
    elif limitToReduce <= 100 and limitToReduce > 10:
        print 'ERROR: REDUCE %s %d - 10' % (choice,limitToReduce)
        old = 'limit='+str(limitToReduce)
        limitToReduce -= 10
    elif limitToReduce <= 10 and limitToReduce > 0:
        print 'ERROR: REDUCE %s %d - 1' % (choice,limitToReduce)
        old = 'limit='+str(limitToReduce)
        limitToReduce -= 1
    elif limitToReduce is 0:
        print 'ERROR: LIMIT_COMMENTS is 0'
        quit()
    else:
        print 'ERROR: LIMIT_COMMENTS less than 0'
        quit()
    new = 'limit='+str(limitToReduce)
    url = url.replace(old,new)
    return limitToReduce,url

def postLikes(url):
    if  not url:
        print 'ERROR: POST_LIKES invalid url'
        return
    while True:
        res = requests.request("GET",url)
        jsondata = json.loads(res.text)
        if  jsondata.get('error') is None:
            break
        else:
            print 'ERROR: POST_LIKES data'
            writeLog('ERROR: POST_LIKES data\n')
            writeLog(str(jsondata)+'\n')
            sleepTime = random.randint(150,180)
            print 'POST_LIKES random sleep: %d seconds' % sleepTime
            time.sleep(sleepTime)
    while True:
        try:
            data = jsondata['data']
            if  hasNext(jsondata):
                data.extend(postLikes(jsondata['paging']['next']))
            return data
        except:
            print 'ERROR: POST_LIKES data'
            writeLog('ERROR: POST_LIKES data\n')
            writeLog(str(jsondata)+'\n')
            #return False


def postComments(url,after=''):
    if  not url:
        print 'ERROR: POST_COMMENTS invalid url'
        return
    if  after != '':
        url = url + '&after=' + after
    
    global limitComment
    limitComment = 1000    
    while True:
        res = requests.request("GET",url)
        jsondata = json.loads(res.text)
        if  jsondata.get('error') is None:
            break
        else:
            print 'ERROR: POST_COMMENTS data'
            writeLog('ERROR: POST_COMMENTS data\n')
            writeLog(str(jsondata)+'\n')
            if  jsondata['error']['code'] is 1:
                limitComment,url = reduceLimit(limitComment, url, 'LIMIT_COMMENT')
                continue
            elif jsondata['error']['code'] is 2:
                sleepTime = random.randint(150,180)
                print 'POST_COMMENTS random sleep: %d seconds' % sleepTime
            else:
                print 'ERROR: POST_COMMENTS other error code'
            time.sleep(sleepTime)
    try:
        data = jsondata['data']
        if  jsondata.has_key('paging'):
            data.extend(postComments(url,jsondata['paging']['cursors']['after']))
        return data
    except:
        print 'ERROR: POST_COMMENTS data'
        writeLog('ERROR: POST_COMMENTS data\n')
        writeLog(str(jsondata)+'\n')
        return False

    
def getPost(postID):
    print postID
    writeLog(postID)
    url = generateUrl('posts', postID)
    res = requests.request("GET",url)
    jsondata = json.loads(res.text)
    writeLog(jsondata['type'] + '\n')
    if 'event' in jsondata['type']:
        print 'event post'
        return False
    else:
        print jsondata['type']
    
    print jsondata['created_time'] + 'start'
    writeLog(jsondata['created_time'] + 'start\n')
    
    comments = {}
    urlComments = generateUrl('comments',postID)
    comments['comments'] = postComments(urlComments)
    while comments['comments'] is False:
        print 'Re GET comments'
        writeLog('Re GET comments\n')
        comments['comments'] = postComments(urlComments)
    jsondata.update(comments)
    print len(jsondata.get('comments'))
    writeLog( str(len(jsondata.get('comments'))) + '\n')
    
    likes = {}
    urlLikes = generateUrl('likes',postID)
    likes['likes'] = postLikes(urlLikes)
    while likes['likes'] is False:
        print 'Re GET likes'
        writeLog('Re GET likes\n')
        likes['likes'] = postLikes(urlLikes)
    jsondata.update(likes)
    print len(jsondata.get('likes'))
    writeLog( str(len(jsondata.get('likes'))) + '\n' )
    
    print jsondata['created_time'] + 'close'
    writeLog(jsondata['created_time'] + 'close\n')
    
    return jsondata

###=====================================================================###
while datetime.datetime(year,month,1,0,0,0) < endTime:
    postDataDict = {}
    postDataList = []
    updateDir()
    url = generateUrl('post list', personID)

    while True:
        checkAddrExist()
        fileHaveDown = checkFileDown()
        
        res = requests.request("GET",url)
        jsondata = json.loads(res.text)
        #print len(jsondata['data'])
    
        if  jsondata.has_key('error'):
            print 'ERROR: get fanpage error'
            print jsondata
            writeLog('ERROR: get fanpage error\n')
            writeLog(str(jsondata)+'\n')
            quit()
        
        postDataList.extend(jsondata['data'])
        
        for post in jsondata['data']:
            postID = post['id']
            if  fileHaveDown.has_key(postID + '.json'):
                '''
                print 'OLD DATA ID: %s'%postID
                tmpFileName = personYearMonthDir + '/'+ postID+'.json'
                oldPostData = json.load(open(tmpFileName,'r'))
                print oldPostData[postID]['created_time']
                
                comments = {}
                urlComments = generateUrl('comments',postID)
                comments['comments'] = postComments(urlComments)
                while comments['comments'] is False:
                    print 'Re GET comments'
                    writeLog('Re GET comments\n')
                    comments['comments'] = postComments(urlComments)
                oldPostData[postID].update(comments)
                #for c in oldPostData[postID]['comments']:
                #    print c.get('from')
                print len(oldPostData[postID].get('comments'))
                writeLog( str(len(oldPostData[postID].get('comments'))) + '\n')
                with open(tmpFileName, 'w') as f:
                    json.dump(oldPostData, f)
                print 'OLD DATA ID: %s close' %postID
                '''
                continue
            
            postDataDict = {}
            postDataDict[postID] = getPost(postID)
            if  postDataDict[postID] is not False:
                jsonDump(postDataDict, postID)
            #break
        #break
        
    
        if  hasNext(jsondata):
            url = jsondata['paging']['next']
        else:
            break
    
    #break
    jsonDump(postDataList, 'postDataList')
    #jsonDump(postDataDict, 'postDataDict')

print 'LUCKY ENDING'
