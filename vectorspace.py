import re
import math
import operator
import json

def processQuery(query):
    letters = re.sub(r'[^a-z]', ' ', query)
    return letters.split()

def processDocuments():
    with open('ejemplo.all.1400','r') as file:
        docs = file.read().split('\n.I')
    return docs

def getAndCleanContent(alldocs):
    contentList = []
    for doc in alldocs:
            contentList.append(doc.split('.W')[1])
    onlyLetters = [re.sub(r'[^a-z]', ' ', content) for content in contentList]
    cleanContent= [" ".join(content.split())for content in onlyLetters]
    return cleanContent

def invertedIndex(cleanDocuments):
    invertedIndex = {}
    termCount = {} 
    for index, doc in enumerate(cleanDocuments):
        for term in doc.split():
            termCount[term] = termCount.get(term,0)+1
            if invertedIndex.get(term,False):
                if index not in invertedIndex[term]:
                    invertedIndex[term].append(index)
            else: 
                invertedIndex[term] = [index] 
    return invertedIndex

def calculatingDocumentsIDF(cleanDoccuments, invertedI):
    idfDict = {}
    n = len(cleanDoccuments)
    idfDict = dict.fromkeys(invertedI, 0)

    for term, docs in invertedI.items():
         idfDict[term] = math.log10(n/len(docs))
    return idfDict

def calculatingTermFrequency(cleanDocuments):
    docsList = []
    splitted = [document.split() for document in cleanDocuments]
    for doc in splitted:
        docsList.append({term: doc.count(term) for term in doc})
    return docsList

def documentsToVectors(termsFrequency, idfDictionary, query):
    result = []
    for docDictionary in termsFrequency:
        docVector = []
        for term in query:
            weight = 0
            frec = 0
            if term in docDictionary.keys():
                frec = docDictionary[term]
            if term in idfDictionary.keys():
                weight = idfDictionary[term]

            docVector.append(weight * frec)
        result.append(docVector)
    return result

def dot(queryVector, docVector):
    result = 0
    for e1,e2 in zip(queryVector,docVector):
        result += e1 * e2
    return result

def queryToVector(query, idfDictionary):
    result = []
    for term in query:
        weight = 0
        if term in idfDictionary.keys():
            weight = idfDictionary[term]
        result.append(weight)
    return result

def ranking(queryVector, docsVectors):
    ranks = []
    for doc,index in zip(docsVectors,range(len(docsVectors))):
        ranks.append([index,dot(queryVector,doc)])
    #ranks.sort(key = operator.itemgetter(1),reverse = True)
    return ranks

def getAndCleanTitles(docs):
        titleList = []
        for doc in docs:
            titleList.append(doc.split('.T')[1].split('.A')[0])
        onlyLetters = [re.sub(r'[^a-z]', ' ', title) for title in titleList]
        cleanTitles = [title.strip() for title in onlyLetters]
        return cleanTitles

def formattingResult(rank, titlesDocuments, contentsDocuments):
    titles = []
    contents = []
    keys = ["No. Document","Title","Sentence","Ranking coefficient"]
    r = []

    for title in enumerate(titlesDocuments):
        titles.append(list(title))
    
    for content in enumerate(contentsDocuments):
        contents.append(list(content))

    for title in titles:
        for content in contents:
            if title[0] == content[0]: 
                title.append(content[1])
    
    for vector in rank:
        for title in titles:
            if vector[0] == title[0]:
                title.append(vector[1])

    results = sorted(titles, key = lambda x: x[3], reverse=True)

    for result in results:
        r.append(dict(zip(keys, result)))

    return r

def start(query):
    cleanQuery = processQuery(query)
    docs = processDocuments()
    contentsDocuments = getAndCleanContent(docs)
    invertedI = invertedIndex(contentsDocuments)
    termsFrequency = calculatingTermFrequency(contentsDocuments)
    idfDictionary = calculatingDocumentsIDF(contentsDocuments, invertedI)
    docsVectors = documentsToVectors(termsFrequency, idfDictionary, cleanQuery)  
    queryVector = queryToVector(cleanQuery, idfDictionary)
    rank = ranking(queryVector, docsVectors)
    titlesDocuments = getAndCleanTitles(docs)
    result = formattingResult(rank, titlesDocuments, contentsDocuments)
    #print(json.dumps(result))
    print(result)

def main():
    query = "what similarity laws must be obeyed when constructing aeroelastic models of heated high speed aircraft ."
    start(query)

if __name__ == "__main__":
    main()