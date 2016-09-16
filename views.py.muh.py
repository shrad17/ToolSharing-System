from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from users import models, forms
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from datetime import datetime, timedelta
from django.db.models import Count
from collections import Counter

# Create your views here.

def register(request):
	registration_form = forms.Registration(request.POST or None)

	reg_context = {
		'reg_form': registration_form,
	}

	if registration_form.is_valid():
		registration_obj = models.User()
		registration_obj.name = registration_form.cleaned_data['name']
		registration_obj.user_name = registration_form.cleaned_data['user_name']
		registration_obj.zipcode = registration_form.cleaned_data['zipcode']
		registration_obj.email = registration_form.cleaned_data['email']
		registration_obj.address = registration_form.cleaned_data['address']
		registration_obj.password = registration_form.cleaned_data['password']
		registration_obj.confirm_password = registration_form.cleaned_data['confirm_password']
		registration_obj.pickup_arrangement = registration_form.cleaned_data['pickup_arrangement']
		#registration_obj.tool_pickup_preference = registration_form.cleaned_data['tool_pickup_preference']
		# registration_obj.tool_location = registration_form.cleaned_data['tool_location']
		registration_obj.save()
		return HttpResponseRedirect('/')

	return render(request, 'register.html', reg_context)


def login(request):
	login_form = forms.Login(request.POST or None)
	Login_context = {
		'login_form': login_form,
	}

	if login_form.is_valid():

		login_obj = models.User.objects.filter(user_name=login_form.cleaned_data['user_name'],
											   password=login_form.cleaned_data['password'])

		if not login_obj:
			Login_context['error'] = 'Invalid Credentials.'
		else:
			try:
				banned = models.BannedUsers.objects.get(user_name=login_form.cleaned_data['user_name'])
			except ObjectDoesNotExist:
				request.session['open'] = True
				request.session['user_name'] = login_form.cleaned_data['user_name']
				user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
				try:
					shed_zip = models.Shed.objects.get(shed_zip=user_zip)
				except ObjectDoesNotExist:
					return HttpResponseRedirect('/shed')
				return HttpResponseRedirect('/up')
			Login_context['error'] = 'The Admin has Banned your account!'	

			
			

	return render(request, 'login.html', Login_context)


def logout(request):
	request.session['open'] = False
	#delete stored user_name key for the session
	del request.session['user_name']
	return HttpResponseRedirect('/')

	return render(request, 'login.html', Login_context)	


'''
Welcome to a Brand New Series, Akil's "Check to see if a shed exists and the user is logged in"

I am written some code which checks if a shed is present or if the user is logged in,
 to use it, simple copy and paste the Following lines, Some one can refactor it later...

 # Check to see if user is logged in.
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')
    #check if a shed exists.
	try:
		shed_zip = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed') 

'''
 

def user_profile(request):
	# Check to see if user is logged in.
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')
    #check if a shed exists.
	try:
		shed = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')

	user = models.User.objects.get(user_name=request.session['user_name'])
	name = user.name
	email = user.email
	zipcode = user.zipcode
	address = user.address
	arrangement = user.pickup_arrangement
	#tool_pickup_preference = user.tool_pickup_preference
	# tool_location = user.tool_location

	'''Getting the shed information'''
	shed_name = shed.shed_name
	shed_address = shed.shed_address
	shed_contact = shed.shed_contact

	'''User Stats'''
	num_tools = models.Tools.objects.all().filter(tool_owner=request.session['user_name']).count()
	num_lent = models.ShareTool.objects.all().filter(owner=request.session['user_name']).count()
	num_borrow = models.ShareTool.objects.all().filter(borrower=request.session['user_name']).count()

	Profile_context = {
		'name': name,
		'email': email,
		'zipcode': zipcode,
		'address': address,
		'arrangement':arrangement,
		'shed_name':shed_name,
		'shed_address':shed_address,
		'shed_contact':shed_contact,
		'tools':num_tools,
		'lent':num_lent,
		'borrow':num_borrow
		#'tool_pickup_preference':tool_pickup_preference
		# 'tool_location':tool_location
	}
	return render(request, 'profile.html', Profile_context)


