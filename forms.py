from django import forms
from django.forms import ModelForm , Textarea , TextInput , PasswordInput , Select
from . import models
from django.utils.translation import ugettext_lazy as _
import re


class Registration(forms.ModelForm):
	class Meta:
		model = models.User

		'''prefs = (
		("Home", "Home"),
		("Shed", "Shed")
		# ('Other','Other'),
		)'''

		arrangements = (
		("Please knock on the door","Please knock on the door"),
		("Please ring on the bell","Please ring on the bell"),
		("Fix up arrangements via Email","Fix up arrangements via Email"),
		)

		fields = ['user_name','first_name','last_name','password','confirm_password','email','zipcode','address','pickup_arrangement']#,'tool_pickup_preference']
		widgets = {
			'user_name': TextInput(attrs={'id' : 'username', 'class' : 'form-control','MAXLENGTH':'16'}),
			#'name': TextInput(attrs={'id' : 'name', 'class' : 'form-control','MAXLENGTH':'20'}),
			'first_name': TextInput(attrs={'id' : 'name', 'class' : 'form-control','MAXLENGTH':'20'}),
			'last_name': TextInput(attrs={'id' : 'name', 'class' : 'form-control','MAXLENGTH':'20'}),
			'email': TextInput(attrs={'id' : 'email', 'class' : 'form-control','MAXLENGTH':'30'}),
			'password': PasswordInput(attrs={'id' : 'password', 'class' : 'form-control','MAXLENGTH':'16'}),
			'confirm_password': PasswordInput(attrs={'class':'form-control','MAXLENGTH':'16'}),
			'zipcode': TextInput(attrs={'id' : 'zipcode', 'class' : 'form-control','MAXLENGTH':'5'}),
			'address': Textarea(attrs={'class' : 'form-control', 'rows' : '5','MAXLENGTH':'25'}),
			'pickup_arrangement': Select(attrs={'id' : 'arrangements', 'class':'form-control','choices':'arrangements'}),
			#'tool_pickup_preference': Select(attrs={'id' : 'toolpref', 'class':'form-control','choices':'prefs'}),
			# 'tool_location': Textarea(attrs={'id' : 'toolloc', 'class' : 'form-control hidden', 'placeholder' : 'Tool Location'}),
		}
		
		labels = {
			"user_name": _("User Name"),
			#"name":_("Name"),
			"first_name":_("First Name"),
			"last_name":_("Last Name"),
			"password":_("Password"),
			"email":_("Email"),
			"zipcode":_("Zipcode"),
			"address":_("Address"),
			"pickup_arrangement":_("Tool Pickup arrangements")
			#"tool_pickup_preference":_("Tool Pickup Preference")
			# "tool_location":_(" ")
		}
		
	def __init__(self, *args, **kwargs):
		super(Registration, self).__init__(*args, **kwargs)
		# self.fields['tool_location'].required = False

	def clean_zipcode(self):
		zip_code = self.cleaned_data['zipcode']

		if len(str(zip_code))!=5:
			raise forms.ValidationError("Please enter a valid zipcode")

		return zip_code

	'''def clean_name(self):
		name = self.cleaned_data['name']
		if (re.search('\d',str(name))):
			raise  forms.ValidationError("Please enter a valid name")
		if str(name).isspace():
			raise  forms.ValidationError("Dude not cool, Enter a name, not spaces!")
			
		return name '''

	def clean_first_name(self):
		name = self.cleaned_data['first_name']
		if (re.search('\d',str(name))):
			raise  forms.ValidationError("Please enter a valid first name")
		if not name.isalnum():
			raise forms.ValidationError("No special Characters Allowed")
				
		if str(name).isspace():
			raise  forms.ValidationError("Dude not cool, Enter a name, not spaces!")
			
		return name

	def clean_last_name(self):
		name = self.cleaned_data['last_name']
		if (re.search('\d',str(name))):
			raise  forms.ValidationError("Please enter a valid last name")
		if not name.isalnum():
			raise forms.ValidationError("No special Characters Allowed")	
		if str(name).isspace():
			raise  forms.ValidationError("Dude not cool, Enter a name, not spaces!")
			
		return name

	def clean_user_name(self):
		username = self.cleaned_data['user_name']
		uname = username.strip()
		return uname	


	def clean_password(self):
		password = self.cleaned_data['password']
		if len(str(password))<5:
			raise forms.ValidationError("Password is too short")
		return password

	def clean_confirm_password(self):
		cleaned_data = self.cleaned_data
		confirm_password = cleaned_data.get('confirm_password')
		password = cleaned_data.get('password')
		if confirm_password != password:	
			raise forms.ValidationError("Passwords Do not match")
		return confirm_password	

	def clean_address(self):
		address = self.cleaned_data['address']
		if str(address).isspace():
			raise  forms.ValidationError("Dude not cool, Enter your address, not spaces!")
		return address

	def clean_tool_image(self):
		tool_image = self.cleaned_data['tool_image']
		return tool_image


	def clean_tool_special(self):
		tool_special = self.cleaned_special['tool_special']
		return tool_special



