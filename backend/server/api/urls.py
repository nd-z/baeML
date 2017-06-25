from django.conf.urls import url
import api_handlers

urlpatterns = [
    url(r'^login/', api_handlers.login, name="login"),
    url(r'^init/', api_handlers.login_init, name="login_init"),
    url(r'^test/', api_handlers.hello, name="hello"),
]