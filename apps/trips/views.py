from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
	if 'id' in request.session:
		return redirect("/travels")

	return render (request, "trips/index.html")

def dashboard(request):
	user= User.objects.get(id=request.session['id'])

	context={
		'user': user,
		'trips': Trip.objects.all().exclude(creator=user).exclude(joined_by=user)
	}

	return render (request, "trips/dashboard.html", context)

def destination(request, id=id):

	return render (request, "trips/destination.html", {'trip': Trip.objects.get(id=id)})

def add(request):

	return render (request, "trips/add.html")


def login(request):
	if request.method=='POST':
		check=User.objects.login_validator(request.POST)
		if isinstance(check, list):
			messages.error(request, check[0], extra_tags='login')		
			return redirect("/")
		else:				
			request.session['id'] = check
			return redirect ("/travels")
	else:
		messages.error("You do not have the permission to access this page")
		return redirect("/")

def register(request):
	if request.method=='POST':
		check=User.objects.reg_validator(request.POST)
		if isinstance(check, list):
			for error in check:
				messages.error(request, error, extra_tags='register')		
			return redirect("/")
		else:
			request.session['id']=check
			return redirect ("/travels")
	else:
		messages.error("You do not have the permission to access this page")
		return redirect("/")

	return redirect("/")

def logout(request):
	request.session.clear()
	return redirect ("/")

def enrolling(request, id=id):
	check=User.objects.enroll_validator(request.POST, id, request.session['id'])
	if check:
		messages.error(request, check)
	return redirect("/")

def adding(request):
	if request.method=='POST':
		check=User.objects.add_validator(request.POST, request.session['id'])
		if isinstance(check, list):
			for error in check:
				messages.error(request, error)
			return redirect("/travels/add")
		else:
			return redirect("/")
	else:
		messages.error("You do not have the permission to access this page")
		return redirect("/travels/add")


def delete(request, id=id):
	check=User.objects.delete_trip(id, request.session['id'])
	if check:
		messages.error(request, check)

	return redirect("/travels")



			
