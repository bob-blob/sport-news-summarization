import psycopg2

class DBAdapter():

    def __init__(self):
        self.connection = psycopg2.connect(
            database='news',
            user='student',
            password='student',
        )
        self.cursor = self.connection.cursor()

    def insert_article(self, title, content, link):
        with self.connection:
            self.cursor.execute('INSERT INTO articles(Title, Content, Link) VALUES(%s, %s, %s)', (title, content, link))

    def get_articles(self):
        with self.connection:
            self.cursor.execute('SELECT * FROM articles')
            articles = self.cursor.fetchall()
        return articles

    def get_article(self, article_id):
        with self.connection:
            self.cursor.execute('SELECT * FROM articles WHERE ArticleID = %s', article_id)
            article = self.cursor.fetchone()
        return article

    def get_article_content(self, article_id):
        with self.connection:
            self.cursor.execute('SELECT * FROM articles WHERE ArticleID = {0}'.format(article_id))
            article = self.cursor.fetchone()
        return article[2]

    def get_article_link(self, article_id):
        with self.connection:
            self.cursor.execute('SELECT * FROM articles WHERE ArticleID = {0}'.format(article_id))
            article = self.cursor.fetchone()
        return article[3]

    def insert_summary(self, content, links):
        with self.connection:
            self.cursor.execute('INSERT INTO summaries(Content, Links) VALUES(%s, %s)', (content, links))

    def get_summary(self, summary_id):
        with self.connection:
            self.cursor.execute('SELECT * FROM summaries WHERE Summary_ID = {0}'.format(summary_id))
            summary = self.cursor.fetchone()
        return summary

    def get_all_summary(self):
        with self.connection:
            self.cursor.execute('SELECT * FROM summaries')
            summary = self.cursor.fetchall()
        return summary

    def close(self):
        self.connection.close()
