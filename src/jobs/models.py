from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
# Create your models here.


User = settings.AUTH_USER_MODEL

class Job(models.Model):
	text = models.CharField(max_length=150,unique=True)
	active = models.BooleanField(default=True)
	flagged = models.ManyToManyField(User,blank=True)
	slug = models.SlugField()

	def __str__(self):
		return self.text

def pre_save_job(sender,instance,*args,**kwargs):
	instance.slug = slugify(instance.text)

pre_save.connect(pre_save_job,sender=Job)

class Location(models.Model):
	name =  models.CharField(max_length=150,unique=True)
	active = models.BooleanField(default=True)
	flagged = models.ManyToManyField(User,blank=True)
	slug = models.SlugField()

	def __str__(self):
		return self.name

def pre_save_location(sender,instance,*args,**kwargs):
	instance.slug = slugify(instance.name)

pre_save.connect(pre_save_location,sender=Location)

class Employer(models.Model):
	name = models.CharField(max_length=150)
	location = models.ForeignKey(Location,blank=True,null=True,on_delete=models.CASCADE)
	slug = models.SlugField()

	def __str__(self):
		return self.name

def pre_save_employer(sender,instance,*args,**kwargs):
	instance.slug = slugify(instance.name)

pre_save.connect(pre_save_employer,sender=Employer)