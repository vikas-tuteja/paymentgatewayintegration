# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

SERVICE_PROVIDER = (
    ('payu_paisa', 'PayU Money'),
)

VALID_PARAMS_LIST = ('firstname', 'lastname', 'key', 'txnid', 'amount', 'productinfo', 'email', 'phone', 'surl', 'furl', 'hash', 'service_provider', 'address1', 'address2', 'city', 'state', 'country', 'zipcode')

# Create your models here.
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Configuration(BaseModel):
    # All fileds here are mandatory
    service_provider = models.CharField(choices=SERVICE_PROVIDER,max_length=30,default='payu_paisa',unique=True)
    key = models.CharField(max_length=100,verbose_name="Merchant Key")
    base_url = models.CharField(max_length=100)
    base_test_url = models.CharField(max_length=100)
    surl = models.CharField(max_length=100, help_text="Callback Url when transaction is successfull.", verbose_name="Success Url")
    furl = models.CharField(max_length=100, help_text="Callback Url when transaction fails.", verbose_name="Failure Url")
    valid_param_list = models.CharField(max_length=500, help_text="Comma separated list of arguments.")
    hash_params_list = models.CharField(max_length=500, help_text="Pipe separated list of arguments from which hash needs to be prepared.")
    salt = models.CharField(max_length=50)

    def __unicode__(self):
        return self.service_provider


class TransactionRequest(BaseModel):
    # Non mandatory Generic FK - in order to relate with you applications 
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    # mandatory parameters
    payment_gateway = models.ForeignKey(Configuration)
    txnid = models.CharField(max_length=30,help_text="Unique id to transact with payU",unique=True)
    amount = models.FloatField()
    productinfo = models.CharField(max_length=300)
    firstname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.BigIntegerField()
    hash = models.CharField(max_length=500, help_text="This is an encrypted value generated to protect against data tampering during transaction")

    # non mandatory parameters
    lastname =  models.CharField(max_length=50,blank=True,null=True)
    address1 =  models.CharField(max_length=100,blank=True,null=True)
    address2 = models.CharField(max_length=100,blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=50,blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)
    zipcode =  models.IntegerField(blank=True,null=True)

    def __unicode__(self):
        return self.txnid


class TransactionResponse(BaseModel):
    txn_request = models.OneToOneField(TransactionRequest)
    status = models.CharField(max_length=50)
    payuMoneyId = models.CharField(max_length=50)
    hash = models.CharField(max_length=500, help_text="This is an encrypted value generated to protect against data tampering during transaction")
    mode = models.CharField(max_length=50)

    firstname = models.CharField(max_length=50)
    amount = models.FloatField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    productinfo = models.CharField(max_length=50)

    def __unicode__(self):
        return self.txn_request.txnid
