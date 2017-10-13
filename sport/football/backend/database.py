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

    def close(self):
        self.connection.close()
