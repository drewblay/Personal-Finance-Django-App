from django.conf.urls import url, include
from budget import views

urlpatterns = [
    url(r'^$', views.MonthlyBudgetOverview.as_view()),
    #url(r'^(?P<account>.*)/$', views.AccountTransactions.as_view()),
    ]