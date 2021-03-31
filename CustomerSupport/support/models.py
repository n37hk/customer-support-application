from django.db import models

class ServiceProvider(models.Model):
    class Meta:
        app_label = 'support'
        db_table = 'service_provider'
    
    service_provider_id = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=320)
    email_id = models.CharField(max_length=320)
    added_on = models.DateTimeField()

class CustomerEnquiry(models.Model):
    class Meta:
        app_label = 'support'
        db_table = 'customer_enquiry'

    name = models.CharField(max_length=320)
    email_id = models.CharField(max_length=320)
    phone_number = models.CharField(max_length=15)
    query = models.TextField()
    received_on = models.DateTimeField()
    service_provided_by = models.CharField(max_length=12)
    reply = models.TextField()
    replied_on = models.DateTimeField(null=True)
    satisfaction = models.CharField(max_length=15)
    review_mail = models.CharField(max_length=10, default='pending')

