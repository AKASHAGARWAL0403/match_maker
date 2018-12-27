from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models.signals import post_save, pre_save
from jobs.models import Job,Location,Employer
# Create your models here.

User  = settings.AUTH_USER_MODEL

def upload_location(self,filename):
	return "%s/%s" %(self.user.username,filename)

class Profile(models.Model):
	user = 	models.OneToOneField(User,on_delete=models.CASCADE)
	location = models.CharField(max_length=150,blank=True)
	picture = models.ImageField(upload_to = upload_location,
			null=True,
			blank=True,
			width_field = "width_field",
			height_field = "height_field")
	width_field = models.IntegerField(default=0)
	height_field = models.IntegerField(default=0)


	def __str__(self):
		return self.user.username


	def get_absolute_url(self):
		return reverse("profile",kwargs={"username":self.user.username})


class UserJob(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	position = models.CharField(max_length=220)
	location = models.CharField(max_length=220)
	employer_name = models.CharField(max_length=220)


def post_save_user_job(sender,instance,created,*args,**kwargs):
	job = instance.position.lower()
	location = instance.location.lower()
	name = instance.employer_name.lower()
																			
	new_job = Job.objects.get_or_create(text = job)
	new_location , created = Location.objects.get_or_create(name=location)
	employer_name = Employer.objects.get_or_create(name=name,location=new_location)


post_save.connect(post_save_user_job,sender=UserJob)

