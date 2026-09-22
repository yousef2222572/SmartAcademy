from django.urls import path 
from . import views 

urlpatterns = [

    path('articles/', views.articless_view, name='artilces.artilces_view'),

    path('article/<int:article_id>', views.article_view, name='artilces.artilce_view'),

]