
import os
import json
import random
import sqlite3
import time
from datetime import datetime, timedelta
from multiprocessing import Process

from urllib.parse import quote, unquote
from django.core.mail import send_mail
from django.core import serializers
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.db.models import Q
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response

from support.models import CustomerEnquiry, ServiceProvider
from CustomerSupport import settings

def formatDateTimeFromUTC(dt):
    if(dt is not None):
        return datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%d/%m/%Y %H:%M:%S')
    else:
        return dt

@api_view(['GET'])
def service_providers(request):
    # view service providers
    service_provider_list = ServiceProvider.objects.all()
    service_provider_list = serializers.serialize('json', service_provider_list)
    service_provider_list = json.loads(service_provider_list)
    service_providers = dict()
    service_providers['headers'] = ['ID', 'Name', 'Email', 'Added On']
    service_providers['rows'] = list()
    for p in service_provider_list:
        service_providers['rows'].append([
            p['fields']['service_provider_id'],
            p['fields']['name'],
            p['fields']['email_id'],
            formatDateTimeFromUTC(p['fields']['added_on'])
        ])
    
    # print(f'Service Providers List: {service_providers}')
    template = get_template('service_providers.html')
    context = {
        'service_provider_list': service_providers,
    }
    return HttpResponse(template.render(context, request), status=200)

@api_view(['POST'])
def service_providers_add(request):
    # Add Service Providers
    service_provider_name = request.data['name']
    service_provider_email = request.data['email']

    id_num = random.randint(0,99999)
    service_provider_id = 'SP'+str(id_num)
    while(ServiceProvider.objects.filter(service_provider_id=service_provider_id).exists()):
        id_num = random.randint(0,99999)
        service_provider_id = 'SP'+str(id_num)

    ServiceProvider.objects.create(service_provider_id=service_provider_id, name=service_provider_name, email_id=service_provider_email, added_on=datetime.now())    
    return redirect('/support/service-providers')

@api_view(['DELETE'])
def service_providers_remove(request):
    # Delete service providers
    service_provider_id= request.data['id']
    ServiceProvider.objects.filter(service_provider_id=service_provider_id).delete()    
    return Response({'message', 'Entry deleted'}, status=200)

@api_view(['GET'])
def customer_query_form(request, service_provider):
    # enquiry form
    template = get_template('enquiry_form.html')
    context = {
        'service_provider': service_provider,
    }
    return HttpResponse(template.render(context, request), status=200)

@api_view(['POST'])
def customer_query(request, service_provider):
    # submit enquiry
    customer_name = request.data['name']
    customer_email = request.data['email']
    customer_phone = request.data['phone']
    customer_query_text = request.data['query']

    enq = CustomerEnquiry.objects.create(name=customer_name, email_id=customer_email, phone_number=customer_phone, query=customer_query_text, received_on=datetime.now(), service_provided_by=service_provider)

    service_provider_email = ServiceProvider.objects.get(service_provider_id=service_provider).email_id

    # url to response form sent to service provider
    feedback_form_url = settings.CURRENT_HOST+f'/support/response/{enq.id}'

    plain_message = f'Please visit the following url to view the enquiry:\n{feedback_form_url}'
    html_message = f'<html><body>Please visit the following url to view the enquiry:</br>{feedback_form_url}</body></html>'

    # send to service provider
    send_mail(
        f'Customer Enquiry {enq.id}',
        plain_message,
        settings.EMAIL_HOST_USER,
        [service_provider_email],
        fail_silently=False,
        html_message=html_message
    )
    
    return redirect('/support/query/status/success')

@api_view(['GET'])
def enquiry_received(request):
    template = get_template('message_page.html')
    context = {
        'message_head': 'Enquiry Received',
        'message_body': 'We have forwarded your enquiry to our support team. They will get back to you shortly.'
    }
    return HttpResponse(template.render(context, request), status=200)

@api_view(['GET'])
def customer_enquiries(request):
    # View enquiries
    customer_enquiry_list = CustomerEnquiry.objects.all()
    customer_enquiry_list = serializers.serialize('json', customer_enquiry_list)
    customer_enquiry_list = json.loads(customer_enquiry_list)
    enquiries = dict()
    
    enquiries['headers'] = ['Name', 'Email', 'Phone Number', 'Query', 'Received On', 'Service Provider', 'Reply', 'Replied On', 'Satisfaction', 'Review Mail']
    enquiries['rows'] = list()
    for e in customer_enquiry_list:
        enquiries['rows'].append([
            e['fields']['name'],
            e['fields']['email_id'],
            e['fields']['phone_number'],
            e['fields']['query'],
            formatDateTimeFromUTC(e['fields']['received_on']),
            e['fields']['service_provided_by'],
            e['fields']['reply'],
            formatDateTimeFromUTC(e['fields']['replied_on']),
            e['fields']['satisfaction'],
            e['fields']['review_mail']
        ])
    
    # print(f'Service Providers List: {service_providers}')
    template = get_template('customer_enquiries.html')
    context = {
        'customer_enquiry_list': enquiries,
    }
    return HttpResponse(template.render(context, request), status=200)

