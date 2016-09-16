from io import StringIO
from django.test import TestCase,Client
from users.forms import StartShare
from users.forms import Shed_Creation
from users.forms import Send_Message
from users.forms import Days
from users.forms import ReserveTool
from users.forms import Login
from users.forms import Tools
from users.forms import EditUser
from users.forms import Registration
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import User
from users import models, forms, views
from django.test import TransactionTestCase, Client
from django.test import RequestFactory

class TestOfForms(TestCase):

    def test_login_form(self):
        form_data = {'user_name':'jaskgja', 'password':'123456789123456789_____ITis30'}
        form = Login(form_data)
        self.assertEqual(form.is_valid(),True,'Added perfect username and password')

    def test_LoginForm1(self):
        form_data = {'user_name':'You can not add username longer than 30chars','password':'123456789123456789_____ITis30_now it is more than30'}
        form = Login(form_data)
        self.assertEqual(form.is_valid(),False,'You entered Username and password correctly according to forms.py ')


    def test_shedcreation_form(self): # This method test Shed_Creation class from the forms.py file and checks the validation
                                        # working properly or not
        form_data = {'shed_name':"Shraddhaplace", 'shed_address':'jdskhfsjlcxnz', 'shed_email':'sm@pandya.com '}
        #shed_email should include @ and .com in correct format
        form = Shed_Creation(form_data)
        self.assertEqual(form.is_valid(),True,'Form data is not valid')

    def test_ShedCreationForm1(self):
        form_data = {'shed_name':"123456789123456789_____ITis30And_it_is more than 30", 'shed_address':'itTakes40chars' ,'shed_email':'221548'}
        # Here entered invalid data shed name is larger than  30chars and shed_address is also invalid
        form =Shed_Creation(form_data)
        self.assertEqual(form.is_valid(),False,'input given to Shade_Creation class is valid.so here AssertFalse got False and test fails')


    def test_tools(self):
        upload_file = open('users/static/imgs/se_logo.jpg','rb')
        form_data = {'tool_name':'AirTool_Shraddhas','tool_description':'kdfcnlnln','tool_category': 'Hammers','tool_condition':'Good'}# Here tool_special field is not mandatory, so can be ignored.
        file_data = {'tool_image': SimpleUploadedFile(upload_file.name, upload_file.read())}
        form = Tools(form_data, file_data)
        self.assertTrue(form.is_valid(),'Hey something is wrong you entered.')
    def test_Tools1(self):
        #check for false test case
        get_file = open('users/static/imgs/se_logo.jpg','rb')
        form_data = {'tool_name':'1234567891234567891234567MOREthan25Chars','tool_description':'You can enter any description upto 30 characters here',
                     'tool_category': 'Screw Drivers','tool_condition':'Excellent'}
                     #Here entered tool_description and tool_name are invalid so it will pass assertFalse
        file_data = {'tool_image': SimpleUploadedFile(get_file.name, get_file.read())}
        form = Tools(form_data, file_data)
        self.assertFalse(form.is_valid(),'Your all data is alright')
    def test_Tools2(self):
        #check for false test case
        get_file = open('users/static/imgs/se_logo.jpg','rb')
        # If we do not enter right path for file,
        #  it will throw Error:No such file/directory
        form_data = {'tool_name':'1234567891234567891234567','tool_description':'upto 30 characters here',
                     'tool_category': 'Others','tool_condition':'Noidea'}
                     #Here entered 'Others' instead of 'Other' tool_category is out of given choices in ToolCat List in forms.py
                    #Also tool_condition is out of hoices given so assertFalse will run
        file_data = {'tool_image': SimpleUploadedFile(get_file.name, get_file.read())}
        form = Tools(form_data, file_data)
        self.assertFalse(form.is_valid(),'Your entered all data is alright')


    def test_startshare_form(self):
        # it checks the class named start share class in forms.py
        form_data ={'tool':'2','days':'22548796'} #number of days get checked in views.py so
                                                    # here only it takes invalid if entered entries are not integer values
        form = StartShare(form_data)
        self.assertEqual(form.is_valid(),True,'Data goes to start share is invalid')
    def test_StartShareForm1(self):
        form_data ={'tool':'Hammer','days':'22'}
        form = StartShare(form_data)
        self.assertEqual(form.is_valid(),False,'input given to StartShare class is valid.so here AssertFalse got False and test fails')


    def test_days(self):
        form_data = {'days':'17'}
        form = Days(form_data)
        self.assertEqual(form.is_valid(),True,'Entered invalid days')
    def test_Days1(self):
        form_data = {'days':'these Are not days'}
        form = Days(form_data)
        self.assertEqual(form.is_valid(),False,'Great! you have inserted right days')

    def test_reservetool_form(self):
        form_data = {'days':'4545','messages':'1112131415161718192021222324252627282930'}
        #Entered integer days and message of 40 chars
        form = ReserveTool(form_data)
        self.assertEqual(form.is_valid(),True,'Days are not in integer and/or message is longer than 40 characters')
    def test_ReserveToolForm1(self):
        form_data = {'days':'days as a string', 'message':'1112131415161718192021222324252627282930Now_itzmorethan40characters'}
        form = ReserveTool(form_data)
        self.assertEqual(form.is_valid(),False,'data goes into ReserveTool is not ')

    def test_sendmessage_form(self):
        form_data = {'message':'This is message for requesting Tool to borrow', 'days':56566665656678678386413454566}
        form = Send_Message(form_data)
        self.assertEqual(form.is_valid(),True,'Data inserted to send_message is invalid')

    def test_edituser(self):
        # NOTE : If you enter email and/or zipcode in wrong manner or pickup_arrangement
        # out of choice given than it will get failed.
        form_data = {'first_name':'User','last_name':'Pandya','email':'dsikh@amc.com','zipcode':'14623','address':'sadjdalj','pickup_arrangement':'Please ring on the bell'}
        form = EditUser(form_data)
        self.assertTrue(form.is_valid(),'You inserted something wrong inputs')

    def test_registration(self):
        #here password and confirm password should match and it must be minimum of 5 characters it can't be shorter than 5 chars.
        #pickup_arrangement must be given from choice given
        form_data = {'user_name':'IMPirate','first_name':'User','last_name':'Pandya','email':'dsikh@amc.com','password':'abcde','confirm_password':'abcde',
                     'zipcode':'14623','address':'sadjdalj','pickup_arrangement':'Please knock on the door'}
        form = Registration(form_data)
        self.assertTrue(form.is_valid())

