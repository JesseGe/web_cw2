import json
import random
import requests

from django.db.models import Count
from django.http import JsonResponse
from rest_framework.views import APIView
from itertools import chain

from .models import Flight, Order, Passenger, Payment_method
from .serializers import FlightSerializer, Pay_mSerializer, orderSerializer


# Create your views here.

class findflight(APIView):
    @staticmethod
    def get(request):
        """
        """
        req = request.query_params.dict()
        departure_date = req['departure_date']
        departure = req['departure']
        arrival = req['arrival']

        if not departure_date or not departure or not arrival:
            Data = {
                'code': '503',
                'msg': 'fail',
            }
            return JsonResponse(Data, safe=False)

        flights = Flight.objects.filter(
            departure_date=departure_date,
            departure=departure,
            arrival=arrival
        )
        Data = {
            'code': '200',
            'msg': 'successful',
        }
        serializer = FlightSerializer(flights, many=True)
        Data['data'] = serializer.data
        return JsonResponse(Data, safe=False)


class bookflight(APIView):
    @staticmethod
    def post(request):
        """
        """
        temp = []
        data = json.loads(request.body)
        flight_num = data.get("flight_num")
        passenger_name = data['passenger_name']
        order_id = data.get('order_id')
        order_price = data.get('order_price')
        ticket_time = data.get('ticket_time')
        payment_status = data.get('payment_status')

        if not flight_num or not passenger_name or not order_id or not order_price or not ticket_time \
                or not payment_status:
            Data = {'code': '503', 'msg': 'fail'}
            return JsonResponse(Data, safe=False)

        AID = random.randint(100000000, 999999999)

        list_length = len(passenger_name)

        flights = Flight.objects.get(flight_id=flight_num)
        seat = flights.seat_number
        flights.seat_number = seat - list_length
        if flights.seat_number < 0:
            Data = {'code': '503', 'msg': 'not enough seat'}
            return JsonResponse(Data, safe=False)
        flights.save()

        for item in passenger_name:
            new_Passenger = Passenger(passenger_name=item)
            new_Passenger.save()
            temp.append(new_Passenger.pk)

        new_order = Order.objects.create(order_id=order_id, order_price=order_price, ticket_time=ticket_time,
                                         payment_status=payment_status, flight_id=flight_num, AID=AID)
        new_order.passenger_id.set(temp)

        Data = {'code': '200', 'msg': 'successful', 'data': {'booking_status': 'booking successful'}}
        return JsonResponse(Data, safe=False)


class paymentmethods(APIView):
    @staticmethod
    def get(request):
        """
        """
        payment = Payment_method.objects.all()
        serializer = Pay_mSerializer(payment, many=True)
        data = serializer.data
        payment_platforms = [item['payment_platform'] for item in data]
        result = {'payment_platform': payment_platforms}
        Data = {'code': '200', 'msg': 'successful', 'data': result}
        return JsonResponse(Data, safe=False)


class payforbooking(APIView):
    @staticmethod
    def post(request):
        """
        """
        temp = []
        data = json.loads(request.body)
        payment_platform = data.get("payment_platform")
        order_id = data.get("order_id")
        if not payment_platform or not order_id:
            Data = {'code': '503', 'msg': 'fail'}
            return JsonResponse(Data, safe=False)
        order = Order.objects.get(order_id=order_id)
        AID = order.AID
        pay_m = Payment_method.objects.get(payment_platform=payment_platform)
        pay_api = pay_m.payment_api
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'orderId': order_id, 'AID': AID, 'totalAmount': order.order_price,
                           'airline': 'CandyAirline'})
        response = requests.post(pay_api, data=data, headers=headers)
        result = response.json()
        PID = result['data']['PID']
        key = result['data']['key']
        if not PID or not key:
            Data = {'code': '503', 'msg': 'fail'}
            return JsonResponse(Data, safe=False)
        order.PID = PID
        order.save()
        order.key = key
        order.save()
        order.payment_status = 1
        order.save()
        order.payment_platform = payment_platform
        order = Order.objects.filter(order_id=order_id)
        serializer = orderSerializer(order, many=True)
        Data = {'code': '200', 'msg': 'successful', 'data': serializer.data}
        return JsonResponse(Data, safe=False)


class finalizebooking(APIView):
    @staticmethod
    def post(request):
        """
        """
        temp = []
        data = json.loads(request.body)
        key = data.get("key")
        order_id = data.get("order_id")
        if not key or not order_id:
            Data = {'code': '503', 'msg': 'fail'}
            return JsonResponse(Data, safe=False)
        order = Order.objects.get(order_id=order_id)
        if key == order.key:
            Data = {'code': '200', 'msg': 'successful', 'data': {'payment_status': '1'}}
            order.payment_status = 1
            order.save()
            return JsonResponse(Data, safe=False)
        else:
            Data = {'code': '200', 'msg': 'key not equal', 'data': {'payment_status': '0'}}
            order.payment_status = 0
            order.save()
            return JsonResponse(Data, safe=False)


class bookingstatus(APIView):
    @staticmethod
    def get(request):
        """
        """
        req = request.query_params.dict()
        order_id = req['order_id']
        flight_id = Order.objects.get(order_id=order_id).flight_id
        order = Order.objects.filter(order_id=order_id).values('order_id', 'payment_status', 'ticket_time')
        flight = Flight.objects.filter(flight_id=flight_id).values('departure_date', 'arrival_date', 'flight_id',
                                                                   'departure_time', 'arrival_time', 'departure',
                                                                   'arrival')
        data = {}
        for obj in order:
            data.update({
                'order_id': obj.get('order_id'),
                'payment_status': obj.get('payment_status'),
                'ticket_time': obj.get('ticket_time'),
            })
        for obj in flight:
            data.update({
                'departure_date': obj.get('departure_date'),
                'arrive_date': obj.get('arrival_date'),
                'flight_id': obj.get('flight_id'),
                'departure_time': obj.get('departure_time'),
                'arrive_time': obj.get('arrival_time'),
                'departure': obj.get('departure'),
                'arrival': obj.get('arrival'),

            })
        Data = {'code': '200', 'msg': 'successful', 'data': data}
        return JsonResponse(Data, safe=False)


class cancelbooking(APIView):
    @staticmethod
    def post(request):
        """
        """
        temp = []
        data = json.loads(request.body)
        order_id = data.get("order_id")
        if not order_id:
            Data = {'code': '503', 'msg': 'fail'}
            return JsonResponse(Data, safe=False)
        order = Order.objects.get(order_id=order_id)
        if order.payment_status == 2:
            Data = {'code': '503', 'msg': 'Already canceled'}
            return JsonResponse(Data, safe=False)
        flight_id = Order.objects.get(order_id=order_id).flight_id
        passenger_name = Order.objects.filter(order_id=order_id).annotate(num_passengers=Count('passenger_id'))
        flights = Flight.objects.get(flight_id=flight_id)
        for num in passenger_name:
            flights.seat_number += num.num_passengers
        flights.save()
        order.payment_status = 2
        order.save()
        Data = {'code': '200', 'msg': 'successful', 'data': {'booking_status': 'Cancel successful'}}
        return JsonResponse(Data, safe=False)
