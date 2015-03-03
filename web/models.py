from django.db import models


from web.storage import AzureBlobStorage

class VehicleAd(models.Model):
	name = models.CharField('Nombre', max_length = 20)
	thumb = models.FileField('Thumbnail', upload_to = '/', storage = AzureBlobStorage('filestock'))