import sys
import nltk
import sqlite3
from sqlite3 import Error

debugText = False
#a ordem dos argumentos é a seguinte
#1:banco_de_dados.db 2:"frase bonita" 3:-v
args = sys.argv

dataBase = args[1]
input = args[2]
if len(args) == 4 and args[3] == "-v":
    print("Debug mode activated")
    debugText = True

#babidi bibidi boo
def bibidiLog(caption, output):
    if debugText == True:
        print("\n ======================================= Bibidi ======================================= \n")
        print(caption + "\n")
        print(output)

bibidiLog("Received input:", input)

#carrega os dados do banco
def load_database(dbFile):
    conn = None
    try:

        conn = sqlite3.connect(dbFile)
        cur = conn.cursor()
        cur.execute("SELECT * FROM sentences")
        rows = cur.fetchall()
        return rows

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

base = load_database(dataBase)
bibidiLog("Loading database...", base)

# remover stopwords, está funcionando e é melhor nem mexer
def removeStopWords(text):
    r = []
    for (sentence, command) in text:
        line = []
        for s in sentence.split():
            if s not in nltk.corpus.stopwords.words("portuguese"):
                line.append(s)
        r.append((line, command))
    return r

bibidiLog("Removing stopwords...", removeStopWords(base))

#extrair o radical das palavras aka stemming

def applyStemming(text):
    stemmer = nltk.stem.RSLPStemmer()
    r = []
    for(sentence, command) in text:
        line = []
        for s in sentence:
            line.append(str(stemmer.stem(s)))
        r.append((line, command))
    return r

bibidiLog("Stemming text...", applyStemming(removeStopWords(base)))

# retorna lista com todas as palavras sem o comando
stemList = applyStemming(removeStopWords(base))

def listWords(text):
    stemmer = nltk.stem.RSLPStemmer()
    r = []
    for(sentence, command) in text:
        r.extend(sentence)
    return r

bibidiLog("Listing words without command...", listWords(stemList))

# retorna lista com a palavra e adrequência
def listWordsFrequency(text):
    r = nltk.FreqDist(listWords(stemList))
    return r

bibidiLog("Listing listing words frequency", listWordsFrequency(listWords(stemList)).most_common(10))

# retorna uma lista com palavras únicas
def listUniqueWords(text):
    r = text.keys()
    return r

bibidiLog("Listing listing words frequency", listUniqueWords(listWordsFrequency(listWords(stemList))))

# extrai as palavras no parâmetro da base de dados (wtf?)

uniqueWords = listUniqueWords(listWordsFrequency(listWords(stemList)));
def wordExtractor(document):
    doc = set(document)
    r = { }
    for words in uniqueWords:
        r["%s" % words] = (words in doc)
        #esse aparentemente cria um dicionário com a palavra e o valor correspondente ao 
        #resultado da operação lógica se as palavras da base de dados estão nas palavras do parâmetro
    return r
#bibidiLog("Checking input and database correspondence...", wordExtractor(["calcul", "googl", "abr"]))

#faz a classificação da palavra
# é basicamente a correspondência das palavras dentro do input 
# com as palavras associadas a comandos na base de dados
fullFeatureBase = nltk.classify.apply_features(wordExtractor, stemList)
bibidiLog("Classifying words list...", fullFeatureBase)

#agora vem a classificação com o naive bayes
classifier = nltk.NaiveBayesClassifier.train(fullFeatureBase)
bibidiLog("","")
if debugText == True:
    classifier.show_most_informative_features(5)
    print("\n")

#aqui é feito o tratamento do input para ser classificado
def getInput(inputText):
    r = []
    stemmer = nltk.stem.RSLPStemmer()
    for (word) in inputText.split():
        if word not in nltk.corpus.stopwords.words("portuguese"):
            r.append(str(stemmer.stem(word)))
    return r
bibidiLog("Showing input stem and stopword routine result...", getInput(input))

featuredInput = wordExtractor(getInput(input))
bibidiLog("Apllied features to input words...", featuredInput)

print(classifier.classify(featuredInput))