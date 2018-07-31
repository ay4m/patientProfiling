Patient Profiling System

Requires:
Django 2,

psycopg2 (for Postgres),

qrcode 6.0 ( pip install qrcode[pil] )

python-barcode (pip install python-barcode)

To start the system:

1> First, create a file local_settings.py in same folder where settings.py is

2> Add SECRET_KEY and DATABASES fields in local_settings.py

NOTE: local_settings.py is already imported in settings.py

      So just create the file, add the fields, run the migrations and the app should start running
      
Working:

There's 5 types of accounts

Admin (will be added soon)

HospitalAccount

UserAccount

DoctorAccount

LabAccount

Register and login views have been developed

use decorator LoggedInAs (for functions in Class-Based Views)

           or logged_in_as (for function based views)
           
to check the account currently logged in.

(For more info, see implementation in accounts.decorators and examples in accounts.views)
