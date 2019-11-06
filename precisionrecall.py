import re
import scipy as sp
from pylab import *
from matplotlib.backends.backend_pdf import PdfPages
import vectorspace as vs
import random

# Opens and formats the cranqrel file with 10 queries
def openRelevantDocumentsFile():
    with open('cranqrel','r') as file:
        dictionary = {}
        docs = file.read().split('\n')
        withoutLastSpace = [element.rstrip() for element in docs]
        splitted =  [element.split(' ') for element in withoutLastSpace]
        withoutLastElement = [(element[0:2] + element[2+1:]) for element in splitted]
        numbers = [[int(element) for element in row] for row in withoutLastElement]

        for n in numbers:
            if n[0] in dictionary:
                dictionary[n[0]].append(n[1])
            else:
                dictionary[n[0]] = [n[1]]
        return dictionary

# Opens the queries file with all the queries and splits each query and then puts in a list and return a list with 10 queries choosen randomly
def chooseQueriesRandomly():
    with open('queries.txt','r') as file:
        docs = file.read().split('\n')
        enum = list(enumerate(docs)) 
    return random.sample(enum,10)

# Enable us to know if a document is relevant or not
def is_relevant(relevants, result):
  if result["No. Document"] in relevants:
    return True
  else:
    return False

# Calculate precision, precision = relevant retrieved / retrieved
def precision(relevants, results):
  relevantRetrieved = list(filter(lambda doc: is_relevant(relevants, doc) , results))
  return len(relevantRetrieved) / len(results)

# Calculate recall, recall = relevant retrieved / relevants
def recall(relevants, results):
  relevantRetrieved = list(filter(lambda doc: is_relevant(relevants, doc) , results))
  return len(relevantRetrieved) / len(relevants)

# Given a list of relevant documents and a result for a vector space, calculate the precision-recall table
def calculate_pr(relevants, result):
  list_iter = iter(result)
  actual_list  = []
  precision_l  = []
  recall_l     = []
  result       = {"precision": [], "recall" : []}
  while(True):
    actual = next(list_iter,'end')
    if actual != 'end':
      actual_list.append(actual)
      precision_l.append(precision(relevants, actual_list))
      recall_l.append(recall(relevants, actual_list))
    else:
      break
  result["precision"] = precision_l
  result["recall"]    = recall_l  
  print(actual_list)
  return result

# Return the list of the relevants for the query
def getRelevants(query):
    relevantsDictionary = openRelevantDocumentsFile()
    if query in relevantsDictionary:
        return relevantsDictionary.get(query)

# To each query of 10, apply the vector space and return a list of lists, each list is the result of the vector space
def vectorSpaceAndRelevants(tenQueries):
    results = []
    for query in tenQueries:
        rel = getRelevants(query[0]) # return a list
        vectorspacemodel = vs.start(query[1]) # return a list of dictionaries
        results.append(calculate_pr(rel,vectorspacemodel))
    return results

# Plot of the average of the 10 queries
def plottingAverage(recallAverage, precisionAverage):
    f = figure(1)
    plot(recallAverage, precisionAverage, color='c')
    xlabel('Recall')
    ylabel('Precision')
    title('Average of 10 queries')
    savefig('average.png')
    return f
    #show()

def start():
    tenQueries = chooseQueriesRandomly()
    vectorAndRelevants = vectorSpaceAndRelevants(tenQueries)

    precisions = []
    recalls = []

    for queryDictionary in vectorAndRelevants:
        for key, value in queryDictionary.items():
            if key == 'precision':
                precisions.append(value)
            if key == 'recall':
                recalls.append(value)

    precisionAverage = [sum(element)/len(precisions) for element in zip(*precisions)]
    recallAverage = [sum(element)/len(recalls) for element in zip(*recalls)]

    print(precisionAverage)
    print(recallAverage)

    averagePlot = plottingAverage(recallAverage,precisionAverage) # Function to plot and save the image

    # Create a Pdf with the plot
    pdf = PdfPages('average.pdf')
    pdf.savefig(averagePlot)
    pdf.close()

start()