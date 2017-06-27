from django.test import TestCase
from .models import Users

class UserTest(TestCase):

	def createUser(self):
		self.user_fbid = 1234
		self.user_name = "legend"
		self.propic_link = "http://www.cs.cornell.edu/courses/cs2112/2016fa/images/Dex16.jpg"
		self.user = Users(user_fbid=self.user_fbid, name=self.user_name, propic_link=self.propic_link)

	def isUserCreated(self):
		count = Users.objects.count()
		self.user.save()
		updated = Users.objects.count()
		self.assertNotEqual(count, updated)