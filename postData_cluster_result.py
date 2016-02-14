#coding=UTF-8

#person = 'TsaiIngWen'
person = 'LLChu'
dataType = 'post'
clusterFileName = './%s/%s_%sData_cluster.txt' % (person,person,dataType)
cleanFileName = './%s/%s_%sData_clean.txt' % (person,person,dataType)
logFileName = './%s/%s_cluster_log.txt' % (person,person)

def clusterEval(data):
    return



cluster = []
postCluster = {}
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

f = open(cleanFileName,'r')
count = 0
while True:
    line = f.readline()
    if  line == '':
        break
    clusterNumber = cluster[count]
    print clusterNumber
    if  postCluster.has_key(clusterNumber):
        postCluster[clusterNumber].append(line)
    else:
        postCluster[clusterNumber] = [line]
    count += 1
f.close()

l = open(logFileName,'w')
for clusterNumber in postCluster:
    l.write('Cluster %s:\n'%clusterNumber)
    for line in postCluster[clusterNumber]:
        l.write(line)
l.close()