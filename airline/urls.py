from django.urls import path
from . import views

urlpatterns = [
    path('findflight/', views.findflight.as_view(), name='findflight'),
    path('bookflight/', views.bookflight.as_view(), name='bookflight'),
    path('paymentmethods/', views.paymentmethods.as_view(), name='paymentmethods'),
    path('payforbooking/', views.payforbooking.as_view(), name='payforbooking'),
    path('finalizebooking/', views.finalizebooking.as_view(), name='finalizebooking'),
    path('bookingstatus/', views.bookingstatus.as_view(), name='bookingstatus'),
    path('cancelbooking/', views.cancelbooking.as_view(), name='cancelbooking'),
]
