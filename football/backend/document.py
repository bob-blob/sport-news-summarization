import nltk
import codecs
import re
import string
import logging
import os.path
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
__currentdir = os.path.dirname(os.path.realpath(__file__))
nltk.data.path.append(__currentdir+'/nltk_data')
__STEMMER = None


def tokenize(text):
    soup = BeautifulSoup(text)
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    strippedText = soup.get_text()#nltk.clean_html(text)#re.sub('<[^<]+?>', '', text)
    lines = (line.strip() for line in strippedText.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
    strippedText = '\n'.join(chunk for chunk in chunks if chunk)
    print(strippedText)

    tokenizer = nltk.data.load(__currentdir + '/nltk_data/tokenizers/punkt/english.pickle')
    return tokenizer.tokenize(strippedText)


def stem(word):
    global __STEMMER

    if __STEMMER is None:
        __STEMMER = nltk.stem.SnowballStemmer("english")

    return __STEMMER.stem(word)


def normalize(text):
    text = text.strip()
    text = re.sub('[\n\t]', ' ', text)
    text = re.sub('\s+', ' ', text)

    return text


def isGoodToken(token, stopwords=nltk.corpus.stopwords.words('english')):
    tok, pos = token
    return tok.lower() not in stopwords and pos != 'PUNCT'


class Document():

    def __init__(self, docfile, skipPreprocess=False):
        with codecs.open(docfile, 'r', 'utf-8') as doc:
            self.content = doc.read()
        self.docfile = docfile

        self.content = normalize(self.content)

        if not skipPreprocess:
            self.preprocess()

    def preprocess(self, tokenizer = tokenize, wordTokenizer = nltk.tokenize.word_tokenize,
                   stopwords = nltk.corpus.stopwords.words('english')):
        logger.info("Preprocessing document %s", os.path.basename(self.docfile))

        self.sentences = tokenizer(self.content)
        self.tokens = [wordTokenizer(sentence) for sentence in self.sentences]
        # self.filteredTokens = [[(tok, pos)
        #                         for tok, pos in sentence
        #                         if isGoodToken((tok, pos), stopwords)]
        #                        for sentence in self.tokens]
        # self.stemTokens = [[(stem(tok), pos)
        #                     for tok, pos in sentence]
        #                    for sentence in self.filteredTokens]
        for i in range(len(self.tokens)):
            print("token: %s" % (self.tokens[i]))

        self.stemTokens = [stem(token) for token in self.tokens]