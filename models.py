import datetime
from django.utils.translation import gettext as _
from django.db import models
from django.utils import timezone
from django.conf import settings

class User(models.Model):
	'''prefs = (
		("Home", "Home"),
		("Shed", "Shed"),
		)'''

	arrangements = (
		("Please knock on the door","Please knock on the door"),
		("Please ring on the bell","Please ring on the bell"),
		("Fix up arrangements via Email","Fix up arrangements via Email"),
		)
	user_name = models.CharField(max_length=40, primary_key=True)
	#name = models.CharField(max_length=20)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	email = models.EmailField()
	password = models.CharField(max_length=20)
	confirm_password = models.CharField(max_length=20)
	zipcode = models.IntegerField(null=True)
	address = models.CharField(max_length=60)
	pickup_arrangement = models.CharField(max_length=60,choices=arrangements)
	isAdmin = models.BooleanField(default=False)

	
	'''tool_pickup_preference	= models.CharField(max_length=20, choices=prefs)
	tool_location	= models.CharField(max_length=60)'''


	def __str__(self):
		return self.user_name

class Tools(models.Model):
	tool_name = models.CharField(max_length=20)
	tool_description = models.CharField(max_length=60)
	tool_category = models.CharField(max_length=30)
	tool_address = models.CharField(max_length=120)
	#tool_pickup_preference = models.CharField(max_length=20)
	tool_condition = models.CharField(max_length=30)
	tool_owner = models.CharField(max_length=20)
	tool_zip = models.IntegerField()
	tool_borrower = models.CharField(max_length=40,blank=True)
	tool_available = models.BooleanField(default=True) #Field to show if tool is being shared right now
	tool_atHome = models.BooleanField(default=True) #Field to check if the tool is at the home or at the shed
	tool_image = models.FileField(upload_to="" , null =True, blank =True)
	tool_special = models.CharField(max_length=50, blank = True, default="None")
	#tool_image = models.FileField(upload_to="media" , null =True, blank =True)
	#'''settings.BASE_DIR + settings.MEDIA_URL'''  #this was used in the upload_to= by high-ro.
	#tool_image = models.FileField(upload_to='media', null =True, blank =True)
	tool_deadline = models.DateField(_("Date"),blank=True, null=True)
	tool_activate = models.BooleanField(default=True)
	tool_isReserved = models.BooleanField(default=False)
	tool_nextBorrower = models.CharField(max_length=30, blank=True)
	#NextDays is the field to store the number of days of a reservation.
	tool_nextDays = models.IntegerField(blank=True,null=True)
	
	

	def __str__(self):
		return self.tool_name

class Shed(models.Model):
	shed_name = models.CharField(max_length=30)
	shed_address = models.CharField(max_length=60)
	shed_zip = models.IntegerField(primary_key=True)
	shed_email = models.EmailField()

	def __str__(self):
		return self.shed_name
		
'''class ShareTool(models.Model):
	share_init = models.CharField(max_length=20)
	share_exec = models.CharField(max_length=20)
	share_tool = models.IntegerField()
	share_approval = models.NullBooleanField()
	share_days = models.IntegerField()
	# share_startdate = models.DateField(blank=False, null=False)
	# share_enddate = models.DateField(blank=False, null=False)

	def __str__(self):
		return self.share_init

'''

class Message(models.Model):
	user_borrower = models.CharField(max_length=40)
	user_owner = models.CharField(max_length=40)
	messages = models.CharField(max_length=80)
	replied = models.BooleanField(default=False)
	tool = models.CharField(max_length=60)
	tid = models.CharField(max_length=10)
	days = models.IntegerField()


	def __str__(self):
		return self.tool




#Models to keep track of each share that takes place. Can be used for statistics
class ShareTool(models.Model):
	tid = models.CharField(max_length=10)
	owner = models.CharField(max_length=30)
	borrower = models.CharField(max_length=30)
	days = models.IntegerField()
	start_date = models.DateField(_("Date"), auto_now_add=True)
	deadline = models.DateField(_("Date"))
	status = models.BooleanField(default=True)


class BannedUsers(models.Model):
	user_name = models.CharField(max_length=30)


class Notifications(models.Model):
	user_from = models.CharField(max_length=30,null=True)
	user_to = models.CharField(max_length=30)
	notification_text = models.CharField(max_length=40)
	active=models.BooleanField(default=True)
	tid = models.CharField(max_length=20,blank=True,null=True)

class RequestDeclined(models.Model):
	user_from = models.CharField(max_length=30)
	user_to = models.CharField(max_length=30)
	text = models.CharField(max_length=60)
	active = models.BooleanField(default=True)
	tid = models.CharField(max_length=10,null=True)

class ReserveMessages(models.Model):
	reserver = models.CharField(max_length=40)
	owner = models.CharField(max_length=40)
	message = models.CharField(max_length=80)
	replied = models.BooleanField(default=False)
	tid = models.CharField(max_length=10)
	days = models.IntegerField()