@api_view(['GET'])
def repsonse_form(request, enqid):
    template = get_template('response_form.html')
    context = {
        'name': CustomerEnquiry.objects.get(pk=enqid).name,
        'email': CustomerEnquiry.objects.get(pk=enqid).email_id,
        'phone': CustomerEnquiry.objects.get(pk=enqid).phone_number,
        'query': CustomerEnquiry.objects.get(pk=enqid).query,
        'id': enqid
    }
    return HttpResponse(template.render(context, request), status=200)

@api_view(['POST'])
def enquiry_response(request, enqid):
    # record and send response to customer
    reply = request.data['response']

    if(CustomerEnquiry.objects.filter(pk=enqid).exists()):
        CustomerEnquiry.objects.filter(pk=enqid).update(reply=reply, replied_on=datetime.now())
        query = CustomerEnquiry.objects.get(pk=enqid).query
        customer_email = CustomerEnquiry.objects.get(pk=enqid).email_id

        # Mail body
        plain_message = f'Your Query:\n{query}\n\n' # if html is not supported by email provider
        plain_message += f'Response:\n{reply}'
        html_message = f'<html><body>Your Query:</br>{query}</br></br>Response:</br>{reply}</body></html>'

        send_mail(
            f'Customer Enquiry {enqid}',
            plain_message,
            settings.EMAIL_HOST_USER,
            [customer_email],
            fail_silently=False,
            html_message=html_message
        )

        template = get_template('message_page.html')
        context = {
            'message_head': 'Response Submitted',
            'message_body': 'Your response has been recorded and sent to the customer'
        }
        return HttpResponse(template.render(context, request), status=200)
    else:
        template = get_template('message_page.html')
        context = {
            'message_head': 'No Such Enquiry Found',
            'message_body': 'Unable to find an enquiry corresponding to your response. Please contact the admin to report any irregularities'
        }
        return HttpResponse(template.render(context, request), status=404)

@api_view(['GET'])
def review_form(request, enqid):
    exp = int(request.query_params['exp']) # url validity time

    if(exp < int(datetime.now().timestamp())): # check url validity 30 min
        template = get_template('message_page.html')
        context = {
            'message_head': 'URL Expired',
            'message_body': 'This URL is no longer valid'
        }
        return HttpResponse(template.render(context, request), status=200)
    else:
        template = get_template('review_form.html')
        context = {
            'id': enqid
        }
        return HttpResponse(template.render(context, request), status=200)

@api_view(['POST'])
def support_review(request, enqid):
    # record customer review
    review = request.data['review']

    if(CustomerEnquiry.objects.filter(pk=enqid).exists()):
        CustomerEnquiry.objects.filter(pk=enqid).update(satisfaction=review)
        template = get_template('message_page.html')
        context = {
            'message_head': 'Thank You!',
            'message_body': 'Your response has been recorded'
        }
        return HttpResponse(template.render(context, request), status=200)
    else:
        template = get_template('message_page.html')
        context = {
            'message_head': 'No Such Enquiry Found',
            'message_body': 'Unable to find an enquiry corresponding to your response. Please contact the admin to report any irregularities'
        }
        return HttpResponse(template.render(context, request), status=404)

def get_utctimestamp(dt=None, seconds=0, minutes=0, days=0):
    if(dt is None):
        return int(time.mktime((datetime.now()+timedelta(seconds=seconds, minutes=minutes, days=days)).timetuple()))
    else:
        return int(time.mktime((dt+timedelta(seconds=seconds, minutes=minutes, days=days)).timetuple()))

def loadUTCDateTime(dt):
    return datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.%fZ')

def send_review_mail():
    print('Review Mail Watchdog Running...')
    while(True):
        enquiry_list = CustomerEnquiry.objects.all()
        enquiry_list = serializers.serialize('json', enquiry_list)
        enquiry_list = json.loads(enquiry_list)

        for e in enquiry_list:
            uid = e['pk']
            if(e['fields']['replied_on'] is None):
                continue

            e_ts = loadUTCDateTime(e['fields']['replied_on'])
            # generate timestamp to check review email delay 60 min
            email_delay = get_utctimestamp(e_ts, minutes=settings.EMAIL_DELAY)
            current_ts = int(datetime.now().timestamp())
            review_mail = e['fields']['review_mail']

            # check if email delay time is reached
            if((current_ts >= email_delay) and (review_mail == 'pending')):
                # generate review url validity timestamp
                exp_time = get_utctimestamp(minutes=settings.REVIEW_URL_VALIDITY)
                service_provider = e['fields']['service_provided_by']
                service_provider_email = ServiceProvider.objects.get(service_provider_id=service_provider).email_id
                review_form_url = settings.CURRENT_HOST+f'/support/review/{uid}?exp={exp_time}'
                customer_mail = e['fields']['email_id']

                plain_message = f'Please visit the following link to review our support services so we can better serve you in the future:\n{review_form_url}'
                html_message = f'<html><body>Please visit the following link to review our support services so we can better serve you in the future::</br>{review_form_url}</body></html>'

                send_mail(
                    f'Customer Enquiry {uid}',
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [customer_mail],
                    fail_silently=False,
                    html_message=html_message
                )
                CustomerEnquiry.objects.filter(pk=uid).update(review_mail='sent')

p = Process(target=send_review_mail)
p.start()