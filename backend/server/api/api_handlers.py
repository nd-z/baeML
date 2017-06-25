from django.http import HttpResponse

#testing, should just return 201 to every call to this
def hello(self):
	print("lol")
	return HttpResponse(status=201)

#TODO implement the logic behind these
def login(self):
	pass

def login_init(self):
	pass