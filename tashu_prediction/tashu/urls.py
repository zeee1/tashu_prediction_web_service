from django.urls import path

from . import views

app_name = "tashu"
urlpatterns = [
	path('', views.index, name = 'index'),
	path('tashuStatus/', views.tashuStatus, name = 'tashuStatus'),
]
