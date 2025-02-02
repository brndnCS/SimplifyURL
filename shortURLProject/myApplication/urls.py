from django.urls import path
from . import views

urlpatterns = [
    path('', views.showIndexHTML, name='indexHTML'),
    path('simplify/', views.simplify, name='simplify'),
    path('<str:simplifiedURL>/', views.simplifyRedirect, name='redirectSimplifiedURL')
]
