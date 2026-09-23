from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import stripe
from django.http import HttpResponse
from checkout import models
from academy_core import models as academy_models
from .models import Order
from academy_core.models import Courses
from django.template.loader import render_to_string
from django.core.mail import send_mail



@csrf_exempt
def stripe_webhook(request):
    print('now we are in stripe webhook')
    print('stripe webhook')
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']


    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, "your-code"
        )
    except ValueError as e:
        print('Invalid payload')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print('Invalid signature')
        return HttpResponse(status=400)

    # Handle the event
    if event and event['type'] == 'payment_intent.succeeded':
        
        payment_intent = event['data']['object']  # contains a stripe.PaymentIntent
        print('payment_intent.succeeded')
        print(payment_intent.metadata)
        transaction_id = payment_intent.metadata['transaction']
        add_permession(transaction_id)
    else:
        print('Unhandled event type {}'.format(event['type']))

    return HttpResponse(status=200)


def add_permession(transaction_id):

    transaction = models.Transaction.objects.get(pk=transaction_id)

    order = Order.objects.create(transaction=transaction)
    course = academy_models.Courses.objects.filter(pk=transaction.items).first()
    transaction.status = models.TransactionStatus.Completed
    transaction.save()

    

    permission = academy_models.UserPermissions.objects.get(
        user=transaction.user
    )

    course_id = transaction.items

    if course_id not in permission.own_books:
        
        permission.own_books.append(course_id)
        
        permission.save()
    else: return 404


    order.orderproduct_set.create(product_id=course.id, price=course.price,user=transaction.user)




    msg_html = render_to_string('emails/order.html', {
        'order': order,
        'course': course,
    })
    print(f'emil{transaction.customer_email} name {transaction.customer_name}')

    
    url = "https://api.brevo.com/v3/smtp/email" 

    headers = {
        "accept": "application/json",
        "api-key": "your-code",

        "content-type": "application/json",
    }

    payload = {
        "sender": {
            "name": "intext",
            "email": "yousefmahmoud2y1@gmail.com"
        },
        "to": [
            {
                "email":transaction.customer_email,
                "name": transaction.customer_name
            }
        ],
        "subject": "order completed",
        
        "htmlContent": msg_html
        
    }


    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        print("Brevo status:", response.status_code)
        print("Brevo response:", response.text)
    except requests.RequestException:
        return False

    return response.status_code in (200, 201)

# views.py




@csrf_exempt
def paddle_webhook(request):
    print('arrive')

    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    payload = json.loads(request.body)

    event_type = payload.get("event_type")
    data = payload.get("data", {})

    print("Paddle event:", event_type)


    if event_type == "transaction.paid":

        print("Payment completed")
        print("Transaction:", data.get("id"))


        custom_data = data.get("custom_data") or {}
        user_id = custom_data.get("user_id")

        if user_id:

            permission, created = academy_models.UserPermissions.objects.get_or_create(
                user_id=user_id
            )

            if created:
                print('new perme')

            permission.plan_type = academy_models.PlanType.PRO
            permission.save()
            print(f"User {user_id} upgraded to pro plan")
        else:
            print(" wed ont found user_id in custom_data, cannot upgrade user")


    return JsonResponse({"status": "ok"})