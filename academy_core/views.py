from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json
from ai_chat import models as ai_models
from . import models
from django.http import HttpResponse,JsonResponse
from django.utils.timesince import timesince
from django.contrib.humanize.templatetags.humanize import naturaltime






def index (request):
    courses = models.Courses.objects.all()
    categories = models.Category.objects.all()

    context = {'courses': courses, 'categories': categories}

    return render(request, 'index.html', context)


def courses (request):
    courses = models.Courses.objects.all()
    context = {'courses': courses}
    return render(request, 'courses.html', context)

def category_detail(request, category_id=None):
    category = models.Category.objects.filter(id=category_id).first() if category_id else None
    courses = models.Courses.objects.all()

    if category:
        courses = courses.filter(category=category)

    paginator = Paginator(courses, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {
        'category': category,
        'categories': models.Category.objects.all(),
        'page_obj': page_obj,
    }
    return render(request, 'category.html', context)



def category(request, category_id=None):
    category = None

    if not category_id:
        category_id = request.GET.get('category')

    query = request.GET.get('query')

    where = {}

    if category_id:
        category = models.Category.objects.filter(pk=category_id).first()
        if category:
            where['category_id'] = category_id

    courses = models.Courses.objects.filter(**where)

    if query:
        courses = courses.filter(
            Q(course_name__icontains=query) |
            Q(course_title__icontains=query) |
            Q(course_description__icontains=query)
        )

    paginator = Paginator(courses, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'category': category,
        'categories': models.Category.objects.all(),
        'page_obj': page_obj,
        'query': query or '',
    }

    return render(request, 'category.html', context)

def checkout_complete(request):
    return render(
       request, 'checkout-complete.html'
    )


def upgrade(request):
    return render(
       request, 'plans.html'
    )


def course_detail(request, course_id):
    course=models.Courses.objects.filter(id=course_id).first()
    
    context = {'course': course}

    return render(request, 'course_detail.html', context)

@login_required
def user_courses(request):

        
    # course=models.Courses.objects.filter(user=request.user).values()
    course_Permissions, _ = models.UserPermissions.objects.get_or_create(
        user=request.user
    )
        
    temporary_courses=None
        
        
        
        
    if course_Permissions.plan_type==1 or course_Permissions.plan_type==2:
        temporary_courses = models.Courses.objects.all()

    own_courses = None


    if course_Permissions.own_books:

        own_courses = models.Courses.objects.filter(
            id__in=course_Permissions.own_books
        )
        
    
    context = {'own_courses': own_courses,"temporary_courses":temporary_courses}

    return render(request, 'user_courses.html', context)



# def course_view (request):

def course_show(request, course_id):
    course=models.Courses.objects.filter(id=course_id).first()
    Tracks=models.Tracks.objects.filter(course=course)
    
    context = {'course': course,"tracks":Tracks}

    return render(request, 'course_show.html', context)

    
# def course_show(request, lesson_id):

#     lesson=models.Tracks.objects.filter(track_id=lesson_id).first()
    
#     context = {'lesson': lesson}

#     return render(request, 'lesson.html', context)

@login_required
def lesson(request, lesson_id):
    
    lesson = models.Lessons.objects.get(id=lesson_id)

    questions = []
    messages = []

    if lesson:
        permissions, created = models.UserPermissions.objects.get_or_create(
            user=request.user
        )
        course_id = lesson.section.track.course.id

        if course_id in permissions.own_books or permissions.plan_type in [1, 2]:
            
            questions = models.Questions.objects.filter(lesson=lesson).all()
            conversation = ai_models.Conversation.objects.filter(lesson=lesson).first()
            messages = ai_models.Message.objects.filter(conversation=conversation).all()
    
    context = {'lesson': lesson, 'questions': questions, 'messages': messages}
    return render(request, 'lesson.html', context)

def messages(request):
    
    if request.method == 'POST':

        message = request.POST.get('message')
        lesson_id = request.POST.get('lesson_id')
        type_question = int(request.POST.get('type_bool'))
        files = request.FILES.getlist('files')

        lesson = models.Lessons.objects.filter(id=lesson_id).first()

        permissions, _ = models.UserPermissions.objects.get_or_create(
            user=request.user
        )

        if lesson:
            course_id = lesson.section.track.course.id

            
            if type_question==0:
                
                if course_id in permissions.own_books or permissions.plan_type in [1,2]:

                    message_add=models.Questions.objects.create(question=message,lesson=lesson,user=request.user)
                    message=message_add.question

                    print(message_add,'question added')
                    if files:
                        for file in files:
                            models.Question_file.objects.create(file=file,question=message_add)
            
                    data={
                        'message':message,
                        'id':message_add.id,
                        'user_name':message_add.user.username,
                        'time': naturaltime(message_add.created_at)

                    }
                    print(data)
            else:

                question_id = request.POST.get('question_id')
                print(question_id)
                
                if course_id in permissions.own_books or permissions.plan_type in [1,2]:
                    message_add=models.Answer.objects.create(answer=message,question_id=question_id,user=request.user)
                    message=message_add.answer
                    
                    if files:
                        
                        for file in files:
                            
                            models.answer_file.objects.create(file=file,answer=message_add)
                    data={
                        'message':message,
                        'user_name':message_add.user.username,
                        'message_reply_id':message_add.question_id,
                        'time': naturaltime(message_add.created_at)
                        
                    }
        
        
            
                    
                
            
            
            
            
                

            
            
            
        
            
        lesson=models.Lessons.objects.filter(id=lesson_id).first()
        

        return JsonResponse(data)

        
        

def checkout(request,course_id):


    user_info=request.user
    return render(
        request, 'checkout.html',{'user_info':user_info,'course_id':course_id}
    )





@login_required
def subscribe(request, plan):

    print('arrive')
    if plan == "pro":
        price_id = "pri_01m2vm34x5k72g13nx4e40zhc7"
        print('done')

    else:
        return render(request, "subscribe.html")
    user_id=request.user.id

    return render(request, "subscribe.html", {
        'user_id':user_id,
        "plan": plan,
        "price_id": price_id,
        "paddle_client_token": 'test_0f53b608fd344671e04ddea1a3e',
    })
    
    
    
    