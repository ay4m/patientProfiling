from datetime import datetime
import qrcode

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

def user_prof_path(instance, filename):
    """ files will be uploaded to MEDIA_ROOT/user_<id>/filename """
    return 'user_{0}/profile/{1}'.format(instance.id, filename)

class BaseAccountManager(BaseUserManager):
	def create_hospital(self, id, password, **kwargs):
		if not id:
			raise ValueError('id field is required')

		if not password:
			raise ValueError('password field is required')

		if not kwargs.get('name', None):
			raise ValueError('name field is required')

		if not kwargs.get('address', None):
			raise ValueError('address field is required')


		account = HospitalAccount(id=id,
								  name=kwargs.get('name', ''),
								  phone_num=kwargs.get('phone_num', ''),
								  address=kwargs.get('address'))

		account.set_password(password)
		account.save()
		return account

	def create_user(self, id, password, **kwargs):
		if not id:
			raise ValueError('id field is required')

		if not password:
			raise ValueError('password field is required')

		if not kwargs.get('first_name', None):
			raise ValueError('first_name field is required')

		if not kwargs.get('last_name', None):
			raise ValueError('last_name field is required')

		if not kwargs.get('dob', None):
			raise ValueError('dob field is required')

		if not kwargs.get('sex', None):
			raise ValueError('sex field is required')

		

		account = UserAccount(id=id,
							  first_name=kwargs.get('first_name'),
							  middle_name=kwargs.get('middle_name', ''),
							  last_name=kwargs.get('last_name'),
							  dob=kwargs.get('dob'),
							  sex=kwargs.get('sex') ,
							  phone_num=kwargs.get('phone_num', ''),
							  email=kwargs.get('email', ''),
							  qr=id,
							  )

		if kwargs.get('profile_image', None):
			account.profile_image = kwargs.get('profile_image')

		account.set_password(password)
		account.save()

		img = qrcode.make(id)
		img.save('media/' + user_prof_path(account, 'qr.png'))

		return account

	def create_doctor(self, id, password, **kwargs):
		if not id:
			raise ValueError('id field is required')

		if not password:
			raise ValueError('password field is required')

		if not kwargs.get('first_name', None):
			raise ValueError('first_name field is required')

		if not kwargs.get('last_name', None):
			raise ValueError('last_name field is required')

		if not kwargs.get('dob', None):
			raise ValueError('dob field is required')

		if not kwargs.get('sex', None):
			raise ValueError('sex field is required')

		if not kwargs.get('specialty', None):
			raise ValueError('specialty field is required')

		account = DoctorAccount(id=id,
							  first_name=kwargs.get('first_name'),
							  middle_name=kwargs.get('middle_name', ''),
							  last_name=kwargs.get('last_name'),
							  dob=kwargs.get('dob'),
							  sex=kwargs.get('sex'),
							  phone_num=kwargs.get('phone_num', ''),
							  email=kwargs.get('email', ''),
							  specialty=kwargs.get('specialty'),
							  qr=id
							  )
		
		if kwargs.get('profile_image', None):
			account.profile_image = kwargs.get('profile_image')

		account.set_password(password)
		account.save()

		return account

	def create_lab(self, id, password, **kwargs):
		if not id:
			raise ValueError('id field is required')

		if not password:
			raise ValueError('password field is required')

		if not kwargs.get('name', None):
			raise ValueError('name field is required')

		if not kwargs.get('hospital', None):
			raise ValueError('hospital field is required')

		account = LabAccount(id=id,
							 name=kwargs.get('name'),
							 hospital=kwargs.get('hospital'))

		account.set_password(password)
		account.save()

		return account

	def create_superuser(self, id, password, **kwargs):
		account = BaseAccount(id=id,
							  is_staff=True,
							  is_admin=True,
							  is_superuser=True,
							  **kwargs)
		
		account.set_password(password)

		account.save()

class BaseAccount(AbstractBaseUser, PermissionsMixin):
	id = models.CharField(max_length=12, primary_key=True)

	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	objects = BaseAccountManager()
	USERNAME_FIELD = 'id'


class UserAccount(BaseAccount):
	first_name = models.CharField(max_length=50)
	middle_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50)
	dob = models.DateField()
	sex = models.CharField(max_length=6)
	phone_num = models.CharField(max_length=15, blank=True)
	email = models.EmailField(max_length=80, blank=True)
	qr = models.CharField(max_length=15)
	profile_image = models.ImageField(upload_to=user_prof_path, max_length=140, 
									  default='default.jpeg')
	#user_prof_path defined at the top
	def get_full_name(self):
		return ' '.join([self.first_name, self.middle_name, self.last_name])

	def get_age(self):
		age = datetime.date(datetime.now()) - self.dob
		return int(age.days / 365)


class DoctorAccount(UserAccount):
	specialty = models.CharField(max_length=20)


class HospitalAccount(BaseAccount):
	name = models.CharField(max_length=100)
	address = models.CharField(max_length=80)
	phone_num = models.CharField(max_length=15, blank=True)
	doctors = models.ManyToManyField(DoctorAccount)


class LabAccount(BaseAccount):
	name = models.CharField(max_length=100)
	hospital = models.ForeignKey('HospitalAccount', on_delete=models.CASCADE)
