from django.contrib import admin
from .models import Flight
from .models import Order
from .models import Passenger, Payment_method

admin.site.register(Flight)
admin.site.register(Order)
admin.site.register(Passenger)
admin.site.register(Payment_method)


# Register your models here.
