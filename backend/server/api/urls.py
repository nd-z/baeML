from django.conf.urls import url
import views, api_handlers, main_handler

urlpatterns = [
    url(r'^login/', views.UsersView.as_view()),
    url(r'^init/', views.UsersView.as_view()),
	url(r'^users/next_article', main_handler.MainHandler.get_article),
	url(r'^users/rate_article', main_handler.MainHandler.post),
    url(r'^test/', api_handlers.hello, name="hello"),

]
