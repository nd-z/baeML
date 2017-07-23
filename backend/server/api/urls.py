from django.conf.urls import url
import views, api_handlers, main_handler

urlpatterns = [
    url(r'^login/', views.UsersView.as_view()),
    url(r'^status/', views.InitView.as_view()),
    url(r'^init/', views.InitView.as_view()),
	url(r'^users/next_article', views.ArticlesView.as_view()),
	url(r'^users/rate_article', views.ArticlesView.as_view()),
    url(r'^test/', api_handlers.hello, name="hello"),

]