def edit_profile(request):

    # Check to see if user is logged in.
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')
    #check if a shed exists.
	try:
		shed_zip = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')

	user_change_form = forms.EditUser(request.POST or None)
	user = models.User.objects.get(user_name=request.session['user_name'])
	name = user.name
	email = user.email
	address = user.address
	zipcode = user.zipcode
	arrangement = user.pickup_arrangement

	#Setting the default values
	user_change_form.fields['name'].initial = name
	user_change_form.fields['email'].initial = email
	user_change_form.fields['address'].initial = address
	user_change_form.fields['zipcode'].initial = user_zip
	user_change_form.fields['pickup_arrangement'].initial = arrangement
	#user_change_form.fields['tool_pickup_preference'].initial = "Home"


	user_change_context = {
		'form': user_change_form,
	}

	user_change_context['name'] = models.User.objects.get(user_name=user).name
	user_change_context['zipcode'] = models.User.objects.get(user_name=user).zipcode
	user_change_context['pickup_arrangement'] = models.User.objects.get(user_name=user).pickup_arrangement
	user_change_context['address'] = models.User.objects.get(user_name=user).address
	user_change_context['email'] = models.User.objects.get(user_name=user).email
	

	if user_change_form.is_valid():
		user.name = user_change_form.cleaned_data['name']
		user.address = user_change_form.cleaned_data['address']
		user.zipcode = user_change_form.cleaned_data['zipcode']
		user.email = user_change_form.cleaned_data['email']
		if user.zipcode!= user_zip:
			if user.isAdmin==1:
				 user_change_context['error']="Please remove yourself as admin first"
				
			elif check_if_borrow_active(user):
				user_change_context['error']="Please wait for all your tools to be returned"
			elif check_if_borrower(user):
				user_change_context['error']="Please return all the tools first"
			else:
				tools = models.Tools.objects.all().filter(tool_owner=request.session['user_name'])
				for tool in tools:
					tool.tool_zip=user.zipcode
					tool.save()
				user.pickup_arrangement=user_change_form.cleaned_data['pickup_arrangement']
				user.save()
				return HttpResponseRedirect('/up')
			   

		
	return render(request, 'edit_profile.html', user_change_context)



'''Functions for the edit profile when changing the shed'''
def check_if_borrow_active(user):
	tools = models.Tools.objects.all().filter(tool_owner=user)
	for t in tools:
		if t.tool_available==0:
			return True
	return False

def check_if_borrower(user):
	tools = models.Tools.objects.all()
	for t in tools:
		if t.tool_borrower==str(user):
			return True
	return False			

'''end'''


def tools(request):

	#Check if user is logged in
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')	
	
    #check if shed exists
	try:
		shed_zip = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')
	tools_form = forms.Tools(request.POST or request.FILES)

	tools_context = {
		'tools_form': tools_form,
	}
	if request.method == 'POST':
		tools_form=forms.Tools(request.POST, request.FILES)

	if tools_form.is_valid():
		tools_obj = models.Tools()
		user_tool = models.User.objects.get(user_name=request.session['user_name'])
		
		tools_obj.tool_description = tools_form.cleaned_data['tool_description']
		tools_obj.tool_category = tools_form.cleaned_data['tool_category']
		tools_obj.tool_special = tools_form.cleaned_data['tool_special']
		tools_obj.tool_image = tools_form.cleaned_data['tool_image']
		image = request.FILES['tool_image']
		#Get the uploaded image's extension
		extension = (image.name).split('.')[1]
		if ((extension=='jpg')or(extension=='png')or(extension=='jpeg')):
			tools_obj.tool_owner = user_tool
			tools_obj.tool_zip = user_tool.zipcode
			tools_obj.tool_address = user_tool.address
			tools_obj.tool_name = tools_form.cleaned_data['tool_name']
			tools_obj.save()	
			return HttpResponseRedirect('/listtools')
		else:
			tools_context['error']="Please Upload a jpg or png image"

	return render(request, 'add_tool.html', tools_context)


