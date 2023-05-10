from django.db import models
from datetime import datetime


class Flight(models.Model):
    objects = models.Manager()
    flight_id = models.CharField(max_length=10, null=False)
    airline = models.CharField(max_length=50, null=False)
    departure_date = models.DateField(null=False)
    arrival_date = models.DateField(null=False)
    departure_time = models.TimeField(auto_now=False, auto_now_add=False)
    arrival_time = models.TimeField(auto_now=False, auto_now_add=False)
    departure = models.CharField(max_length=50, null=False)
    arrival = models.CharField(max_length=50, null=False)
    flight_price = models.IntegerField(null=False)
    seat_number = models.IntegerField(null=False)


class Order(models.Model):
    objects = models.Manager()
    order_id = models.IntegerField(null=False)
    AID = models.IntegerField(null=False)
    PID = models.IntegerField(null=True)
    flight_id = models.CharField(max_length=10, null=False)
    order_price = models.IntegerField(null=True)
    ticket_time = models.DateTimeField(null=True)
    payment_status = models.SmallIntegerField(null=True)
    key = models.CharField(max_length=50,null=True)
    payment_platform = models.CharField(max_length=50, null=True)
    passenger_id = models.ManyToManyField(to='passenger')



class Passenger(models.Model):
    passenger_name = models.CharField(max_length=50, null=False)

    class Meta:
        db_table = 'passenger'

class Payment_method(models.Model):
    objects = models.Manager()
    payment_platform = models.CharField(max_length=50, null=False)
    payment_api = models.CharField(max_length=200, null=True)
