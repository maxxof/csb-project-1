from django.urls import path

from .views import homePageView, transferView, balanceView

urlpatterns = [
    path('', homePageView, name='home'),
    path('transfer/', transferView, name='transfer'),
    path('balance/<str:username>', balanceView, name='balance'),
]