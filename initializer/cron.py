from os import remove

from time import time
from datetime import datetime

from .models import qr_map
from patientProfiling.settings import BASE_DIR

current_time = datetime.fromtimestamp(time())

def delete_expired_qr_maps():
	#delete qr maps created 7(or more) days ago
	qr_map_objects = qr_map.objects.all()

	for obj in qr_map_objects:
		t = float(obj.timestamp)
		record_time = datetime.fromtimestamp(t)
		
		if (current_time-record_time).days >= 7:
			user_timestamp = str(obj.user_id) + '_' + obj.timestamp.split('.')[0]
			file_name = user_timestamp+'.png'
			file_path = BASE_DIR + '/initializer/static/' + str(obj.user_id) + '/' + file_name

			try:
				remove(file_path)
			except:
				pass

			obj.delete()
