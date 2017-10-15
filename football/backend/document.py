import nltk
import codecs
import re
import string
import logging
import os.path
from bs4 import BeautifulSoup
from database import DBAdapter

logger = logging.getLogger(__name__)
__currentdir = os.path.dirname(os.path.realpath(__file__))
nltk.data.path.append(__currentdir+'/nltk_data')
__STEMMER = None
_POSMODEL = __currentdir + '/data/stanford-en'
_POSJAR = __currentdir + '/data/stanford-postagger.jar'
_POSTAGGER = None

def tokenize(text):
    #soup = BeautifulSoup(text)
    #for script in soup(["script", "style"]):
    #    script.extract()  # rip it out

    #strippedText = soup.get_text()#nltk.clean_html(text)#re.sub('<[^<]+?>', '', text)
    #lines = (line.strip() for line in strippedText.splitlines())
    #chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
    #strippedText = '\n'.join(chunk for chunk in chunks if chunk)
    #print(strippedText)
    #tokenizer = nltk.RegexpTokenizer(r'\w+')
    #tokenizer = nltk.data.load(__currentdir + '/nltk_data/tokenizers/punkt/english.pickle')
    text.split('.')

    return [x for x in map(str.strip, text.split('.')) if x]

def postag(sentence):
    """
    Postag utility using Stanford POStagger
    """
    global _POSTAGGER
    if _POSTAGGER is None:
        _POSTAGGER = nltk.tag.stanford.StanfordPOSTagger(
            _POSMODEL, _POSJAR, encoding='utf-8')

    tagsentence = _POSTAGGER.tag(sentence)

    # replace punctuation with PUNCT tag
    tagsentencepunct = []
    for tok, pos in tagsentence:
        allpunct = all(c in string.punctuation for c in tok)
        if tok in string.punctuation or allpunct:
            tagsentencepunct.append((tok, 'PUNCT'))
        else:
            tagsentencepunct.append((tok, pos))

    return tagsentencepunct

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
    return token.lower() not in stopwords


class Document:
    def __init__(self, doc_id, skip_preprocess=False):
        #with codecs.open(docfile, 'r', 'utf-8') as doc:
        #    self.content = doc.read()
        db = DBAdapter()
        self.content = db.get_article_content(doc_id)
        self.link = db.get_article_link(doc_id)
        db.close()
        self.doc_id = doc_id

        self.content = normalize(self.content)

        if not skip_preprocess:
            self.preprocess()

    def preprocess(self, tokenizer=tokenize, word_tokenizer=nltk.tokenize.word_tokenize,
                   stopwords = nltk.corpus.stopwords.words('english')):
        logger.info("Preprocessing article %s", os.path.basename(self.doc_id))

        self.sentences = tokenizer(self.content)
        print(self.sentences)
        self.tokens = [word_tokenizer(sentence) for sentence in self.sentences]
        # self.taggedTokens = [postag(toksentence)
        #                      for toksentence in self.tokens]
        #self.filtered_tokens = [[tok for tok in sentence if isGoodToken(tok, stopwords)]
                               #for sentence in self.tokens]
        #self.stem_tokens = [[stem(tok) for tok in sentence] for sentence in self.filtered_tokens]

        #print(self.tokens)
        #print(len(self.tokens))
        #for i in range(len(self.tokens)):
        #    print("token: %s" % (self.tokens[i]))

        #self.stemTokens = [stem(token) for token in self.tokens]