from django.urls import path
from . import views
urlpatterns=[
    path('dashboard',views.dashboard,name='dashboard'),
    path('linegraph',views.linegraph,name='linegraph'),
    path('bargraph',views.bargraph,name='bargraph'),
    path('piechart',views.piechart,name='piechart')
    ]