from django.conf.urls import url
import views, api_handlers

urlpatterns = [
    url(r'^login/', api_handlers.login, name="login"),
    url(r'^init/', views.UsersView.as_view()),
    url(r'^test/', api_handlers.hello, name="hello"),
]