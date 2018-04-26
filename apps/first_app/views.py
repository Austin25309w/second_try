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
		request.session['name'] =request.POST['name']
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")
	else:
		guest = User.objects.create()
		guest.name= request.POST['name']
		guest.email = request.POST['reg_email']
		guest.password =  bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())		

		
		guest.save()
		request.session['id'] = guest.id

		messages.success(request, "successfully registered! ")
       	
		return redirect('/success')

def login(request):
	errors = User.objects.log_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")
	else:
		guest = User.objects.get(email = request.POST['log_email'])
		request.session['name'] = guest.name
		request.session['id'] = guest.id

		messages.success(request, "successfully registered! ")
		return redirect('/success')

def success (request):
	user = User.objects.get(id = request.session['id'])
	context = {
				"other_items":Quote.objects.exclude(liked_users = user),
				"my_items" : Quote.objects.filter(liked_users = user),
				# "all_item" : Quote.objects.creator.all()
			}
	return render(request,'success.html', context)

def logout(request):
	request.session.clear()
	return redirect('/')


def create(request):
	if request.method == "POST":
		errors = User.objects.quote_validator(request.POST)
		if len(errors):
			for key, value in errors.items():
				messages.error(request, value)
			return redirect("/success")
		else:
			quote = Quote.objects.create (
				name = request.POST['quote_name'],
				desc = request.POST['quote_message'],
				creator = User.objects.get(id =request.session['id'])
				)
			return redirect('/success')

def addItem(request, id):
	user = User.objects.get(id = request.session['id'])
	item = Quote.objects.get(id = id)
	user.liked_items.add(item)
	return redirect('/success')

def removeItem(request, id):
	user = User.objects.get(id = request.session['id'])
	item = Quote.objects.get(id = id)
	user.liked_items.remove(item)
	return redirect('/success')


def show(request, id):
	the_user = User.objects.get(id=id)
	user = {
		"name" : the_user.name,
		"desc" : the_user.liked_items.all().name
	}
	return render(request, "show.html", user)


























