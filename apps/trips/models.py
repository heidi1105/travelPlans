from __future__ import unicode_literals

from django.db import models
import bcrypt, datetime


class TripManager(models.Manager):
	def reg_validator(self, postData):
		errors=[]
		if not ( postData['name'] and postData['password'] and postData['cfmpwd'] and postData['username']):
			errors.append("Look again! Some fields are not filled in")
		if len(postData['name'])<2 or not postData['name'].isalpha():
			errors.append("name should be at least 3 characters and all in LETTERS")
		if len(postData['username'])<2 or not (postData['username'].isalpha()):
			errors.append("username should be at least 3 characters and all in LETTERS")
		if len(postData['password'])<8:
			errors.append("Password should not less than 8 characters")
		if postData['password'] != postData['cfmpwd']:
			errors.append("Passwords are not the same")	
		try:
			User.objects.get(username=postData['username'])
			errors.append("You have registered already")
		except:
			pass
		if len(errors):
			return errors
		hashed=bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
		user=self.create(name=postData['name'], username=postData['username'], password=hashed)
		return user.id

	def login_validator(self, postData):
		errors=[]
		try:
			user=User.objects.get(username=postData['username'])
			hashed= User.objects.get(username=postData['username']).password
			pwcheck= postData['password']
			if bcrypt.checkpw(pwcheck.encode(), hashed.encode()):
				return user.id
			errors.append('Invalid password')
		except:
				errors.append('You have to register')
		return errors

	def add_validator(self, postData, user_id):
		errors=[]
		if not (postData['dest'] and postData['description'] and postData['startDate'] and postData['endDate']):
			errors.append("All fields must be filled in")
		try:
			start = datetime.datetime.strptime(postData['startDate'], "%Y-%m-%d")
			end = datetime.datetime.strptime(postData['endDate'], "%Y-%m-%d")
			if start < datetime.datetime.today() or end < datetime.datetime.today():
				errors.append("The start date and end date must be in the future. I guess...You don't have a time machine.")
			if end < start:
				errors.append("The end of the trip must be after ths start date of the trip")
		except:
			errors.append("The date you entered is not valid")
		if len(errors):
			return errors
		trip=Trip.objects.create(creator=User.objects.get(id=user_id), dest=postData['dest'], description=postData['description'], startDate=start, endDate=end)
		return 

	def enroll_validator(self, postData, trip_id, user_id):
		if self.get(id=user_id)==Trip.objects.get(id=trip_id).creator:
			return "You created this trip!"
#		if Trip.objects.get(id=trip_id, joined_by__id=user_id).all():
		Trip.objects.get(id=trip_id).joined_by.add(self.get(id=user_id))
		return
#		return "You have joined the trip already"
	def delete_trip(self, trip_id, user_id):
		try:
			Trip.objects.get(id=trip_id, creator__id=user_id)
			Trip.objects.filter(id=trip_id).delete()
		except:
			return "You did not create this travel plan, you cannot delete it"
		


class User(models.Model):
	username = models.CharField(max_length=255)
	name=models.CharField(max_length=255)
	password=models.CharField(max_length=255)
	objects=TripManager()
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)

class Trip(models.Model):
	dest=models.CharField(max_length=255)
	description= models.CharField(max_length=255) #do not expect a very long description
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now=True)
	startDate=models.DateField()
	endDate=models.DateField()
	creator=models.ForeignKey(User, related_name="created_trips")
	joined_by=models.ManyToManyField(User, related_name="joined_trips")





