from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt
# Create your views here.

def index(request):
	
	return render(request,"login_reg.html")

def validate(request):
	# if request.method == "POST":
	errors = User.objects.reg_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")
	else:
		guest = User.objects.create()
		guest.first_name = request.POST['first_name']
		guest.last_name = request.POST['last_name']
		guest.email = request.POST['reg_email']
		guest.password =  bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		print(guest.password)
		# .encode(),bcrypt.gensalt()
		# guest.password = bcrypt.
		guest.save()
		# request.session['first_name'] = request.POST['first_name']
		# request.session['last_name'] = request.POST['last_name']
		request.session['id'] = guest.id
		messages.success(request, "successfully registered! ")
       	# redirect to a success route
		return redirect('/success')

def login(request):
	errors = User.objects.log_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")
	else:
		guest = User.objects.get(email = request.POST['log_email'])
		# request.session['email'] = request.POST['log_email']
		request.session['id'] = guest.id
		messages.success(request, "successfully registered! ")
		return redirect('/success')

def success (request):

	return render(request,'success.html')

def logout(request):
	request.session.clear()
	return redirect('/')