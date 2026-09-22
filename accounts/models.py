from django.db import models


class VerificationCode(models.Model):
    email = models.EmailField(db_index=True)
    code = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.email} - {self.code}"
    
    
class vendor(models.Model):
    user=models.OneToOneField('auth.User',on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    logo=models.ImageField(upload_to="vendors/", blank=True, null=True)
    description=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"