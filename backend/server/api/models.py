from django.db import models
import psycopg2 #adapater

#Each model has an automatic field named 'id' which increments automatically

class Users(models.Model):
    user_fbid = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    propic_link = models.URLField(max_length=400)

class article(models.Model):
	fk_user = models.IntegerField()
	article_name = models.CharField(max_length=45)
	user_rating = models.SmallIntegerField()

class Tags(models.Model):
	fk_keyword_id = models.IntegerField()
	fk_recommendation_id = models.IntegerField()	

class Keywords(models.Model): 
	keyword = models.CharField(max_length=45)


#uh what is this
# def main():
#      #Define connection string
#     conn_string = "host='localhost' dbname='baeML_db' user='admin' password=''"
 
#     # get a connection
#     try:
#         conn = psycopg2.connect(conn_string)
#         cursor = conn.cursor()
#         print "Connected!\n"
#     except:
#         print "Connection failed"
 
#     # conn.cursor will return a cursor object, you can use this cursor to perform queries
    

# if __name__ == "__main__":
#     main()