class Login(forms.Form):
	user_name = forms.CharField(label='Username',max_length=30, required=True, widget=forms.TextInput(attrs={'id' : 'username', 'class' : 'form-control', 'placeholder' : 'Username'}))
	password = forms.CharField(label='Password',max_length=30, required=True, widget=forms.PasswordInput(attrs={'id' : 'password', 'class' : 'form-control', 'placeholder' : 'Password'}))


class Tools(forms.Form):
	tool_name = forms.CharField(label='Tool Name',max_length=25, required=True, widget=forms.TextInput(attrs={'id' : 'toolname', 'class' : 'form-control', 'required':'True'}))
	tool_description = forms.CharField(label='Tool Description',max_length=30, required=True, widget=forms.Textarea(attrs={'id' : 'tooldesc', 'class' : 'form-control','required':'True'}))
	ToolCat = (
		('Abrasives','Abrasives'),
		('Air Tools','Air Tools'),
		('Cutting Tools','Cutting Tools'),
		('Electric Tools','Electric Tools'),
		('Hammers','Hammers'),
		('Hardware','Hardware'),
		('Impact Socket','Impact Socket'),
		('Lifting Equipment','Lifting Equipment'),
		('Lighting','Lighting'),
		('Lubrication','Lubrication'),
		('Misc Hand Tools','Misc Hand Tools'),
		('Pliers','Pliers'),
		('Pry Bars','Pry Bars'),
		('Pullers and Drivers','Pullers and Drivers'),
		('Punches and Chisels','Punches and Chisels'),
		('Safety and Apparel','Safety and Apparel'),
		('Screw Drivers','Screw Drivers'),
		('Sockets and Drives','Sockets and Drives'),
		('Suspension Tools','Suspension Tools'),
		('Test Equipments','Test Equipments'),
		('Thread Repair','Thread Repair'),
		('Tire Service','Tire Service'),
		('Welding and Heating','Welding and Heating'),
		('Wrenches','Wrenches'),
		('Other','Other'),
		)

	ToolCondition = (('Excellent','Excellent'),
		('Good','Good'),
		('Cosmetic imperfections','Cosmetic imperfections'))

	tool_category = forms.ChoiceField(label='Tool Category', widget=forms.Select(attrs={'id' : 'toolcat', 'class':'form-control'}), choices = ToolCat)
	tool_condition = forms.ChoiceField(label='Tool Condition',  widget=forms.Select(attrs={'id' : 'toolcon', 'class':'form-control'}), choices = ToolCondition)
	tool_image = forms.FileField(label='Upload an image', help_text='max. 42 megabytes')
	#tool_special = forms.CharField(label='special instructions for borrower', max_length=50, required=False)
	tool_special = forms.CharField(label='Special instructions for borrower',max_length=50, required=False, widget=forms.TextInput(attrs={'id' : 'toolspecs', 'class' : 'form-control'}))
	



class Shed_Creation(forms.Form):
	shed_name = forms.CharField(label='Shed Name',max_length=30, required=True, widget=forms.TextInput(attrs={'id' : 'shedname', 'class' : 'form-control', 'placeholder' : 'Shed Name'}))
	shed_address = forms.CharField(label='Shed Address',max_length=40, required=True, widget=forms.Textarea(attrs={'id' : 'shedaddr', 'class' : 'form-control', 'placeholder' : 'Shed Address', 'rows' : '3'}))
	shed_email = forms.EmailField(label='Shed Email',max_length=30, required=True, widget=forms.TextInput(attrs={'id' : 'shed_email', 'class' : 'form-control', 'placeholder' : 'Shed Email'}))
	


