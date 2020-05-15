from django.urls import path
from .views import *

app_name = "bouquetapp"

urlpatterns = [
    path('', home, name='home'),
    path('bouquets/form', bouquet_form, name='bouquet_form'),
    path('bouquets/<int:bouquet_id>/', bouquet_details, name='bouquet'),
]
