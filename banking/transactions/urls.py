from django.conf.urls import url, include
from transactions import views

urlpatterns = [
    url(r'^(?P<account>.*)/$', views.AccountTransactions.as_view()),
    ]