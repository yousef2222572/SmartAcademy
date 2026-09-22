from django.contrib import admin

from .import models 




admin.site.register(models.Courses)
admin.site.register(models.Category)
admin.site.register(models.Tracks)
admin.site.register(models.Sections)
admin.site.register(models.Lessons) 

admin.site.register(models.Questions) 
admin.site.register(models.Question_file) 
admin.site.register(models.Answer) 
admin.site.register(models.answer_file) 

admin.site.register(models.UserPermissions) 