from django.shortcuts import render

from accounts.decorators import logged_in_as

@logged_in_as(['Doctor', 'Lab'])
def barcode_view(request):
	return render(request, 'barcode.html')
