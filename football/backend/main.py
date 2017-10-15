import sys
import getopt
from document import Document
import articles_processor as ap
import os
from web_parser import parse_goal_com
from web_parser import parse_news
from web_parser import get_article
from summarization_system import CBS
from database import DBAdapter

def main():

    step = 0
    for b in range(40):
        documents = []
        for i in range(1+step, 6+step):
            doc = Document(str(i))
            if doc.sentences:
                documents.append(doc)
        group = []
        for doc in documents:
            group.append(doc.tokens)
        cbs = CBS()
        bob = cbs.get_selection(group, 10)
        # print(bob)
        summary = ''
        links_set = set()
        links = []
        links_string=''
        for el in bob:
            summary = summary + documents[el[2]].sentences[el[0]] + ". \n"
            links.append(documents[el[2]].link)
        links_set = links
        for link in links_set:
            links_string += link + ' '

        db = DBAdapter()
        db.insert_summary(summary, links_string)
        db.close()
        print(summary)
        print(links_string)
        step += 5

if __name__ == "__main__":
    main()