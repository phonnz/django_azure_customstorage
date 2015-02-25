from django.shortcuts import render
from .models import *

def home(request):
	a = (VehicleAd.objects.all())[0]
	print a.thumb
	print '*'*20
	print a.thumb.open
	print '*'*20
	print a.thumb.url
	print '*'*20
	print '*'*20
	print '*'*20


	return render(request, 'index.html',{ })
