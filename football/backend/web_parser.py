import requests
from bs4 import BeautifulSoup
from lxml import html
from database import DBAdapter

user_id = 12345
goal_com_url = 'http://www.goal.com/en/news/'
results = []

def parse_GoalCom():
    global results

    for i in range(1, 250):
        r = requests.get(goal_com_url+str(i))
        soup = BeautifulSoup(r.text, "lxml")
        news_list = soup.find('div', {'class': 'main-content'})
        items = news_list.find_all('article')

        # results=[]
        for item in items:
            news_title = item.find('div', {'class': 'title-wrapper'}).find('h3').text

            news_link = item.find('a').get('href')
            results.append({
                'title': news_title,
                'link': news_link,
            })
        print('Processed %d page' % i)
    # for item in results:
    #     print("Title: %s, Link: %s\n" % (item['title'], item['link']))

    # with open('test.html', 'w') as output_file:
    #     output_file.write(r.text)


def parse_news():
    global results
    db = DBAdapter()
    for i in range(len(results)):
        r = requests.get(results[i]['link'])
        soup = BeautifulSoup(r.text, "lxml")
        try:
            raw_content = soup.find('div', {'class': 'body'}).findAll('p')
            clear_content = ''
            for elem in raw_content:
                clear_content += elem.get_text()
            db.insert_article(results[i]['title'], clear_content, results[i]['link'])
            print('added %d article' % i)
        except AttributeError:
            print('Not paper')
    db.close()


def get_article(article_id):
    db = DBAdapter()
    article = db.get_article(article_id)
    print(article[2])