def listtools(request):

	#check if user is logged in.
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')
		
	#check if shed Exists		
	try:
		shed_zip = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')

	user_tool = models.User.objects.get(user_name=request.session['user_name'])
	tools = models.Tools.objects.all().filter(tool_owner=user_tool)

	the_tool_list = []
	for tool in tools:
		inner_list = [
					  str(tool.id),
					  tool.tool_name,
					  tool.tool_image,
					  tool.tool_description,
					  tool.tool_special,
					  tool.tool_available,
					  tool.tool_address,
					  tool.tool_atHome

					 ]
		the_tool_list.append(inner_list)

	context = {
		'tool_list': the_tool_list,
	}

	return render(request, 'list_tools.html', context)


def toolsinzip(request):
	#Check if user is logged in..................................
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')
	#Check if a shed is pressent..............	
	try:
		shed_zip = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')


    #Get the Session Data.
	user_tool = models.User.objects.get(user_name=request.session['user_name'])
	user_zip = models.User.objects.get(user_name=user_tool).zipcode
	user_name = request.session['user_name']

    #Getting only avaliable tools in the zip code which are not the current users.
	tools = models.Tools.objects.all().filter(tool_zip=user_zip).exclude(tool_owner=user_name)
	

	the_tool_list = []
	for tool in tools:
		if tool.tool_activate==1:
			inner_list = [str(tool.id),
			tool.tool_name,
			tool.tool_image,
			tool.tool_description,
			tool.tool_special,
			tool.tool_category,
			tool.tool_address,
			tool.tool_owner,
			tool.tool_available,
			tool.tool_isReserved]
			the_tool_list.append(inner_list)

	context = {
		'tool_list': the_tool_list
	}

	return render(request, 'tools_in_zip.html', context)


def shed_creation(request):

	#Check if user is logged in..................................
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')


	shed_form = forms.Shed_Creation(request.POST or None)

	shed_context = {
		'shed_form': shed_form,
	}

	if shed_form.is_valid():
		shed_obj = models.Shed()
		shed_obj.shed_name = shed_form.cleaned_data['shed_name']
		shed_obj.shed_address = shed_form.cleaned_data['shed_address']
		shed_obj.shed_contact = shed_form.cleaned_data['shed_contact']
		#Get current user.
		
		admin = models.User.objects.get(user_name=request.session['user_name'])
		shed_obj.shed_admin=admin.user_name
		shed_obj.shed_zip=admin.zipcode
		shed_obj.save()
		admin.isAdmin=True
		admin.save()


		# Following line sends user to profile after registration
		return HttpResponseRedirect('/up')

	return render(request, 'shed.html', shed_context)


def request_share(request,tid):
	# View To borrow a tool , check if the tool is in the shed or home
	#Check if user is logged in..................................
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')

	#Check if shed exists
	try:
		shed_zip = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')

	borrow_user = models.User.objects.get(user_name=request.session['user_name'])
	borrow_tool = models.Tools.objects.get(id=tid)

	if borrow_tool.tool_atHome==False:
		#Redirect to Share from tool page.
		return HttpResponseRedirect('/shedshare/%s'%tid)

	elif borrow_tool.tool_atHome==True:
		form = forms.Send_Message(request.POST or None)
		context = {'form': form,}

		if form.is_valid():
			message_obj = models.Message()
			message_obj.days = form.cleaned_data['days']
			if 0<message_obj.days<15:
				message_obj.user_borrower = borrow_user.user_name
				message_obj.user_owner = borrow_tool.tool_owner
				message_obj.messages = form.cleaned_data['message']
				message_obj.tool = borrow_tool.tool_name
				message_obj.tid = tid
				message_obj.save()
				return HttpResponseRedirect('/up')
			else:
				context['error']="Please enter a number less than 15"
				
		return render(request, 'startshare.html', context)


		return HttpResponseRedirect('/request')

	return render(request, 'startshare.html', share_context)


