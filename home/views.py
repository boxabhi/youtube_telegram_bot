from django.shortcuts import render

# Create your views here.
from .helpers import *
from django.http import JsonResponse

def home(request):
    data = get_cowin_data_by_pincode('226020')
    return JsonResponse({'status' : 200})