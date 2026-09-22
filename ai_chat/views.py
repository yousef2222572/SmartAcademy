from django.shortcuts import render
from . import models
from academy_core import models as academy_models
from django.http import JsonResponse, StreamingHttpResponse
from openai import OpenAI



deepseek_client = OpenAI(
    api_key="i remove", 
    base_url="https://api.deepseek.com"
)



def messages(request):
    
    if request.method == 'POST':


        message = request.POST.get('message')
        lesson_id = request.POST.get('lesson_id')


        lesson = academy_models.Lessons.objects.filter(id=lesson_id).first()

        permissions = academy_models.UserPermissions.objects.filter(
            user=request.user
        ).first()

        print('1not')
        if lesson:
            print('1pass')


            

            

            if permissions.plan_type in [1,2]:
                print('2pass')
                
                conversation = models.Conversation.objects.filter(lesson=lesson,user=request.user).first()
                if not conversation:

                    conversation=models.Conversation.objects.create(lesson=lesson,user=request.user)
                if conversation:
                    print('3pass')
                    
                
                    
                    messages_saved=models.Message.objects.filter(conversation=conversation).values('role','content')
                    all_messages=[]
                    
                    print(messages_saved)
                    for msg in messages_saved:


                        if msg['role'] == 0:
                            role_string='user'
                        else:
                            role_string='assistant'
                            
                            
                        all_messages.append({
                            "role": role_string,
                            "content": msg['content']
                        })
                        
                    
                    messages_list=list(all_messages)
                    
                    message_add=models.Message.objects.create(content=message,conversation=conversation,role=0)
                    
                    
                    message_system={'role':'system','content':f"you are a assistant into a smart academy that use ai to explain for the student the things they aren't now it and you will answer on them questions and you are exisst into a box under the video box and this is the lesson title {lesson.lesson_name} and this is the lesson descrption {lesson.lesson_title} "}
                    messages_list.append(message_system)
                    message={'role':'user','content':message_add.content}
                    
                    messages_list.append(message)
                    deepseek_model="deepseek-v4-flash"
                    thinking=None
                    
                    print(messages_list)

                    response = deepseek_client.chat.completions.create(
                        model=deepseek_model,                                                                                                                                                
                        messages=messages_list,
                        temperature=0.5,
                        top_p = 0.9,
                        stream=True  ,
                        max_tokens=15000,
                        reasoning_effort=thinking
                    )
                    
                    






                    

                    
                    def generate():
                        full_response = "" 
                        try:
                            
                            for chunk in response:
                                text_piece = chunk.choices[0].delta.content
                                if text_piece:
                                    full_response += text_piece
                                    yield text_piece
                                        
                        except Exception as e:
                            print(f"error :{e}")
                            
                        finally:

                            if full_response.strip():
                                
                                message_add=models.Message.objects.create(content=full_response,conversation=conversation,role=1)
                                


                    return StreamingHttpResponse(generate(), content_type='text/plain')

                    
                    
                    
                    # data={
                    #     'message':message,
                    #     'id':message_add.id,
                    #     'user_name':message_add.user.username,
                    #     'time': naturaltime(message_add.created_at)

                    # }

            else:
                print('4not')


                data={

                    'message':'plsease subscribe',

                    
                }
                return JsonResponse(data)
                
        
        
            
                    
                
            
            
            
            
                

            
            
            
        
            

        