def ShedShare(request,tid):
	#Function to get the number of days and accept a borrow request for a tool from a shed

	#Check if user is logged in..................................
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')

	form = forms.Days(request.POST or None)
	context = {'form':form,"hide":False}
	if form.is_valid():
		days = form.cleaned_data['days']
		if (0<days<15):
			shareTool_obj = models.ShareTool()
			shareTool_obj.tid = tid
			shareTool_obj.days = days
			tool = models.Tools.objects.get(id=tid)
			if tool.tool_available == 1:
				shareTool_obj.owner = tool.tool_owner
				shareTool_obj.borrower = models.User.objects.get(user_name=request.session['user_name']).user_name
				shareTool_obj.deadline = datetime.today() + timedelta(days=days)
				shareTool_obj.save()
				tool.tool_borrower= shareTool_obj.borrower
				tool.tool_available=0
				tool.tool_deadline= str(shareTool_obj.deadline)[:10]
				tool.save()
				context={}
				context={"hide":True,"message":"The tool is your now","owner":tool.tool_owner}
		else:
			context['error']="Please input a number less than 15"
	return render(request, 'shedshare.html', context)	


def User_Messages(request):
	#Check if user is logged in..................................
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')

	#Check if shed exists
	try:
		shed_zip = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')

	current_user = 	models.User.objects.get(user_name=request.session['user_name'])

	Message = models.Message.objects.all().filter(user_owner=current_user).exclude(replied=True)
	message_list = []
	for message in Message:
		if models.Tools.objects.get(id=message.tid).tool_available==1:
			inner_list = [
			str(message.tid),
			message.user_borrower,
			message.messages,
			message.tool,
			message.id,
			message.days
			]
			message_list.append(inner_list)

	
	ReserveMessage = models.ReserveMessages.objects.all().filter(owner=current_user).exclude(replied=True)
	rmessage_list =[]
	for message in ReserveMessage:
		if models.Tools.objects.get(id=message.tid).tool_isReserved:
			inner_list = [
			str(message.tid),
			message.reserver,
			message.message,
			models.Tools.objects.get(id=message.tid).tool_name,
			message.days,
			message.id
			]
			rmessage_list.append(inner_list)

	context = {'list' : message_list,
	'rlist':rmessage_list}	


	if(request.GET.get('Accept')):
		#if he accepts the request.
		value= request.GET.get('value')
		Amessage = models.Message.objects.get(id=value)
		#First handle the message
		Amessage.replied=True
		#Then Mark the tool as unavailable.
		tool = models.Tools.objects.get(id=Amessage.tid)
		tool.tool_borrower=Amessage.user_borrower
		
		Amessage.save()
		
		#Creating the share in the sharetool model
		if tool.tool_available==1:
			tool.tool_available=0
			shareTool_obj = models.ShareTool()
			shareTool_obj.tid = tool.id
			shareTool_obj.days = Amessage.days
			shareTool_obj.borrower = Amessage.user_borrower
			shareTool_obj.owner = models.User.objects.get(user_name=request.session['user_name']).user_name
			shareTool_obj.deadline = datetime.today() + timedelta(days=Amessage.days)
			tool.tool_deadline= str(shareTool_obj.deadline)[:10]
			shareTool_obj.save()
			tool.save()
			return HttpResponseRedirect('/messages')

		
	if(request.GET.get('Reject')):
		value= request.GET.get('value')
		Rmessage = models.Message.objects.get(id=value)
		Rmessage.replied=True
		Rmessage.save()
		return HttpResponseRedirect('/messages')

		#Handle Accept or reject of Reservation messages

	if(request.GET.get('rAccept')):
		value = request.GET.get('value')
		Amessage = models.ReserveMessages.objects.get(id=value)
		Amessage.replied=True
		tool = models.Tools.objects.get(id=Amessage.tid)
		Amessage.save()
		if tool.tool_isReserved==0:
			tool.tool_isReserved=1
			tool.tool_nextBorrower = Amessage.reserver
			tool.tool_nextDays = Amessage.days
			tool.save()
			page =  request.get_full_path()
			page = page.rpartition('?')[0]
			return HttpResponseRedirect(page)


	if(request.GET.get('rReject')):
		value= request.GET.get('value')
		Rmessage = models.ReserveMessages.objects.get(id=value)
		Rmessage.replied=True
		Rmessage.save()
		page =  request.get_full_path()
		page = page.rpartition('?')[0]
		return HttpResponseRedirect(page)	

	return render(request,'messages.html',context)	


