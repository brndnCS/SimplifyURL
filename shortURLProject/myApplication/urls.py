from django.urls import path
from . import views

app_name = 'myApplication'

urlpatterns = [
    path('', views.showIndexHTML, name='indexHTML'),
    path('simplify/', views.simplify, name='simplify'),
    path('<str:simplifiedURL>/', views.simplifyRedirect, name='redirectSimplifiedURL')
]
