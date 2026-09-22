from django.urls import path 
from . import views 

urlpatterns = [

    
    path('sendaimessage/', views.messages, name='chaat_ai.send_message'),

]