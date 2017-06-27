from django.db import models
import psycopg2 #adapater

'''models go here,get data from database'''

class Article(object):
    title=""
    link=""
    summary=""

    def __init__(self, title, link, summary):
        self.title = title
        self.link = link
        self.summary = summary

def main():
     #Define connection string
    conn_string = "host='localhost' dbname='baeML_db' user='admin' password=''"
 
    # get a connection
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        print "Connected!\n"
    except:
        print "Connection failed"
 
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    
 
if __name__ == "__main__":
    main()



