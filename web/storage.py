# -*- coding: utf-8 -*-
import datetime, os, mimetypes
from django.conf import settings
from django.core.files.storage import Storage
from azure.storage import *
from django.core.files.base import ContentFile

credentials = {
	'blobAccount' : 'nyxstorage',
	'blobContainer' : 'filestock',
	'blobKey' : '4Ly8rDtQwz2UuPpd7CRZyQF6HWtPSB3xrk7X/5lSBGwLJLHNHh4YvpWzcrVZSD/iDwj4JTkUXG7toTNINyM6+Q==',
}
baseStorageUri = "http://{blobAccount}.blob.core.windows.net/{blobContainer}/".format(**credentials)

class AzureBlobStorage(Storage):
	
	def __init__(self, container=None):
		self.blob_service = BlobService(account_name=credentials['blobAccount'], account_key=credentials['blobKey'])
		if not container == None:
			self.container = credentials['blobContainer']
		else:
			self.container = container

		## x_mx_blob_public_access = ('blob', 'container')
		self.blob_service.create_container(self.container, x_ms_blob_public_access='container')
		## To set new privileges
		## blob_service.set_container_acl('mycontainer', x_ms_blob_public_access='container')

	def _open(self, name, mode='rb'):
		data = self.blob_service.get_blob(self.container, name)
		return ContentFile(data)


	def get_valid_name(self, name):

		return name
	def get_available_name(self, name):

		return name

	def _save(self, name, content):
		# content.open(mode="rb")
		myblob = content.read()
		content_type = mimetypes.guess_type(name)[0]
		myblobname = make_readable_name(content.name)
		print 'save'
		metadata = {"modified_time": "%s" % datetime.now()}#os.path.getmtime(name)}
		print 'opened'
		self.blob_service.put_blob(self.container, myblobname , myblob, x_ms_blob_type='BlockBlob', x_ms_blob_content_type=content_type, x_ms_meta_name_values=metadata)
		## If file's data exceeds 64MB you can use chunking methods
		## blob_service.put_block_blob_from_bytes(self.container, myblobname , myblob, x_ms_blob_content_type=content_type, x_ms_meta_name_values=metadata)
		## blob_service.put_block_blob_from_path(self.container, myblobname , myblob, x_ms_blob_content_type=content_type, x_ms_meta_name_values=metadata)
		## from an already opened file/stream
		## blob_service.put_block_blob_from_file(self.container, myblobname , myblob, x_ms_blob_content_type=content_type, x_ms_meta_name_values=metadata)
		## uploads the specified text value using the specified encoding (defaults to UTF-8)
		## blob_service.put_block_blob_from_text(self.container, myblobname , myblob, x_ms_blob_content_type=content_type, x_ms_meta_name_values=metadata)

		return myblobname

	def delete(self, name):
		self.blob_service.delete_blob(self.container, name)
    		
	def exists(self, name):    	##
		try:
			self.blob_service.get_blob_properties(self.container, name)
			return True
		except:
			return False


	def listdir(self, path):
		dirs = []
		files = []
		blobs = self.blob_service.list_blobs(self.container, prefix=(path or None))
		for blob in blobs:
			directory, file_name = os.path.split(blob.name)
			dirs.append(directory)
			files.append(file_name)

		for d in dirs:
			print d
		for f in files:
			print f

		return (dirs, files)

	def size(self, name):
		properties = self.blob_service.get_blob_properties(self.container, name)
		return properties.get('content-length')

	def url(self, name):
		blob = self.blob_service.list_blobs(self.container, prefix=name)
		return blob.blobs[0].url

	def modified_time(self, name):
		metadata = self.blob_service.get_blob_metadata(self.container, name)
		modified_time = float(metadata.get('x-ms-meta-modified_time'))
		return datetime.fromtimestamp(modified_time)


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
		