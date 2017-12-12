from django.conf.urls import url
from paymentgateway.views import TransactionRequestView, TransactionResponseView

app_name = "paymentgateway"

urlpatterns = [    
    url(r'^paymentgateway/transactionrequest/add/', TransactionRequestView.as_view(), name="transactionrequest"),
    url(r'^paymentgateway/transactionresponse/(?P<status>[a-z]+)/', TransactionResponseView.as_view(), name="transactionresponse"),
]
