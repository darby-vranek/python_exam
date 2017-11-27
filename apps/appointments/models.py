from __future__ import unicode_literals
from django.db import models
from collections import namedtuple
import bcrypt
import re
from datetime import date
import time

error_message = namedtuple('Error_Message', 'field message')
re_email = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


class UserManager(models.Manager):
	def validate(self, post):
		messages = list()
		# validate name
		if len(post['name']) < 2:
			messages.append(error_message('name', 'Name must be at least 2 characters long'))
		if not re.match(r"[A-Za-z\s-]+", post['name']):
			messages.append(error_message('name', 'Name contains invalid characters'))
		# validate emaill
		if not post['email']:
			messages.append(error_message('email', 'Email is required'))
		elif not re_email.match(post['email']):
			messages.append(error_message('email', 'Invalid email address'))
		elif len(User.objects.filter(email=post['email'])) != 0:
			messages.append(error_message('email', 'Email is already registered'))
		# validate password
		if len(post['password']) < 8:
			messages.append(error_message('password', 'Password must be at least 8 characters long'))
		elif post['password'] != post['confirm_password']:
			messages.append(error_message('password', 'Passwords do not match'))
		# validate date of birth
		# CURRENTLY NOT WORKING!!!!!
		# if post['date_of_birth'] >= date.today():
		# 	messages.append(error_message('date_of_birth', 'Invalid date of birth'))
		return messages


	def log_in(self, post):
		error_messages = list()
		# check that a record with
		if not User.objects.filter(email=post['email']):
			error_messages.append(error_message('login_email', 'Email has not been registered'))
		elif not bcrypt.checkpw(post['password'].encode(), User.objects.get(email=post['email']).password.encode()):
			error_message.append(error_message['login_password'], 'Incorrect password')
		return error_messages


class User(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	date_of_birth = models.DateField()
	objects = UserManager()


class AppointmentManager(models.Manager):
	def validate(self, post):
		print post['time']
		error_messages = list()
		if not post['tasks']:
			error_messages.append(error_message('tasks', 'Tasks field is required'))
		# I'm not sure if I should add anything in here to validate the select field -- I'll leave that until a little bit later
		if not post['date']:
			error_messages.append(error_message('date', 'Date field is required'))
		if not post['time']:
			error_messages.append(error_message('time', 'Time field is required'))
		# I'm going to first validate to make sure all fields are filled in - if they aren't, return here. Don't validate the rest until all fields are confirmed present
		if error_messages:
			return error_messages
		if post['date'] < date.today().isoformat():
			error_messages.append(error_message('date', 'Date must be now or later'))
		elif post['date'] == date.today().isoformat():
			print 'successfully compared dates'
			if post['time'] < time.strftime('%H:%M'):
				error_messages.append(error_message('time', 'Times today must be now or later'))
		return error_messages


class Appointment(models.Model):
	user = models.ForeignKey(User, related_name='appointments')
	tasks = models.TextField()
	status = models.CharField(max_length=10)
	date = models.DateField()
	time = models.TimeField()
	objects = AppointmentManager()
