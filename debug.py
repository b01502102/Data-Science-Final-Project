from __future__ import print_function

from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

from sklearn.cluster import KMeans, MiniBatchKMeans

import logging
from optparse import OptionParser
import sys
from time import time


# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# parse commandline arguments
op = OptionParser()
op.add_option("--lsa",
              dest="n_components", type="int",
              help="Preprocess documents with latent semantic analysis.")
op.add_option("--no-minibatch",
              action="store_false", dest="minibatch", default=True,
              help="Use ordinary k-means algorithm (in batch mode).")
op.add_option("--no-idf",
              action="store_false", dest="use_idf", default=True,
              help="Disable Inverse Document Frequency feature weighting.")
op.add_option("--use-hashing",
              action="store_true", default=False,
              help="Use a hashing feature vectorizer")
op.add_option("--n-features", type=int, default=10000,
              help="Maximum number of features (dimensions)"
                   " to extract from text.")
op.add_option("--verbose",
              action="store_true", dest="verbose", default=False,
              help="Print progress reports inside k-means algorithm.")

print(__doc__)
op.print_help()

(opts, args) = op.parse_args()
if len(args) > 0:
    op.error("this script takes no arguments.")
    sys.exit(1)



true_k =147

print("Extracting features from the training dataset using a sparse vectorizer")
t0 = time()

import json

termFreqLowBound = 2
terms = []

def resetWordDict(word_dict):
    for key in word_dict:
        word_dict[key] = 0

def initWordDict(word_dict,vocabFileName):
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
    global terms
    terms = word_dict.keys()
    w.close()

def initDocTermMatrix(docTermMatrix,cleanFileName,vocabFileName):
    word_dict = {}
    initWordDict(word_dict,vocabFileName)
    
    f = open(cleanFileName,'r')
    
    while True:
        line = f.readline()
        if  line == '':
            break
            
        #ID = line.split()[0]
        line = line.split()[1:]  
        resetWordDict(word_dict)
        for term in line:
            if  word_dict.has_key(term):
                word_dict[term] += 1
        
        docTermMatrix.append(word_dict.values())
        
    f.close()
#
#person = 'TsaiIngWen'person = 'LLChu'
dataType = 'post'
cleanFileName = './%s/%s_%sData_clean.txt' % (person,person,dataType)
vocabFileName = './%s/%s_%sData_term_unigram.txt' % (person,person,dataType)
dimReFileName = './%s/%s_%sData_dimRe.txt' % (person,person,dataType)

X = []
initDocTermMatrix(X,cleanFileName,vocabFileName)

opts.n_components = 200
if opts.n_components:
    print("Performing dimensionality reduction using LSA")
    t0 = time()
    # Vectorizer results are normalized, which makes KMeans behave as
    # spherical k-means for better results. Since LSA/SVD results are
    # not normalized, we have to redo the normalization.
    svd = TruncatedSVD(opts.n_components)
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)

    X = lsa.fit_transform(X)

    print("done in %fs" % (time() - t0))

    explained_variance = svd.explained_variance_ratio_.sum()
    print("Explained variance of the SVD step: {}%".format(
        int(explained_variance * 100)))

    print()
dimReFileName = './%s/%s_%sData_dimRe.txt' % (person,person,dataType)
json.dump(X.tolist(),open(dimReFileName,'w'))quit()
##################################################
# Do the actual clustering

if opts.minibatch:
    km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
                         init_size=1000, batch_size=1000, verbose=opts.verbose)
else:
    km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1,
                verbose=opts.verbose)

print("Clustering sparse data with %s" % km)
t0 = time()
km.fit_transform(X)

if not opts.use_hashing:
    print("Top terms per cluster:")

    if opts.n_components:
        original_space_centroids = svd.inverse_transform(km.cluster_centers_)
        order_centroids = original_space_centroids.argsort()[:, ::-1]
    else:
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]
    #print str(order_centroids[, :10])
    global terms
    for i in range(true_k):
        print("Cluster %d:" % i, end='')
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind], end='')
        print()