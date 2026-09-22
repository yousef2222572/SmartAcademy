from django.db import models
from django.utils import timezone

class Courses(models.Model):
    course_name = models.CharField(max_length=100)
    course_title=models.CharField(max_length=255)
    course_description=models.TextField()
    image = models.ImageField(upload_to="courses/")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor=models.ForeignKey('auth.User', on_delete=models.PROTECT)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    
class Tracks(models.Model):
    track_name = models.CharField(max_length=100)
    track_title=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course=models.ForeignKey('Courses',on_delete=models.CASCADE)


class Sections(models.Model):
    section_name = models.CharField(max_length=100)
    section_title=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    track=models.ForeignKey('Tracks',on_delete=models.CASCADE)
    
class Lessons(models.Model):
    lesson_name = models.CharField(max_length=100)
    lesson_title=models.CharField(max_length=255)
    lesson_video = models.FileField(upload_to="videos/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    section=models.ForeignKey('Sections',on_delete=models.CASCADE)

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=1)
    image = models.ImageField(upload_to="category/")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ('Category')
        verbose_name_plural = ('Categories')
        
        
    

class PlanType(models.IntegerChoices):
    FREE = 0, 'Free'
    PRO = 1, 'Pro'
    UNLIMITED = 2, 'Unlimited'


class UserPermissions(models.Model):
    user = models.OneToOneField('auth.User',on_delete=models.CASCADE)
    plan_type=models.IntegerField(choices=PlanType.choices,default=PlanType.FREE )
    own_books = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subscription_expires_at = models.DateTimeField(null=True, blank=True)


    
    
    
class Questions(models.Model):
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    lesson=models.ForeignKey(Lessons,on_delete=models.CASCADE,related_name='questions')
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Question_file(models.Model):
    file=models.FileField(upload_to='question_files/')
    question=models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='question_files')
    


    
    
class Answer(models.Model):
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    question=models.ForeignKey(Questions,on_delete=models.CASCADE,related_name='answers')
    
    
class answer_file(models.Model):
    file=models.FileField(upload_to='question_files/')
    answer=models.ForeignKey(Answer,on_delete=models.CASCADE,related_name='answers_files')