# Unittesting for views.py file

class TestViews(TestCase):
    def test_registration(self): #User registration URL testing
        c = Client()
        response = c.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        c = Client() #User login URL testing
        response = c.post('//',{'username':'abc','password':'123456'})
        self.assertEqual(response.status_code,200)

class UserLoginTest(TransactionTestCase):

		def setUp(self):
			user = User.objects.create(user_name='you', password='hellohello')

		def test_history(self):
			#self.client = Client()
			client = Client()
			response = client.post('/', {'user_name': 'you', 'password': 'hellohello'})
			self.assertEqual(response.status_code, 302)	
			

class TestShedCreation(TestCase):

		def setUp(self):
			self.user = User.objects.create(user_name='pirateBay', first_name='urvi', last_name='gandhi', email='urvi@gmail.com', password='urvigandhi', confirm_password='urvigandhi',  zipcode='14623', address='johnstreet', pickup_arrangement='Please knock on the door')

			self.factory = RequestFactory()
			session = self.client.session
			session['user_name'] = 'pirateBay'
			session['is_open'] = True
			session.save()

		def test_shed_creation(self):
			response = self.client.get('/shed')
			self.assertEqual(response.status_code, 200)

			#request = self.factory.post('users.views.shed_creation')
			#request.user = self.user
			#response = shed_creation(request)
			#self.assertEqual(response.status_code, 302)


class TestUserProfile(TestCase):

		def setUp(self):
			self.user = User.objects.create(user_name='pirateBay', first_name='urvi', last_name='gandhi', email='urvi@gmail.com', password='urvigandhi', confirm_password='urvigandhi',  zipcode='14623', address='johnstreet', pickup_arrangement='Please knock on the door')

			session = self.client.session
			session['user_name'] = 'pirateBay'
			session['is_open'] = True
			session.save()

		def test_user_profile(self):
			response = self.client.get('/up', follow= True)
			self.assertEqual(response.status_code, 200)
			
			
class TestEditUserProfile(TestCase):

		def setUp(self):
			self.user = User.objects.create(user_name='pirateBay', first_name='urvi', last_name='gandhi', email='urvi@gmail.com', password='urvigandhi', confirm_password='urvigandhi',  zipcode='14623', address='johnstreet', pickup_arrangement='Please knock on the door')

			session = self.client.session
			session['user_name'] = 'pirateBay'
			session['is_open'] = True
			session.save()

		def test_edit_user_profile(self):
			response = self.client.get('/edit_profile', follow= True)
			self.assertEqual(response.status_code, 200)
			
			
class TestAddTools(TestCase):

		def setUp(self):
        
			self.user = User.objects.create(user_name='pirateBay', first_name='urvi', last_name='gandhi', email='urvi@gmail.com', password='urvigandhi', confirm_password='urvigandhi',
											zipcode='14623', address='johnstreet', pickup_arrangement='Please knock on the door')

			session = self.client.session
			session['user_name'] = 'pirateBay'
			session['is_open'] = True
			session.save()

		def test_add_tools(self):
			response = self.client.get('/tools/', follow= True)
			self.assertEqual(response.status_code, 200)


class TestListTools(TestCase):

		def setUp(self):
			self.user = User.objects.create(user_name='pirateBay', first_name='urvi', last_name='gandhi', email='urvi@gmail.com', password='urvigandhi', confirm_password='urvigandhi',
											zipcode='14623', address='johnstreet', pickup_arrangement='Please knock on the door')

			session = self.client.session
			session['user_name'] = 'pirateBay'
			session['is_open'] = True
			session.save()

		def test_list_tools(self):
			response = self.client.get('/listtools/', follow= True)
			self.assertEqual(response.status_code, 200)
			

class TestToolsInZip(TestCase):

		def setUp(self):
			self.user = User.objects.create(user_name='pirateBay', first_name='urvi', last_name='gandhi', email='urvi@gmail.com', password='urvigandhi', confirm_password='urvigandhi',
											zipcode='14623', address='johnstreet', pickup_arrangement='Please knock on the door')

			session = self.client.session
			session['user_name'] = 'pirateBay'
			session['is_open'] = True
			session.save()

		def test_tools_in_zip(self):
			response = self.client.get('/toolsinzip', follow= True)
			self.assertEqual(response.status_code, 200)
			

class TestStatistics(TestCase):

		def setUp(self):
        
			self.user = User.objects.create(user_name='pirateBay', first_name='urvi', last_name='gandhi', email='urvi@gmail.com', password='urvigandhi', confirm_password='urvigandhi',
											zipcode='14623', address='johnstreet', pickup_arrangement='Please knock on the door')

			session = self.client.session
			session['user_name'] = 'pirateBay'
			session['is_open'] = True
			session.save()

		def test_statistics(self):
			response = self.client.get('/statistics', follow= True)
			self.assertEqual(response.status_code, 200)

