from django.contrib import admin

# Register your models here.
from .models import User, Offer, Transaction
admin.site.register(User)
admin.site.register(Offer)
admin.site.register(Transaction)
