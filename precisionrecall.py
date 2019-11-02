import re
import scipy as sp
from pylab import *
from matplotlib.backends.backend_pdf import PdfPages

# Opens the cran file with all documents and splits each document and then puts in a list all the splits enumarated. The enumeration starts with 1
def openDocumentsFile():
    with open('cran.all.1400','r') as file:
        docs = file.read().split('\n.I')
    return list(enumerate(docs,1))

# Extracts the indexes of the list with the enumerations of the documents and puts them in a list
def getDocumentsIndexes(documents):
    return [doc[0] for doc in documents]

# Opens and formats the cranqrel file with 10 queries
def openRelevantDocumentsFile():
    with open('ejemplocranqrel','r') as file:
        docs = file.read().split('\n')
        withoutLastSpace = [element.rstrip() for element in docs]
    return [element.split(' ') for element in withoutLastSpace]    

# Extract the relevant documents for each query
def getRelevants(allrelevants):
    query1,query2,query3,query4,query5,query6,query7,query8,query9,query10 = ([] for i in range(10))
    for relevant in allrelevants:
        if relevant[0] is '1':
            query1.append(int(relevant[1]))
        elif relevant[0] is '2':
            query2.append(int(relevant[1]))
        elif relevant[0] is '3':
            query3.append(int(relevant[1]))
        elif relevant[0] is '4':
            query4.append(int(relevant[1]))
        elif relevant[0] is '5':
            query5.append(int(relevant[1]))
        elif relevant[0] is '6':
            query6.append(int(relevant[1]))
        elif relevant[0] is '7':
            query7.append(int(relevant[1]))
        elif relevant[0] is '8':
            query8.append(int(relevant[1]))
        elif relevant[0] is '9':
            query9.append(int(relevant[1]))
        else:
            query10.append(int(relevant[1]))
    return [query1,query2,query3,query4,query5,query6,query7,query8,query9,query10]

# Each list in the list represents the calculation of precision for each query
def getQueriesPrecisions(documents, relevants):
    return [calculatePrecision(documents, qRelevants) for qRelevants in relevants]

# Calculates the precision of a query and return a list with the query's precision    
def calculatePrecision(documents, queryRelevants):
    relevantRetrieved = 0 # Numerador
    retrieved = 0 # Retrieved
    r = []
    for document in documents:
        if document in queryRelevants:
            relevantRetrieved += 1
        retrieved += 1
        r.append(relevantRetrieved/retrieved)
    return r

# Each list in the list represents the calculation of recall for each query
def getQueriesRecalls(documents, relevants):
    return [calculateRecall(documents, qRelevants) for qRelevants in relevants]

# Calculates the recall of a query and return a list with the query's recall    
def calculateRecall(documents, queryRelevants):
    relevantRetrieved =  0
    relevant = len(queryRelevants)
    r = []
    for document in documents:
        if document in queryRelevants:
            relevantRetrieved += 1
        r.append(relevantRetrieved/relevant)
    return r

def plottingAverage(recallAverage, precisionAverage):
    f = figure(11)
    plot(recallAverage, precisionAverage, color='green')
    xlabel('Recall')
    ylabel('Precision')
    title('Average of 10 queries')
    savefig('average.png',dpi=300)
    return f
    #show()

def plottingQueries(recall, precision):
    colours=['r','b','c','m','y','r','b','c','m','y']
    r = []
    #pdf = PdfPages('queries.pdf')
    for i in range(len(recall)):
        f = figure(i)
        plot(recall[i], precision[i], colours[i])
        xlabel('Recall')
        ylabel('Precision')
        title('Query '+str(i+1))
        r.append(f)
        #pdf.savefig()
        #show()
    #pdf.close()
    return r

def start():
    alldocs = openDocumentsFile()
    indexesDocuments = getDocumentsIndexes(alldocs)

    listRelevants = openRelevantDocumentsFile()
    relevants = getRelevants(listRelevants)

    precisions = getQueriesPrecisions(indexesDocuments, relevants)
    recalls = getQueriesRecalls(indexesDocuments, relevants)

    precisionAverage = [sum(element)/len(precisions) for element in zip(*precisions)]
    recallAverage = [sum(element)/len(recalls) for element in zip(*recalls)]

    averagePlot = plottingAverage(recallAverage,precisionAverage) 
    queriesPlots = plottingQueries(recalls, precisions)

    pdf = PdfPages('queries.pdf')
    queriesPlots.append(averagePlot)
    for figure in queriesPlots:
        pdf.savefig(figure)
    pdf.close()

start()