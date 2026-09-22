from django.db import models

# Create your models here.





class Article(models.Model):

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    content = models.TextField()
    
    image = models.ImageField(
        upload_to='articles/',
        null=True,
        blank=True
    )
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,related_name="articles")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