def borrowed_tools(request):

	#check if user is logged in.
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')
		
	#check if shed Exists		
	try:
		shed_zip = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')

	user = models.User.objects.get(user_name=request.session['user_name'])
	tools = models.Tools.objects.all().filter(tool_borrower=user)
	

	the_tool_list = []
	for tool in tools:
		inner_list = [
					  tool.id,
					  tool.tool_name,
					  tool.tool_image,
					  tool.tool_description,
					  tool.tool_special,
					  tool.tool_category,
					  tool.tool_owner,
					  tool.tool_deadline,
					 ]
		the_tool_list.append(inner_list)

	context = {
		'tool_list': the_tool_list
	}


	if(request.GET.get('Return')):
		request_id = request.GET.get('values')
		tool = models.Tools.objects.get(id=request_id)
		tool.tool_borrower=''
		tool.tool_available=1
		tool.tool_deadline=''
		tool.save()
		#if tool is reserved, make the reservation into a borrow
		if tool.tool_isReserved==1:
			tool.tool_isReserved=0
			tool.tool_available=0
			tool.tool_deadline= datetime.today() + timedelta(days=tool.tool_nextDays)
			tool.tool_borrower= tool.tool_nextBorrower
			tool.tool_nextBorrower=''
			tool.tool_nextDays=''
			tool.save()
		return HttpResponseRedirect('/borrowed_tools')

	return render(request, 'return_tool.html', context)


def edit_tools(request,tid):
	# Check to see if user is logged in.
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')
    #check if a shed exists.
	try:
		shed_zip = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')
	page =  request.get_full_path()	

	
	user = models.User.objects.get(user_name=request.session['user_name'])
	tool = models.Tools.objects.get(id=tid)
	edit_tool_form = forms.Tools(request.POST or None, request.FILES or None)
	if tool.tool_owner!=user.user_name:
		return HttpResponseRedirect('/up')
	name = tool.tool_name
	desc = tool.tool_description
	cat = tool.tool_category
	img = tool.tool_image
	spl = tool.tool_special
	available = tool.tool_activate

	#Setting the default values
	edit_tool_form.fields['tool_name'].initial = name
	edit_tool_form.fields['tool_description'].initial = desc
	edit_tool_form.fields['tool_category'].initial = cat
	edit_tool_form.fields['tool_image'].initial = img
	edit_tool_form.fields['tool_special'].initial = spl

	edit_tools_context = {
		'form': edit_tool_form,
		'available': available,
		'home':tool.tool_atHome,
	}

	if edit_tool_form.is_valid():
		tool.tool_name = edit_tool_form.cleaned_data['tool_name']
		tool.tool_description = edit_tool_form.cleaned_data['tool_description']
		tool.tool_category = edit_tool_form.cleaned_data['tool_category']
		tool.tool_image = edit_tool_form.cleaned_data['tool_image']
		tool.tool_special = edit_tool_form.cleaned_data['tool_special']
		tool.save()
		return HttpResponseRedirect('/up')

	
    
	if(request.GET.get('activate')):
		tool_act = models.Tools.objects.get(id=tid)
		tool_act.tool_activate = 1
		tool_act.save()

			
		page =  request.get_full_path()
		page = page.rpartition('?')[0]
		return HttpResponseRedirect(page)	

	if(request.GET.get('deactivate')):
		tool_act = models.Tools.objects.get(id=tid)
		tool_act.tool_activate = 0
		tool_act.save()
		page =  request.get_full_path()
		page = page.rpartition('?')[0]
		return HttpResponseRedirect(page)

	if(request.GET.get('Move')):
		tools = models.Tools.objects.get(id=tid)
		tools.tool_atHome=0
		tools.save()
		page =  request.get_full_path()
		page = page.rpartition('?')[0]
		return HttpResponseRedirect(page)

	if(request.GET.get('Home')):
		tools = models.Tools.objects.get(id=tid)
		tools.tool_atHome=1
		tools.save()
		page =  request.get_full_path()
		page = page.rpartition('?')[0]
		return HttpResponseRedirect(page)

	if(request.GET.get('Delete')):
		tool_act = models.Tools.objects.get(id=tid)
		if tool_act.tool_available==1:
			tool_act.delete()
			return HttpResponseRedirect('/listtools')	
		else:
			edit_tools_context['delete_error']="Please wait till the tool is available"
					
		
	return render(request, 'edit_tools.html', edit_tools_context)


