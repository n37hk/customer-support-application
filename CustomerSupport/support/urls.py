from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
   path('service-providers', views.service_providers),
   path('service-providers/add', views.service_providers_add),
   path('service-providers/remove', views.service_providers_remove),
   path('enquiries', views.customer_enquiries),
   path('query/<str:service_provider>', views.customer_query_form),
   path('query/submit/<str:service_provider>', views.customer_query),
   path('query/status/success', views.enquiry_received),
   path('response/<int:enqid>', views.repsonse_form),
   path('response/submit/<int:enqid>', views.enquiry_response),
   path('review/<int:enqid>', views.review_form),
   path('review/submit/<int:enqid>', views.support_review)
]

# To serve static files from app folder
urlpatterns += staticfiles_urlpatterns()