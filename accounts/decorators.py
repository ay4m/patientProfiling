import functools

from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect

class LoggedInAs:
	#use as decorator for functions
	#inside Class-Based Views i.e. having 'self' parameter
	def __init__(self, accounts):
		self.accounts=[]
		[self.accounts.append(account+'Account') for account in accounts]

	def __call__(self, func):
		@functools.wraps(func)
		def my_logic(slef , request, *args, **kwargs):
			if request.user.__class__.__name__ in self.accounts:
				return func(slef, request, *args, **kwargs)
			else:
				account = self.accounts[0][:-(len('Account'))]
				#chopping off substring 'Account' from the string
				#eg: if string 'UserAccount', then slice to 'User'
				url = '/account/login/'+str.lower(account)
				return HttpResponseRedirect(url)

		return my_logic


class logged_in_as:
	#use as decorator for
	#function views i.e. not having 'self' parameter
	def __init__(self, accounts):
		self.accounts=[]
		[self.accounts.append(account+'Account') for account in accounts]

	def __call__(self, func):
		@functools.wraps(func)
		def my_logic(request, *args, **kwargs):
			if request.user.__class__.__name__ in self.accounts:
				return func(request, *args, **kwargs)
			else:
				account = self.accounts[0][:-(len('Account'))]
				#chopping off substring 'Account' from the string
				#eg: if string 'UserAccount', then slice to 'User'
				url = '/account/login/'+str.lower(account)
				return HttpResponseRedirect(url)

		return my_logic