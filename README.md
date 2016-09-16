# ToolSharing-System
1. INTRODUCTION
		The tool share web app lets the users to login or register is the user is new and then takes them to their profile page where they can addtools to the tool listing, visit tool listing to check out what tools are available in the user’s zipcode, the share tool functionality has been implemented partially as of now and will be completed by the next release along with other features. The user can edit his profile. When a user registers in a new zipcode zone, the user will be asked to create a shed which will make him the sharezone admin. All tools have a specific location mentioned which is the place they can be obtained from.


2. REQUIREMENTS
		As of now the system should consist of Django 1.8.3 and python 3.4.3, and a browser which supports the Django version.


3. INSTALLATION
		This version of the webapp can be run by opening the respective folder using command prompt and then giving the appropriate command for running the Django server.
		
		Steps:
		1.	Open command prompt.
		2.	Goto the folder in which the project is present using “CD path”. Path refers to the location of the folder containing the project on the system, maybe an external device.
		3.	Type in “python manage.py migrate". 
			Type in “python manage.py runserver”.
		4.	Open browser and type http://127.0.0.1:8000/ in the url box.
		5.	All other functionalities can be figured out pretty easily.


4. USERS PROFILES 
	
	Creating the super user can be done by following the steps below:
		1.	Open command prompt.
		2.	Goto the folder in which the project is present using “CD path”. Path refers to the location of the folder containing the project on the system, maybe an external device.
		3.	Type in “python manage.py createsuperuser", and then type in the details that are requested.
		4.  The superuser can be accessed by going to http://127.0.0.1:8000/admin.

	The regular users can be created by going to the login page and clicking on the register link, provide the required details and submit the form which will redirect you to the login page where u can now login.

