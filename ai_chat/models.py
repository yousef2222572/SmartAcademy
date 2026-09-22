from django.db import models
from academy_core.models import Lessons

class Conversation(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lessons, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    
    
    
    
    
class Role(models.IntegerChoices):
    USER = 0, 'User'
    MODEL = 1, 'assistant'



    
class Message(models.Model):

    content = models.TextField()
    role=models.IntegerField(choices=Role.choices)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)