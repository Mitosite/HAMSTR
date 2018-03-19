from django.db import models
from django.forms import ModelForm
from datetime import datetime

from .validators import validate_file_extension


class SingleJob(models.Model):
	#User uploaded fastq file
	readsfile = models.FileField(default='/project/home17/whb17/public_html/randtestreads.fasta', validators=[validate_file_extension])
	#adapters to be typed into textbox
	adapter = models.CharField(null=True, max_length=50, default='ACGT')
	#user's email address
	user_email = models.EmailField(default='whb17@ic.ac.uk')
	#10-digit randomly generated key
	key = models.CharField(max_length=10, default=10*'0', unique=True)

class PairedJob(models.Model):
	readsfile1 = models.FileField(null=True)
	readsfile2 = models.FileField(null=True)
	adapter = models.CharField(null=True, max_length=50)
	key = models.CharField(null=True, max_length=10, default=10*'0')



class UploadFile(models.Model):
	#title = models.CharField(max_length=50, default='sample')
	file = models.FileField(default='/project/home17/whb17/public_html/randtestreads.fasta')
	#usr's email address
	user_email = models.EmailField(default='whb17@ic.ac.uk')
	randkey = models.CharField(max_length=101, default=10*'0')
	#adapters to be typed into textbox
	adapter = models.CharField(null=True, max_length=50, default='ACGT')
	#image display test
	#image = models.FileField()



	def __str__(self):
		return self.name

class EntKey(models.Model):
	key = models.CharField(max_length=10, default=10*'0')


class ImageTest(models.Model):
	#image = models.ImageField(upload_to='media')
	name = models.CharField(max_length=50, default='Default Person')
	user_email = models.EmailField(default='whb17@ic.ac.uk')

