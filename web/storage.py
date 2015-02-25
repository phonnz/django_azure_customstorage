# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.core.files.storage import Storage
from azure.storage import *

credentials = {
	'blobAccount' : 'nyxstorage',
	'blobContainer' : 'filestock',
	'blobKey' : '4Ly8rDtQwz2UuPpd7CRZyQF6HWtPSB3xrk7X/5lSBGwLJLHNHh4YvpWzcrVZSD/iDwj4JTkUXG7toTNINyM6+Q==',
}
baseStorageUri = "http://{blobAccount}.blob.core.windows.net/{blobContainer}/".format(**credentials)

class AzureBlobStorage(Storage):
	
	def __init__(self, option=None):
		# pass
		if not option == None:
			option = settings.CUSTOM_STORAGE_OPTIONS
	# def __open(self, name, mode='rb'):
	# 	print 'invoque open'
	# 	return name

	# def _url(self):
	# 	print 'invoque url'
	# 	blob_service = BlobService(account_name=credentials['blobAccount'], account_key=credentials['blobKey'])
	# 	blob = blob_service.get_blob(blobContainer, self)
	# 	return baseStorageUri + 'image' + self.blob

	def get_valid_name(self, name):

		return name
	def get_available_name(self, name):

		return name

	def _save(self, name, content):
		print 'invoque save'
		blob_service = BlobService(account_name=credentials['blobAccount'], account_key=credentials['blobKey'])
		blob_service.create_container('filestock', x_ms_blob_public_access='container')
		# blob_service.set_container_acl('mycontainer', x_ms_blob_public_access='container')
		# print content.path
		myblob = content.read()
		myblobname = make_readable_name(content.name)
		myblobExtension = myblobname[-3:]
		# blob_service.put_blob(credentials['blobContainer'], myblobname , myblob, x_ms_blob_type='BlockBlob')
		blob_service.put_block_blob_from_bytes(credentials['blobContainer'], myblobname , myblob, x_ms_blob_content_type='application/'+myblobExtension)
		return baseStorageUri + myblobname

	# def _path(self):
	# 	return self.name



def make_readable_name(name):
	name = name.replace(' ', '_')
	# name = name.replace('á', 'a')
	# name = name.replace('é', 'e')
	# name = name.replace('í', 'i')
	# name = name.replace('ó', 'o')
	# name = name.replace('ñ', 'n')
	name = name[-30:]
	current = datetime.now()
	name = str(current.year) + '_' + str(current.month) + '_' + str(current.day) + '_' + str(current.hour) + '_' + str(current.minute) + '_' + str(current.second) + '_' + name
	return name
		


# storage.path
# storage.open
# storage.save
# storage.delete
# storage.exist