class EditUser(forms.ModelForm):
	class Meta:
		model = models.User	
		arrangements = (
		("Please knock on the door","Please knock on the door"),
		("Please ring on the bell","Please ring on the bell"),
		("Fix up arrangements via Email","Fix up arrangements via Email"),
		)

		fields = ['first_name','last_name','email','zipcode','address','pickup_arrangement']#,'tool_pickup_preference']


		

		widgets = {
			#'name': TextInput(attrs={'id' : 'name', 'class' : 'form-control','MAXLENGTH':'20'}),
			'first_name': TextInput(attrs={'id' : 'first_name', 'class' : 'form-control','MAXLENGTH':'20'}),
			'last_name': TextInput(attrs={'id' : 'last_name', 'class' : 'form-control','MAXLENGTH':'20'}),
			'email': TextInput(attrs={'id' : 'email', 'class' : 'form-control','MAXLENGTH':'25'}),
			'zipcode': TextInput(attrs={'id' : 'zipcode', 'class' : 'form-control','MAXLENGTH':'5'}),
			'address': Textarea(attrs={'id' : 'address', 'class' : 'form-control', 'rows' : '5','MAXLENGTH':'25'}),
			'pickup_arrangement': Select(attrs={'id' : 'pickup_arrangement', 'class':'form-control','choices':'arrangements'}),
			
			}
		
		labels = {
			#"name":_("Name"),
			"first_name":_("First Name"),
			"last_name":_("Last Name"),
			"email":_("Email"),
			"zipcode":_("Zipcode"),
			"address":_("Address"),
			"pickup_arrangement":_("Pickup Arrangement")
			
		}
		
	def __init__(self, *args, **kwargs):
		super(EditUser, self).__init__(*args, **kwargs)

	def clean_address(self):
		address = self.cleaned_data['address']
		if str(address).isspace():
			raise  forms.ValidationError("Dude not cool, Enter your address, not spaces!")
		return address


	def clean_zipcode(self):
		zip_code = self.cleaned_data['zipcode']

		if len(str(zip_code))!=5:
			raise forms.ValidationError("Please enter a valid zipcode")

		return zip_code

	def clean_name(self):
		name = self.cleaned_data['name']
		if (re.search('\d',str(name))):
			raise  forms.ValidationError("Please enter a valid name")
		if str(name).isspace():
			raise  forms.ValidationError("Dude not cool, Enter a name, not spaces!")
		if not name.isalnum():
			raise forms.ValidationError("No special Characters Allowed")	
			
		return name

	def clean_first_name(self):
		name = self.cleaned_data['first_name']
		if (re.search('\d',str(name))):
			raise  forms.ValidationError("Please enter a valid name")
		if str(name).isspace():
			raise  forms.ValidationError("Dude not cool, Enter a name, not spaces!")
			
		return name

	def clean_last_name(self):
		name = self.cleaned_data['last_name']
		if (re.search('\d',str(name))):
			raise  forms.ValidationError("Please enter a valid name")
		if str(name).isspace():
			raise  forms.ValidationError("Dude not cool, Enter a name, not spaces!")
		if not name.isalnum():
			raise forms.ValidationError("No special Characters Allowed")	
			
		return name


class StartShare(forms.Form):
	tool = forms.IntegerField(label='ToolId', required=True, widget=forms.TextInput(attrs={'id' : 'tool', 'class' : 'form-control', 'type' : 'hidden'}))
	days = forms.IntegerField(label='Number of Days', widget=forms.TextInput(attrs={'id' : 'days', 'class' : 'form-control col-lg-3'}))
	# days = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),('31','31'))
	# months = (('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'),('12','12'))
	# years = (('2015','2015'),('2016','2016'))
	# share_startday = forms.ChoiceField(label='day',required=True, widget=forms.Select(attrs={'id' : 'startday', 'class':''}), choices = days)
	# share_startmonth = forms.ChoiceField(label='month',required=True, widget=forms.Select(attrs={'id' : 'startmonth', 'class':''}), choices = months)
	# share_startyear = forms.ChoiceField(label='year',required=True, widget=forms.Select(attrs={'id' : 'startyear', 'class':''}), choices = years)
	# share_endday = forms.ChoiceField(label='day',required=True, widget=forms.Select(attrs={'id' : 'endday', 'class':''}), choices = days)
	# share_endmonth = forms.ChoiceField(label='month',required=True, widget=forms.Select(attrs={'id' : 'endmonth', 'class':''}), choices = months)
	# share_endyear = forms.ChoiceField(label='year',required=True, widget=forms.Select(attrs={'id' : 'endyear', 'class':''}), choices = years)
	# startdate = forms.DateField(label='Start Date', input_formats=['%m/%d/%Y', '%d/%m/%Y',], required=True, widget=forms.DateInput(format = '%m/%d/%Y'))
	# enddate = forms.DateField(label='End Date', input_formats=['%m/%d/%Y', '%d/%m/%Y',], required=True, widget=forms.DateInput(format = '%m/%d/%Y'))

class Send_Message(forms.Form):
	message = forms.CharField(label='Message',max_length=60, required=True, widget=forms.Textarea(attrs={'id' : 'message', 'class' : 'form-control', 'rows' : '3'}))
	days = forms.IntegerField(label='Number of Days', required=True, widget=forms.Textarea(attrs={'id' : 'days', 'class' : 'form-control', 'rows' : '1'}))

class Days(forms.Form):
	days = forms.IntegerField(label='Number of Days', required=True, widget=forms.Textarea(attrs={'id' : 'days', 'class' : 'form-control', 'rows' : '1'}))
	

class ReserveTool(forms.Form):
	days = forms.IntegerField(label='Number of Days', required=True, widget=forms.TextInput(attrs={'id' : 'number','type':'number', 'class' : 'form-control', 'placeholder' : 'Number of Days','required':'True'}))
	messages = forms.CharField(label='Message',max_length=40, required=True, widget=forms.TextInput(attrs={'id' : 'messages', 'class' : 'form-control', 'placeholder' : 'messages'}))



		