from django.shortcuts import render 
from . import models
from django.http import HttpResponse,JsonResponse




def article_view(request,article_id):
    article=models.Article.objects.filter(pk=article_id).first()
    
    
    

    return render(request,'article.html',{'article':article})


def articless_view(request):
    articles = models.Article.objects.all()
    
    
    

    return render(request,'view_articles.html',{'articles':articles})