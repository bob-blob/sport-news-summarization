import sys
import getopt
from document import Document
import os
from web_parser import parse_GoalCom
from web_parser import parse_news
from web_parser import get_article

def main():
    # currpath = os.path.dirname(os.path.realpath(__file__))
    # doc = currpath + '/Documents/Mica.html'
    # documents = []
    # documents.append(Document(doc))
    # print(documents[0].sentences)
    #parse_GoalCom()
    #parse_news()
    #get_article('1')

if __name__ == "__main__":
    main()