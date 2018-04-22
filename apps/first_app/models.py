
from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# Create your models here.

class userManager(models.Manager):
	def reg_validator(self, postData):
		errors ={}
		if len(postData['first_name']) < 4:
			errors['name'] = "First Name should be at least 4 characters"

		if len(postData['last_name']) < 2:
			errors['last_name'] = "Last Name should be at least 2 characters"

		if len(postData['reg_email']) < 1:
			errors['email'] = "please enter email"

		if postData['password'] != postData['con_pass']:
			errors['con_pass'] = "Please confirm your password"

		if len(postData['password']) < 8:
			errors['pw'] = "please enter more than 8 characters for your password"

		if not EMAIL_REGEX.match(postData['reg_email']):
			errors['reg_email'] = "Please enter a valid email"

		return errors 


	def log_validator(self, postData):
		errors = {}
		checkUser = User.objects.filter(email=postData['log_email'])
		checkPw = User.objects.filter(password = postData['log_password'])

		if len(postData['log_email']) < 1:
			errors['email'] = "please enter your email"
		if len(checkUser) == 0:
			errors['match'] = "invalid email and password" 
		return errors

class User(models.Model):
	first_name =models.CharField(max_length = 255)
	last_name = models.CharField(max_length = 255)
	email =	models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)	
	created_at = models.DateTimeField(auto_now_add = True)

	objects = userManager()