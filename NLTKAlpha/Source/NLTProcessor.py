##Imports
from unidecode import unidecode
from nltk.tag.perceptron import PerceptronTagger
from nltk.corpus import stopwords
import nltk as nltk
import joblib

##Classe
class NLTKProcessor:
    def __init__(self, tagger_path = None ,stop_words = None, pattern = None, tokenizer = lambda x: x.split()):
        if tagger_path != None:
            self._load_tagger(tagger_path)
        else:
            self.tagger = PerceptronTagger()
        self.stop_words = stop_words
        self.pattern = pattern
        self.tokenizer = tokenizer
        self.parser = nltk.RegexpParser(self.pattern)
        
    def tagger_training(self, taglist, tagger = PerceptronTagger(load=False) ):
        self.tagger = tagger
        self.tagger.train(taglist)
        
    def process(self, sent):
        sent = self.tokenizer(unidecode(sent.lower()))
        sent = self.tagger.tag(sent)
        returner = []
        aux_sent = ''
        cs = self.parser.parse(sent)
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
    
    def raw_process(self, sent):
        sent = self.tokenizer(unidecode(sent.lower()))
        sent = self.tagger.tag(sent)
        return sent
    
    def _load_tagger(self, path=None):
        self.tagger = joblib.load(path)