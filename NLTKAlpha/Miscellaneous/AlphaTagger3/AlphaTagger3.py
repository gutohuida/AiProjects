##Imports
from unidecode import unidecode
import nltk as nltk
from nltk.tag.perceptron import PerceptronTagger
from sklearn.externals import joblib

##Caminho do modelo nltk
PATH = '...AlphaTagger2.pkl' 

##Carrega um modelo
tagger = joblib.load(PATH)

##Função que processa uma sentença.
def process(sent):
    sent = nltk.word_tokenize(unidecode(sent.lower()))
    stop_words = stopwords.words('portuguese')
    sent = tagger.tag(sent)
    new_sent = []
    returner = []
    aux_sent = ''
    pattern = '''NP:  {<K><STOP>*<K>+} 
                      {<K>+}'''
    cp = nltk.RegexpParser(pattern)
    cs = cp.parse(sent)
    for i in cs:
        if len(i) < 2 and i[0][1] == 'K':
            returner.append(i[0][0])
        elif len(i) > 2:
            for j in i:
                aux_sent += j[0]+' '
            returner.append(aux_sent)
            aux_sent = ''
        elif isinstance(i[0],tuple):
            returner.append(i[0][0]+' '+i[1][0])
    return returner