def addAdmin(request):
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')
    #check if a shed exists.
	try:
		shed_zip = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')

	if models.User.objects.get(user_name=request.session['user_name']).isAdmin:
		print('admin')
		users_in_zip = models.User.objects.all().filter(zipcode=user_zip)
		
		users_list = []
		for user in users_in_zip:
			inner_list = [
					  user.user_name,
					  user.address,
					  user.isAdmin
					 ]
			users_list.append(inner_list)
		context = {'user_list': users_list}
	else:
		return HttpResponseRedirect('/up')

	if(request.GET.get('addAdmin')):
		user_id = request.GET.get('user_id')
		try:
			user = models.User.objects.get(user_name=user_id)
		except:
			pass
		user.isAdmin=1
		user.save()
		return HttpResponseRedirect('/addAdmin')	

	if(request.GET.get('deleteAdmin')):
		user_id = request.GET.get('user_id')
		number = models.User.objects.all().filter(zipcode=user_zip).exclude(isAdmin=0).count()
		if 1<number:
			try:
				user = models.User.objects.get(user_name=user_id)
			except:
				pass
			user.isAdmin=0
			user.save()
			return HttpResponseRedirect('/addAdmin')

			
		return HttpResponseRedirect('/addAdmin')		




	return render(request,'add_admin.html',context)


def edit_shed(request):
	# Check to see if user is logged in.
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')
    #check if a shed exists.
	try:
		shed = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')

	edit_shed_form = forms.Shed_Creation(request.POST or None)
	user = models.User.objects.get(user_name=request.session['user_name'])

	
	if not user.isAdmin:
		return HttpResponseRedirect('/up')
	name = shed.shed_name
	address = shed.shed_address
	contact = shed.shed_contact

	#Setting the default values
	edit_shed_form.fields['shed_name'].initial = name
	edit_shed_form.fields['shed_address'].initial = address
	edit_shed_form.fields['shed_contact'].initial = contact

	edit_shed_context = {
		'form': edit_shed_form,
	}

	if edit_shed_form.is_valid():
		shed.shed_name = edit_shed_form.cleaned_data['shed_name']
		shed.shed_address = edit_shed_form.cleaned_data['shed_address']
		shed.shed_contact = edit_shed_form.cleaned_data['shed_contact']
		shed.save()
		return HttpResponseRedirect('/up')
		
	return render(request, 'edit_shed.html', edit_shed_context)	


def manage_users(request):
	# Check to see if user is logged in.
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')
    #check if a shed exists.
	try:
		shed = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')

	admin = models.User.objects.get(user_name=request.session['user_name'])
	if admin.isAdmin==0:
	    return HttpResponseRedirect('/up')
	users = models.User.objects.all().filter(zipcode=user_zip).exclude(isAdmin=1)

	users_list = []
	for user in users:
		try:
			banned = models.BannedUsers.objects.get(user_name=user.user_name)
		except ObjectDoesNotExist:
			inner_list = [
			user.user_name,
			user.name,]
			users_list.append(inner_list)
	
	context = {'user_list': users_list}

	if(request.GET.get('ban')):
		user_name = request.GET.get('user_name')
		ban = models.BannedUsers()
		ban.user_name = user_name
		ban.save()
		return HttpResponseRedirect('/manage_users')

	return render(request,'manage_users.html',context)	


