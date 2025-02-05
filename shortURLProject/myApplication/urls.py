from django.urls import path
from . import views

app_name = 'myApplication'

urlpatterns = [
    path('', views.showIndexHTML, name='indexHTML'),
    path('simplify/', views.simplify, name='simplify'),
    path('custom/', views.customURL, name='custom'),
    path('<str:simplifiedURL>/', views.simplifyRedirect, name='redirectSimplifiedURL'),
]
