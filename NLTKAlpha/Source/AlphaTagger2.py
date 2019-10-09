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
    sent = nltk.word_tokenize(unidecode(sent))
    sent = tagger.tag(sent)
    new_sent = []
    for i in sent:
        if i[1] == 'K' or i[1] == 'KPT':
            new_sent.append(i)    
    return new_sent