def statistics(request):
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')

    #check if a shed exists.
	try:
		shed = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')

	admin = models.User.objects.get(user_name=request.session['user_name'])
	if admin.isAdmin==0:
		return HttpResponseRedirect('/up')

	stats = models.ShareTool.objects.all()

	tools_list = []
	for stat in stats:
		tname = models.Tools.objects.get(id=stat.tid).tool_name
		tools_list.append(tname)


	lender_list = []
	for stat in stats:
		lender_list.append(stat.owner)
		

	borrower_list = []
	for stat in stats:
		borrower_list.append(stat.borrower)

	try:
		tool = max(set(tools_list), key=tools_list.count)
	except:
		tool = "Not enough data."
	
	try:
		lender = max(set(lender_list), key=lender_list.count)
	except:
		lender = "Not enough Data"
	try:
		borrower = max(set(borrower_list), key=borrower_list.count)
	except:
		borrower = "Not enough Data"
    	
    	


	context={
	'tool':tool, 'lender':lender, 'borrower':borrower
	}



	return render(request,'statistics.html',context)


def makeReservation(request,tid):

	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')

    #check if a shed exists.
	try:
		shed = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')


	tool = models.Tools.objects.get(id=tid)
	deadline = tool.tool_deadline
	Date = deadline + timedelta(days=1)
	if tool.tool_atHome==1:
		reservation_form = forms.ReserveTool(request.POST or None)
		context={
		'home_form':reservation_form,
		'home':True,
		'nextDate': Date
		}

		if reservation_form.is_valid():
			reserveMessage_obj = models.ReserveMessages()
			reserveMessage_obj.reserver =  request.session['user_name']
			reserveMessage_obj.owner = tool.tool_owner
			reserveMessage_obj.message = reservation_form.cleaned_data['messages']
			reserveMessage_obj.tid = tool.id
			reserveMessage_obj.days = reservation_form.cleaned_data['days']
			if (0<reserveMessage_obj.days<15):
				reserveMessage_obj.save()
				return HttpResponseRedirect('/toolsinzip')
			else:
				context['error']="Please enter a number less than 15"
				

	else:
		url = '/reserveShed/'+ str(tid)
		return HttpResponseRedirect(url)
		
	return render(request,'reserve.html',context)


def reserveShed(request,tid):

	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')

    #check if a shed exists.
	try:
		shed = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')

	tool = models.Tools.objects.get(id=tid)
	deadline = tool.tool_deadline
	Date = deadline + timedelta(days=1)
	days_forms = forms.Days(request.POST or None)

	context={'shed_form':days_forms,'nextDate':Date}

	if days_forms.is_valid():
		tool.tool_isReserved=True
		tool.tool_nextBorrower=request.session['user_name']
		tool.tool_nextDays = days_forms.cleaned_data['days']
		if (0<tool.tool_nextDays<15):
			tool.save()
			return HttpResponseRedirect('/toolsinzip')
		else:
		    context['error']="Please enter a number less than 15"
	return render(request,'reserve_shed.html',context)





def shed_tools(request):

	#check if user is logged in.
	try:
		user_zip = models.User.objects.get(user_name=request.session['user_name']).zipcode
	except KeyError:
		return HttpResponseRedirect('/')
		
	#check if shed Exists		
	try:
		shed_zip = models.Shed.objects.get(shed_zip=user_zip)
	except ObjectDoesNotExist:
		return HttpResponseRedirect('/shed')

	user = models.User.objects.get(user_name=request.session['user_name'])
	tools = models.Tools.objects.all().filter(tool_zip=user.zipcode).exclude(tool_atHome=0)

	the_tool_list = []
	for tool in tools:
		inner_list = [
					  str(tool.id),
					  tool.tool_name,
					  tool.tool_image,
					  tool.tool_description,
					  tool.tool_special,
					  tool.tool_available,
					  tool.tool_address,
					  tool.tool_atHome

					 ]
		the_tool_list.append(inner_list)

	context = {
		'tool_list': the_tool_list,
	}

	return render(request, 'shed_tools.html', context)	
