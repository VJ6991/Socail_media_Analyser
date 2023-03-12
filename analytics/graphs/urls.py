from django.urls import path
from . import views
urlpatterns=[
    path('',views.registration,name='registration'),
    path('login',views.login,name='login'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('linegraph',views.linegraph,name='linegraph'),
    path('bargraph',views.bargraph,name='bargraph'),
    path('piechart',views.piechart,name='piechart'),
    path('vectormap',views.vectormap,name='vectormap'),
    
    
    ]