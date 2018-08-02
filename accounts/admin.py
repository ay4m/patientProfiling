from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin

from .models import HospitalAccount

class HospitalCreationForm(forms.ModelForm):
	class Meta:
		model = HospitalAccount
		fields = ['name', 'address', 'phone_num']

	def save(self, commit=True):
		account = super(HospitalCreationForm, self).save(commit=False)
		account.set_password(self.cleaned_data['password'])
		
		if commit:
			account.save()

		return account

class HospitalAccountAdmin(UserAdmin):
	add_form = HospitalCreationForm
	list_display = ('name', 'address', 'phone_num')
	ordering = ('name',)

	fieldsets = (
		(None, {'fields': ('id', 'password', 'name', 'address', 'phone_num')}),
		)

	list_filter = ()

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('id', 'password', 'name', 'address', 'phone_num',)
			}
			),
		)

filter_horizontal = ()

admin.site.register(HospitalAccount, HospitalAccountAdmin)