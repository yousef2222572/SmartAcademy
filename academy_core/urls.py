from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.index, name='academy.home'),
    
    path('sendmessage/', views.messages, name='academy.send_message'),
    path('lesson/<int:lesson_id>/', views.lesson, name='academy.lesson'),
    path('course_show/<int:course_id>/', views.course_show, name='academy.course.show'),
    path('courses/<int:course_id>/', views.course_detail, name='academy.course'),
    path('mycourses/', views.user_courses, name='academy.usercourses'),
    path('checkout/<int:course_id>', views.checkout, name='academy.checkout'),
    path('checkoutcomplete/', views.checkout_complete, name='academy.checkout_complete'),
    path('category/', views.category, name='academy.category_search'),
    path('categories/', views.category_detail, name='academy.category'),
    path('upgrade/', views.upgrade, name='academy.upgrade'),
    path('categories/<int:category_id>/', views.category_detail, name='academy.category'),
    path("subscribe/<str:plan>/", views.subscribe, name="subscribe"),
    
]