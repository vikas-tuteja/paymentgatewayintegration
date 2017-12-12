# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

from .models import *
from .serializers import *

# Create your views here.


class TransactionRequestView(generics.ListCreateAPIView):
    serializer_class = TransactionRequestSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            response = self.create(request, *args, **kwargs)
            return Response(response.data, status=response.status_code)
        except Exception as e:
            return Response({'message':str(e)}, status=200)

    

# TODO : for more secured transaction, one can re-verify the reversed hash sent by payuMoney.
class TransactionResponseView(generics.ListCreateAPIView):
    serializer_class = TransactionResponseSerializer
    template_name = "pay_response.html"
    authentication_classes = []
    
    def get_queryset(self, *args, **kwargs):
        return TransactionResponse.objects.filter(txn_request=self.txnreqid)

    def get_serializer(self, *args, **kwargs):
        self.data = self.request.POST.dict()
        self.set_transaction_request()
        serialized = self.serializer_class(data=self.data)
        serialized.is_valid()
        return serialized


    def post(self, request, *args, **kwargs):
        """
            payU is going to call the response api (surl / furl) using post method.
            Wwe will show the success/failure page after
            saving this response in transaction response table

        """
        try:
            response = self.create(request, *args, **kwargs)
        except Exception as e:
            pass

        return self.list(self, *args, **kwargs)

    
    def set_transaction_request(self):
        self.txnreqid = TransactionRequest.objects.get(txnid=self.data['txnid']).pk
        self.data['txn_request'] = self.txnreqid
