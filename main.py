import sys, re, string, math

knownLanguages = {} # a dictionary that maps from a known language to a vector* created from its documents
unknownDocuments = {} # a dictionary that maps from each document of unknown language to the vector* created from the document
similarities = {} # a dictionary that maps from unknown document to a dictionary that maps from language to similarity

# * note that by "vector", i mean a dictionary that maps from all possible trigrams to their respective counts

# populates the two dictionaries with the appropriate languages and vectors
def constructDictionaries(inputFilePath):
    inputFile = open(inputFilePath)
    for lineOfText in inputFile:
        strippedLine = lineOfText.strip()
        language, documentFilePath = strippedLine.split()[0], strippedLine.split()[1]
        if language != "Unknown":
            # the language is known, add to _knownLanguages_ dictionary
            if knownLanguages.has_key(language):
                # add to the existing vector
                editLanguageDictionary(documentFilePath, language)
            else: 
                # add the language and instantiate vector
                knownLanguages[language] = initializeLanguageDictionary()
        else: 
            # the language is unknown, add to the _unknownDocuments_ dictionary with a key of the document name
            unknownDocuments[documentFilePath] = initializeLanguageDictionary()
            editLanguageDictionary(documentFilePath, documentFilePath)
    inputFile.close()
    # now to construct the dictionary of similarities
    for documentName in unknownDocuments.keys():
        similarities[documentName] = {}
        for language in knownLanguages.keys():
            similarities[documentName][language] = 0 # we will initialize the similarity to each language as zero

# returns a dictionary that maps from all possible trigrams to zero
def initializeLanguageDictionary():
    characters = string.ascii_lowercase + " "
    initializedDictionary = {}
    for i in range(len(characters)):
        for j in range(len(characters)):
            for k in range(len(characters)):
                currentTrigram = characters[i] + characters[j] + characters[k]
                initializedDictionary[currentTrigram] = 0
    return initializedDictionary

# returns a vector that represents the counts of each possible trigram in the document from
# the text file at the given file 
def editLanguageDictionary(inputFilePath, language):
    inputFile = open(inputFilePath)
    textString = inputFile.read()
    # this will replace all the special characters mentioned with an empty string
    textString = re.sub("[{}\d]".format(re.escape("'\"?!@#$%^&*()[]{};:,./<>\|`~-=_+")), "", textString) 
    textStringAsList = textString.split()
    textString = " ".join(textStringAsList)
    # now we have a string that has no special characters, and each word is separated by one whitespace character
    # note, there are n-2 trigrams for a string of length n
    for i in range(len(textString) - 2):
        currentTrigram = textString[i:i+3].lower()
        if language in knownLanguages:
            knownLanguages[language][currentTrigram] += 1
        else: 
            unknownDocuments[language][currentTrigram] += 1

# populates the similarities dictionary for each document and each language
def constructSimilarities():
    for documentName in unknownDocuments:
        documentVector = unknownDocuments[documentName]
        for languageName in knownLanguages:
            languageVector = knownLanguages[languageName]
            similarity = cosineSimilarity(documentVector, languageVector)
            similarities[documentName][languageName] = similarity

# returns the cosine of the angle between the two vectors
def cosineSimilarity(first, second):
    convertToFrequency(first)
    convertToFrequency(second)
    magnitudeOfFirst = math.sqrt(dotProduct(first, first))
    magnitudeOfSecond = math.sqrt(dotProduct(second, second))
    result = (dotProduct(first, second)) / (magnitudeOfFirst * magnitudeOfSecond)
    return result

# "normalizes" the given vector by computing the sum of all the components and dividing each component by this sum
def convertToFrequency(vector):
    sum = 0
    for count in vector.values():
        sum += count
    for count in vector.values():
        count = count / sum

# returns the dot product of the two vectors
def dotProduct(first, second):
    sum = 0
    for trigram in first.keys():
        countOfFirst = first[trigram]
        countOfSecond = second[trigram]
        sum += countOfFirst * countOfSecond
    return sum

# writes to the output file with the completed dictionary of similarities
def constructOutputFile(outputFilePath):
    outputFile = open(outputFilePath, "w")
    for documentName in similarities:
        outputFile.write("{}".format(documentName))
        outputFile.write("\n")
        # we sort the similarities in descending order
        similaritiesSorted = similarities[documentName].items()
        similaritiesSorted.sort(reverse = True, key = (lambda x: x[1]))
        for similarityTuple in similaritiesSorted:
            # each tuple maps from a language to the unknown document's similarity to that language
            outputFile.write("    {} {}".format(similarityTuple[0], similarityTuple[1]))
            outputFile.write("\n")
    outputFile.close()

def main():
    inputFilePath = sys.argv[1]
    outputFilePath = sys.argv[2]
    constructDictionaries(inputFilePath)
    constructSimilarities()
    constructOutputFile(outputFilePath)

main()






