from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User, Appointment
import bcrypt
from datetime import date
import time

# helper functions
def log_errors(request, errors):
	for message in errors:
		messages.add_message(request, messages.ERROR, message.message, extra_tags=message.field)

# routes
def index(request):
	if 'logged_in' in request.session:
		return redirect('/appointments/')
	return render(request, 'appointments/index.html')


def register(request):
	post = request.POST
	error_messages = User.objects.validate(post)
	if error_messages:
		log_errors(request, error_messages)
		return redirect('/')
	User.objects.create(
		name=post['name'],
		email=post['email'],
		password=bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt()),
		date_of_birth=post['date_of_birth']
	)
	request.session['logged_in'] = User.objects.last().id
	return redirect('/appointments/')


def log_in(request):
	errors = User.objects.log_in(request.POST)
	if errors:
		log_errors(request, errors)
		return redirect('/')
	request.session['logged_in'] = User.objects.get(email=request.POST['email']).id
	return redirect('/appointments/')


def log_out(request):
	del request.session['logged_in']
	return redirect('/')


def show_appointments(request):
	user = User.objects.get(id=request.session['logged_in'])
	today = Appointment.objects.filter(user=user).filter(date=date.today())
	upcoming = Appointment.objects.filter(user=user).exclude(date=date.today())
	return render(request, 'appointments/appointments.html', context={'user': user, 'today': today, 'upcoming': upcoming})


def edit_appointment(request, id):
	return render(request, 'appointments/update.html', context={'appointment': Appointment.objects.get(id=id)})


def update_appointment(request, id):
	post = request.POST
	errors = Appointment.objects.validate(post)
	if errors:
		log_errors(errors)
		return redirect('/appointments/%s/' % id)
	Appointment.objects.filter(id=id).update(
		tasks=post['tasks'],
		status=post['status'],
		date=post['date'],
		time=post['time']
	)
	return redirect('/appointments/')



def delete_appointment(request, id):
	Appointment.objects.get(id=id).delete()
	return redirect('/appointments/')


def create_appointment(request):
	post = request.POST
	errors = Appointment.objects.validate(post)
	if errors:
		log_errors(request, errors)
		return redirect('/appointments/')
	Appointment.objects.create(
		user=User.objects.get(id=request.session['logged_in']),
		tasks=post['tasks'],
		status='Pending',
		date=post['date'],
		time=post['time']
	)
	return redirect('/appointments/')
