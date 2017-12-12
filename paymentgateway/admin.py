# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.
class PGConfAdmin(admin.ModelAdmin):
    list_display = ('service_provider', 'key', 'base_url', 'surl', 'furl')


class TransactionRequestAdmin(admin.ModelAdmin):
    list_display = ('txnid', 'firstname', 'content_type', 'object_id', 'email', 'phone', 'amount')


class TransactionResponseAdmin(admin.ModelAdmin):
    list_display = ('txn_request', 'payuMoneyId', 'firstname', 'email', 'phone', 'amount', 'status', 'mode')


admin.site.register(Configuration, PGConfAdmin)
admin.site.register(TransactionRequest, TransactionRequestAdmin)
admin.site.register(TransactionResponse, TransactionResponseAdmin)
