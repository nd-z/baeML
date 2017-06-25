from django.test import TestCase

class ModelTest(TestCase):

	def setUp(self):
		self.id=1234
		self.model = ArticleRetriever(user_id=self.id)

